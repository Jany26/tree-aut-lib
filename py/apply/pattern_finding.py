import copy
from typing import Optional

from apply.abdd_pattern import ABDDPattern, MaterializationRecipe
from canonization.folding import ubda_folding
from tree_automata import (
    TTreeAut,
    iterate_edges,
    iterate_key_edge_tuples,
    tree_aut_intersection,
    tree_aut_complement,
    non_empty_bottom_up,
    non_empty_top_down,
)
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from apply.abdd import ABDD
from tree_automata.automaton import iterate_edges_from_state
from tree_automata.functions.trimming import remove_useless_states
from tree_automata.transition import TEdge, TTransition


def create_trivial_aut(materialized_box: TTreeAut) -> TTreeAut:
    """
    During materialized box traversal, when we try to find patterns that are
    identical (semantically) to some of the boxes, we might encounter an automaton,
    that has a language almost the same as one of the boxes, except it can produce
    trivial trees (only one leaf node - either a port or a terminal symbol).

    For this reason, during "equality" check, we create an arbitrary automaton,
    that can accept ONLY these trivial trees (based on the compared box's output symbols),
    and complement it and then intersect it with the initial materialized box,
    resulting in an automaton that CANNOT produce these trivail trees,
    making the language comparison against boxes simpler and more straightforward.
    """
    symbols = materialized_box.get_output_symbols()

    rootstates = [i for i in materialized_box.roots]
    transitions = {
        i: {f"k{c}": TTransition(i, TEdge(s, [], ""), []) for c, s in enumerate(symbols)} for i in rootstates
    }
    name = f"trivial({materialized_box.name})"
    result = TTreeAut(rootstates, transitions, name, 0)
    return result


