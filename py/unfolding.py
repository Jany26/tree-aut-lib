"""
[file] unfolding.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] ABDD/BDA unfolding procedure implementation.
"""

from utils import *
from ta_classes import *
from ta_functions import *
from test_data import *


# Returns a list of states which have a port transition.
# NOTE: assuming each port only appears once - for one state
def find_port_states(ta: TTreeAut):
    # {port_name: state_name}
    result = {}
    for edge in iterate_edges(ta):
        label: str = edge.info.label
        if label.startswith("Port") and label not in result:
            result[label] = edge.src
    # print([result[key] for key in sorted(result.keys())])
    return [result[key] for key in sorted(result.keys())]


# Performs an unfolding operation for one edge (edge with box reductions).
# Adds the transitions from box on the unfolded edge to the resulting TA.
# - counter = for unique state names (if >1 identical boxes are on one edge)
# - sub_table = remembers which states ("states with ports" from the box)
# should be substituted for the initial TA states
def unfold_edge(result: TTreeAut, folded_edge: TTransition, counter: int, sub_table: dict):
    new_edge_info = TEdge(folded_edge.info.label, [], folded_edge.info.variable)
    new_edge = TTransition(folded_edge.src, new_edge_info, [])
    edge = copy.deepcopy(folded_edge)
    unfolded = 0

    while edge.info.box_array != []:
        src_state = edge.src
        box_name = edge.info.box_array[0]
        edge.info.box_array.pop(0)
        box = None

        if box_name is None:
            new_edge.children.append(edge.children[0])
            edge.children.pop(0)
            continue
        box = copy.deepcopy(box_catalogue[box_name])

        children = edge.children[: box.port_arity]
        edge.children = edge.children[box.port_arity :]

        # unfold the box content into result
        # print(result.name, src_state, box.name, children, counter + unfolded)
        for state_name in box.get_states():
            new_name = f"{counter+unfolded}_{state_name}_{src_state}"
            result.transitions[new_name] = copy.copy(box.transitions[state_name])
            box.rename_state(state_name, new_name)
        new_edge.children.extend(box.roots)
        connector_list = find_port_states(box)

        for index, state in enumerate(connector_list):
            sub_table[state] = children[index]

        unfolded += 1
    return unfolded, new_edge


# The whole 'unfolding' cycle. This function goes through all transitions of
# the tree automaton, searching for 'non-short' edges (or edges labeled with
# boxes) and 'unfolds' them (replaces the part of the edge with corresponding
# box = tree automaton). The cycle creates a new TA from scratch.
def unfold(ta: TTreeAut, reformat=True) -> TTreeAut:
    # stringification of boxes
    result = TTreeAut([i for i in ta.roots], {s: {} for s in ta.roots}, "unfolded(" + ta.name + ")", ta.port_arity)

    unfold_counter = 1
    sub_table = {}
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

    for place_state, content_state in sub_table.items():
        new_dict = {}
        for edge in result.transitions[content_state].values():
            new_edge = copy.deepcopy(edge)
            new_edge.src = place_state
            new_key = f"{new_edge.src}-{new_edge.info.label}-{new_edge.children}"
            new_dict[new_key] = new_edge

        # this line is left in only for testing purposes, it is bugged,
        # as port states got all their initial transitions removed
        # result.transitions[place_state] = new_dict

        # it is assumed that only one port transition at a time
        # can be reached from one state
        key_to_pop = ""
        for key, edge in result.transitions[place_state].items():
            if edge.info.label.startswith("Port"):
                key_to_pop = key
        # merging the transitions from box and initial transitions
        result.transitions[place_state].update(new_dict)
        # but also removing the initial port transition
        result.transitions[place_state].pop(key_to_pop)
    result = shrink_to_top_down_reachable(result)
    if reformat is True:
        result.reformat_states()
        result.reformat_keys()
    return result


# Goes through all edges and "updates" their keys in the transition lookup
# dictionary. After unfolding, some edges could be labeled incorrectly.
# NOTE: probably obsolete
def fix_keys(ta: TTreeAut):
    for state, edge_dict in ta.transitions.items():
        new_edge_dict = {}
        for edge in edge_dict.values():
            new_key = f"{edge.src}-{edge.info.label}-{edge.children}"
            new_edge_dict[new_key] = edge
        ta.transitions[state] = new_edge_dict


# This function checks if there are any boxes in the tree automaton (UBDA),
# if no boxes are found, the UBDA is unfolded. For testing purposes.
def is_unfolded(ta: TTreeAut) -> bool:
    for edge in iterate_edges(ta):
        for box in edge.info.box_array:
            if box is not None:
                eprint(f"is_unfolded[ {ta.name} ]: found a box: {edge}")
                return False
    return True


def stringify_boxes(ta: TTreeAut):
    for edge in iterate_edges(ta):
        new_array = []
        for box in edge.info.box_array:
            if box is None:
                new_array.append(None)
            elif type(box) == TTreeAut:
                new_array.append(box.name)
            else:
                new_array.append(box)
        edge.info.box_array = new_array


# End of file unfolding.py
