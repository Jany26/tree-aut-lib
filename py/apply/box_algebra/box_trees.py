import copy
from typing import Optional

from apply.box_algebra.port_connection import PortConnectionInfo
from apply.equality import tree_aut_equal
from tree_automata import TTreeAut
from helpers.utils import box_catalogue


class BoxTreeNode:
    """
    Each BoxTreeNode will then contain not only the used box, but also a list of port connection info instances.

    Then during apply, when materialization is not needed and both input variables and output variables
    agree (are the same level), then we can utilize the box algebrae to obtain the BoxTreeNode
    within each node of this tree is a string representing the used box AND PortConnectionInfo
    that says what the results of each of the target nodes of leaf nodes of this tree are.
    """

    def __init__(
        self,
        node: Optional[str] = None,
        port_info: list[PortConnectionInfo] = [],
        is_leaf: bool = True,
        low: Optional["BoxTreeNode"] = None,
        high: Optional["BoxTreeNode"] = None,
    ):
        # if leaf, node is boxname string
        # if non-leaf, node is state name
        self.node = node
        self.port_info = port_info
        self.is_leaf = is_leaf
        # low and high are boxname strings (from box_catalogue)
        self.low = low
        self.high = high

    def __repr__(self, level=4):
        cname = self.__class__.__name__
        ind = f" " * level
        indm = f" " * (level - 4)
        indp = f" " * (level + 4)
        port_info = f" port_info=["
        for i in self.port_info:
            port_info += f"\n{indp}{i},"
        port_info += f"\n{ind}]" if self.port_info != [] else "]"
        nodename = f'"{self.node}"' if self.node else "None"

        attributes = [
            f"\n{ind}node={nodename}",
            port_info,
            f" is_leaf={self.is_leaf}" if not self.is_leaf else "",
            f"\n{ind}low={self.low.__repr__(level=level+4)}" if self.low else "",
            f"\n{ind}high={self.high.__repr__(level=level+4)}" if self.high else "",
        ]
        return f"{cname}({','.join([a for a in attributes if a != ""])}\n{indm})"

    def __eq__(self, other: "BoxTreeNode") -> bool:
        if not all(
            [
                type(self.node) == type(other.node),
                self.is_leaf == other.is_leaf,
                not self.is_leaf or self.node == other.node,
                not self.is_leaf or self.port_info == other.port_info,
            ]
        ):
            return False

        low = type(self.low) == type(other.low) and self.low == other.low
        high = type(self.high) == type(other.high) and self.high == other.high

        if not low or not high:
            return False

        return True

    def depth(self, target: "BoxTreeNode") -> Optional[int]:
        """
        Return the depth of the "target" node if it is in the BoxTree, if not, return None.
        """
        queue = [(self, 0)]
        while queue != []:
            node, depth = queue.pop(0)
            if node == target:
                return depth
            if node.low is not None:
                queue.append((node.low, depth + 1))
            if node.high is not None:
                queue.append((node.high, depth + 1))
        return None


def boxtree_intersectoid_compare(aut: TTreeAut, root: str) -> tuple[str | None, list[PortConnectionInfo]]:
    origroots = [i for i in aut.roots]
    aut.roots = [root]
    aut.reformat_ports()
    for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort", "False", "True"]:
        box_copy = copy.deepcopy(box_catalogue[boxname])
        box_copy.reformat_ports()
        if tree_aut_equal(aut, box_copy):
            portstates = aut.get_port_order()[: box_copy.port_arity]
            aut.roots = origroots
            return (boxname, portstates)
    aut.roots = origroots
    return (None, [])


def build_box_tree(aut: TTreeAut, port_map: dict[str, PortConnectionInfo]) -> BoxTreeNode | None:
    def build_box_tree_recursive(
        aut: TTreeAut, state: str, port_map: dict[str, PortConnectionInfo]
    ) -> BoxTreeNode | None:
        # leaf case
        boxname, portinfo = boxtree_intersectoid_compare(aut, state)
        if boxname is not None:
            result_node = BoxTreeNode(node=boxname, port_info=[port_map[state] for (port, state) in portinfo])
            return result_node

        # inner node case
        for edge in aut.transitions[state].values():
            if len(edge.children) == 2:
                low_result: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[0], port_map)
                high_result: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[1], port_map)
                if (low_result is not None) and (high_result is not None):
                    result = BoxTreeNode(node=state, port_info=[], is_leaf=False, low=low_result, high=high_result)
                    return result
        return None

    for i in aut.roots:
        box_tree = build_box_tree_recursive(aut, i, port_map)
        if box_tree is not None:
            return box_tree
