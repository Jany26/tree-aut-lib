"""
[file] unfolding.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] ABDD/BDA unfolding procedure implementation.
"""

import copy
from typing import Optional

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges, iterate_states_bfs, shrink_to_top_down_reachable
from helpers.utils import eprint, box_catalogue


def find_port_states(ta: TTreeAut) -> list[str]:
    """
    Returns a list of states which have a port transition.
    NOTE: assuming each port only appears once - for one state
    """
    result: dict[str, str] = {}  # {port_name: state_name}
    for edge in iterate_edges(ta):
        label: str = edge.info.label
        if label.startswith("Port") and label not in result:
            result[label] = edge.src
    # print([result[key] for key in sorted(result.keys())])

    # since we assume port transitions are labeled with numbers in a lexicographic order (Port0, Port1, Port2, ...),
    # i.e. port transitions reached through 0000 (LLLL) come before the ones reached through 1111 (HHHH),
    # we return the sorted list.
    return [result[key] for key in sorted(result.keys())]


def unfold_edge(result: TTreeAut, folded_edge: TTransition, counter: int, sub_table: dict) -> tuple[int, TTransition]:
    """
    Performs an unfolding operation for one edge (edge with box reductions).
    Adds the transitions from box on the unfolded edge to the resulting TA.
    - counter = for unique state names (if >1 identical boxes are on one edge),
    - sub_table = remembers which states ("states with ports" from the box)
    should be substituted for the initial TA states.

    The function returns a 2-tuple of:
    - a number (how many boxes were unfolded on "folded_edge", between 0 and 2 for xBDDs),
    - and the edge after unfolding.
    """
    new_edge_info = TEdge(folded_edge.info.label, [], folded_edge.info.variable)
    new_edge = TTransition(folded_edge.src, new_edge_info, [])
    edge: TTransition = copy.deepcopy(folded_edge)
    unfolded_count: int = 0

    # while edge.info.box_array != [] and edge.children != []:
    while edge.info.box_array != []:
        box_name: str = edge.info.box_array[0]
        edge.info.box_array.pop(0)
        box: Optional[TTreeAut] = None

        if box_name is None:
            new_edge.children.append(edge.children[0])
            edge.children.pop(0)
            continue
        box = copy.deepcopy(box_catalogue[box_name])

        children: list[str] = edge.children[: box.port_arity]
        edge.children = edge.children[box.port_arity :]

        # unfold the box content into result
        # print(result.name, src_state, box.name, children, counter + unfolded)
        for state_name in box.get_states():
            new_name = f"{counter + unfolded_count}_{state_name}_{edge.src}"
            result.transitions[new_name] = copy.copy(box.transitions[state_name])
            box.rename_state(state_name, new_name)
        new_edge.children.extend(box.roots)
        connector_list: list[str] = find_port_states(box)

        for index, state in enumerate(connector_list):
            sub_table[state] = children[index]

        unfolded_count += 1
    return unfolded_count, new_edge


def ubda_unfolding(ta: TTreeAut, reformat=True) -> TTreeAut:
    """
    The whole 'unfolding' cycle. This function goes through all transitions of
    the tree automaton, searching for 'non-short' edges (or edges labeled with
    boxes) and 'unfolds' them (replaces the part of the edge with corresponding
    box = tree automaton). The cycle creates a new TA from scratch.
    stringification of boxes
    """
    result = TTreeAut([i for i in ta.roots], {s: {} for s in ta.roots}, "unfolded(" + ta.name + ")", ta.port_arity)

    unfold_counter: int = 1
    sub_table: dict[str, str] = {}  # substitution table, which states are replaced by which
    # for edge_list in ta.transitions.values():
    #     for key, edge in edge_list.items():
    for state in iterate_states_bfs(ta):
        for key, edge in ta.transitions[state].items():
            if edge.src not in result.transitions:
                result.transitions[edge.src] = {}

            # no boxes on transition (all short edges)
            if edge.info.box_array == []:
                result.transitions[edge.src][key] = copy.deepcopy(edge)
                continue

            boxes_count, new_edge = unfold_edge(result, edge, unfold_counter, sub_table)
            result.transitions[edge.src][key] = new_edge
            unfold_counter += boxes_count

    # Since now the edges have been redirected to the "new" states (unfolded from boxes),
    # and the rest of the original structure is disconnected from the top of the UBDA,
    # we need to redirect the port transitions of the box-edges to the rest of the UBDA.

    # So, now we add all the 'content' edges from states from the initial ABDD/UBDA structure
    # to the states from the unfolded boxes, that have their assigned port transitions.
    for box_state_with_port_tr, state_from_initial_ubda in sub_table.items():
        new_dict: dict[str, str] = {}
        # add original edges to new state with assigned port
        # this cycle 'should' only be performed once (since we assume each node of an ABDD has 'one' transition)
        for edge in result.transitions[state_from_initial_ubda].values():
            new_edge = copy.deepcopy(edge)
            new_edge.src = box_state_with_port_tr
            new_key = f"{new_edge.src}-{new_edge.info.label}-{new_edge.children}"
            new_dict[new_key] = new_edge

        # NOTE: this line is left in only for testing purposes, it is bugged,
        # as port states got all their initial transitions removed
        # result.transitions[place_state] = new_dict

        # it is assumed that only one port transition at a time
        # can be reached from one state, so we remove it
        key_to_pop: str = ""
        for key, edge in result.transitions[box_state_with_port_tr].items():
            if edge.info.label.startswith("Port"):
                key_to_pop = key
        # merging the transitions from box and initial transitions
        result.transitions[box_state_with_port_tr].update(new_dict)
        # but also removing the initial port transition
        result.transitions[box_state_with_port_tr].pop(key_to_pop)
    result: TTreeAut = shrink_to_top_down_reachable(result)
    if reformat is True:
        result.reformat_states()
        result.reformat_keys()
    return result


def is_unfolded(ta: TTreeAut) -> bool:
    """
    This function checks if there are any boxes in the tree automaton (UBDA),
    if no boxes are found, the UBDA is unfolded.
    """
    for edge in iterate_edges(ta):
        for box in edge.info.box_array:
            if box is not None:
                eprint(f"is_unfolded[ {ta.name} ]: found a box: {edge}")
                return False
    return True


# redundant below ...


def fix_keys(ta: TTreeAut):
    """
    Goes through all edges and "updates" their keys in the transition lookup
    dictionary. After unfolding, some edges could be labeled incorrectly.
    NOTE: probably obsolete
    """
    for state, edge_dict in ta.transitions.items():
        new_edge_dict = {}
        for edge in edge_dict.values():
            new_key = f"{edge.src}-{edge.info.label}-{edge.children}"
            new_edge_dict[new_key] = edge
        ta.transitions[state] = new_edge_dict


def stringify_boxes(ta: TTreeAut):
    """
    Change box objects on edges to their names (strings).
    NOTE: Initial attempt for compatibility with dot/vtf format modules, now redundant.
    """
    for edge in iterate_edges(ta):
        new_array = []
        for box in edge.info.box_array:
            if box is None:
                new_array.append(None)
            elif type(box) == TTreeAut or type(box) == type(TTreeAut):
                new_array.append(box.name)
            else:
                new_array.append(box)
        edge.info.box_array = new_array


# End of file unfolding.py
