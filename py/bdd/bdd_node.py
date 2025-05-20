"""
[file] bdd_node.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Class encapsulating one node of a BDD.
[note] Needed in order to parse DIMACS format and for creating BDDs
for further testing/experimenting with tree automata.
"""

from typing import List, Dict, Set, Optional


class BDDnode:
    """
    One node of a binary decision diagram.
    - 'name'      - arbitrary name for a node (should be unique within a BDD)
    - 'value'     - variable (value) which symbolizes the node (e.g. 'x1')
                  - in case of leaves, the value is 0 or 1 (int)
    - 'parents'   - list of all parent nodes (root node has empty parents list)
    - 'low'       - points to a low descendant node (symbolizes 'False' branch)
    - 'high'      - points to a high descendant node (symbolizes 'True' branch)
    (* leaf node has both low and high descendants None)
    """

    def __init__(self, name: str, value: int | str, low=None, high=None):
        self.name: str = name
        self.value: int | str = value
        self.parents: List[BDDnode] = []
        self.low: BDDnode = low
        self.high: BDDnode = high
        if low is not None and high is not None:
            self.attach(low, high)

    def __repr__(self):
        if self is None:
            return ""
        if self.is_leaf():
            if self.value == 0:
                return f"({self.name}, [0])"
            else:
                return f"({self.name}, [1])"
        return f"({self.name}, {self.value})"

    def is_root(self):
        if self is None:
            return False
        return self.parents is None

    def is_leaf(self):
        if self is not None and (self.low is None or self.high is None):
            return True
        return False

    def attach(self, low_node: Optional["BDDnode"] = None, high_node: Optional["BDDnode"] = None):
        if self is None:
            return
        self.low = low_node
        if low_node is not None:
            low_node.parents.append(self)
        self.high = high_node
        if high_node is not None:
            high_node.parents.append(self)

    def rename_node(self, new_name: str):
        if self is None:
            return
        old_name: str = self.name
        self.name = new_name
        if not self.is_leaf():
            try:
                self.low.parents.remove(old_name)
                self.high.parents.remove(old_name)
            except:
                pass
            self.low.parents.append(new_name)
            self.high.parents.append(new_name)

    def height(self) -> int:
        """
        Calculate the height of the node (distance from leaves).
        """
        if self is None:
            return 0

        lh: int = 0 if self.low is None else self.low.height()
        rh: int = 0 if self.high is None else self.high.height()

        if lh > rh:
            return rh + 1
        else:
            return lh + 1

    def find_node(self, name: str) -> Optional[str]:
        """
        Searches recursively down from this node for a node with a certain name.
        If not found, returns None, otherwise returns BDDnode.
        """
        if self is None:
            return None
        if self.name == name:
            return self
        low_child: str = self.find_node(self.low)
        if low_child is not None:
            return low_child
        high_child: str = self.find_node(self.high)
        if high_child is not None:
            return high_child
        return None

    def get_nodes_from_level(self, level: int) -> List["BDDnode"]:
        """
        Recursively search for all nodes of a specific level (depth) and return a list of such nodes.

        Note: may be obsolete => originally used in iterate_bfs()
        """

        def get_nodes_from_level_helper(node: BDDnode, level: int, result: List[BDDnode]):
            if self is None:
                return
            if level == 1:
                result.append(node)
            elif level > 1:
                get_nodes_from_level_helper(node.low, level - 1, result)
                get_nodes_from_level_helper(node.high, level - 1, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result: List[BDDnode] = []
        get_nodes_from_level_helper(self, level, result)
        return result
