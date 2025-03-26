import copy
import itertools
from typing import Optional
from collections import namedtuple

from apply.abdd import ABDD
from apply.abdd_pattern import MaterializationRecipe
from apply.box_materialization import create_materialized_box
from apply.pattern_finding import abdd_subsection_create, get_state_sym_lookup
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_key_edge_tuples
from helpers.utils import box_catalogue, box_arities

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition


class VariablePredicate(namedtuple("VariablePredicate", ["var1", "rel", "var2"])):
    def __repr__(self, short=False):
        if short:
            return f"[{self.var1} {self.rel} {self.var2}]"
        return f'{self.__class__.__name__}("{self.var1}", "{self.rel}", "{self.var2}")'


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
    has_leaf = False
    if any([i in boxname for i in ["0", "1"]]):
        has_leaf = True
        predicate_sets["leaf"] = [VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "<<", "leaf")]

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
                        not has_leaf or compare_predicates[var1] <= compare_predicates["leaf"],
                    ]
                ):
                    result.add(frozenset([i for i in lookup.values() if i is not None]))

                if all(
                    [
                        compare_vars[var1] < compare_vars[var2],
                        compare_predicates[var1] <= compare_predicates[var2],
                        compare_predicates[var2] != 0,
                        not (compare_predicates["in"] == 1 and compare_predicates[var1] == 0),
                        not has_leaf or compare_predicates[var2] <= compare_predicates["leaf"],
                    ]
                ):
                    result.add(frozenset([i for i in lookup.values() if i is not None]))
        else:
            for var in compare_vars:
                if all(
                    [
                        compare_predicates[var] != 0,
                        not (compare_predicates["in"] == 1 and compare_predicates[var] == 0),
                        not has_leaf or compare_predicates[var] <= compare_predicates["leaf"],
                    ]
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
    other_vars = [f"out{i}" for i in range(arity)] + ["mat", "leaf"]
    outvar = [i for i in range(2, 10)]
    # leafvar = [i for i in range(2, 10)]
    result: dict[frozenset[VariablePredicate], MaterializationRecipe] = {}
    for predicate_set in predicate_sets:
        for comb in itertools.product(outvar, repeat=arity + 2):  # arity = # of ports + mat level + leaf level
            for i, val in enumerate(list(comb)):
                varassign[other_vars[i]] = val
            if check_predicate_against_values(predicate_set, varassign):
                invar = varassign["in"]
                outvars = [varassign[f"out{i}"] for i in range(arity)]
                # print(predicate_set)
                matvar = varassign["mat"]
                leafvar = varassign["leaf"]
                matbox = create_materialized_box(box, invar, matvar, outvars, leafvar)
                # print(matbox)
                state_sym_lookup: dict[str, str] = get_state_sym_lookup([f"out{i}" for i in range(arity)], matbox)
                pattern = abdd_subsection_create(state_sym_lookup, matbox)
                # print(pattern)
                result[predicate_set] = pattern
                break
    return result


def format_frozenset(predicates: frozenset) -> str:
    def predicate_key(predicate: VariablePredicate) -> str:
        v_order = {f"out{i}": f"{i + 1}" for i in range(5)}
        v_order["in"] = "0"
        v_order["leaf"] = "6"
        p_order = {"1<": "1", "<<": "2"}
        if predicate.var1 != "mat":
            var = predicate.var1
        if predicate.var2 != "mat":
            var = predicate.var2
        return v_order[var] + p_order[predicate.rel]

    return f"frozenset({repr(sorted(predicates, key=predicate_key))})"


def print_generated_patterns(filename: str) -> None:
    t = " " * 4
    f = open(filename, "w")
    f.write("from apply.abdd_pattern import MaterializationRecipe, ABDDPattern\n")
    f.write("from apply.pattern_generate import VariablePredicate\n")
    f.write("\n\n")
    f.write("# fmt: off\n")

    all_patterns = {}

    for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
        name_list: list[tuple[str, str]] = []
        patterns = generate_patterns(boxname)
        # for pset in patterns.keys():
        #     print(format_frozenset(pset))
        psets = [sorted(i, key=repr) for i in patterns.keys()]
        psets = sorted(psets, key=repr)
        for idx, i in enumerate(psets):
            predicate_name = f"predicate_set_{boxname}_{idx}"
            f.write(f"{predicate_name} = frozenset({i})\n")
            f.write("\n")
            recipe_name = f"materialization_recipe_{boxname}_{idx}"
            f.write(f"{recipe_name} = {patterns[frozenset(i)]}\n")
            f.write("\n")
            name_list.append((predicate_name, recipe_name))
        all_patterns[boxname] = name_list

    cache_name = "cached_materialization_recipes"

    f.write(f"{cache_name}: dict[str, dict[frozenset[VariablePredicate], MaterializationRecipe]] = {{\n")
    for box, name_list in all_patterns.items():
        f.write(f"{t}'{box}': {{\n")
        for pset, recipe in name_list:
            f.write(f"{t}{t}{pset}: {recipe},\n")
        f.write(f"{t}}},\n")
    f.write("}\n")
    f.write("# fmt: on\n")

    f.close()

    # for boxname in box_arities.keys():
    #     print(boxname)
    #     f.write(f"{t}'{boxname}': {{\n")
    #     # print(boxname)
    #     patterns = generate_patterns(boxname)
    #     for pset, recipe in patterns.items():
    #         # print(pset)
    #         # f.write(f"{t}{t}frozenset([\n")
    #         # for predicate in pset:
    #         #     f.write(f"{t}{t}{t}{predicate},\n")
    #         #     pass
    #         # f.write(f"{t}{t}]): ")
    #         f.write(f"{t}{t}{format_frozenset(pset)}")
    #         f.write(":(\n")
    #         f.write(f"{recipe.__repr__(level=8)}")
    #         f.write("),\n")
    #         # print(recipe)

    #         # f.write(str(pset))
    #         # f.write
    #     f.write("    }\n")
    #     break
