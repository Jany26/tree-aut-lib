from typing import Dict, Optional, Tuple, Set, List

from tree_automata.transition import TTransition, TEdge
from tree_automata.automaton import iterate_edges, iterate_output_edges, iterate_key_edge_tuples, TTreeAut
from helpers.string_manipulation import get_var_prefix_from_list


# This is strictly for compacting the UBDA before output for testing purposes.
# Instead of many identical edges (with just different variables),
# the edges are merged into one where variables are compacted into one string.
# This provides much more readable format.
# Only use this function before outputting the UBDA.
def compress_vars(ta: TTreeAut) -> TTreeAut:
    temp = {}
    for edge in iterate_edges(ta):
        # box_names parsing for the key:
        boxes_str = ""
        for box in edge.info.box_array:
            if box is None:
                box_name = "_"
            else:
                box_name = box if type(box) == str else box.name
                if box_name.startswith("box"):
                    box_name = box_name[len("box") :]
            boxes_str += "," + box_name
        boxes_str.lstrip(",")
        # end of box_names parsing
        temp_key = f"{edge.src}-{edge.info.label}{boxes_str}-{edge.children}"
        if temp_key not in temp:
            temp[temp_key] = [[], []]
        temp[temp_key][0] = [edge.src, edge.info.label, edge.info.box_array, edge.children]
        temp[temp_key][1].append(edge.info.variable)

    transitions = {}
    for key, edge_data in temp.items():
        src = edge_data[0][0]
        symb = edge_data[0][1]
        box_array = edge_data[0][2]
        children = edge_data[0][3]
        vars = ",".join(edge_data[1])
        edge = TEdge(symb, box_array, vars)
        if src not in transitions:
            transitions[src] = {}
        transitions[src][key] = TTransition(src, edge, children)
    result = TTreeAut(ta.roots, transitions, f"{ta.name}", ta.port_arity)
    return result


# For faster/more precise decision making, especially in unfolded UBDAs.
# TODO: Needs fixing (see results/folding-error-2/...)
def add_variables_bottom_up(ta: TTreeAut, max_var: int):
    def convert_vars(var_list: list, prefix: str) -> dict:
        return {i: int(i[len(prefix) :]) for i in var_list}

    var_vis = ta.get_var_visibility()
    true_leaves = set()
    var_prefix = get_var_prefix_from_list(ta.get_var_order())
    for leaf in ta.get_output_states():
        if len(ta.transitions[leaf]) == 1:
            true_leaves.add(leaf)
    var_lookup = convert_vars(ta.get_var_order(), var_prefix)

    for edge in iterate_edges(ta):
        if edge.info.variable != "" or edge.src in edge.children:
            continue
        for child in edge.children:
            if child in var_vis:
                var = var_lookup[list(var_vis[child])[0]]
                new_var = f"{var_prefix}{int(var)-1}"
                edge.info.variable = new_var
            if child in true_leaves:
                edge.info.variable = f"{var_prefix}{max_var}"
    # end for


