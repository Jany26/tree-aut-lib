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
            Optional[str],  # box used on the edge leading to the first operand node
            tuple[int],  # node list of the second operand node
            Optional[str],  # box used on the edge leading to the second operand node
        ],
        # returning a rule and target nodes
        tuple[Optional[str], list[ABDDNode]],
    ],
)


class ABDDCallCacheClass:
    def __init__(self):
        self.cache: ABDDCallCache = {}

    def insert_call(
        self,
        op: BooleanOperation,
        var: int,
        edge1: ApplyEdge,
        edge2: ApplyEdge,
        rule: Optional[str],
        targets: list[ABDDNode],
    ) -> None:
        tgt1 = tuple([n.node for n in edge1.target])
        tgt2 = tuple([n.node for n in edge2.target])
        lookup = (op, var, edge1.rule, tgt1, edge2.rule, tgt2)
        self.cache[lookup] = (rule, targets)

    def find_call(
        self, op: BooleanOperation, var: int, edge1: ApplyEdge, edge2: ApplyEdge
    ) -> Optional[tuple[Optional[str], list[ABDDNode]]]:
        tgt1 = tuple([n.node for n in edge1.target])
        tgt2 = tuple([n.node for n in edge2.target])
        lookup = (op, var, edge1.rule, tgt1, edge2.rule, tgt2)
        if lookup in self.cache:
            rule, nodes = self.cache[lookup]
            return rule, nodes
        return None

    def __repr__(self) -> str:
        result = "%-*s %-*s %-*s %-*s %-*s %-*s %-*s -> %-*s\n" % (
            4,
            "op",
            4,
            "var",
            5,
            "box1",
            10,
            "nodes1",
            5,
            "box2",
            10,
            "nodes2",
            10,
            "resBox",
            30,
            "resNodes",
        )
        result += "-" * 80 + "\n"
        for tup, node in self.cache.items():
            op: BooleanOperation
            op, var, rule1, tgt1, rule2, tgt2 = tup
            result += "%-*s %-*s %-*s %-*s %-*s %-*s %-*s -> %-*s\n" % (
                4,
                op.name,
                4,
                var,
                5,
                "-" if rule1 is None else rule1,
                10,
                "[" + ",".join([str(l) for l in tgt1]) + "]",
                5,
                "-" if rule2 is None else rule2,
                10,
                "[" + ",".join([str(l) for l in tgt2]) + "]",
                50,
                node,
            )
        return result
