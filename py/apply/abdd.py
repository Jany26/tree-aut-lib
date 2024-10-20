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

    def __init__(self, ta: TTreeAut, vars: Optional[int] = None):
        """
        Initializing ABDD structure will omit self-looping transitions in the TA/UBDA structure.
        Missing variables or box information will raise an exception.
        """
        # ta.reformat_states()
        self.name = f"{ta.name}"
        self.variable_count = vars if vars is not None else ta.get_var_max()
        self.node_map = {}

        if not check_if_abdd(ta):
            ValueError(f"cannot turn {ta.name} to an ABDD")

        try:
            slen: int = len(ta.get_statename_prefix())
        except ValueError:
            ta.reformat_states()
            slen: int = len(ta.get_statename_prefix())
        vlen = len(ta.get_var_prefix())
        for state in iterate_states_bfs(ta):
            self.node_map[state] = ABDDNode(state, state_prefix_len=slen)

        if len(ta.roots) > 1:
            raise ValueError("ABDD can have only one root")

        for state in ta.roots:
            self.node_map[state].is_root = True
            self.root = self.node_map[state]

        for edge in iterate_edges(ta):
            node: ABDDNode = self.node_map[edge.src]
            if edge.children == []:
                node.set_leaf_info_from_ta_transition(edge, var_prefix_len=vlen)
                continue
            if edge.info.box_array == []:
                edge.info.box_array = [None, None]
            node.set_node_info_from_ta_transition(edge, self.node_map, var_prefix_len=vlen)

    def iterate_bfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        queue: list[ABDDNode] = [self.root]
        visited = set()
        while queue != []:
            node = queue.pop(0)
            if not repeat and node in visited:
                continue
            yield node
            visited.add(node)
            if type(node.low) == ABDDNode:
                queue.append(node.low)
            if type(node.low) == list:
                queue.extend(node.low)
            if type(node.high) == ABDDNode:
                queue.append(node.high)
            if type(node.high) == list:
                queue.extend(node.high)

    def iterate_dfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        stack: list[ABDDNode] = [self.root]
        visited = set()
        while stack != []:
            node = stack.pop()
            if not repeat and node in visited:
                continue
            yield node
            # we have to insert nodes in a reverse order
            visited.add(node)
            if type(node.high) == ABDDNode:
                stack.append(node.low)
            if type(node.high) == list:
                stack.extend(reversed(node.low))
            if type(node.low) == ABDDNode:
                stack.append(node.high)
            if type(node.low) == list:
                stack.extend(reversed(node.high))

    def __repr__(self):

        return "ABDD.__repr__()"

    def convert_to_treeaut_obj(self) -> TTreeAut:
        pass


def import_abdd_from_abdd_file(path: str) -> ABDD:
    """Assuming"""
    pass
