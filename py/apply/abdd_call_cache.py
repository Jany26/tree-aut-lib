from typing import NewType, Optional

from apply.apply_edge import ApplyEdge
from apply.box_algebra.apply_tables import BooleanOperation
from apply.abdd_node import ABDDNode


# cache[ op, var, nodes_a, box_a, nodes_b, box_b ] -> rule, nodes
ABDDCallCache = NewType(
    "ABDDCallCache",
    dict[
        tuple[
            BooleanOperation,  # operation used in the apply call
            int,  # at which variable level is apply called
            tuple[int],  # node list of the first operand node
            str,  # box used on the edge leading to the first operand node
            tuple[int],  # node list of the second operand node
            str,  # box used on the edge leading to the second operand node
        ],
        # returning a rule and target nodes
        tuple[Optional[str], list[ABDDNode]],
    ],
)


class ABDDCallCacheClass:
    def __init__(self):
        self.cache: ABDDCallCacheClass = {}

    def insert_call(self, op: BooleanOperation, edge1: ApplyEdge, edge2: ApplyEdge) -> None:
        pass

    def find_call(self, op: BooleanOperation, edge1: ApplyEdge, edge2: ApplyEdge) -> Optional[ABDDNode]:
        pass
