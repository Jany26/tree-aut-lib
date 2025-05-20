"""
[file] abdd_apply_main.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Top-level implementation of Apply() on ABDDs (Automata-based Binary Decision Diagrams).
"""

from typing import Optional

from apply.abdd import ABDD
from apply.abdd_node import ABDDNode
from apply.apply_edge import ApplyEdge
from apply.abdd_apply_helper import ABDDApplyHelper
from apply.abdd_node_cache import ABDDNodeCacheClass

from apply.box_algebra.apply_intersectoid import BooleanOperation
from apply.box_algebra.box_trees import BoxTreeNode

from apply.materialize import materialize_abdd_pattern
from apply.materialization.pattern_generate import obtain_predicates

from apply.negation import negate_subtree, negate_box_label
from apply.short_circuit_evaluation import process_boxtree_leafcase, short_circuit_evaluation, short_edge_corrector

from apply.pregenerated.box_algebrae import boxtree_cache
from apply.pregenerated.materialization_recipes import cached_materialization_recipes


def abdd_apply(
    op: BooleanOperation,
    in1: ABDD,
    in2: Optional[ABDD] = None,
    cache: Optional[ABDDNodeCacheClass] = None,
    maxvar: Optional[int] = None,
) -> ABDD:
    """
    This serves as a wrapper to the recursive abdd_apply_from(), where actual apply takes place.

    Herein, we just precompute and create some initial information and then call abdd_apply_from() on root nodes
    of the two given ABDDs.

    Apply can change/modify the structures of initial inputs (materialization), so it is advised to always create
    copies before apply calls.
    """
    # some preliminary typecasting and checking
    if maxvar is None:
        # for now, we should assume that variable counts are the same
        if in1.variable_count != in2.variable_count:
            raise ValueError(
                f"abdd_apply(): unequal variable counts in1={in1.variable_count}, in2={in2.variable_count}"
            )
        maxvar = in1.variable_count

    if not (maxvar is not None and type(in1) == ABDD and (type(in2) == ABDD or in2 is None)):
        raise ValueError("invalid parameters")

    helper = ABDDApplyHelper(in1, in2, maxvar=maxvar, cache=cache)
    e1 = ApplyEdge(in1, None, None)

    # special handling for negation
    if op.name == "NOT" and in2 is None:
        roots = [negate_subtree(in1, r, helper) for r in in1.roots]
        print(f"negation result = {roots}")
        abdd = ABDD(f"{op.name} {in1.name}", maxvar, roots)
        abdd.root_rule = negate_box_label[in1.root_rule]
        return abdd

    if not (op.name != "NOT" and type(in2) == ABDD):
        raise ValueError("invalid parameters")

    # handling for normal binary operator apply
    e2 = ApplyEdge(in2, None, None)
    rule, roots = abdd_apply_from(op, None, e1, e2, helper)
    abdd = ABDD(f"({in1.name} {op.name} {in2.name})", maxvar, roots)
    abdd.root_rule = rule
    return abdd


# NOTE: we probably need to have rule1, rule2 as operands too, since we need the
def abdd_apply_from(
    op: BooleanOperation, var: Optional[int], e1: ApplyEdge, e2: ApplyEdge, helper: ABDDApplyHelper
) -> tuple[Optional[str], list[ABDDNode]]:
    """
    The main recursive Apply() function for ABDDs.
    Utilizes node cache (unique table), call cache (dynamic programming), short-circuit evaluation.

    First, materialization happens if needed (introducing a node to synchronize the source node variables).
    Then, recursion itself happens inside the 'process_box_tree()' function which calculates the product of the two used
    reduction rules (nodes of the tree contain some extra information about mapping
    the intermediate results, negations, recursion, etc.).

    'op': Boolean Operation (supported: AND, OR, XOR, NOR, NAND, IMPLY, IFF ~ XNOR)
    'var': variable of the source nodes (None in case of the top-level call on the root of the ABDD)
    'e1', 'e2': edge objects (see apply_edge.py) - contain information about reduction rules and target nodes
    'helper': data class with extra meta data (references to caches, counters, debug info)

    Note: negation cache is a special case for a call cache, since sometimes we can skip the computation of
    recursive calls and return one of the operands, just in the negated form.
    """
    # check call cache
    cache_hit = helper.call_cache.find_call(op, var, e1, e2)
    if cache_hit is not None:
        rule, nodes = cache_hit
        return rule, nodes

    # short circuit evaluation
    rule, nodes = short_circuit_evaluation(e1, op, e2, helper)
    if nodes != []:
        helper.call_cache.insert_call(op, var, e1, e2, rule, nodes)
        return rule, nodes

    # now we can assume that e1 and e2 have targets with the same variable
    # materialization
    min1 = min(n.var if not n.is_leaf else (helper.abdd1.variable_count + 1) for n in e1.target)
    min2 = min(n.var if not n.is_leaf else (helper.abdd2.variable_count + 1) for n in e2.target)
    max1 = max(n.var if not n.is_leaf else (helper.abdd1.variable_count + 1) for n in e1.target)
    max2 = max(n.var if not n.is_leaf else (helper.abdd2.variable_count + 1) for n in e2.target)
    matlevel = min(min1, min2)

    if matlevel != max1:
        predicates1 = obtain_predicates(helper.abdd1, e1.source, e1.direction, matlevel)
        if predicates1 != frozenset() and e1.rule:
            pattern = cached_materialization_recipes[e1.rule][predicates1]
            e1 = materialize_abdd_pattern(e1, pattern, matlevel, helper)
            return abdd_apply_from(op, matlevel, e1, e2, helper)
    if matlevel != max2:
        predicates2 = obtain_predicates(helper.abdd2, e2.source, e2.direction, matlevel)
        if predicates2 != frozenset() and e2.rule:
            pattern = cached_materialization_recipes[e2.rule][predicates2]
            e2 = materialize_abdd_pattern(e2, pattern, matlevel, helper)
            return abdd_apply_from(op, matlevel, e1, e2, helper)

    # edges to leaves -> this might not be needed if short-circuit evaluation happens before materialization
    # however, it seems necessary
    if all([n.is_leaf for n in e1.target]) and all([n.is_leaf for n in e2.target]):
        boxtree = boxtree_cache[(e1.rule, op, e2.rule)]
        treelevel = (
            min(e1.source.var if e1.source is not None else 1, e2.source.var if e2.source is not None else 1) + 1
        )
        rule, nodes = process_boxtree_leafcase(boxtree, e1, e2, op, helper, matlevel, treelevel)
        helper.call_cache.insert_call(op, matlevel, e1, e2, rule, nodes)
        return rule, nodes
    # NOTE: inserting into and checking against the "node_cache" is done during boxtree exploration

    boxtree = boxtree_cache[(e1.rule, op, e2.rule)]
    treelevel = min(e1.source.var if e1.source is not None else 1, e2.source.var if e2.source is not None else 1) + 1
    rule, nodes = process_boxtree_innercase(boxtree, e1, e2, op, helper, matlevel, treelevel)
    helper.call_cache.insert_call(op, matlevel, e1, e2, rule, nodes)
    return rule, nodes


