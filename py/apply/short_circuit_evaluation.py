"""
[file] short_circuit_evaluation.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Function for utilizing annihilation/absorption laws in ABDD Apply.
"""

from typing import Optional
from enum import Enum

from apply.abdd_node import ABDDNode
from apply.apply_edge import ApplyEdge
from apply.abdd_apply_helper import ABDDApplyHelper
from apply.negation import negate_subtree, negate_box_label

from apply.box_algebra.apply_tables import BooleanOperation
from apply.box_algebra.box_trees import BoxTreeNode


class ShortCircuitEvaluation(Enum):
    ZERO = 0  # constant function annihilates the other edge to 0 - annihilation
    ONE = 1  # constant function annihilates the other edge to 1  - annihilation
    FIRST = 2  # when the constant function is neutral towards an operator - absorption
    SECOND = 3  # when the constant function is neutral towards an operator - absorption
    NEG_FIRST = 4  # when the constant function negates the edge
    NEG_SECOND = 5  # when the constant function negates the edge


# (leaf_value, OP, leaf_value) -> leaf_value / keep first / keep second / keep first negated / keep second negated
early_return_lookup: dict[tuple[Optional[int], BooleanOperation, Optional[int]], ShortCircuitEvaluation] = {
    (0, BooleanOperation.AND, None): ShortCircuitEvaluation.ZERO,
    (1, BooleanOperation.AND, None): ShortCircuitEvaluation.SECOND,
    (None, BooleanOperation.AND, 0): ShortCircuitEvaluation.ZERO,
    (None, BooleanOperation.AND, 1): ShortCircuitEvaluation.FIRST,
    (0, BooleanOperation.OR, None): ShortCircuitEvaluation.SECOND,
    (1, BooleanOperation.OR, None): ShortCircuitEvaluation.ONE,
    (None, BooleanOperation.OR, 0): ShortCircuitEvaluation.FIRST,
    (None, BooleanOperation.OR, 1): ShortCircuitEvaluation.ONE,
    (0, BooleanOperation.XOR, None): ShortCircuitEvaluation.SECOND,
    (1, BooleanOperation.XOR, None): ShortCircuitEvaluation.NEG_SECOND,
    (None, BooleanOperation.XOR, 0): ShortCircuitEvaluation.FIRST,
    (None, BooleanOperation.XOR, 1): ShortCircuitEvaluation.NEG_FIRST,
    (0, BooleanOperation.IFF, None): ShortCircuitEvaluation.NEG_SECOND,
    (1, BooleanOperation.IFF, None): ShortCircuitEvaluation.SECOND,
    (None, BooleanOperation.IFF, 0): ShortCircuitEvaluation.NEG_FIRST,
    (None, BooleanOperation.IFF, 1): ShortCircuitEvaluation.FIRST,
    (0, BooleanOperation.NAND, None): ShortCircuitEvaluation.ONE,
    (1, BooleanOperation.NAND, None): ShortCircuitEvaluation.NEG_SECOND,
    (None, BooleanOperation.NAND, 0): ShortCircuitEvaluation.ONE,
    (None, BooleanOperation.NAND, 1): ShortCircuitEvaluation.NEG_FIRST,
    (0, BooleanOperation.NOR, None): ShortCircuitEvaluation.NEG_SECOND,
    (1, BooleanOperation.NOR, None): ShortCircuitEvaluation.ZERO,
    (None, BooleanOperation.NOR, 0): ShortCircuitEvaluation.NEG_FIRST,
    (None, BooleanOperation.NOR, 1): ShortCircuitEvaluation.ZERO,
    (0, BooleanOperation.IMPLY, None): ShortCircuitEvaluation.ONE,
    (1, BooleanOperation.IMPLY, None): ShortCircuitEvaluation.SECOND,
    (None, BooleanOperation.IMPLY, 0): ShortCircuitEvaluation.NEG_FIRST,
    (None, BooleanOperation.IMPLY, 1): ShortCircuitEvaluation.ONE,
}


def get_shc_lookup(e: ApplyEdge) -> Optional[int]:
    leaf0 = all([n.leaf_val == 0 for n in e.target])
    leaf1 = all([n.leaf_val == 1 for n in e.target])
    if leaf0 and e.rule in ["X", "L0", "H0", "LPort", "HPort"]:
        return 0
    if leaf1 and e.rule in ["X", "L1", "H1", "LPort", "HPort"]:
        return 1
    return None


def target_print(target: list[ABDDNode]) -> str:
    """
    Format target nodes of an edge, useful for debugging.
    """
    return "[" + ", ".join([f"<{i.leaf_val}>" if i.is_leaf else f"{i.node}({i.var})" for i in target]) + "]"


def source_print(source: Optional[ABDDNode]) -> str:
    """
    Format source node of an edge, useful for debugging.
    """
    return "-" if source is None else (f"<{source.leaf_val}>" if source.is_leaf else f"{source.node}({source.var})")


def node_var_compare(node1: Optional[ABDDNode], node2: Optional[ABDDNode]) -> bool:
    if node1 is None and node2 is None:
        return True
    if node1 is None and node2 is not None:
        return False
    if node1 is not None and node2 is None:
        return False
    if node1.var == node2.var:
        return True
    return False


