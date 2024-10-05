"""
[file] unfolding.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] ABDD/BDA unfolding procedure implementation.
"""

import copy
from os import remove
from typing import Optional

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges, iterate_states_bfs, shrink_to_top_down_reachable
from helpers.utils import eprint, box_catalogue
from tree_automata.automaton import iterate_key_edge_tuples


class UnfoldingHelper:
    def __init__(self, input: TTreeAut, max_var: int, reformat: bool, sat: bool):
        self.input = input
        self.output = TTreeAut(
            [i for i in input.roots], {s: {} for s in input.roots}, "unfolded(" + input.name + ")", input.port_arity
        )
        self.max_var = max_var
        self.reformat = reformat
        self.unfold_counter: int = 1
        self.sub_table: dict[str, str] = {}  # substitution table, which states are replaced by which
        self.prefix = self.input.get_var_prefix()
        self.prefix_len = len(self.prefix)
        self.variable_saturation = sat


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


def get_outgoing_variables(helper: UnfoldingHelper, edge: TTransition) -> list[int]:
    """
    We derive variable indexes for each of the edge's child states.
    Since box can have more ports and each port is assigned to a different state,
    we assume that each state has a different out_var, so that's why we store
    these variables in a list.

    Variable saturation does not need to know the state names
    (in box transitions, we work different set of states,
    and only know where do the variables belong to based on the numbered ports),
    we only need to know the order of these variable numbers -- i.e. to which index of port transition
    will the variable later belong to.
    """
    result: list[int] = []
    for child in edge.children:
        for edge2 in helper.input.transitions[child].values():
            if edge2.info.variable == "":
                continue
            result.append(int(edge2.info.variable[helper.prefix_len :]))
            break
    return result


def saturate_box_edges_with_variables(
    box: TTreeAut, prefix: str, min_var: int, out_vars: list[int], max_var: int
) -> None:
    variable_map: dict[str, int] = {}
    # store state-key pairs of edges that "can" and should be saturated, basically non-self-loops
    work_set: set[tuple[str, str]] = set()
    selflooping_states: set[str] = set()
    # assign root variable
    for root in box.roots:
        variable_map[root] = min_var

    ports_states_list: list[tuple[str, str]] = []
    # get information about port transitions -- tuple (portname, statename)
    # initialize set of selflooping states and set of saturable edges
    for key, edge in iterate_key_edge_tuples(box):
        if edge.info.label.startswith("Port"):
            ports_states_list.append(tuple((edge.info.label, edge.src)))
        if edge.is_self_loop():
            selflooping_states.add(edge.src)
        else:
            work_set.add(tuple((edge.src, key)))

    # lexicographically sort portnames and assign variables from ordered out_vars array
    ports_states_list = sorted(ports_states_list, key=lambda x: x[0])
    for idx, (_, state) in enumerate(ports_states_list, start=0):
        variable_map[state] = out_vars[idx]

    for edge in iterate_edges(box):
        # saturate port edges with variables (using the var map)
        if edge.info.label.startswith("Port"):
            edge.info.variable = f"{prefix}{variable_map[edge.src]}"
            continue
        # saturate non-port output edges with variables
        if not edge.info.label.startswith("Port") and len(edge.children) == 0:
            edge.info.variable = f"{prefix}{max_var}"
            variable_map[edge.src] = max_var
            continue
    # fixpoint-like algorithm that saturates the edges top-down and bottom-up
    while True:
        # top-down saturation
        used_edges: set[tuple[str, str]] = set()
        for state, key in work_set:
            edge: TTransition = box.transitions[state][key]
            if edge.is_self_loop() or edge.src in selflooping_states:
                continue
            if edge.info.variable != "":
                continue
            if state not in variable_map:
                continue
            # At this point, we have an edge that:
            #   - its source state does not have any self loop,
            #   - has not yet been labeled with a variable,
            #   - its source state is assigned a variable
            # So now we can:
            #   - add the variable to the edge,
            #   - propagate the variable information to children, where possible,
            #   - store a flag for removing this edge from a work_set.
            edge.info.variable = f"{prefix}{variable_map[state]}"
            for child in edge.children:
                if child not in variable_map:
                    variable_map[child] = variable_map[state] + 1
            used_edges.add(tuple((state, key)))
        work_set = work_set - used_edges

        # bottom-up saturation
        for state, key in work_set:
            edge: TTransition = box.transitions[state][key]
            if edge.is_self_loop():
                continue
            if edge.info.variable != "":
                continue
            if state not in variable_map:
                continue
            var_to_add: Optional[int] = None
            for child in edge.children:
                if child not in selflooping_states and child in variable_map:
                    var_to_add = variable_map[child] - 1
            # We want to saturate variables bottom-up only when:
            #   - the edge itself is not a self loop
            #   - the edge
            #   - some child is non-self-looping and has an assigned variable
            if var_to_add is not None:
                edge.info.variable = f"{prefix}{var_to_add}"
                variable_map[edge.src] = var_to_add
                used_edges.add(tuple((state, key)))
        work_set = work_set - used_edges

        if len(used_edges) == 0:  # if no progress is done, terminate.
            break


