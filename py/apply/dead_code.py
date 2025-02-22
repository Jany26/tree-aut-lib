from typing import Optional
from apply.abdd_node import ABDDNode
from apply.abdd import ABDD


def materialize_node_above(current: ABDD, node: ABDDNode, var_index: int):
    """
    in current ABDD, above node 'node', create
    """
    pass


def materialize_node_below(current_abdd: ABDD, current_node: Optional[ABDDNode], edge: bool, var: int):
    """
    In 'current' ABDD, below node 'node', and above its 'edge'-directed child, create a node with variable 'var'.
    If 'node' is None, materialize a node above the root.

    Materialization is the process of creating an 'in-between node' within the ABDD structure.
    This is needed in order to properly propagate boolean operator during the apply recursion,
    since we cannot apply a function on two BDDs that start at different variables.

    - current   = ABDD in which the node is being materialized
    - node      = ABDDnode which is the parent of the materialized node (parent guides the materialization process).
    - edge      = if True, materialize node on the 'high' edge (above 'high' child)
                  if False, materialize the new node on the 'low' edge (above 'low' child of node 'node')
    - var       = the materialized node will contain this variable
    """

    def set_edge_helper(
        node: ABDDNode, low_tgt: ABDDNode, low_box: str | None, high_tgt: ABDDNode, high_box: str | None
    ):
        node.low = low_tgt
        node.low_box = low_box
        node.high = high_tgt
        node.high_box = high_box

    new_node = ABDDNode(current_abdd.node_count)
    new_node.var = var
    current_abdd.node_count += 1
    box: str | None = None
    original_target: ABDDNode | list[ABDDNode] | None = None
    if current_node is not None and edge is True:  # materialized node is on high-edge of the source
        box = current_node.high_box
        current_node.high.parents_through_high.remove(current_node)
        original_target = current_node.high
        current_node.high = new_node
        new_node.parents_through_high.add(current_node)
        if abs(current_node.var - var) == 1:
            current_node.high_box = None
    if current_node is not None and edge is False:
        box = current_node.low_box
        current_node.low.parents_through_low.remove(current_node)
        original_target = current_node.low
        current_node.low = new_node
        new_node.parents_through_low.add(current_node)
        if abs(current_node.var - var) == 1:
            current_node.low_box = None

    if box is None:  # in case of materializing above the root (should not happen)
        set_edge_helper(new_node, original_target, "X", original_target, "X")
    elif box == "X":
        set_edge_helper(new_node, original_target, "X", original_target, "X")
    elif box == "L0":
        set_edge_helper(new_node, current_abdd.terminal_0, "X", original_target, "L0")
    elif box == "L1":
        set_edge_helper(new_node, current_abdd.terminal_1, "X", original_target, "L1")
    elif box == "LPort":
        set_edge_helper(new_node, original_target[0], "X", original_target, "LPort")
    elif box == "H0":
        set_edge_helper(new_node, original_target, "H0", current_abdd.terminal_0, "X")
    elif box == "H1":
        set_edge_helper(new_node, original_target, "H1", current_abdd.terminal_1, "X")
    elif box == "HPort":
        set_edge_helper(new_node, original_target, "HPort", original_target[1], "X")


def materialize_node_below_no_box(current_abdd: ABDD, current_node: Optional[ABDDNode], edge: bool, var: int):
    """
    Serves the same purpose as the other variant, except when only one variable is skipped on the edge,
    the resulting node materialization will only produce short edges between the initial source node
    and the initial target node.
    """
    pass