def short_circuit_evaluation(
    e1: ApplyEdge, op: BooleanOperation, e2: ApplyEdge, helper: ABDDApplyHelper
) -> tuple[Optional[str], list[ABDDNode]]:
    """
    Attempt short-circuit evaluation on two edges.
    This is possible when one of the edges describes a constant Boolean function.
    For example L1-[1], or H0-[0], or LPort-[0,0], etc.

    Uses the table 'early_return_lookup' dictionary for obtaining information about what to return.
        - assuming edge 'a' is constant function and edge 'b' is not, there are 3 cases of what can happen:
            - return 0/1 -- annihilation properties of some operators (AND with 0, OR with 1)
            - return edge b directly
            - return edge b in negated form
    """
    if not node_var_compare(e1.source, e2.source):
        return None, []

    val1 = get_shc_lookup(e1)
    val2 = get_shc_lookup(e2)
    if (val1, op, val2) in early_return_lookup:
        eval: ShortCircuitEvaluation = early_return_lookup[(val1, op, val2)]
        if eval == ShortCircuitEvaluation.ONE:
            return "X", [helper.node_cache.terminal_1]
        if eval == ShortCircuitEvaluation.ZERO:
            return "X", [helper.node_cache.terminal_0]
        if eval == ShortCircuitEvaluation.FIRST:
            return e1.rule, e1.target
        if eval == ShortCircuitEvaluation.NEG_FIRST:
            return negate_box_label[e1.rule], [negate_subtree(e1.abdd, n, helper) for n in e1.target]
        if eval == ShortCircuitEvaluation.SECOND:
            return e2.rule, e2.target
        if eval == ShortCircuitEvaluation.NEG_SECOND:
            return negate_box_label[e2.rule], [negate_subtree(e2.abdd, n, helper) for n in e2.target]
    return None, []


def short_circuit_evaluation_boxtree(
    boxtree: BoxTreeNode, e1: ApplyEdge, e2: ApplyEdge, op: BooleanOperation, helper: ABDDApplyHelper, varlevel: int
) -> tuple[Optional[str], list[ABDDNode]]:
    """
    # Short Circuit Evaluation version of a boxtree traversal.
    # - this was supposed to be the equivalent to leafcase/innercase boxtree traversal
    # - however, it is not working, because it can produce incorrect results
    # - example:    edge1: x1 -- L1 --> [0]
    #               <OR>
    #               edge2: x1 -- X  --> [x4]
    #       - creates LPort leading to x4, x4... which is kind of incorrect.
    #       - it does not work because it assumes that it can work with semantics of
    #       - a constant Boolean function, even when it is not (L1 leading to 0 describes a "leaf" edge),
    #         but it is not a constant function [1 1 1 0] -- L1 leading to 1 would be a constant function [1 1 1 1]
    """
    if boxtree.node == "True":
        rule = "X"
        nodes = [e1.abdd.terminal_1]
        return rule, nodes
    if boxtree.node == "False":
        rule = "X"
        nodes = [e1.abdd.terminal_0]
        return rule, nodes
    if boxtree.is_leaf:
        rule = boxtree.node
        nodes: list[ABDDNode] = []
        for pc in boxtree.port_info:
            if pc.target1 is not None and pc.target2 is not None:
                eval: ShortCircuitEvaluation = early_return_lookup[
                    (e1.target[pc.target1].leaf_val, op, e2.target[pc.target2].leaf_val)
                ]
                if eval == ShortCircuitEvaluation.ZERO:
                    nodes.append(helper.node_cache.terminal_0)
                elif eval == ShortCircuitEvaluation.ONE:
                    nodes.append(helper.node_cache.terminal_1)
                elif eval == ShortCircuitEvaluation.FIRST:
                    nodes.append(e1.target[pc.target1])
                elif eval == ShortCircuitEvaluation.SECOND:
                    nodes.append(e2.target[pc.target2])
                elif eval == ShortCircuitEvaluation.NEG_FIRST:
                    nodes.append(negate_subtree(e1.abdd, e1.target[pc.target1], helper))
                elif eval == ShortCircuitEvaluation.NEG_SECOND:
                    nodes.append(negate_subtree(e2.abdd, e2.target[pc.target2], helper))
            elif pc.target1 is not None:
                term = e1.target[pc.target1]
                nodes.append(negate_subtree(e1.abdd, term, helper) if pc.negation else term)
            elif pc.target2 is not None:
                term = e2.target[pc.target2]
                nodes.append(negate_subtree(e2.abdd, term, helper) if pc.negation else term)

        # Check LPort / HPort var level consistency -> if short circuit evaluation
        # breaks this consistency, raise an Exception
        # => optimization cannot be utilized, so apply should continue with materialization etc...

        if rule == "LPort" and nodes[1].leaf_val is not None and nodes[0].leaf_val is None:
            raise ValueError("short-circuit evaluation broke LPort consistency")
        if rule == "HPort" and nodes[0].leaf_val is not None and nodes[1].leaf_val is None:
            raise ValueError("short-circuit evaluation broke HPort consistency")
        return rule, nodes

    try:
        low_rule, low_targets = (
            short_circuit_evaluation(boxtree.low, e1, e2, op, helper, varlevel + 1) if boxtree.low else (None, [])
        )
    except:
        raise ValueError("short-circuit evaluation broke LPort/HPort consistency")
    try:
        high_rule, high_targets = (
            short_circuit_evaluation(boxtree.high, e1, e2, op, helper, varlevel + 1) if boxtree.high else (None, [])
        )
    except:
        raise ValueError("short-circuit evaluation broke LPort/HPort consistency")

    new_abdd_node = ABDDNode(helper.counter)
    new_abdd_node.var = varlevel + 1  # not sure with the variable
    new_abdd_node.is_leaf = False
    new_abdd_node.low_box = low_rule
    new_abdd_node.low = low_targets
    new_abdd_node.high_box = high_rule
    new_abdd_node.high = high_targets
    cache_hit = helper.node_cache.find_node(new_abdd_node)
    nodes = []
    if cache_hit is not None:
        nodes.append(cache_hit)
    else:
        nodes.append(new_abdd_node)
        helper.counter += 1
        helper.node_cache.insert_node(new_abdd_node)
    rule = None
    return rule, nodes