def saturate_box_edges_with_variables(
    box: TTreeAut, prefix: str, min_var: int, out_vars: list[int], max_var: int
) -> None:
    """
    Before the box is unfolded into the UBDA, it is saturated with variables.
    `prefix` is the variable prefix used in the UBDA for proper variable tagging.
    `min_var` is the variable the rootstate is supposed to see.
    `out_vars` is a sorted array of the output edge variables for the port states (sortable by the port indexes).
    This algorithm assumes that each port potentially could lead to a different variable.
    `max_var` is the maximum variable of the whole UBDA.
    """
    variable_map: dict[str, int] = {}
    # store state-key pairs of edges that "can" and should be saturated, basically non-self-loops
    work_set: set[TTransition] = set()
    selflooping_states: set[str] = set()
    # assign root variable
    for root in box.roots:
        variable_map[root] = min_var

    ports_states_list: list[tuple[str, str]] = []
    # get information about port transitions -- tuple (portname, statename)
    # initialize set of selflooping states and set of saturable edges
    for edge in iterate_edges(box):
        if edge.info.label.startswith("Port"):
            ports_states_list.append(tuple((edge.info.label, edge.src)))
        if edge.is_self_loop():
            selflooping_states.add(edge.src)
        else:
            work_set.add(edge)

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
        used_edges: set[TTransition] = set()
        for edge in work_set:
            if edge.is_self_loop() or edge.src in selflooping_states:
                continue
            if edge.info.variable != "":
                continue
            if edge.src not in variable_map:
                continue
            # At this point, we have an edge that:
            #   - its source state does not have any self loop,
            #   - has not yet been labeled with a variable,
            #   - its source state is assigned a variable
            # So now we can:
            #   - add the variable to the edge,
            #   - propagate the variable information to children, where possible,
            #   - store a flag for removing this edge from a work_set.
            edge.info.variable = f"{prefix}{variable_map[edge.src]}"
            for child in edge.children:
                if child not in variable_map:
                    variable_map[child] = variable_map[edge.src] + 1
            used_edges.add(edge)
        work_set = work_set - used_edges

        # bottom-up saturation
        for edge in work_set:
            if edge.is_self_loop():
                continue
            if edge.info.variable != "":
                continue
            var_to_add: Optional[int] = None
            for child in edge.children:
                if child not in selflooping_states and child in variable_map:
                    var_to_add = variable_map[child] - 1
            # We want to saturate variables bottom-up only when:
            #   - the edge itself is not a self loop
            #   - the edge is still untagged with a variable
            #   - some child is non-self-looping and has an assigned variable
            if var_to_add is not None:
                edge.info.variable = f"{prefix}{var_to_add}"
                variable_map[edge.src] = var_to_add
                used_edges.add(edge)
        work_set = work_set - used_edges

        if len(used_edges) == 0 or len(work_set) == 0:  # if no progress is done, terminate.
            break


def add_variables_fixpoint(ta: TTreeAut, maxvar: Optional[int] = None):
    """
    Saturate UBDA structure using both a bottom-up and a top-down approach, until no changes are possible.
    In this version of the saturation, it is possible to infer variables of the root states.
    Another difference is that all leaf states are assumed to have the same variable on the output edges = `maxvar`.
    If `maxvar` is not given, an attempt to infer its value from all leaf transitions is made.
    If it fails, ValueError is raised.
    Otherwise it is very similar to `saturate_box_edges_with_variables()`
    """
    # initialize work_set and maxvar (if None)
    work_set: set[TTransition] = set()
    variable_map: dict[str, int] = {}
    selfloop_states: set[str] = set()
    var_prefix = ta.get_var_prefix()

    # initialization phase - find edges  set maxvar, get selfloop states, get state->variable info
    for edge in iterate_edges(ta):
        if edge.is_self_loop():
            selfloop_states.add(edge.src)
            continue
        if edge.info.variable != "":
            if edge.src not in variable_map:
                variable_map[edge.src] = edge.info.variable
            if edge.children == [] and maxvar is None:
                maxvar = edge.info.variable
        if edge.children != []:
            work_set.add(edge)  # we only add non-leaf, no-selfloop edges without a variable

    if maxvar is None:
        raise ValueError("maxvar not set")

    # leaf edges saturation
    for edge in iterate_output_edges(ta):
        if edge.info.variable == "":
            edge.info.variable = f"{var_prefix}{maxvar}"
            variable_map[edge.src] = maxvar
            continue
        elif edge.info.variable != f"{var_prefix}{maxvar}":
            raise ValueError("inconsistent leaf edge variables")

    # main fixpoint cycle
    while True:
        used_set: set[TTransition] = set()
        for edge in work_set:  # top-down saturation
            if (
                edge.is_self_loop()  # we only saturate edges top-down, when they themselves are not self-loops,
                or edge.src in selfloop_states  # the source state is not able to otherwise perform self-loops,
                or edge.info.variable != ""  # the edge itself is still untagged with a variable,
                or edge.src not in variable_map
            ):  # and we know the variable of the source state.
                continue
            edge.info.variable = f"{var_prefix}{variable_map[edge.src]}"  # add the variable to the edge,
            for child in edge.children:  # propagate the variable information to children,
                if child not in variable_map:  # where possible,
                    variable_map[child] = variable_map[edge.src] + 1
            used_set.add(edge)  # and flag an edge for work_set removal
        work_set = work_set - used_set

        for edge in work_set:  # bottom-up saturation
            # we only saturate edges bottom-up, when they are not self-loops, are without a variable,
            if edge.is_self_loop() or edge.info.variable != "":
                continue
            # and at least one of the children is not selflooping and has an assigned variable
            var_to_add: Optional[int] = None
            for child in edge.children:
                if child not in selfloop_states and child in variable_map:
                    var_to_add = variable_map[child] - 1
            if var_to_add is not None:
                edge.info.variable = f"{var_prefix}{var_to_add}"
                used_set.add(edge)
                variable_map[edge.src] = var_to_add
        work_set = work_set - used_set

        if len(used_set) == 0 or len(work_set) == 0:  # if no changes can be made, we stop
            break


