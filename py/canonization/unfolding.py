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
from tree_automata.var_manipulation import saturate_box_edges_with_variables
from tree_automata.automaton import iterate_key_edge_tuples


class UnfoldingHelper:
    def __init__(self, input: TTreeAut, max_var: int, reformat: bool, sat: bool):
        self.input = input
        self.output = TTreeAut(
            [i for i in input.roots], {s: {} for s in input.roots}, "unfolded(" + input.name + ")", 0
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
            raise Exception(f"ubda_unfolding(): didn't get enough information about outgoing variables, edge {edge}")

    while edge.info.box_array != []:
        box_name: str = edge.info.box_array[0]
        edge.info.box_array.pop(0)
        box: Optional[TTreeAut] = None

        if box_name is None:
            new_edge.children.append(edge.children[0])
            edge.children.pop(0)
            # NOTE: even when we do not need to unfold, we HAVE to discard one used outvar
            out_vars = out_vars[1:]
            continue
        box = copy.deepcopy(box_catalogue[box_name])

        children: list[str] = edge.children[: box.port_arity]
        edge.children = edge.children[box.port_arity :]

        if helper.variable_saturation:
            # Here we saturate the box transitions with variable information
            saturate_box_edges_with_variables(box, helper.prefix, start_var, out_vars, helper.max_var)
            out_vars = out_vars[box.port_arity :]  # discard used variables

        # unfold the box content into result
        for state_name in box.get_states():
            new_name = f"{helper.unfold_counter + unfolded_count}_{state_name}_{edge.src}"
            helper.output.transitions[new_name] = copy.copy(box.transitions[state_name])
            box.rename_state(state_name, new_name)
        new_edge.children.extend(box.roots)
        connector_list: list[str] = find_port_states(box)

        for index, state in enumerate(connector_list):
            helper.sub_table[state] = children[index]

        unfolded_count += 1
    return unfolded_count, new_edge


def unfold_root_rule(ta: TTreeAut, max_var: int, helper: UnfoldingHelper):
    box = copy.deepcopy(box_catalogue[ta.rootbox])
    if box.port_arity != len(ta.roots):
        raise ValueError("unfold_root_rule(): number of roots != port arity of root reduction box")

    start_var = 1
    out_vars = get_outgoing_variables(
        helper, TTransition("", TEdge("temp", [], f"{helper.prefix}{start_var}"), [r for r in ta.roots])
    )
    statemap = {box_state: ubda_state for box_state, ubda_state in zip([s for _, s in box.get_port_order()], ta.roots)}

    if helper.variable_saturation:
        # Here we saturate the box transitions with variable information
        saturate_box_edges_with_variables(box, helper.prefix, start_var, out_vars, helper.max_var)
        out_vars = out_vars[box.port_arity :]  # discard used variables

    # unfold the box content into result
    # print(result.name, src_state, box.name, children, counter + unfolded)
    for state_name in box.get_states():
        new_name = f"{helper.unfold_counter}_{state_name}_root"
        if state_name in statemap:
            new_name = statemap[state_name]
        if state_name in box.roots:
            helper.output.roots = [new_name]
        for key, tr in box.transitions[state_name].items():
            if new_name not in helper.output.transitions:
                helper.output.transitions[new_name] = {}
            if tr.info.label.startswith("Port"):
                continue
            helper.output.transitions[new_name][key] = tr
        box.rename_state(state_name, new_name)


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

    # unfold root box
    if ta.rootbox is not None:
        unfold_root_rule(ta, max_var, helper)

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
    if ta.rootbox is not None:
        eprint(f"is_unfolded[ {ta.name} ]: found a root box: {ta.rootbox}")
        return False
    if len(ta.roots) != 1:
        eprint(f"is_unfolded[ {ta.name} ]: unfolded UBDA have 1 root")
        return False
    for edge in iterate_edges(ta):
        for box in edge.info.box_array:
            if box is not None:
                eprint(f"is_unfolded[ {ta.name} ]: found a box: {edge}")
                return False
    return True


def remove_useless_transitions(ta: TTreeAut):
    minvarin: dict[str, int] = {r: 1 for r in ta.roots}
    maxvarout: dict[str, int] = {}
    plen = len(ta.get_var_prefix())
    for e in iterate_edges(ta):
        if e.is_self_loop() or e.info.variable == "":
            continue
        var = int(e.info.variable[plen:])
        maxvarout[e.src] = max(var, maxvarout[e.src]) if e.src in maxvarout else var
        for c in e.children:
            minvarin[c] = min(var + 1, minvarin[c]) if c in minvarin else var + 1
    to_remove: list[tuple[str, str]] = []
    for k, e in iterate_key_edge_tuples(ta):
        if e.is_self_loop() and minvarin[e.src] == maxvarout[e.src]:
            to_remove.append((e.src, k))
    for s, k in to_remove:
        ta.remove_transition(s, k)


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