def process_boxtree_leafcase(
    boxtree: BoxTreeNode,
    e1: ApplyEdge,
    e2: ApplyEdge,
    op: BooleanOperation,
    helper: ABDDApplyHelper,
    varlevel: int,
    rootlevel: int,
) -> tuple[Optional[str], list[ABDDNode]]:
    """
    Traverse the box tree and correctly map ABDD nodes from edges 'e1' and 'e2' based on the information hidden in
    PortConnectionInfo instances within leaf nodes of the boxtree.
    In case recursion flag is true, use the produce_terminal() function.
    """
    if boxtree.node == "True":
        rule = "X"
        nodes = [e1.abdd.terminal_1]
        return rule, nodes
    if boxtree.node == "False":
        rule = "X"
        nodes = [e1.abdd.terminal_0]
        return rule, nodes
    if boxtree.is_leaf:
        rule = boxtree.node
        nodes = []
        for pc in boxtree.port_info:
            if pc.target1 is not None and pc.target2 is not None:
                term = produce_terminal(e1.target[pc.target1].leaf_val, e2.target[pc.target2].leaf_val, op, helper)
                nodes.append(term)
            elif pc.target1 is not None:
                term = e1.target[pc.target1]
                nodes.append(negate_subtree(e1.abdd, term, helper) if pc.negation else term)
            elif pc.target2 is not None:
                term = e2.target[pc.target2]
                nodes.append(negate_subtree(e2.abdd, term, helper) if pc.negation else term)
        return rule, nodes

    low_rule, low_targets = (
        process_boxtree_leafcase(boxtree.low, e1, e2, op, helper, varlevel, rootlevel + 1)
        if boxtree.low
        else (None, [])
    )
    high_rule, high_targets = (
        process_boxtree_leafcase(boxtree.high, e1, e2, op, helper, varlevel, rootlevel + 1)
        if boxtree.high
        else (None, [])
    )

    use_short = rootlevel == helper.maxvar

    new_abdd_node = ABDDNode(helper.counter)
    new_abdd_node.var = rootlevel
    new_abdd_node.is_leaf = False
    new_abdd_node.low_box = None if use_short else low_rule
    new_abdd_node.low = short_edge_corrector(low_rule, low_targets) if use_short else low_targets
    new_abdd_node.high_box = None if use_short else high_rule
    new_abdd_node.high = short_edge_corrector(high_rule, high_targets) if use_short else high_targets
    cache_hit = helper.node_cache.find_node(new_abdd_node)
    nodes = []
    if cache_hit is not None:
        nodes.append(cache_hit)
    else:
        nodes.append(new_abdd_node)
        helper.counter += 1
        helper.node_cache.insert_node(new_abdd_node)
    rule = None
    return rule, nodes


def produce_terminal(val1: int, val2: int, op: BooleanOperation, helper: ABDDApplyHelper) -> ABDDNode:
    """
    Combines two leaf nodes together according to the semantics of the used Boolean operator.
    Basically leaf-level version of Apply.
    """
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
    if op_translate[op] == 0:
        return helper.abdd1.terminal_0
    elif op_translate[op] == 1:
        return helper.abdd1.terminal_1
    else:
        raise ValueError("produce_terminal(): unsupported binary operator")


def short_edge_corrector(rule: str, targets: list[ABDDNode]) -> list[ABDDNode]:
    """
    In case mapping cannot use the reduced edge, but due to box tree 'vector splitting' has to use short
    edge instead of the box itself, this function will correctly pick the target
    """
    if rule == "LPort":
        return [targets[1]]
    if rule == "HPort":
        return [targets[0]]

    # in cases of L1/L0/H1/H0, we disregard the "sink" and just use the port mapped state (same with X)
    return [targets[0]]


# End of file short_circuit_evaluation.py
