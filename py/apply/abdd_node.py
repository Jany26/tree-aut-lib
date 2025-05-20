"""
[file] abdd_node.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Class for representing nodes of ABDDs.
"""

from typing import Generator, Iterator, Optional, Union

from tree_automata.transition import TTransition
from helpers.utils import box_arities, eprint


class ABDDNode:
    """
    One node of an ABDD. Contains information about

    States/Nodes and variables are represented as integers.
    In case of boxes with higher port arity than one, the child nodes will
    be represented as lists of integers (positions in the ordered list of
    ports will correspond to positions in this child list).
    """

    # node name / index for lookup
    # the structure is NOT sorted like a binary search tree !
    # node idx is also used for reference in parent sets
    node: int

    # variable index, 0 is reserved for leaves and error checking, variables start from 1
    # TODO: perhaps it would be better to actually use normal index to store variable level,
    # and not always reference the overall abdd's level
    var: int

    is_leaf: bool  # probably irrelevant since we can check leaf_val is None...
    # if is_leaf=True, it is the terminal node value [0/1]
    leaf_val: Optional[int]

    # None if the edge is short or node is a leaf
    low_box: Optional[str]
    # None if the edge is short or node is a leaf
    high_box: Optional[str]

    # [] in case of leaf transitions,
    # [node] for short edges or 1-port reduction boxes,
    # [node1, ..., noden] in case of n-port box transitions
    low: list["ABDDNode"]
    high: list["ABDDNode"]

    def __init__(self, name: Union[str, int], state_prefix_len: int = 1):
        # in ABDD-convertible BDA/UBDA structures, one node should always have one outgoing edge,
        # which allows us to definitely infer all information about one ABDD node from exactly one edge
        # of the ABDD-like structure (reduced BDA).
        if type(name) == str:
            self.node = int(name[state_prefix_len:])
        if type(name) == int:
            self.node = name
        self.var = 0  # normally, we start indexing variables from 1, but is set to 0 for nodes with unset data

        self.is_leaf = True
        self.leaf_val = None

        self.low_box = None
        self.low = []

        self.high_box = None
        self.high = []

    def __repr__(self):
        attrib = [
            f"node={self.node}",
            f"var={self.var}",
            f"leaf{f' {self.leaf_val}' if self.leaf_val is not None else ''}" if self.is_leaf else "",
            f"lbox={self.low_box}" if self.low != [] else "",
            f"low={prettyprint_nodes(self.low)}" if self.low != [] else "",
            f"hbox={self.high_box}" if self.high != [] else "",
            f"high={prettyprint_nodes(self.high)}" if self.high != [] else "",
        ]

        return f"{self.__class__.__name__}({', '.join([i for i in attrib if i != ""])})"

    def __hash__(self):
        return hash(
            (
                self.node,
                self.var,
                self.leaf_val if self.is_leaf else "",
                ",".join([str(i.node) for i in self.low]),
                self.low_box,
                ",".join([str(i.node) for i in self.high]),
                self.high_box,
            )
        )

    def __eq__(self, other: "ABDDNode"):
        if any(
            [
                not isinstance(other, ABDDNode),
                # node indices do not differentiate the semantics of a BDD node
                # self.node != other.node:
                self.var != other.var,
                self.is_leaf != other.is_leaf,
                self.is_leaf and self.leaf_val != other.leaf_val,
                self.low_box != other.low_box,
                self.high_box != other.high_box,
            ]
        ):
            return False

        # leaf and non-leaf
        if self.is_leaf != other.is_leaf:
            return False

        # both are leaves
        if self.is_leaf:
            return self.leaf_val == other.leaf_val

        # both are internal nodes
        # checking low-low, high-high arity compatibility
        if len(self.low) != len(other.low) or len(self.high) != len(self.high):
            return False
        # comparing children themselves in-order
        if any([a != b for a, b in zip(self.low, other.low)]):
            return False
        if any([a != b for a, b in zip(self.high, other.high)]):
            return False

        return True

    # the following three functions are used during TTreeAut -> ABDD conversion.

    def set_node_info_from_ta_transition(
        self, edge: TTransition, node_map: dict[str, "ABDDNode"], var_prefix_len: int = 1
    ):
        self.var = int(edge.info.variable[var_prefix_len:])
        self.is_leaf = False

        if len(edge.info.box_array) == 0:
            self.low_box = None
            self.high_box = None
        else:
            self.low_box = None if edge.info.box_array[0] in ["", None] else edge.info.box_array[0]
            self.high_box = None if edge.info.box_array[1] in ["", None] else edge.info.box_array[1]

        low_arity: int = 1 if self.low_box is None else box_arities[self.low_box]
        high_arity: int = 1 if self.high_box is None else box_arities[self.high_box]
        if low_arity + high_arity != edge.children:
            ValueError("inconsistent box arities with children list")
        low_slice = [node_map[state] for state in edge.children[0:low_arity]]
        high_slice = [node_map[state] for state in edge.children[low_arity : low_arity + high_arity]]
        self.low = low_slice
        self.high = high_slice

    def set_leaf_info_from_ta_transition(self, edge: TTransition, var_prefix_len: int = 1):
        if edge.info.variable != "":
            self.var = int(edge.info.variable[var_prefix_len:])
        self.is_leaf = True
        self.leaf_val = int(edge.info.label)

    def set_as_leaf(self, leaf_val: int) -> None:
        self.var = 0
        self.is_leaf = True
        self.leaf_val = leaf_val
        self.low_box = None
        self.high_box = None
        self.low = []
        self.high = []

    def check_node(self) -> bool:
        """
        Check information/attribute consistency of the node.
        If node contains contradictory information, return False.
        """
        result = True

        # leaf consistency
        if self.is_leaf and any(
            [
                self.var != 0,
                self.leaf_val is None,
                self.low != [],
                self.high != [],
                self.low_box is not None,
                self.high_box is not None,
            ]
        ):
            eprint(f"ABDDNode check: node {self.node} is leaf, but has non-leaf attributes")
            result = False

        # early return in case of leaf, since afterwars we access non-leaf attributes
        if self.is_leaf:
            return result

        # inner node - variable consistency
        if any([self.var <= 0] + [self.var >= i.var for i in self.low + self.high]):
            eprint(f"ABDDNode check: inner node {self.node} has inconsistent variable info")
            result = False

        # inner node attributes, box arity consistency with children
        if any(
            [
                self.low_box is None and len(self.low) > 1,
                self.high_box is None and len(self.high) > 1,
                type(self.low_box) == str and box_arities[self.low_box] != len(self.low),
                type(self.high_box) == str and box_arities[self.high_box] != len(self.high),
            ]
        ):
            eprint(f"ABDDNode check: inner node {self.node} box info is inconsistent with child info")
            result = False

        return result

    def connect_to_low_child(self, node: "ABDDNode") -> None:
        """
        From POV of parent node N, connect a child node P (argument 'node') to N's low nodes.
        If used multiple times on the same node, low turns from ABDDNode to list[ABDDNode]
        """
        self.low.append(node)

    def connect_to_high_child(self, node: "ABDDNode") -> None:
        """
        From POV of parent node N, connect a child node P (argument 'node') to N's high nodes.
        """
        self.high.append(node)

    def connect_to_parent_from_low(self, node: "ABDDNode") -> None:
        """
        From POV of child node P, connect it as a low node to parent node P (argument 'node').
        """
        node.low.append(self)

    def connect_to_parent_from_high(self, node: "ABDDNode") -> None:
        """
        From POV of child node P, connect it as a high node to parent node P (argument 'node').
        """
        node.high.append(self)

    def explore_subtree_bfs(self, repeat=False) -> Iterator["ABDDNode"]:
        """
        BFS traversal of the ABDD rooted at the given node.
        If repeat=False, each node is visited max. once.
        """
        queue: list[ABDDNode] = [self]
        visited = set()
        while queue != []:
            node = queue.pop(0)
            if not repeat and node in visited:
                continue
            yield node
            visited.add(node)
            queue.extend(node.low)
            queue.extend(node.high)

    def explore_subtree_dfs(self, repeat=False) -> Iterator["ABDDNode"]:
        """
        DFS traversal of the ABDD rooted at the given node.
        If repeat=False, each node is visited max. once.
        """
        stack: list[ABDDNode] = [self]
        visited = set()
        while stack != []:
            node = stack.pop()
            if not repeat and node in visited:
                continue
            yield node
            # we have to insert nodes in a reverse order
            visited.add(node)
            stack.extend(reversed(node.low))
            stack.extend(reversed(node.high))

    def explore_subtree_bfs_backrefs(self, repeat=False) -> Iterator[tuple["ABDDNode", bool, "ABDDNode"]]:
        """
        BFS traversal of the ABDD rooted at the given node, but instead of yielding nodes,
        this yields triples (source-node, direction, target-node). Low edge -> direction=False.
        If repeat=False, each node is visited max. once.
        """
        queue: list[ABDDNode] = [(self, False, i) for i in self.low] + [(self, True, i) for i in self.high]
        visited = set()
        while queue != []:
            node = queue.pop(0)
            if not repeat and node in visited:
                continue
            yield node
            visited.add(node)
            queue.extend([(node, False, i) for i in node.low])
            queue.extend([(node, True, i) for i in node.high])

    def explore_subtree_dfs_backrefs(self, repeat=False) -> Iterator[tuple["ABDDNode", bool, "ABDDNode"]]:
        """
        DFS traversal of the ABDD rooted at the given node, but instead of yielding nodes,
        this yields triples (source-node, direction, target-node). Low edge -> direction=False.
        If repeat=False, each node is visited max. once.
        """
        queue: list[ABDDNode] = [(self, True, i) for i in reversed(self.high)] + [
            (self, False, i) for i in reversed(self.low)
        ]
        visited = set()
        while queue != []:
            node = queue.pop()
            if not repeat and node in visited:
                continue
            yield node
            visited.add(node)
            queue.extend([(node, False, i) for i in reversed(node.high)])
            queue.extend([(node, False, i) for i in reversed(node.low)])

    def find_terminal(self, target: int) -> Optional["ABDDNode"]:
        for i in self.explore_subtree_bfs():
            if i.is_leaf and i.leaf_val == target:
                return i
        return None


def prettyprint_nodes(l: list[ABDDNode]) -> str:
    return "[" + ", ".join([f"{i.node}({i.var})" if not i.is_leaf else f"<{i.leaf_val}>" for i in l]) + "]"


# End of file abdd_node.py
