"""
[file] pattern_generate.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Generate all possible materialization patterns into an Python-importable cache.

The cache is indexed by a box and a set of predicates (about relationships between variables) of an edge that needs
to be materialized in one of the input ABDDs.
"""

import itertools
from collections import namedtuple
from typing import Optional

from apply.abdd import ABDD
from apply.materialization.abdd_pattern import MaterializationRecipe
from apply.materialization.box_materialization import create_materialized_box
from apply.materialization.pattern_finding import abdd_subsection_create, get_state_sym_lookup
from apply.abdd_node import ABDDNode

from helpers.utils import box_catalogue
from tree_automata import TTreeAut


class VariablePredicate(namedtuple("VariablePredicate", ["var1", "rel", "var2"])):
    def __repr__(self, short=False):
        if short:
            return f"[{self.var1} {self.rel} {self.var2}]"
        return f'{self.__class__.__name__}("{self.var1}", "{self.rel}", "{self.var2}")'


def obtain_predicates(
    abdd: ABDD, node_src: Optional[ABDDNode], direction: Optional[bool], materialization_var: int
) -> frozenset[VariablePredicate]:
    """
    Based on the current node 'node_src' from the ABDD 'abdd' and the 'direction' of the apply call,
    figure out, based on the edge information, the set of predicates that are true in order
    to search the appropriate MaterializationRecipe in the pre-computed cache.

    When an empty set is returned, no materialization is needed.
    """
    invar: int = 0 if node_src is None else node_src.var
    node_tgt: list[ABDDNode] = (
        [r for r in abdd.roots] if node_src is None else node_src.high if direction else node_src.low
    )
    tgt_vars: list[int] = [abdd.variable_count + 1 if n.is_leaf else n.var for n in node_tgt]
    box: Optional[str] = None
    if direction is None:
        box = abdd.root_rule
    else:
        box = node_src.high_box if direction else node_src.low_box
    leaf_var = abdd.variable_count + 1

    # early returns -> None box == short edge => no materialization needed
    # <in, ...,  mat, ..., out> order is broken iff in >= mat or mat >= all outs
    if any(
        [
            box is None,
            materialization_var <= invar,
            all([materialization_var >= var for var in tgt_vars]),
            # any([invar + 1 >= var for var in tgt_vars])
        ]
    ):
        return frozenset([])

    result = []
    # TODO: rework this to a more "robust" automata-based approach
    # i.e. pre-computing boxes that contain leaf transitions with terminal symbols
    if box in ["L0", "L1", "H0", "H1"]:
        if materialization_var + 1 == leaf_var:
            result.append(VariablePredicate("mat", "1<", "leaf"))
        if materialization_var + 1 < leaf_var:
            result.append(VariablePredicate("mat", "<<", "leaf"))

    # relationship between materialization variable and input variables
    if invar + 1 == materialization_var:
        result.append(VariablePredicate("in", "1<", "mat"))
    if invar + 1 < materialization_var:
        result.append(VariablePredicate("in", "<<", "mat"))

    # relationship between materialization variable and output variables
    for idx, var in enumerate(tgt_vars):
        if materialization_var + 1 == var:
            result.append(VariablePredicate("mat", "1<", f"out{idx}"))
        if materialization_var + 1 < var:
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
    # predicate_sets is a helper array which contains all possible symbolic values
    # and a list of possible predicates which concern them (wrt. 'mat' variable)
    predicate_sets = {"in": [VariablePredicate("in", "1<", "mat"), VariablePredicate("in", "<<", "mat")]}
    if any([i in boxname for i in ["0", "1"]]):
        predicate_sets["leaf"] = [VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "<<", "leaf")]

    # equal or larger (None) < smaller by one (1<) < smaller by more than one (<<)
    predicate_order = {None: 0, "1<": 1, "<<": 2}

    # will contain "strength" of output/port symbols
    # loopable portstates are assigned 2, nonloopable portstates are assigned 1
    # this is relevant for multiport boxes, where different port-mapped nodes
    # can have different variables, e.g.
    # x1 --LPort--> [x5, x3] is valid (since state reperesetn)
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

    # Generate all possible assignments - basically a cartesian product over all lists in 'predicate_sets'
    # (invar predicates ...) x (outi predicates ...) x (leaf predicates ...)
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
            check_pairwise_vars(result, lookup, compare_vars, compare_predicates)
        else:
            check_singleton_var(result, lookup, compare_vars, compare_predicates)

    return result


def check_singleton_var(
    result: set[frozenset[VariablePredicate]],
    lookup: dict[str, VariablePredicate],
    compare_vars: dict[str, int],
    compare_predicates: dict[str, int],
):
    """
    For singleport boxes, check the consistency of the variable assignment.
    """
    for var in compare_vars:
        if all(
            [
                compare_predicates[var] != 0,
                not (compare_predicates["in"] == 1 and compare_predicates[var] == 0),
                not "leaf" in compare_predicates or compare_predicates[var] <= compare_predicates["leaf"],
            ]
        ):
            result.add(frozenset([i for i in lookup.values() if i is not None]))


