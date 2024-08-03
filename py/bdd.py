"""
[file] bdd.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Module for implementing basic BDD operations.
[note] Needed in order to parse DIMACS format (read as DNF* for simplification).
"""

# from __future__ import annotations
from typing import Union

from ta_classes import TTreeAut, TTransition, TEdge, iterate_edges
from unfolding import is_unfolded
import copy


# One node of a binary decision diagram.
# - 'name'      - arbitrary name for a node (should be unique within a BDD)
# - 'value'     - variable (value) which symbolizes the node (e.g. 'x1')
#               - in case of leaves, the value is 0 or 1 (int)
# - 'parents'    - list of all parent nodes (root node has empty parents list)
# - 'low'       - points to a low descendant node (symbolizes 'False' branch)
# - 'high'      - points to a high descendant node (symbolizes 'True' branch)
# (* leaf node has both low and high descendants None)
class BDDnode:

    def __init__(self, name, value, low=None, high=None):
        self.name: str = name
        self.value: Union[int, str] = value
        self.parents: list = []
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

    def attach(self, low_node=None, high_node=None):
        if self is None:
            return
        self.low = low_node
        if low_node is not None:
            low_node.parents.append(self)
        self.high = high_node
        if high_node is not None:
            high_node.parents.append(self)

    def rename_node(self, new_name):
        if self is None:
            return
        old_name = self.name
        self.name = new_name
        if not self.is_leaf():
            try:
                self.low.parents.remove(old_name)
                self.high.parents.remove(old_name)
            except:
                pass
            self.low.parents.append(new_name)
            self.high.parents.append(new_name)

    # calculates height of the node (distance from leaves)
    def height(self) -> int:
        if self is None:
            return 0

        lh = self.low.height() if self.low is not None else 0
        rh = self.high.height() if self.high is not None else 0

        if lh > rh:
            return rh + 1
        else:
            return lh + 1

    # Searches recursively down from this node for a node with a certain name.
    # If not found, returns None, otherwise returns BDDnode.
    def find_node(self, name):
        if self is None:
            return None
        if self.name == name:
            return self
        low_child = self.find_node(self.low)
        if low_child is not None:
            return low_child
        high_child = self.find_node(self.high)
        if high_child is not None:
            return high_child
        return None

    # may be obsolete => originally used in iterate_bfs()
    def get_nodes_from_level(self, level: int) -> list:
        def get_nodes_from_level_helper(node, level, result):
            if self is None:
                return
            if level == 1:
                result.append(node)
            elif level > 1:
                get_nodes_from_level_helper(node.low, level - 1, result)
                get_nodes_from_level_helper(node.high, level - 1, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = []
        get_nodes_from_level_helper(self, level, result)
        return result


# Binary decision diagram. open for expansion (more attributes etc.)
class BDD:
    def __init__(self, name: str, root: BDDnode):
        self.name = name
        self.root = root

    # List-like output format for a BDD
    def __repr__(self):
        max_node_name_length = len("node")
        max_var_name_length = len("<var>")
        max_child_name_length = max(len("low"), len("high"))
        for i in self.iterate_dfs():
            max_node_name_length = max(len(str(i.name)) + 2, max_node_name_length)
            max_var_name_length = max(len(str(i.value)) + 2, max_var_name_length)
            max_child_name_length = max(len(str(i.value)), max_child_name_length)
            if i.is_leaf():
                max_child_name_length = max(len(f"<{i.value}>"), max_child_name_length)
        result = f"  [BDD]: '{self.name}'\n"
        result += f"  [root]: {self.root.name}\n"
        header_str = "  > %-*s - %-*s -> %-*s %-*s" % (
            max_node_name_length,
            "node",
            max_var_name_length,
            "<var>",
            max_child_name_length,
            "low",
            max_child_name_length,
            "high",
        )
        result += header_str + "\n"
        result += "  " + "-" * (len(header_str) - 2) + "\n"

        for i in self.iterate_bfs():
            if i.is_leaf():
                continue
            ln = i.low.name if type(i.low.value) != int else f"[{i.low.value}]"
            hn = i.high.name if type(i.high.value) != int else f"[{i.high.value}]"
            result += "  > %-*s - %-*s -> %-*s %-*s\n" % (
                max_node_name_length,
                i.name,
                max_var_name_length,
                f"<{i.value}>",
                max_child_name_length,
                ln,
                max_child_name_length,
                hn,
            )
        return result

    # Tree-like format of outputting/printing a BDD
    def print_bdd(self):
        def print_bdd_node(node: BDDnode, lvl: int, prefix: str):
            if node is None:
                return
            spaces = " " * 2 * lvl
            value = f"<{node.value}>"
            if type(node.value) == int:
                value = f"[{node.value}]"
            is_leaf = "LEAF" if node.low is None or node.high is None else ""
            print(f"{spaces}{prefix} {value} {node.name} {is_leaf}")
            prefix_low = ""  # f"[{node.name}-L->]"
            prefix_high = ""  # f"[{node.name}-H->]"
            print_bdd_node(node.low, lvl + 1, prefix_low)
            print_bdd_node(node.high, lvl + 1, prefix_high)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print(f"> BDD {self.name}")
        print_bdd_node(self.root, 0, "[root]")

    # Breadth first traversal of BDD nodes (iterator)
    # if allow_repeats=False: each node is only visited once (leaf nodes etc.)
    # by having repeats on, the tree traversal may be more understandable
    def iterate_bfs(self, allow_repeats=False):
        if self.root is None:
            return

        visited = set()
        queue = [self.root]

        while len(queue) > 0:
            node = queue.pop(0)
            if node is None:
                continue
            if not allow_repeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            queue.append(node.low)
            queue.append(node.high)

    # Depth first traversal of BDD nodes (iterator)
    # see iterate_bfs() for explanation of allow_repeats
    def iterate_dfs_recursive(self, allow_repeats=False):
        def DFS(node, visited, allow_repeats):
            if not allow_repeats:
                if node in visited:
                    return
                visited.add(node)

            yield node

            if node.low is not None:
                yield from DFS(node.low, visited, allow_repeats)

            if node.high is not None:
                yield from DFS(node.high, visited, allow_repeats)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        visited = set()
        return DFS(self.root, visited, allow_repeats)

    def iterate_dfs(self, allow_repeats=False):
        if self.root is None:
            return

        visited = set()
        stack = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                continue

            if not allow_repeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            stack.append(node.high)
            stack.append(node.low)

    def get_variable_list(self) -> list:
        def get_var(node: BDDnode, result: set):
            if node.is_leaf():
                return
            result.add(node.value)
            if node.low is not None:
                get_var(node.low, result)
            if node.high is not None:
                get_var(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = set()
        get_var(self.root, result)
        result = list(result)
        result.sort()
        return result

    def get_terminal_nodes_list(self) -> "list[BDDnode]":
        def get_terminal_node(node: BDDnode, result: list):
            if node is None:
                return
            if node.is_leaf():
                result.append(node)
            get_terminal_node(node.low, result)
            get_terminal_node(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = []
        return get_terminal_node(self.root, result)

    def get_terminal_symbols_list(self) -> list:
        def get_terminal(node: BDDnode, result: set):
            if node is None:
                return
            if node.is_leaf():
                result.add(node.value)
            else:
                get_terminal(node.low, result)
                get_terminal(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = set()
        get_terminal(self.root, result)
        return list(result)

    # DFS counting the number of paths leading to a specific symbol - usually
    # a leaf. Used to count how many dimacs clausules is the BDD made of.
    def count_branches_iter(self, symbol) -> int:
        counter = 0

        if self.root is None:
            return

        # visited = set()
        stack = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                continue

            if node.value == symbol:
                counter += 1

            stack.append(node.high)
            stack.append(node.low)

        return counter

    def count_nodes(self) -> int:
        counter = 0
        for node in self.iterate_dfs():
            counter += 1
        return counter

    def reformat_nodes(self, prefix="n"):
        if self.root is None:
            return
        cnt = 0
        visited = set()
        queue = [self.root]

        while len(queue) > 0:
            node = queue.pop(0)
            if node is None:
                continue
            if node in visited:
                continue

            node.rename_node(f"{prefix}{cnt}")
            cnt += 1

            visited.add(node)
            if node.low is not None:
                queue.append(node.low)
            if node.high is not None:
                queue.append(node.high)

    def is_valid(self) -> bool:
        if self.root is None:
            return

        visited = set()
        stack = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                continue
            if node in visited:
                continue
            visited.add(node)

            if node.high is not None and not node.high.is_leaf() and int(node.high.value) <= int(node.value):
                print("INVALID", node, node.high)
                return False
            if node.low is not None and not node.low.is_leaf() and int(node.low.value) <= int(node.value):
                print("INVALID", node, node.low)
                return False
            stack.append(node.high)
            stack.append(node.low)
        return True


# Deep recursive check if two BDD structures are equal.
# Does not check names of the nodes, only values and overall structure.
def compare_bdds(bdd1: BDD, bdd2: BDD) -> bool:
    def compare_nodes(node1: BDDnode, node2: BDDnode) -> bool:
        if (node1 is None) != (node2 is None):
            return False
        if node1 is None and node2 is None:
            return True
        if (
            # node1.name != node2.name  # node names do not have to match
            node1.value != node2.value
            or compare_nodes(node1.low, node2.low) is False
            or compare_nodes(node1.high, node2.high) is False
        ):
            return False
        return True

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    return compare_nodes(bdd1.root, bdd2.root)


# WIP ...
# unfolding self-loops and partial-loops is needed.
# def create_bdd_from_tree_aut(ta: TTreeAut) -> BDD:
#     if not is_unfolded(ta):
#         raise Exception('create_bdd_from_ta(): folded input')
#     if len(ta.roots) != 1:
#         raise Exception('create_bdd_from_ta(): more than 1 root state')

#     root = BDDnode(ta.roots[0], ta.transitions[ta.roots])

#     visited = set()
#     stack = [ta.roots[0]]

#     while len(stack) > 0:
#         node = stack.pop()
#         if node is None:
#             continue

#         if node in visited:
#             continue
#         visited.add(node)

#         yield node
#         stack.append(node.high)
#         stack.append(node.low)


# Convert a BDD to a tree automaton.
def create_tree_aut_from_bdd(bdd: BDD) -> TTreeAut:
    roots = [bdd.root.name]
    transitions = {}
    key = 0
    for node in bdd.iterate_bfs():
        transitions[node.name] = {}
        edge = None
        children = []
        if node.is_leaf():
            edge = TEdge(str(node.value), [], "")
        else:
            edge = TEdge("LH", [], node.value)
            children = [node.low.name, node.high.name]
        new_transition = TTransition(node.name, edge, children)
        transitions[node.name][f"k{key}"] = new_transition

        key += 1
    result = TTreeAut(roots, transitions, bdd.name, 0)
    result.port_arity = result.get_port_arity()
    return result


def get_var_prefix(var_list: list) -> str:
    if var_list == []:
        return ""
    prefix_len = 0
    for i in range(len(var_list[0])):
        if not var_list[0][i:].isnumeric():
            prefix_len += 1
    prefix = var_list[0][:prefix_len]
    return prefix


# Parses the tree automaton (freshly after dimacs parsing) and adds X boxes
# to the places which make sense.
#   - case 1: when an edge skips some variables
#       * e.g. node deciding by x1 leads to x4 (as opposed to x2)
#   - case 2: when a node that does not contain last variable
#       leads straight to a leaf node
#       * e.g deciding by var x5, but there are 10 variables)
def add_dont_care_boxes(ta: TTreeAut, vars: int) -> TTreeAut:
    result = copy.deepcopy(ta)
    var_visibility = {i: int(list(j)[0]) for i, j in ta.get_var_visibility().items()}
    leaves = set(ta.get_output_states())
    counter = 0
    skipped_var_edges = []
    var_prefix = ta.get_var_prefix()
    for edge in iterate_edges(result):
        if edge.is_self_loop():
            continue
        for idx, child in enumerate(edge.children):
            if (
                child in leaves
                and var_visibility[edge.src] != vars
                or child not in leaves
                and var_visibility[child] - var_visibility[edge.src] >= 2
            ):
                if len(edge.info.box_array) < idx + 1:
                    edge.info.box_array = [None] * len(edge.children)
                edge.info.box_array[idx] = "X"
    for new_state, new_key, new_edge in skipped_var_edges:
        if new_state not in result.transitions:
            result.transitions[new_state] = {}
        if new_key not in result.transitions[new_state]:
            result.transitions[new_state][new_key] = new_edge

    return result


# End of file bdd.py
