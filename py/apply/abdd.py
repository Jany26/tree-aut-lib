from typing import Generator, Optional
from apply.abdd_check import check_if_abdd
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_states_bfs
from tree_automata.transition import TTransition
from apply.abdd_node import ABDDNode


class ABDD:
    name: str
    variable_count: int
    root: ABDDNode
    node_map: dict[str, ABDDNode]
    node_count: int
    terminal_0: Optional[ABDDNode]
    terminal_1: Optional[ABDDNode]

    def __init__(self, name: str, variable_count: int, root: ABDDNode):
        """
        Initializing ABDD structure will omit self-looping transitions in the TA/UBDA structure.
        Missing variables or box information will raise an exception.
        """
        self.name = name
        self.variable_count = variable_count
        self.root = root
        self.node_map = {}
        self.node_count = 0
        self.terminal_0: Optional[ABDDNode] = root.find_terminal(0)
        self.terminal_1: Optional[ABDDNode] = root.find_terminal(1)

    def iterate_bfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_bfs(repeat)

    def iterate_dfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_dfs(repeat)

    def count_nodes(self) -> int:
        result = 0
        for i in self.root.explore_subtree_bfs():
            result += 1
        return result

    def evaluate_for(self, assignment: dict[int, bool]) -> int:
        pass

    def __repr__(self):
        result = f"  [ABDD]: '{self.name}'\n"
        result += f"  > Root = {self.root.node}\n"
        result += "  > %-*s %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
            8,
            "nodeID",
            8,
            "varID",
            8,
            "leaf",
            8,
            "lowBox",
            8,
            "lowNode",
            8,
            "highBox",
            8,
            "highNode",
        )
        result += f"  " + "-" * 65 + "\n"
        for i in self.root.explore_subtree_bfs(repeat=False):
            lowStr = i.low.node if i.low is not None else "-"
            highStr = i.high.node if i.high is not None else "-"
            leaf = i.leaf_val if i.leaf_val is not None else "-"
            lowBox = i.low_box if i.low_box is not None else "-"
            highBox = i.high_box if i.high_box is not None else "-"
            result += "  > %-*s %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
                8,
                i.node,
                8,
                i.var,
                8,
                leaf,
                8,
                lowBox,
                8,
                lowStr,
                8,
                highBox,
                8,
                highStr,
            )
        return result

    def convert_to_treeaut_obj(self) -> TTreeAut:
        pass

    def reformat_node_names(self):
        name_map: dict[int, int] = {}
        counter = 0
        for i in self.root.explore_subtree_bfs():
            if i.node is not None and i.node not in name_map:
                i.node = counter
                counter += 1

    def materialize_node_above(self):
        pass


def import_abdd_from_abdd_file(path: str) -> ABDD:
    """
    TODO
    """
    pass


def init_abdd_from_ta(ta: TTreeAut, var_count: Optional[int] = None) -> ABDD:
    """
    TODO DOCS
    """
    if not check_if_abdd(ta):
        ValueError(f"cannot turn {ta.name} to an ABDD")

    try:
        slen: int = len(ta.get_statename_prefix())
    except ValueError:
        ta.reformat_states()
        slen: int = len(ta.get_statename_prefix())
    vlen = len(ta.get_var_prefix())

    if len(ta.roots) != 1:
        raise ValueError("ABDD can have only one root")

    root = ta.roots[0]
    root_node = ABDDNode(ta.roots[0], state_prefix_len=slen)
    result = ABDD(f"{ta.name}", var_count if var_count is not None else ta.get_var_max(), root_node)
    result.node_map[root] = root_node

    for state in iterate_states_bfs(ta):
        if state in ta.roots:
            continue
        result.node_map[state] = ABDDNode(state, state_prefix_len=slen)

    for state in ta.roots:
        result.node_map[state].is_root = True
        result.root = result.node_map[state]

    for edge in iterate_edges(ta):
        node: ABDDNode = result.node_map[edge.src]
        if edge.children == []:
            node.set_leaf_info_from_ta_transition(edge, var_prefix_len=vlen)
            if edge.info.label == "0":
                result.terminal_0 = node
            if edge.info.label == "1":
                result.terminal_1 = node
            continue
        if edge.info.box_array == []:
            edge.info.box_array = [None, None]
        node.set_node_info_from_ta_transition(edge, result.node_map, var_prefix_len=vlen)
    result.node_count = result.count_nodes()
    return result
