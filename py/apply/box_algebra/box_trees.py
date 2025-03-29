import copy

from apply.box_algebra.port_connection import PortConnectionInfo
from apply.equality import tree_aut_equal
from tree_automata import TTreeAut
from helpers.utils import box_catalogue


class BoxTreeNode:
    # leaf constructor
    def __init__(self, node: str | None, low=None, high=None):
        # if leaf, node is boxname string
        # if non-leaf, node is state name
        self.node = node
        # portname -> structure of information
        self.port_info: dict[str, PortConnectionInfo]
        self.is_leaf: bool = (low is None) and (high is None)
        self.low: BoxTreeNode | None = low  # str = boxname (from boxCatalogue)
        self.high: BoxTreeNode | None = high

    def __repr__(self):
        result = "n" if not self.is_leaf else self.node
        result += f"({self.low}" if self.low is not None else ""
        result += ";" if self.low is not None and self.high is not None else ""
        result += f"{self.high})" if self.high is not None else ""
        return result


# maybe not needed, since recursive solution seems more elegant
def get_transient_states(aut: TTreeAut) -> set[str]:
    reach_dict = {i: aut.get_reachable_states_from(i) for i in aut.get_states()}
    result = set()
    for state in aut.transitions.keys():
        transient = True
        for t in aut.transitions[state].values():
            if t.is_self_loop():
                transient = False
        unreachable = True
        if transient:
            for reachable_state in reach_dict[state]:
                if state in reach_dict[reachable_state]:
                    unreachable = False
        non_leaf = state not in aut.get_output_states()
        if transient and unreachable and non_leaf:
            result.add(state)
    return result


def boxtree_intersectoid_compare(aut: TTreeAut, root: str) -> str | None:
    roots = [i for i in aut.roots]
    aut.roots = [root]
    aut.reformat_ports()
    for boxname in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort", "False", "True"]:
        box_copy = copy.deepcopy(box_catalogue[boxname])
        box_copy.reformat_ports()
        if tree_aut_equal(aut, box_copy):
            aut.roots = roots
            return boxname
    aut.roots = roots
    return None


def build_box_tree(aut: TTreeAut) -> BoxTreeNode | None:
    def build_box_tree_recursive(aut: TTreeAut, state: str) -> BoxTreeNode | None:
        # leaf case
        boxname = boxtree_intersectoid_compare(aut, state)
        if boxname is not None:
            return BoxTreeNode(boxname)

        # inner node case
        for edge in aut.transitions[state].values():
            if len(edge.children) == 2:
                low: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[0])
                high: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[1])
                if (low is not None) and (high is not None):
                    result = BoxTreeNode(state, low, high)
                    return result
        return None

    aut_copy = copy.deepcopy(aut)
    for i in aut.roots:
        box_tree = build_box_tree_recursive(aut, i)
        if box_tree is not None:
            return box_tree
