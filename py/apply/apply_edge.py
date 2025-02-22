from typing import Optional
from apply.abdd_node import ABDDNode
from apply.abdd import ABDD


class ApplyEdge:
    abdd: ABDD
    from_node: Optional[ABDDNode]
    to_node: ABDDNode | list[ABDDNode]
    box_reduction: str
    low_high: bool  # False = low, True = high

    def __init__(self, abdd, from_node, to_node, box_reduction, low_high):
        self.abdd = abdd
        self.from_node = from_node
        self.to_node = to_node
        self.box_reduction = box_reduction
        self.low_high = low_high
