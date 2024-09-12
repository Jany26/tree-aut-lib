from tree_automata.transition import TTransition, TEdge
from tree_automata.automaton import state_name_sort as var_name_sort, iterate_edges, TTreeAut


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


def create_var_order_dict(prefix: str, count: int, start=1):
    return [f"{prefix}{i+start}" for i in range(count)]


def create_var_order_apply(variables: list[str], terminals: list) -> dict:
    """
    Makes the list into a dictionary for easy lookup of indexing
    """
    if variables is not None:
        variables = var_name_sort(variables)
    result = {}
    i = 1
    for var in variables:
        if var not in result:
            result[var] = i
            i += 1
    # for t in terminals:
    #     result[str(t)] = i
    return result


def get_var_prefix(var_list: list[str]) -> str:
    if var_list == []:
        return ""
    prefix_len = 0
    for i in range(len(var_list[0])):
        if not var_list[0][i:].isnumeric():
            prefix_len += 1
    prefix = var_list[0][:prefix_len]
    return prefix


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


# creates a list of variable truth-values indexed by their order
# (the order in which they are evaluated during BDD top-down traversal)
# if an ABDD has a variable range of size 10, this function would be used 2^10 times
def assign_variables(num: int, size: int) -> list[int]:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return result


# creates a int (var index) -> int (0/1 = true/false) dictionary from an integer number
# (iterated number in a cycle)
# if an ABDD has a variable range of size 10, this function is used 2^10 times
def assign_variables_dict(num: int, size: int) -> dict[int, int]:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    result_dict = {i + 1: result[i] for i in range(size)}
    return result_dict
