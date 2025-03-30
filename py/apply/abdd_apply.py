# during recursive traversal, upon encountering an edge with two boxes used,
# 1) store the port-state mapping // or, rather boxstate-abddstate mapping
# 2) use the table lookup, in the table, there should also be PortConnectionInfo for each of the resulting boxes within the box-tree, which contains:
#       - negation flag, recursion flag (with original ports from which it starts)
# 3)

# A) first create boxstate-abddstate mapping // should be simple
# // OR, alternatively, before box-use, rename the port-states to those from the ABDD // probably not

# B) then we need to get something like this:
# Tuple[BoxTree, PortInfoTree] // box tree and PortInfoTree are picked out using the table lookup

# TODO
# table lookup is created automatically using some recursive magic + apply_tables_outputs stuff
# the automaton analysis is done with help of the port_transition help:

# within the lookup


from typing import Optional, Union
from apply.abdd import ABDD, init_abdd_from_ta
from apply.apply_edge import ApplyEdge
from apply.box_algebra.apply_intersectoid import BooleanOperation
from helpers.utils import box_catalogue
from tree_automata.automaton import TTreeAut
from apply.abdd_node import ABDDNode
from apply.dead_ends.apply_node_materialization import materialize_node_on_edge


class ABDDApplyHelper:
    """
    Helper class with necessary cache and information
    needed during the recursive apply function.

    'call_cache' - Stores results of recursive apply calls.

    'node_cache' - Makes sure that identical nodes are not duplicated.
    This differs from ApplyCallCache in the sense that two different apply
    calls might create two nodes that represent the same boolean function.

    """

    # cache[ op, var, node_a, box_a, node_b, box_b ] -> node
    call_cache: dict[
        tuple[
            BooleanOperation,  # operation used in the apply call
            int,  # at which variable level is apply called
            int,  # node index of the first operand node
            str,  # box used on the edge leading to the first operand node
            int,  # node index of the second operand node
            str,  # box used on the edge leading to the second operand node
        ],
        ABDDNode,
    ]

    # cache [ var, low_box, low_target, high_box, high_target ] -> node
    node_cache: dict[
        tuple[
            int,  # variable of the node
            Optional[str],  # low-edge box              / None in case of leaf nodes
            Optional[int],  # low-edge target node idx  / None in case of leaf nodes
            Optional[str],  # high-edge box             / None in case of leaf nodes
            Optional[int],  # high-edge target node idx / None in case of leaf nodes
        ],
        ABDDNode,
    ]

    def __init__(self, in1: ABDD, in2: ABDD, maxvar: int):
        self.call_cache = {}
        self.node_cache = {}

        self.counter_1: int = in1.count_nodes()
        self.counter_2: int = in2.count_nodes()
        self.counter: int = 0
        self.maxvar = maxvar

    def insert_call(self, op, edge1, edge2) -> None:
        pass

    def find_call(self, op, edge1, edge2) -> Optional[ABDDNode]:
        pass


def abdd_apply(
    op: BooleanOperation, in1: Union[TTreeAut, ABDD], in2: Union[TTreeAut, ABDD], maxvar: Optional[int] = None
) -> ABDD:
    # some preliminary typecasting and checking
    if maxvar is None:
        maxvar = max(in1.get_var_max(), in2.get_var_max())
    if type(in1) == TTreeAut:
        in1 = init_abdd_from_ta(in1, var_count=maxvar)
    if type(in2) == TTreeAut:
        in2 = init_abdd_from_ta(in2, var_count=maxvar)

    if not (maxvar is not None and type(in1) == ABDD and type(in2) == ABDD):
        ValueError("invalid parameters")

    arg1 = ApplyEdge(in1, None, in1.root, None, None)
    arg2 = ApplyEdge(in2, None, in2.root, None, None)
    helper = ABDDApplyHelper(in1, in2, maxvar)

    abdd_apply_from(op, arg1, arg2, helper)


