from types import NoneType
from typing import Generator, Optional, Union

from tree_automata.automaton import TTreeAut
from tree_automata.transition import TTransition
from helpers.utils import box_arities, eprint


class ABDDNode:
    """
    States/Nodes and variables are represented as integers.
    In case of boxes with higher port arity than one, the child nodes will
    be represented as lists of integers (positions in the ordered list of
    ports will correspond to positions in this child list).
    """

    node: int  # node name / index for lookup -- the structure is not sorted like a binary search tree !
    var: int  # variable index
    is_leaf: bool
    is_root: bool
    leaf_val: Optional[int]  # if is_leaf=True, it is the terminal node value [0/1]
    low_box: Optional[str]
    high_box: Optional[str]

    # None in case of leaf transitions, list in case of multi-port box transitions
    low: Union[NoneType, "ABDDNode", list["ABDDNode"]]
    high: Union[NoneType, "ABDDNode", list["ABDDNode"]]
    parents_through_low: set["ABDDNode"]  # if root, both parent lists are []
    parents_through_high: set["ABDDNode"]

    def __init__(self, name: Union[str, int], state_prefix_len: int = 1):
        # in ABDD-like structures, one node should always have one outgoing edge, which allows us to definitely
        # infer all information about one ABDD node from exactly one edge of the ABDD-like structure (reduced BDA).
        if type(name) == str:
            self.node = int(name[state_prefix_len:])
        if type(name) == int:
            self.node = name
        self.var = 0  # normally, we start indexing variables from 1

        self.is_leaf = True
        self.is_root = False
        self.leaf_val = None

        self.low_box = None
        self.low = None
        self.parents_through_low = set()

        self.high_box = None
        self.high = None
        self.parents_through_high = set()

    def __repr__(self):
        if self.is_leaf:
            return f"{self.node} [{self.leaf_val}]"
        result: str = f"{self.node} <{self.var}> "
        result += f"[L:{self.low_box if self.low_box is not None else 'S'}]"

        result += f"{self.low.node} "

        result += f"[H:{self.low_box if self.low_box is not None else 'S'}]"

        result += f"{self.high.node}"

        return result

    def __hash__(self):
        return hash(
            (
                self.node,
                self.var,
                self.leaf_val if self.is_leaf else None,
                self.low.node if self.low else None,
                self.low_box,
                self.high.node if self.low else None,
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
        if self.is_leaf:
            if self.low is not None or self.high is not None:
                return False
        else:
            if isinstance(self.low, list) and isinstance(other.low, list):
                if len(self.low) != len(other.low):
                    return False
                for a, b in zip(self.low, other.low):
                    if a != b:
                        return False
            elif self.low != other.low:
                return False

            if isinstance(self.high, list) and isinstance(other.high, list):
                if len(self.high) != len(other.high):
                    return False
                for a, b in zip(self.high, other.high):
                    if a != b:
                        return False
            elif self.high != other.high:
                return False

        return True

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
        self.set_child_info(low_slice, low=True)
        self.set_child_info(high_slice, high=True)

    def set_child_info(self, child_list: list["ABDDNode"], low=False, high=False):
        if low and high:
            ValueError("only one of low/high can be true")
        if low:
            self.low = child_list if len(child_list) > 1 else child_list[0]
            for node in child_list:
                node.parents_through_low.add(self)
        if high:
            self.high = child_list if len(child_list) > 1 else child_list[0]
            for node in child_list:
                node.parents_through_high.add(self)

    def set_leaf_info_from_ta_transition(self, edge: TTransition, var_prefix_len: int = 1):
        if edge.info.variable != "":
            self.var = int(edge.info.variable[var_prefix_len:])
        self.is_leaf = True
        self.leaf_val = int(edge.info.label)

    def set_as_leaf(self, leaf_val: int) -> None:
        self.is_leaf = True
        self.leaf_val = leaf_val
        self.low_box = None
        self.high_box = None
        self.low = None
        self.high = None

    def iterate_children(self, low=False, high=False) -> Generator["ABDDNode", None, None]:
        targets = []
        if low:
            targets.append(self.low)
        if high:
            targets.append(self.high)
        for target in targets:
            if target is None:
                return
            if type(target) == ABDDNode:
                yield target
            if type(target) == list:
                for i in target:
                    yield i

    def check_node(self) -> bool:
        result = True

        if self.var == 0:
            result = False
            eprint(f"ABDDNode check: node {self.node} - no var")
        else:
            for i in self.iterate_children(low=True, high=True):
                if i.var != 0 and self.var >= i.var:
                    eprint(f"ABDDNode check: node {self.node} - inconsistent order with child var")
                    return False

        if self.is_leaf:
            if self.leaf_val is None:
                eprint(f"ABDDNode check: node {self.node} - leaf check failed")
                result = False

        if self.is_root:
            if len(self.parents_through_low) != 0:
                eprint(f"ABDDNode check: node {self.node} - root check failed")
                result = False
            if len(self.parents_through_high) != 0:
                eprint(f"ABDDNode check: node {self.node} - root check failed")
                result = False

        if not self.check_child(self, low=True):
            eprint(f"ABDDNode check: node {self.node} - low check failed")
            result = False
        if not self.check_child(self, high=True):
            eprint(f"ABDDNode check: node {self.node} - high check failed")
            result = False

        return result

    def check_child(self, low=False, high=False) -> bool:
        target: NoneType | "ABDDNode" | list["ABDDNode"]
        target_box: Optional[str]
        if low and not high:
            target = self.low
            target_box = self.low_box
        elif high and not low:
            target = self.high
            target_box = self.high_box
        else:
            ValueError("ABDDNode.check_child(): one of low/high has to be True")

        if self.is_leaf and target is None and target_box is None:
            return True
        if type(target) == ABDDNode and target_box is None:
            return True
        if type(target) == ABDDNode and target_box is not None and box_arities[target_box] == 1:
            if low and self not in target.parents_through_low:
                return False
            if high and self not in target.parents_through_high:
                return False
            return True
        if type(target) == list and target_box is not None and box_arities[target_box] == len(target):
            for child in target:
                if low and self not in child.parents_through_low:
                    return False
                if high and self not in child.parents_through_high:
                    return False
            return True
        return False

    def get_leaf_sym(self) -> Optional[int]:
        if self.is_leaf:
            return self.leaf_val
        return None

    def connect_to_low_child(
        self, node: "ABDDNode"
    ) -> None:  # if multiple attach_low, ABDDNode turns to list[ABDDNode]
        """
        From POV of parent node N, connect a child node P (argument 'node') to N's low nodes.
        """
        self.low
        node.parents_through_low.add(self)

    def connect_to_high_child(self, node: "ABDDNode") -> None:
        """
        From POV of parent node N, connect a child node P (argument 'node') to N's high nodes.
        """
        node.parents_through_high.add(self)

    def connect_to_parent_from_low(self, node: "ABDDNode") -> None:
        """
        From POV of child node P, connect it as a low node to parent node P (argument 'node').
        """
        new_low: ABDDNode | list[ABDDNode]
        if node.low is None:
            new_low = self
        if type(node.low) == ABDDNode:
            new_low = [node.low, self]
        if type(node.low) == list:
            new_low = node.low.extend([self])
        node.low = new_low
        self.parents_through_low.add(node)

    def connect_to_parent_from_high(self, node: "ABDDNode") -> None:
        """
        From POV of child node P, connect it as a high node to parent node P (argument 'node').
        """
        new_high: ABDDNode | list[ABDDNode]
        if node.high is None:
            new_high = self
        if type(node.high) == ABDDNode:
            new_high = [node.high, self]
        if type(node.high) == list:
            new_high = node.high.extend([self])
        node.high = new_high
        self.parents_through_high.add(node)

    def explore_subtree_bfs(self, repeat=False) -> Generator["ABDDNode", None, None]:
        queue: list[ABDDNode] = [self]
        visited = set()
        while queue != []:
            node = queue.pop(0)
            if not repeat and node in visited:
                continue
            yield node
            visited.add(node)
            if type(node.low) == ABDDNode:
                queue.append(node.low)
            if type(node.low) == list:
                queue.extend(node.low)
            if type(node.high) == ABDDNode:
                queue.append(node.high)
            if type(node.high) == list:
                queue.extend(node.high)

    def explore_subtree_dfs(self, repeat=False) -> Generator["ABDDNode", None, None]:
        stack: list[ABDDNode] = [self]
        visited = set()
        while stack != []:
            node = stack.pop()
            if not repeat and node in visited:
                continue
            yield node
            # we have to insert nodes in a reverse order
            visited.add(node)
            if type(node.high) == ABDDNode:
                stack.append(node.low)
            if type(node.high) == list:
                stack.extend(reversed(node.low))
            if type(node.low) == ABDDNode:
                stack.append(node.high)
            if type(node.low) == list:
                stack.extend(reversed(node.high))

    def find_terminal(self, target: int) -> Optional["ABDDNode"]:
        for i in self.explore_subtree_bfs():
            if i.is_leaf and i.leaf_val == target:
                return i
        return None
