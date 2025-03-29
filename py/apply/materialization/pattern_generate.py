import itertools
from collections import namedtuple

from apply.abdd import ABDD
from apply.materialization.abdd_pattern import MaterializationRecipe
from apply.materialization.box_materialization import create_materialized_box
from apply.materialization.pattern_finding import abdd_subsection_create, get_state_sym_lookup
from apply.abdd_node import ABDDNode

from helpers.utils import box_catalogue, box_arities
from tree_automata import TTransition, TTreeAut


class VariablePredicate(namedtuple("VariablePredicate", ["var1", "rel", "var2"])):
    def __repr__(self, short=False):
        if short:
            return f"[{self.var1} {self.rel} {self.var2}]"
        return f'{self.__class__.__name__}("{self.var1}", "{self.rel}", "{self.var2}")'


def obtain_predicates(
    abdd: ABDD, node_src: ABDDNode, direction: bool, materialization_var: int
) -> frozenset[VariablePredicate]:
    """
    Based on the current node 'node_src' from the ABDD 'abdd' and the 'direction' of the apply call,
    figure out, based on the edge information, the set of predicates that are true in order
    to search the appropriate MaterializationRecipe in the pre-computed cache.

    When an empty set is returned, no materialization is needed.
    """
    node_tgt = node_src.high if direction else node_src.low
    box = node_src.high_box if direction else node_src.low_box
    leaf_var = abdd.variable_count + 1

    # early returns -> None box == short edge => no materialization needed
    # <in, ...,  mat, ..., out> order is broken iff in >= mat or mat >= all outs
    if any(
        [
            box is None,
            materialization_var <= node_src.var,
            all([materialization_var >= out_node.var for out_node in node_tgt]),
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
    if node_src.var + 1 == materialization_var:
        result.append(VariablePredicate("in", "1<", "mat"))
    if node_src.var + 1 < materialization_var:
        result.append(VariablePredicate("in", "<<", "mat"))

    # relationship between materialization variable and output variables
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
    # has_leaf = False
    if any([i in boxname for i in ["0", "1"]]):
        # has_leaf = True
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
    return holds


def generate_patterns(boxname: str) -> dict[frozenset[VariablePredicate], MaterializationRecipe]:
    predicate_sets: set[frozenset[VariablePredicate]] = create_all_predicate_sets(boxname)
    varassign = {"in": 1}
    box = box_catalogue[boxname]
    arity = box.port_arity
    other_vars = [f"out{i}" for i in range(arity)] + ["mat", "leaf"]
    outvar = [i for i in range(2, 10)]
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


ABDD_PATTERN_PACKAGE = "apply.materialization.abdd_pattern"
ABDD_GENERATE_PACKAGE = "apply.materialization.pattern_generate"


def print_generated_patterns(filename: str) -> None:
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