def matbox_equal_to_box(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    symbols = box.get_symbol_arity_dict()
    symbols.update(aut.get_symbol_arity_dict())

    # we don't consider trivial trees - i.e. only one node (either port or terminal symbol),
    # as a proof that languages are not subsets of each other
    # this is why we intersect with a complement of a tree automaton accepting only trivial trees
    trivial = create_trivial_aut(aut)
    nontrivial = tree_aut_complement(trivial, symbols)
    nontrivial_aut = tree_aut_intersection(aut, nontrivial)

    # aut and co-box == empty => 'aut subseteq box'
    intersection1 = tree_aut_intersection(nontrivial_aut, tree_aut_complement(box, symbols))
    witness_BU_1, _ = non_empty_bottom_up(intersection1)
    witness_TD_1, _ = non_empty_top_down(intersection1)

    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None

    # box and co-aut == empty => 'box subseteq aut'
    intersection2 = tree_aut_intersection(box, tree_aut_complement(nontrivial_aut, symbols))
    witness_BU_2, _ = non_empty_bottom_up(intersection2)
    witness_TD_2, _ = non_empty_top_down(intersection2)
    box_subset_of_aut = witness_BU_2 is None or witness_TD_2 is None

    if debug:
        print(f"{aut.name} ==? {box.name}")
        print("witness 1")
        witness_BU_1.print_node() if witness_BU_1 is not None else "None"
        print("witness 2")
        witness_BU_2.print_node() if witness_BU_2 is not None else "None"
    return aut_subset_of_box and box_subset_of_aut


def matbox_sublang_of_box(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    """
    If an automaton has nonempty language and this language is a subset of some box language,
    return True.
    """
    symbols = box.get_symbol_arity_dict()
    symbols.update(aut.get_symbol_arity_dict())

    # we don't consider trivial trees - i.e. only one node (either port or terminal symbol),
    # as a proof that languages are not subsets of each other
    # this is why we intersect with a complement of a tree automaton accepting only trivial trees
    trivial = create_trivial_aut(aut)
    nontrivial = tree_aut_complement(trivial, symbols)
    nontrivial_aut = tree_aut_intersection(aut, nontrivial)
    witnessBU, _ = non_empty_bottom_up(nontrivial_aut)
    witnessTD, _ = non_empty_top_down(nontrivial_aut)
    aut_empty = witnessBU is None or witnessTD is None

    if aut_empty:
        return False

    # aut and co-box == empty => 'aut subseteq box'
    intersection1 = tree_aut_intersection(nontrivial_aut, tree_aut_complement(box, symbols))
    witness_BU_1, _ = non_empty_bottom_up(intersection1)
    witness_TD_1, _ = non_empty_top_down(intersection1)

    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None
    return aut_subset_of_box


def get_state_sym_lookup(nodes: list[ABDDNode], materialized_box: TTreeAut) -> dict[str, ABDDNode]:
    portstates: list[tuple[str, str]] = []  # (port, state) tuples
    for e in iterate_edges(materialized_box):
        if e.info.label.startswith("Port") and e.info.label != "Port_arbitrary":
            portstates.append((e.info.label, e.src))
    portstates = sorted(portstates, key=lambda item: item[0])
    result = {state: node for (port, state), node in zip(portstates, nodes)}
    return result


def remove_irrelevant_ports(materialized_box: TTreeAut, arbitrary=False):
    remove_tuples = []
    for k, e in iterate_key_edge_tuples(materialized_box):
        if arbitrary and e.info.label == "Port_arbitrary":
            remove_tuples.append((e.src, k))
        if not arbitrary and e.info.label.startswith("Port") and e.info.label != "Port_arbitrary":
            remove_tuples.append((e.src, k))
    for s, k in remove_tuples:
        materialized_box.remove_transition(s, k)


def abdd_subsection_create(
    state_sym_lookup: dict[str, str | ABDDNode], materialized_box: TTreeAut
) -> MaterializationRecipe:
    """
    This process is similar to folding, but instead of trying to fold as much as possible,
    we fold (or rather, compare) until the first ports are reached.

    This is done by gradually including/removing ports in "two" waves
    1) first, we select only arbitrary ports, the others (original) are temporarily removed
    2) we try matching the materialized box with any other box
    3) then we select only original ports, arbitrary ports are removed
    4) starting from the 'matched' states (to the ports of the 'matched' box),
        we similarly try finding the matching boxes of the children of the terminating transitions from the matched states
    """

    # print('lookup', state_sym_lookup)
    working_aut = copy.deepcopy(materialized_box)
    root = working_aut.roots[0]
    port_trs = [
        (k, copy.deepcopy(e)) for k, e in iterate_key_edge_tuples(working_aut) if e.info.label.startswith("Port")
    ]
    term_trs = {t.src: t for t in working_aut.get_terminating_transitions() if len(t.children) > 0}

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # A) initial edge -> materialized nodes
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # note: lookup ports not based on the lexicographic order of the states but based
    # on if they are arbitrary or not + in the changed order, empty comes after anything starting with 0
    # (i.e. similarly to preorder tree traversal assuming 0=left/low, 1=right/high)
    # so, first, remove all non-arbitrary ports, remove unreachable states,
    # rename arbitrary ports for the equality test

    # since we will need to work with the initial Ports that were removed, we don't trim the materialized automaton,
    # just reformat the port transitions

    remove_irrelevant_ports(working_aut, arbitrary=False)
    working_aut.reformat_ports(preorder=True)
    port_states: list[tuple[str, str, str]] = []  # matbox_only_arbitrary_ports.get_port_order(preorder=True)
    port_states = working_aut.get_port_order(preorder=True, varinfo=True)

    # now we find the arbitrary port connection:
    targets: list[tuple[str, int]]  # (nodename, nodevariable)
    result_box = None
    for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
        boxcopy = copy.deepcopy(box_catalogue[boxname])
        boxcopy.reformat_ports()
        if matbox_sublang_of_box(working_aut, boxcopy):
            result_box = boxname
            break
    if result_box is not None:
        # now we find the portstates and sort them
        targets = [(s, int(var)) for (_, s, var) in port_states]
    else:
        var = int(term_trs[root].info.variable)
        targets = [(root, var)]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # B) materialized nodes -> initial targets
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # return the original port transitions to the automaton
    for k, e in port_trs:
        working_aut.transitions[e.src][k] = e
    # arbitrary ports should probably be removed
    remove_irrelevant_ports(working_aut, arbitrary=True)

    result_targets: list[ABDDPattern] = []
    for state, var in targets:
        if state in state_sym_lookup:
            noderef = state_sym_lookup[state]
            result_targets.append(ABDDPattern(new=False, name=noderef, level=noderef))
            continue
        pattern = ABDDPattern()
        pattern.new = True
        pattern.name = state
        terminating_transition = None
        for e in iterate_edges_from_state(working_aut, state):
            if e.src in e.children:
                continue
            terminating_transition = e
        if terminating_transition is None:
            raise ValueError(f"no terminating transition found for intermediate state {state}")
        # pattern.level = int(terminating_transition.info.variable)
        pattern.level = "mat"
        for idx, child in enumerate(terminating_transition.children):
            working_aut.roots = [child]
            working_aut.reformat_ports()
            match = None
            subtargets = []
            for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
                boxcopy = copy.deepcopy(box_catalogue[boxname])
                boxcopy.reformat_ports()
                if matbox_sublang_of_box(working_aut, boxcopy):
                    match = boxname
                    for port, s in working_aut.get_port_order():
                        noderef = state_sym_lookup[s]
                        # subtargets.append(ABDDPattern(new=False, name=noderef, level=noderef.var))
                        subtargets.append(ABDDPattern(new=False, name=noderef, level=noderef))
            if not match:
                terminating_transition_2 = None
                for e in iterate_edges_from_state(working_aut, state):
                    if e.src in e.children:
                        continue
                    terminating_transition_2 = e
                if terminating_transition_2 is None:
                    raise ValueError(f"no terminating transition found for intermediate state {state}")
                noderef = state_sym_lookup[child]
                # subtargets.append(ABDDPattern(new=False, name=noderef, level=noderef.var))
                subtargets.append(ABDDPattern(new=False, name=noderef, level=noderef))
            if idx == 0:
                pattern.low = subtargets
                pattern.low_box = match
            elif idx == 1:
                pattern.high = subtargets
                pattern.high_box = match
        result_targets.append(pattern)
    return MaterializationRecipe(result_box, result_targets)


def abdd_subsection_create_wrapper(
    original_abdd: ABDD, original_node: ABDDNode, direction: bool, materialized_box: TTreeAut
) -> MaterializationRecipe:
    # root = materialized_box.roots[0]  # we expect one root state
    # name_node_lookup: dict[str, ABDDNode] = {
    #     f"out{i}": nodes[i] for nodes
    # }

    tgts = original_node.high if direction else original_node.low
    syms = [f"out{i}" for i in range(len(tgts))]
    sym_node_lookup = {s: t for (s, t) in zip(syms, tgts)}

    # state_sym_lookup: dict[str, ABDDNode] = get_state_node_lookup(
    #     original_node.high if direction else original_node.low, materialized_box
    # )
    state_sym_lookup: dict[str, str] = get_state_sym_lookup(syms, materialized_box)
    # print('lookup', state_sym_lookup)
    mat_recipe = abdd_subsection_create(state_sym_lookup, materialized_box)
    return mat_recipe