def check_pairwise_vars(
    result: set[frozenset[VariablePredicate]],
    lookup: dict[str, VariablePredicate],
    compare_vars: dict[str, int],
    compare_predicates: dict[str, int],
) -> None:
    """
    For multiport boxes, check the consistency of the variable assignment.
    Requires different set of checks (even between port-mapped node variables - symbolic values "outi")
    """
    for var1, var2 in itertools.combinations(compare_vars, 2):
        smaller_var = var1 if compare_vars[var1] < compare_vars[var2] else var2
        larger_var = var2 if compare_vars[var1] < compare_vars[var2] else var1
        if all(
            [
                compare_predicates[larger_var] >= compare_predicates[smaller_var],
                compare_predicates[larger_var] != 0,
                not (compare_predicates["in"] == 1 and compare_predicates[smaller_var] == 0),
                not "leaf" in compare_predicates or compare_predicates[larger_var] <= compare_predicates["leaf"],
            ]
        ):
            result.add(frozenset([i for i in lookup.values() if i is not None]))


def check_predicate_against_values(predicates: frozenset[VariablePredicate], assignment: dict[str, int]) -> bool:
    holds = True
    for pred in predicates:
        val1 = assignment[pred.var1]
        val2 = assignment[pred.var2]
        if pred.rel == "1<":
            holds = holds and val1 + 1 == val2
        if pred.rel == "<<":
            holds = holds and val1 + 1 < val2

    # TODO: we also need to enforce that outi is at least 2 larger than in
    # otherwise the root state of the box would have to perform 0 transitions to reach out state
    # since invar is the variable used while getting to the rootstate,
    # and the box evaluation itself starts at invar + 1
    # NOTE: for unknown reason, the following does not work so well
    # perhaps there is a discrepancy between invar and minvar of rootstate of the box ?
    # Right now, as it is, the predicate set generation and materialized patterns are working and consistent with
    # the expected (theoretical) behavior.

    # invar = assignment['in']
    # outvars = [val for var, val in assignment.items() if var.startswith("out") or var.startswith("leaf")]
    # if any([invar + 1 >= o for o in outvars]):
    #     holds = False

    return holds


# 'in' can be fixed, since when materialization happens, the source node variables are assumed equal
INVAR_FIXED = 1
# range <2,10> should cover all possible materialization configurations
OUTVAR_MIN = 2
OUTVAR_MAX = 10


def generate_patterns(boxname: str) -> dict[frozenset[VariablePredicate], MaterializationRecipe]:
    """
    For a given box, iterate over all consistent predicate sets,
    and generate variable assignments such that all predicates from the set hold.
    Given the generated assignment (which will be replaced by symbolic values later),
    create a materialized box and then return a cache of predicate_set : materialization_recipe pairs.
    """
    predicate_sets: set[frozenset[VariablePredicate]] = create_all_predicate_sets(boxname)
    varassign = {"in": INVAR_FIXED}
    box = box_catalogue["Xdet" if boxname == "X" else boxname]
    arity = box.port_arity
    other_vars = [f"out{i}" for i in range(arity)] + ["mat", "leaf"]
    outvar = [i for i in range(OUTVAR_MIN, OUTVAR_MAX)]
    result: dict[frozenset[VariablePredicate], MaterializationRecipe] = {}
    for predicate_set in predicate_sets:
        for comb in itertools.product(outvar, repeat=arity + 2):  # arity = # of ports + mat level + leaf level
            for i, val in enumerate(list(comb)):
                varassign[other_vars[i]] = val
            if check_predicate_against_values(predicate_set, varassign):
                invar = varassign["in"]
                outvars = [varassign[f"out{i}"] for i in range(arity)]
                matvar = varassign["mat"]
                leafvar = varassign["leaf"]
                matbox = create_materialized_box(box, invar, matvar, outvars, leafvar)
                state_sym_lookup: dict[str, str] = get_state_sym_lookup([f"out{i}" for i in range(arity)], matbox)
                pattern = abdd_subsection_create(state_sym_lookup, matbox)
                result[predicate_set] = pattern
                break
    return result


# for now we allow max 5 ports
PORT_MAX = 5


def format_frozenset(predicates: frozenset) -> str:
    """
    For debugging, prettyprinting of a frozenset (in an orderly way).
    """

    def predicate_key(predicate: VariablePredicate) -> str:
        v_order = {f"out{i}": f"{i + 1}" for i in range(PORT_MAX)}
        v_order["in"] = "0"
        v_order["leaf"] = f"{PORT_MAX + 1}"
        p_order = {"1<": "1", "<<": "2"}
        if predicate.var1 != "mat":
            var = predicate.var1
        if predicate.var2 != "mat":
            var = predicate.var2
        return v_order[var] + p_order[predicate.rel]

    return f"frozenset({repr(sorted(predicates, key=predicate_key))})"


ABDD_PATTERN_PACKAGE = "apply.materialization.abdd_pattern"
ABDD_GENERATE_PACKAGE = "apply.materialization.pattern_generate"


def print_generated_patterns(filename: str) -> None:
    """
    Create an importable Python module that contains cached results of materialization
    based on the sets of predicates about the variables.
    """
    t = " " * 4
    f = open(filename, "w")
    f.write(f"from {ABDD_PATTERN_PACKAGE} import MaterializationRecipe, ABDDPattern\n")
    f.write(f"from {ABDD_GENERATE_PACKAGE} import VariablePredicate\n")
    f.write("\n\n")
    f.write("# fmt: off\n")

    all_patterns = {}

    for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
        name_list: list[tuple[str, str]] = []
        patterns = generate_patterns(boxname)
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


# End of file pattern_generate.py