def abdd_apply_from(op: BooleanOperation, edge1: ApplyEdge, edge2: ApplyEdge, helper: ABDDApplyHelper) -> ABDDNode:
    # we will probably need to return a reduction rule plus the node that is the result of the apply

    # materialize_new_root_if_needed(op, edge1, edge2, helper)

    if edge1.to_node.var < edge2.to_node.var:
        new_node = materialize_node_on_edge(edge2, edge1.to_node.var, helper.counter_2)
        helper.counter_2 += 1
        edge2.from_node = new_node
        abdd_apply_from(op, edge1, edge2, helper)

    if edge1.to_node.var > edge2.to_node.var:
        new_node = materialize_node_on_edge(edge1, edge2.to_node.var, helper.counter_1)
        helper.counter_1 += 1
        edge1.from_node = new_node
        abdd_apply_from(op, edge1, edge2, helper)

    # edge1str = f"{edge1.from_node}, {edge1.to_node}, {'H' if edge1.low_high else 'L'}, {edge1.box_reduction}"
    # edge2str = f"{edge2.from_node}, {edge2.to_node}, {'H' if edge2.low_high else 'L'}, {edge2.box_reduction}"
    # print(f"abdd_apply ( edge1 = {edge1str} , edge2 = {edge2str} )")

    if edge1.to_node.is_leaf and edge2.to_node.is_leaf:
        return produce_terminal(edge1.to_node.leaf_val, edge2.to_node.leaf_val, op)

    # LOW APPLY
    low_edge_1 = ApplyEdge(edge1.abdd, edge1.to_node, edge1.to_node.low, edge1.to_node.low_box, False)
    low_edge_2 = ApplyEdge(edge2.abdd, edge2.to_node, edge2.to_node.low, edge2.to_node.low_box, False)

    low_targets_1 = edge1.to_node.low
    low_targets_2 = edge2.to_node.low

    low_dict_tuple = (get_boxstate_nodename_dict(low_edge_1), get_boxstate_nodename_dict(low_edge_2))

    # in case of apply on nodes with the same level

    low_apply = abdd_apply_from(op, low_edge_1, low_edge_2, helper)

    # HIGH APPLY
    high_edge_1 = ApplyEdge(edge1.abdd, edge1.to_node, edge1.to_node.high, edge1.to_node.high_box, True)
    high_edge_2 = ApplyEdge(edge2.abdd, edge2.to_node, edge2.to_node.high, edge2.to_node.high_box, True)

    high_dict_tuple = (get_boxstate_nodename_dict(high_edge_1), get_boxstate_nodename_dict(high_edge_2))
    high_apply = abdd_apply_from(op, high_edge_1, high_edge_2, helper)


def get_boxstate_nodename_dict(edge_obj: ApplyEdge) -> dict[str, ABDDNode]:
    box: TTreeAut = box_catalogue[edge_obj.box_reduction]
    portstates = []
    for sym, states in box.get_output_edges().items():
        if sym.startswith("Port"):
            portstates.extend(states)
    portstates = [state for sym, states in box.get_output_edges().items() if sym.startswith("Port") for state in states]
    # ports = [sym for sym in box.get_output_edges().keys() if sym.startswith('Port')]
    portstates.sort()
    nodes: list[ABDDNode]
    if isinstance(edge_obj.to_node, ABDDNode):
        nodes = [edge_obj.to_node]
    elif isinstance(edge_obj.to_node, ABDDNode):
        nodes = edge_obj.to_node
    elif edge_obj.to_node is None:
        return {}
    return {portstates[i]: nodes[i] for i in range(len(portstates))}


def produce_terminal(val1: int, val2: int, op: BooleanOperation, helper: ABDDApplyHelper) -> ABDDNode:
    op_translate: dict[BooleanOperation, int] = {
        BooleanOperation.NOP: -1,
        BooleanOperation.AND: val1 and val2,
        BooleanOperation.OR: val1 or val2,
        BooleanOperation.XOR: (val1 and not val2) or (not val1 and val2),
        BooleanOperation.IFF: (val1 and val2) or (not val1 and not val2),
        BooleanOperation.NAND: not (val1 and val2),
        BooleanOperation.NOR: not (val1 or val2),
        BooleanOperation.IMPLY: not val1 or val2,
        BooleanOperation.NOT: -1,
    }
    node = ABDDNode(helper.counter)
    node.set_as_leaf(op_translate[op])
    if node in helper.node_cache:
        return helper.node_cache[node]
    else:
        helper.node_cache[node] = node
        return node


## Make the materialization take ABDD, and two nodes (or one in case it is above root node) in between which the materialized node will sit
