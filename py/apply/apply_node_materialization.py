from typing import Optional, Union
import copy
import itertools

from tree_automata.automaton import TTreeAut
from helpers.utils import box_catalogue

from apply.abdd import ABDD
from apply.abdd_node import ABDDNode
from apply.apply_edge import ApplyEdge
from tree_automata.transition import TEdge, TTransition


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# previous ad-hoc attempt for materialization
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def edge_setter_helper(
    node: ABDDNode, low_tgt: ABDDNode, low_box: str | None, high_tgt: ABDDNode, high_box: str | None
):
    node.low = low_tgt
    node.low_box = low_box
    node.high = high_tgt
    node.high_box = high_box


def materialize_node_on_edge(abdd: ABDD, edge: ApplyEdge, var: int, new_node_id: int) -> ABDDNode:
    """
    - 'abdd' = in which structure the new node will be materialized
    - 'node_from' = the parent of the materialized node (None, if materialization takes place above root)
    - 'node_to' = one of the children of the materialized node
    - 'var' = what variable will the materialized node contain
    - 'edge' = whether the edge between 'node_from' and 'node_to' was high (edge=True) or low (edge=False)
    """
    variable_order_ok: bool = (
        edge.from_node is not None and edge.from_node.var > 0 and edge.from_node.var < var and var < edge.to_node.var
    ) or (edge.from_node is None and var > 0 and var < edge.to_node.var)
    if not variable_order_ok:
        ValueError("inconsistent variable ordering between nodes' variables and materialized node var")

    requires_box_above: bool = edge.from_node is not None and var > edge.from_node.var + 1
    requires_box_below: bool = edge.to_node.var > var + 1

    new_node = ABDDNode(new_node_id)
    new_node.var = var
    box_to_new_node: Optional[str] = edge.box_reduction if requires_box_above else None

    # materializing above root node
    if edge.from_node is None:
        new_node.low = edge.to_node
        new_node.low_box = "X" if requires_box_below else None
        new_node.high = edge.to_node
        new_node.high_box = "X" if requires_box_below else None
        abdd.root.parents_through_low.add(new_node)
        abdd.root.parents_through_high.add(new_node)
        abdd.root = new_node
        return new_node

    # if no box on edge, then materialization will not be possible nor needed
    # that is why we only consider cases when there is a box present on the edge

    # target = ( low_node, low_box, high_node, high_box )
    targets: dict[str, tuple[ABDDNode, str, ABDDNode, str]] = {
        "X": (edge.to_node, "X", edge.to_node, "X"),
        "L0": (abdd.terminal_0, "X", edge.to_node, "L0"),
        "L1": (abdd.terminal_1, "X", edge.to_node, "L1"),
        "H0": (
            edge.to_node,
            "H0",
            abdd.terminal_0,
            "X",
        ),
        "H1": (
            edge.to_node,
            "H1",
            abdd.terminal_1,
            "X",
        ),
        "LPort": (edge.to_node[0], "X", edge.to_node, "LPort"),
        "HPort": (edge.to_node, "HPort", edge.to_node[-1], "X"),
    }

    if edge.low_high:  # high edge
        edge.from_node.high = new_node
        edge.from_node.high_box = box_to_new_node
        new_node.parents_through_high.add(edge.from_node)
        edge.to_node.parents_through_high.remove(edge.from_node)
    else:  # low edge
        edge.from_node.low = new_node
        edge.from_node.low_box = box_to_new_node
        new_node.parents_through_low.add(edge.from_node)
        edge.to_node.parents_through_low.remove(edge.from_node)

    if edge.box_reduction is None:
        raise ValueError("materialization called on unreduced edge")
    new_node.low, new_node.low_box, new_node.high, new_node.high_box = targets[edge.box_reduction]
    return new_node