def process_boxtree_innercase(
    boxtree: BoxTreeNode,
    e1: ApplyEdge,
    e2: ApplyEdge,
    op: BooleanOperation,
    helper: ABDDApplyHelper,
    varlevel: int,
    rootlevel: int,
) -> tuple[Optional[str], list[ABDDNode]]:
    """
    [description]
    Combine two edge objects (their reduction rules) while traversing an structure (boxtree), which has
    information needed to properly merge reduction rules on the edges, such that semantics are in tact.

    [parameters]
    'boxtree': box tree (picked from the boxtree_cache before this function is called)
    'e1', 'e2': the two edges needed for obtaining edge targets for boxes in the leaf nodes of the boxtree
    'op': operation used in the parent apply call
    'helper': metadata guiding the whole apply procedure (especially handling memoization, call cache)
    'varlevel': variable of target nodes (since node materialization precedes boxtree traversal,
        var should be the same for all edge targets)
    'rootlevel': variable of the root node of the boxtree (important in case the boxtree contains non-leaf nodes)

    [return]
    The edge pointing to the root node of the boxtree
        - either a short edge in case boxtree has non-leaf nodes
        - or the reduced edge using box from the singular node of the box tree (root and leaf) with the properly
            computed targets
    """

    # We represent constant Boolean functions with edge ---<X>---> 0/1
    # Note that this breaks canonicity in some cases, and is one more reason why
    # post-hoc canonization of the result of ABDD Apply() is needed.
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
                edge1low = ApplyEdge(e1.abdd, e1.target[pc.target1], False)
                edge2low = ApplyEdge(e2.abdd, e2.target[pc.target2], False)
                edge1high = ApplyEdge(e1.abdd, e1.target[pc.target1], True)
                edge2high = ApplyEdge(e2.abdd, e2.target[pc.target2], True)
                l_rule, l_target = abdd_apply_from(op, varlevel + 1, edge1low, edge2low, helper)
                h_rule, h_target = abdd_apply_from(op, varlevel + 1, edge1high, edge2high, helper)
                node = ABDDNode(helper.counter)
                node.var = varlevel
                node.low_box = l_rule
                node.low = l_target
                node.high_box = h_rule
                node.high = h_target
                node.is_leaf = False
                cache_hit = helper.node_cache.find_node(node)
                if cache_hit is not None:
                    nodes.append(cache_hit)
                else:
                    nodes.append(node)
                    helper.node_cache.insert_node(node)
            elif pc.target1 is not None:
                resultnode = e1.target[pc.target1]
                if pc.negation:
                    resultnode = negate_subtree(helper.abdd1, resultnode, helper)
                nodes.append(resultnode)
            elif pc.target2 is not None:
                resultnode = e2.target[pc.target2]
                if pc.negation:
                    resultnode = negate_subtree(helper.abdd2, resultnode, helper)
                nodes.append(resultnode)
        return rule, nodes

    low_rule, low_targets = (
        process_boxtree_innercase(boxtree.low, e1, e2, op, helper, varlevel, rootlevel + 1)
        if boxtree.low
        else (None, [])
    )
    high_rule, high_targets = (
        process_boxtree_innercase(boxtree.high, e1, e2, op, helper, varlevel, rootlevel + 1)
        if boxtree.high
        else (None, [])
    )

    # Edge case: when the box tree has non-leaf nodes, and is supposed to represent
    # a Boolean function of two variables, then the leaf nodes represent boxes that reduce over one variable
    # labeling such edges with reductions would be wrong, since they are inherently short,
    # thus we need to specifically take care of this.
    use_short = varlevel - rootlevel == 1

    new_abdd_node = ABDDNode(helper.counter)
    new_abdd_node.var = rootlevel
    new_abdd_node.low_box = None if use_short else low_rule
    new_abdd_node.low = short_edge_corrector(low_rule, low_targets) if use_short else low_targets
    new_abdd_node.high_box = None if use_short else high_rule
    new_abdd_node.high = short_edge_corrector(high_rule, high_targets) if use_short else high_targets
    new_abdd_node.is_leaf = False

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


# End of file abdd_apply_main.py
