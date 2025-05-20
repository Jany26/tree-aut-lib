"""
[file] apply_edge.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Class encapsulating one edge of ABDDs with references to source nodes and the whole ABDD.
This class helps to keep the number of arguments in Apply low,
since we encapsulate the whole context of an edge in one class.
"""

from typing import Optional
from apply.abdd_node import ABDDNode
from apply.abdd import ABDD


class ApplyEdge:
    """
    Helper structure which represents one edge of an ABDD.
    Edge e is a tuple (e.node, e.rule), since we can have multiport reduction rules,
    e.node is actually a list of ABDDNodes.

    ApplyEdge contains references to nodes and rules so that modifying this information
    in the ApplyEdge object will translate to the original ABDD.

    For algorithm's (conceptual) purposes, only 'target' and 'rule' are needed.
    For implementation's purposes (modifying, referencing, etc.), 'abdd', 'source' and 'direction' are needed.
    """

    def __init__(self, abdd: ABDD, source: Optional[ABDDNode] = None, direction: Optional[bool] = None):
        self.abdd: ABDD = abdd
        self.source: Optional[ABDDNode] = source
        self.direction: Optional[bool] = direction
        self.target: list[ABDDNode] = [r for r in self.abdd.roots]
        # self.rule: Optional[str] = self.abdd.root_rule
        self.rule: Optional[str] = None if max(r.var for r in self.abdd.roots) == 1 else "X"
        if source is not None and direction is not None:
            self.target = source.high if direction else source.low
            self.rule = source.high_box if direction else source.low_box

    def __repr__(self) -> str:
        rule = "S" if self.rule is None else self.rule
        dir = "None" if self.direction is None else "H" if self.direction else "L"
        src = "None" if self.source is None else f"{self.source.node}({self.source.var})"
        tgt = "[" + ", ".join([f"{n.node}({n.var})" if not n.is_leaf else f"<{n.leaf_val}>" for n in self.target]) + "]"
        return f"{self.__class__.__name__}(abdd={self.abdd.name}, src={src}, dir={dir}, tgt={tgt}, rule={rule})"

    def __eq__(self, other: "ApplyEdge") -> bool:
        return all(
            [
                self.abdd.name == other.abdd.name,  # NOTE: comparing whole ABDD structures seems unnecessary
                self.source == other.source,
                self.direction == other.direction,
                self.target == other.target,
                self.rule == other.rule,
            ]
        )


# End of file apply_edge.py