def find_useless_loop_transitions(ta: TTreeAut) -> Dict[str, set[str]]:
    """
    Useless loop transitions will never be used, since there is only one variable that is checked while within the state.

    E.g.:
    q0 -- x1 -> (q1, q2)
    q1 -- __ -> (q1, q1)  == this loop is useless
    q1 -- x2 -> (q3, q4)  == for variables x3 or higher, the looping transition would not be useless.

    Returns a state name -> set of transition keys dictionary to edges that can be removed.

    NOTE: This was part of an attempt to fix normalization, with var_cache fix it is now discontinued.
    """
    var_translator = ta.var


def find_all_root_leaf_paths(ta: TTreeAut) -> list[list[tuple[str, str, int]]]:
    """
    A path is a list of tuples containing state, key, child-index
        - state and key are for edge lookup
        - child index is for knowing how the next item was reached

    E.g.:
    `[ (q0, k0, 0), (q1, k1, 1), ... ]`
        - starting in state q0, taking edge with key k0, and visiting child at index 0
        - the next state is q1, and next edge taken is at key k1, etc...

    NOTE: This was an attempt to check the result of normalization in a brute-force manner, now discontinued.
    """
    pass


def check_variable_overlap(ta: TTreeAut, max_var: Optional[int] = None) -> bool:
    """
    For each state, check if there is a possibility to reach this state using some var xi
    and a transition through xj such that j <= i is possible.

    If possible, the given UBDA structure is faulty.
    This function is mainly used to check the result of normalization.

    Return True if no overlap is found (result is okay / not faulty), otherwise False.
    """
    # init max_var using output_edges' variables
    var_prefix_len: int = len(ta.get_var_prefix())
    if max_var is None:
        for edge in iterate_output_edges(ta):
            if edge.info.variable != "":
                max_var = int(edge.info.variable[var_prefix_len:])
        if max_var is None:
            raise ValueError("check_in_var_out_var_overlap(): could not infer maximum variable in the UBDA.")

    # we try to find max{in_vars} and min{out_vars} to maximize chance of variable overlap for error detection
    in_vars: dict[str, int] = {s: 0 for s in ta.get_states()}
    out_vars: dict[str, int] = {s: max_var for s in ta.get_states()}

    # loading phase
    for edge in iterate_edges(ta):
        if edge.info.variable == "":
            continue
        var: int = int(edge.info.variable[var_prefix_len:])
        out_vars[edge.src] = max(out_vars[edge.src], var)
        for child in edge.children:
            in_vars[child] = min(in_vars[child], var)

    # checking phase - minimum outgoing variable has to be strongly larger than maximum incoming variable
    for state in ta.get_states():
        if in_vars[state] >= out_vars[state]:
            return False

    return True
