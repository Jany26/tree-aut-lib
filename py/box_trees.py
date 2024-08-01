import re
import sys
import os

from apply_testing import tree_aut_equal
from format_vtf import import_treeaut_from_vtf
from ta_classes import TTreeAut
from test_data import box_catalogue

class BoxTreeNode:
    # leaf constructor
    def __init__(self, node: str | None, low=None, high=None):
        # if leaf, node is boxname string
        # if non-leaf, node is state name
        self.node = node
        self.is_leaf : bool = (low is None) and (high is None)
        self.low: BoxTreeNode | None = low  # str = boxname (from boxCatalogue)
        self.high: BoxTreeNode | None = high

    def __repr__(self):
        children = "" if self.is_leaf else f" ({self.low} {self.high})"
        return "'" + self.node + "'" + children
        # return f"{self.node} '({self.low if self.low is not None else ''} {self.high if self.high is not None else ''})"

        # return f"{self.node}{self.low if self.low is not None else ''}{self.high if self.high is not None else ''}"


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
        box = box_catalogue[boxname]
        box.reformat_ports()
        if tree_aut_equal(aut, box):
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
        print(" state", state)
        for edge in aut.transitions[state].values():
            print("  edge", edge)
            # for child in edge.children:
            if len(edge.children) == 2:
                low: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[0])
                high: BoxTreeNode | None = build_box_tree_recursive(aut, edge.children[1])
                print("   low", low.node if low is not None else "none")
                print("   high", high.node if high is not None else "none")
                if (low is not None) and (high is not None):
                    result = BoxTreeNode(state, low, high)
                    print(f" returning result {state} {edge}")
                    return result
        print(" returning none")
        return None

    for i in aut.roots:
        box_tree = build_box_tree_recursive(aut, i)
        if box_tree is not None:
            return box_tree


if __name__ == "__main__":
    ta = import_treeaut_from_vtf(sys.argv[1])
    print(ta)
    print(build_box_tree(ta))
