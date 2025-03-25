import copy
import itertools
from typing import Optional
from collections import namedtuple

from apply.abdd import ABDD
from apply.abdd_pattern import MaterializationRecipe
from apply.box_materialization import create_materialized_box
from apply.pattern_finding import abdd_subsection_create, get_state_sym_lookup
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_key_edge_tuples
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition


# class VariablePredicate(NamedTuple):
#     var1: str
#     rel: str,
#     var2: str
class VariablePredicate(namedtuple("VariablePredicate", ["var1", "rel", "var2"])):
    def __repr__(self):
        return f"[{self.var1} {self.rel} {self.var2}]"


def obtain_predicates(
    node_src: ABDDNode, node_tgt: list[ABDDNode], materialization_var: int
) -> frozenset[VariablePredicate]:
    result = []
    if node_src.var + 1 == materialization_var:
        result.append(VariablePredicate("in", "1<", "mat"))
    if node_src.var + 1 < materialization_var:
        result.append(VariablePredicate("in", "<<", "mat"))
    for idx, out_node in enumerate(node_tgt):
        if materialization_var + 1 == out_node.var:
            result.append(VariablePredicate("mat", "1<", f"out{idx}"))
        if materialization_var + 1 < out_node.var:
            result.append(VariablePredicate("mat", "<<", f"out{idx}"))
    return frozenset(result)


def create_all_predicate_sets(boxname: str) -> set[frozenset[VariablePredicate]]:
    """
    For a given box, generate all possible variable predicate sets that compare input variables (root) and
    output variables (each of the port states) with the materialization variable.

    E.g for box X (X has only one port state representing out0, out states are indexed from zero):

    [in 1< mat, mat 1< out0],
    [in 1< mat, mat << out0],
    [in << mat, mat 1< out0],
    [in << mat, mat << out0].

    [additional notes]
    It always holds that 'in' < 'mat', and 'mat' < 'outi' for some i in output states.
    In case of multiple instances of 'outi', the order between 'mat' and all but last 'outi' is not fixed.

    We should probably somehow trim the set of possible combinations of predicates by leveraging the inherent
    restrictions inferred from the box structure.

    For example: in case of LPort box, out0 >= out1, since they are both targets of the terminating transition
    AND out0 can self-loop while out1 cannot.
    """
    box: TTreeAut = box_catalogue[boxname]
    result = set()
    predicate_sets = {"in": [VariablePredicate("in", "1<", "mat"), VariablePredicate("in", "<<", "mat")]}

    # equal or larger (None) < smaller by one (1<) < smaller by more than one (<<)
    predicate_order = {None: 0, "1<": 1, "<<": 2}

    compare_vars = {}
    loopstates = set([i.src for i in box.get_loopable_transitions()])
    for i, (_, s) in enumerate(box.get_port_order()):
        compare_vars[f"out{i}"] = 2 if s in loopstates else 1

    for idx, (port, state) in enumerate(box.get_port_order()):
        predicate_sets[f"out{idx}"] = [
            VariablePredicate("mat", "1<", f"out{idx}"),
            VariablePredicate("mat", "<<", f"out{idx}"),
            None,
        ]

    keys = predicate_sets.keys()
    values = (predicate_sets[k] for k in keys)

    # Generate all possible assignments
    predicate_lookups: list[dict[str, VariablePredicate]] = [
        dict(zip(keys, selection)) for selection in itertools.product(*values)
    ]

    for lookup in predicate_lookups:
        compare_predicates = {}
        for var, predicate in lookup.items():
            lookup_item = None
            if predicate is not None:
                lookup_item = predicate.rel
            compare_predicates[var] = predicate_order[lookup_item]

        if len(compare_vars) > 1:
            for var1, var2 in itertools.combinations(compare_vars, 2):
                if all(
                    [
                        compare_vars[var1] > compare_vars[var2],
                        compare_predicates[var1] >= compare_predicates[var2],
                        compare_predicates[var1] != 0,
                        not (compare_predicates["in"] == 1 and compare_predicates[var2] == 0),
                    ]
                ):
                    result.add(frozenset([i for i in lookup.values() if i is not None]))

                if all(
                    [
                        compare_vars[var1] < compare_vars[var2],
                        compare_predicates[var1] <= compare_predicates[var2],
                        compare_predicates[var2] != 0,
                        not (compare_predicates["in"] == 1 and compare_predicates[var1] == 0),
                    ]
                ):
                    result.add(frozenset([i for i in lookup.values() if i is not None]))
        else:
            for var in compare_vars:
                if all(
                    [compare_predicates[var] != 0, not (compare_predicates["in"] == 1 and compare_predicates[var] == 0)]
                ):
                    result.add(frozenset([i for i in lookup.values() if i is not None]))

    # for fset in result:
    #     for predicate in fset:
    #         print(f"[{predicate.var1} {predicate.rel} {predicate.var2}]" if predicate is not None else "[]", end=', ')
    #     print()
    return result


def check_predicate_against_values(predicates: frozenset[VariablePredicate], assignment: dict[str, int]) -> bool:
    holds = True
    for pred in predicates:
        val1 = assignment[pred.var1]
        val2 = assignment[pred.var2]
        if pred.rel == "1<":
            holds = holds and val1 + 1 == val2
        if pred.rel == "<<":
            holds = holds and val1 + 1 < val2
    return holds


def generate_patterns(boxname: str) -> dict[frozenset[VariablePredicate], MaterializationRecipe]:
    predicate_sets: set[frozenset[VariablePredicate]] = create_all_predicate_sets(boxname)
    varassign = {"in": 1}
    box = box_catalogue[boxname]
    arity = box.port_arity
    other_vars = [f"out{i}" for i in range(arity)] + ["mat"]
    outvar = [i for i in range(2, 10)]
    for predicate_set in predicate_sets:
        for comb in itertools.product(outvar, repeat=arity + 1):
            for i, val in enumerate(list(comb)):
                varassign[other_vars[i]] = val
            if check_predicate_against_values(predicate_set, varassign):
                invar = varassign["in"]
                outvars = [varassign[f"out{i}"] for i in range(arity)]
                matvar = varassign["mat"]
                leafvar = 10
                matbox = create_materialized_box(box, invar, matvar, outvars, leafvar)
                pset_str = ", ".join([s.__repr__() for s in predicate_set])
                print("Predicates:", pset_str)
                # state_sym_lookup =
                # print(matbox)
                state_sym_lookup: dict[str, str] = get_state_sym_lookup([f"out{i}" for i in range(arity)], matbox)
                pattern = abdd_subsection_create(state_sym_lookup, matbox)
                print(pattern)
                break
