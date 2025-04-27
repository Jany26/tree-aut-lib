from typing import NewType, Optional

from apply.abdd_node import ABDDNode


# cache [ var, leaf_val, low_box, low_target, high_box, high_target ] -> node
ABDDNodeCache = NewType(
    "ABDDNodeCache",
    dict[
        tuple[
            int,  # variable of the node
            Optional[int],  # leaf value - for inner nodes this is None
            Optional[str],  # low-edge box              / None in case of leaf nodes
            tuple[int],  # low-edge target node idx
            Optional[str],  # high-edge box             / None in case of leaf nodes
            tuple[int],  # high-edge target node idx
        ],
        ABDDNode,
    ],
)


class ABDDNodeCacheClass:
    def __init__(self):
        self.cache: ABDDNodeCache = {}
        zero = ABDDNode(0)
        one = ABDDNode(1)
        zero.set_as_leaf(0)
        one.set_as_leaf(1)
        self.terminal_0 = zero
        self.terminal_1 = one
        self.cache[(0, 0, None, (), None, ())] = self.terminal_0
        self.cache[(0, 1, None, (), None, ())] = self.terminal_1
        self.counter = 2

    def insert_node(self, node: ABDDNode) -> None:
        low_tuple = tuple([id(n) for n in node.low])
        high_tuple = tuple([id(n) for n in node.high])
        lookup = tuple([node.var, node.leaf_val, node.low_box, low_tuple, node.high_box, high_tuple])
        self.cache[lookup] = node

    def find_node(self, node: ABDDNode) -> Optional[ABDDNode]:
        low_tuple = tuple([id(n) for n in node.low])
        high_tuple = tuple([id(n) for n in node.high])
        lookup = tuple([node.var, node.leaf_val, node.low_box, low_tuple, node.high_box, high_tuple])
        if lookup in self.cache:
            return self.cache[lookup]
        return None

    def refresh_nodes(self):
        counter = 2
        for tup, i in self.cache.items():
            if i.is_leaf:
                continue
            i.node = counter
            counter += 1
        self.counter = counter

    def __repr__(self) -> str:
        result = "%-*s %-*s %-*s %-*s %-*s %-*s -> %-*s %-*s\n" % (
            4,
            "var",
            4,
            "leaf",
            5,
            "Lbox",
            20,
            "Lnodes",
            5,
            "Hbox",
            20,
            "Hnodes",
            8,
            "NodePtr",
            8,
            "NodeID",
        )
        result += "-" * 84 + "\n"
        for tup, node in self.cache.items():
            var, leaf, lbox, lnodes, hbox, hnodes = tup
            result += "%-*s %-*s %-*s %-*s %-*s %-*s -> %-*s %-*s\n" % (
                4,
                var,
                4,
                "-" if leaf is None else leaf,
                5,
                "-" if lbox is None else lbox,
                20,
                "[" + ",".join([str(hex(l))[6:] for l in lnodes]) + "]",
                5,
                "-" if hbox is None else hbox,
                20,
                "[" + ",".join([str(hex(l))[6:] for l in hnodes]) + "]",
                8,
                hex(id(node))[6:],
                8,
                f"<{node.leaf_val}>" if node.is_leaf else f"{node.node}({node.var})",
            )
        return result
