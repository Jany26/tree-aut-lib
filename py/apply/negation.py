from apply.abdd import ABDD
from apply.abdd_node import ABDDNode
from apply.abdd_apply_helper import ABDDApplyHelper


negate_box_label = {
    None: None,
    "X": "X",
    "L0": "L1",
    "L1": "L0",
    "H0": "H1",
    "H1": "H0",
    "LPort": "LPort",
    "HPort": "HPort",
}


def negate_subtree(abdd: ABDD, node: ABDDNode, helper: ABDDApplyHelper) -> ABDDNode:
    cache_hit = helper.find_negated_node(node)
    if cache_hit is not None:
        return cache_hit

    # since terminal nodes are in the cache from the start, we don't have to explicitly
    # check leaf nodes for early return, it would happen in the initial cache check

    neg_low = [negate_subtree(abdd, child, helper) for child in node.low]
    neg_high = [negate_subtree(abdd, child, helper) for child in node.high]
    low_box = negate_box_label[node.low_box]
    high_box = negate_box_label[node.high_box]

    newnode = ABDDNode(helper.counter)
    newnode.var = node.var
    newnode.low = neg_low
    newnode.low_box = low_box
    newnode.high = neg_high
    newnode.high_box = high_box
    # newnode.is_root = node.is_root
    newnode.is_leaf = node.is_leaf

    cache_hit = helper.node_cache.find_node(newnode)
    if cache_hit is None:
        helper.counter += 1
        helper.node_cache.insert_node(newnode)
    else:
        del newnode
        newnode = cache_hit
    helper.insert_negated_node(node, newnode)
    return newnode
