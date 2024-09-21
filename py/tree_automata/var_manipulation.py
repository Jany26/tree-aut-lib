from typing import Dict, Tuple, Set, List

from tree_automata.transition import TTransition, TEdge
from tree_automata.automaton import iterate_edges, TTreeAut
from helpers.string_manipulation import get_var_prefix


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
    var_prefix = get_var_prefix(ta.get_var_order())
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


def add_variables_fixpoint(ta: TTreeAut, maxvar: int):
    work_set = []

    # state -> (minimum incoming variable, maximum outgoing variable, loop present)
    visibility_cache: Dict[str, Tuple[int, int, bool]]
    fixpoint_changed = True
    for edge in iterate_edges(ta):
        if not edge.is_self_loop() and edge.info.variable == "" and len(edge.children) != 0:
            work_set.append(edge)

    for i in work_set:
        print(i)

    while fixpoint_changed and work_set != []:
        fixpoint_changed = False


def find_useless_loop_transitions(ta: TTreeAut) -> Dict[str, set[str]]:
    """
    Useless loop transitions will never be used, since there is only one variable that is checked while within the state.

    E.g.:
    q0 -- x1 -> (q1, q2)
    q1 -- __ -> (q1, q1)  == this loop is useless
    q1 -- x2 -> (q3, q4)  == for variables x3 or higher, the looping transition would not be useless.

    Returns a state name -> set of transition keys dictionary to edges that can be removed.
    """
    var_translator = ta.var
