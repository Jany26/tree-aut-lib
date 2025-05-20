"""
[file] abdd_apply_helper.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Helper class for the main Apply algorithm.
"""

from typing import Optional
from apply.abdd import ABDD
from apply.abdd_node import ABDDNode
from apply.abdd_call_cache import ABDDCallCacheClass
from apply.abdd_node_cache import ABDDNodeCacheClass


class ABDDApplyHelper:
    """
    Helper class with necessary cache and information
    needed during the recursive apply function.

    'call_cache' - Stores results of recursive apply calls.

    'node_cache' - Makes sure that identical nodes are not duplicated.
    This differs from ApplyCallCache in the sense that two different apply
    calls might create two nodes that represent the same boolean function.

    'negation_cache' - Basically a call cache, just for negation, which is often used
    during box tree traversal.

    'abdd1', 'abdd2' - references to original ABDD inputs
    'maxvar' - for checking nodes above leaves, etc. (from root to leaves, the variables are increasing)
    """

    call_cache: ABDDCallCacheClass
    node_cache: ABDDNodeCacheClass

    # we will use id(node) as keys into the cache
    negation_cache: dict[int, ABDDNode]

    def __init__(
        self, in1: ABDD, in2: Optional[ABDD], maxvar: Optional[int] = None, cache: Optional[ABDDNodeCacheClass] = None
    ):
        self.call_cache = ABDDCallCacheClass()
        self.node_cache = cache if cache is not None else ABDDNodeCacheClass()
        self.negation_cache = {id(cache.terminal_0): cache.terminal_1, id(cache.terminal_1): cache.terminal_0}

        self.abdd1: ABDD = in1
        self.abdd2: Optional[ABDD] = in2

        if cache is None:
            insert_abdd_in_node_cache(self.node_cache, in1)
            if in2 is not None:
                insert_abdd_in_node_cache(self.node_cache, in2)
        self.node_cache.refresh_nodes()
        self.counter = self.node_cache.counter
        self.maxvar = maxvar

    def find_negated_node(self, node: ABDDNode) -> Optional[ABDDNode]:
        if id(node) in self.negation_cache:
            return self.negation_cache[id(node)]
        return None

    def insert_negated_node(self, node: ABDDNode, negation: ABDDNode) -> None:
        self.negation_cache[id(node)] = negation


def insert_abdd_in_node_cache(ncache: ABDDNodeCacheClass, abdd1: ABDD) -> None:
    """
    It is assumed that ncache already contains terminal nodes (since initialization).
    It is also assumed that abdd does not already contain duplicates/redundant nodes.
    """
    for n in abdd1.iterate_bfs_nodes():
        if n.is_leaf:
            continue
        hit = ncache.find_node(n)
        if hit is not None:
            ncache.insert_node(n)


# End of file abdd_apply_helper.py