def unfold_edge(helper: UnfoldingHelper, folded_edge: TTransition) -> tuple[int, TTransition]:
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

    if helper.variable_saturation:
        # Preparing some information about variables
        # + 1 is there because the edge itself points to the rootstate of the box,
        # and so the edges starting from the rootstate are one higher than what was on the original folded edge
        start_var: int = int(folded_edge.info.variable[helper.prefix_len :]) + 1
        out_vars: list[int] = get_outgoing_variables(helper, edge)
        if len(out_vars) != len(edge.children):
            print(out_vars)
            raise Exception(f"ubda_unfolding(): didn't get enough information about outgoing variables, edge {edge}")

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

        if helper.variable_saturation:
            # Here we saturate the box transitions with variable information
            saturate_box_edges_with_variables(box, helper.prefix, start_var, out_vars, helper.max_var)
            out_vars = out_vars[box.port_arity :]  # discard used variables

        # unfold the box content into result
        # print(result.name, src_state, box.name, children, counter + unfolded)
        for state_name in box.get_states():
            new_name = f"{helper.unfold_counter + unfolded_count}_{state_name}_{edge.src}"
            helper.output.transitions[new_name] = copy.copy(box.transitions[state_name])
            box.rename_state(state_name, new_name)
        new_edge.children.extend(box.roots)
        connector_list: list[str] = find_port_states(box)

        for index, state in enumerate(connector_list):
            helper.sub_table[state] = children[index]
        # print(helper.sub_table)

        unfolded_count += 1
    return unfolded_count, new_edge


def ubda_unfolding(ta: TTreeAut, max_var: int, reformat=True, saturate=True) -> TTreeAut:
    """
    The whole 'unfolding' cycle. This function goes through all transitions of
    the tree automaton, searching for 'non-short' edges (or edges labeled with
    boxes) and 'unfolds' them (replaces the part of the edge with corresponding
    box = tree automaton). The cycle creates a new TA from scratch.
    stringification of boxes
    """
    helper = UnfoldingHelper(ta, max_var, reformat, saturate)

    if helper.variable_saturation:
        # Variable saturation of output edges:
        for state in ta.get_output_states():
            for edge in ta.transitions[state].values():
                edge.info.variable = f"{helper.prefix}{helper.max_var}"

    for state in iterate_states_bfs(ta):
        for key, edge in ta.transitions[state].items():
            if edge.src not in helper.output.transitions:
                helper.output.transitions[edge.src] = {}

            # no boxes on transition (all short edges)
            if not edge.info.check_edge_for_boxes():
                helper.output.transitions[edge.src][key] = copy.deepcopy(edge)
                continue

            boxes_count, new_edge = unfold_edge(helper, edge)
            helper.output.transitions[edge.src][key] = new_edge
            helper.unfold_counter += boxes_count

    # Since now the edges have been redirected to the "new" states (unfolded from boxes),
    # and the rest of the original structure is disconnected from the top of the UBDA,
    # we need to redirect the port transitions of the box-edges to the rest of the UBDA.

    # So, now we add all the 'content' edges from states from the initial ABDD/UBDA structure
    # to the states from the unfolded boxes, that have their assigned port transitions.
    for box_state_with_port_tr, state_from_initial_ubda in helper.sub_table.items():
        new_dict: dict[str, str] = {}
        # add original edges to new state with assigned port
        # this cycle 'should' only be performed once (since we assume each node of an ABDD has 'one' transition)
        for edge in helper.output.transitions[state_from_initial_ubda].values():
            new_edge: TTransition = copy.deepcopy(edge)
            new_edge.src = box_state_with_port_tr
            new_key = f"{new_edge.src}-{new_edge.info.label}-{new_edge.children}"
            new_dict[new_key] = new_edge

        # NOTE: this line is left in only for testing purposes, it is bugged,
        # as port states got all their initial transitions removed
        # result.transitions[place_state] = new_dict

        # it is assumed that only one port transition at a time
        # can be reached from one state, so we remove it
        key_to_pop: str = ""
        for key, edge in helper.output.transitions[box_state_with_port_tr].items():
            if edge.info.label.startswith("Port"):
                key_to_pop = key
        # merging the transitions from box and initial transitions
        helper.output.transitions[box_state_with_port_tr].update(new_dict)
        # but also removing the initial port transition
        helper.output.transitions[box_state_with_port_tr].pop(key_to_pop)
    result: TTreeAut = shrink_to_top_down_reachable(helper.output)
    if helper.reformat is True:
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
