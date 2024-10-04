"""
[file] bdd.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Module for implementing basic BDD operations.
[note] Needed in order to parse DIMACS format (read as DNF* for simplification).
"""

from typing import Optional, Union, List, Set, Dict, Tuple, Generator, Any
from bdd.bdd_node import BDDnode


class BDD:
    """
    Binary decision diagram. Sometimes referred to as ROBDD (reduced ordered BDD).

    Note: open for expansion (more attributes etc.)
    """

    def __init__(self, name: str, root: BDDnode):
        self.name: str = name
        self.root: BDDnode = root

    def __repr__(self):
        """
        List-like output format for a BDD
        """
        max_node_name_length: int = len("node")
        max_var_name_length: int = len("<var>")
        max_child_name_length: int = max(len("low"), len("high"))
        for i in self.iterate_dfs():
            max_node_name_length = max(len(str(i.name)) + 2, max_node_name_length)
            max_var_name_length = max(len(str(i.value)) + 2, max_var_name_length)
            max_child_name_length = max(len(str(i.value)), max_child_name_length)
            if i.is_leaf():
                max_child_name_length = max(len(f"<{i.value}>"), max_child_name_length)
        result: str = f"  [BDD]: '{self.name}'\n"
        result += f"  [root]: {self.root.name}\n"
        header_str: str = "  > %-*s - %-*s -> %-*s %-*s" % (
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
            ln: str = i.low.name if type(i.low.value) != int else f"[{i.low.value}]"
            hn: str = i.high.name if type(i.high.value) != int else f"[{i.high.value}]"
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

    def print_bdd(self) -> None:
        """
        Tree-like format of outputting/printing a BDD
        """

        def print_bdd_node(node: Optional[BDDnode], lvl: int, prefix: str) -> None:
            if node is None:
                return
            spaces: str = " " * 2 * lvl
            value: str = f"<{node.value}>"
            if type(node.value) == int:
                value = f"[{node.value}]"
            is_leaf: str = "LEAF" if node.low is None or node.high is None else ""
            print(f"{spaces}{prefix} {value} {node.name} {is_leaf}")
            prefix_low: str = ""  # f"[{node.name}-L->]"
            prefix_high: str = ""  # f"[{node.name}-H->]"
            print_bdd_node(node.low, lvl + 1, prefix_low)
            print_bdd_node(node.high, lvl + 1, prefix_high)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print(f"> BDD {self.name}")
        print_bdd_node(self.root, 0, "[root]")

    def iterate_bfs(self, allow_repeats=False) -> Generator[Any, Any, BDDnode]:
        """
        Breadth first traversal of BDD nodes (node generator)
        if allow_repeats=False: each node is only visited once (leaf nodes etc.)
        by having repeats on, the tree traversal may be more understandable
        """
        if self.root is None:
            return

        visited: Set[BDDnode] = set()
        queue: List[BDDnode] = [self.root]

        while len(queue) > 0:
            node: BDDnode = queue.pop(0)
            if node is None:
                continue
            if not allow_repeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            queue.append(node.low)
            queue.append(node.high)

    def iterate_dfs_recursive(self, allow_repeats=False) -> Generator[Any, Any, BDDnode]:
        """
        Depth first traversal of BDD nodes (node generator).
        See iterate_bfs() for explanation of allow_repeats.
        """

        def DFS(node: BDDnode, visited: Set[BDDnode], allow_repeats: bool) -> Generator[Any, Any, BDDnode]:
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
        visited: Set[BDDnode] = set()
        return DFS(self.root, visited, allow_repeats)

    def iterate_dfs(self, allow_repeats=False) -> Generator[Any, Any, BDDnode]:
        if self.root is None:
            return

        visited: Set[BDDnode] = set()
        stack: List[BDDnode] = [self.root]

        while len(stack) > 0:
            node: BDDnode = stack.pop()
            if node is None:
                continue

            if not allow_repeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            stack.append(node.high)
            stack.append(node.low)

    def get_variable_list(self) -> List[int | str]:
        def get_var(node: BDDnode, result: set) -> None:
            if node.is_leaf():
                return
            result.add(node.value)
            if node.low is not None:
                get_var(node.low, result)
            if node.high is not None:
                get_var(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result: Set[BDDnode] = set()
        get_var(self.root, result)
        result: List[BDDnode] = list(result)
        result.sort()  # NOTE: might need to be done wrt. a specified variable order
        return result

    def get_terminal_nodes_list(self) -> List[BDDnode]:
        def accumulate_terminal_nodes(node: Optional[BDDnode], result: List[BDDnode]) -> None:
            if node is None:
                return
            if node.is_leaf():
                result.append(node)
            accumulate_terminal_nodes(node.low, result)
            accumulate_terminal_nodes(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        node_accumulator = []
        accumulate_terminal_nodes(self.root, node_accumulator)
        return list(set(node_accumulator))

    def get_terminal_symbols_list(self) -> List[int | str]:
        def accumulate_terminal_symbols(node: BDDnode, result: set) -> None:
            if node is None:
                return
            if node.is_leaf():
                result.add(node.value)
            else:
                accumulate_terminal_symbols(node.low, result)
                accumulate_terminal_symbols(node.high, result)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        node_accumulator: Set[BDDnode] = set()
        accumulate_terminal_symbols(self.root, node_accumulator)
        return list(node_accumulator)

    def count_branches_iter(self, symbol: int | str) -> int:
        """
        DFS counting the number of paths leading to a specific symbol - usually
        a leaf. Used to count how many dimacs clausules is the BDD made of.
        """
        counter: int = 0

        if self.root is None:
            return

        # visited = set()
        stack: List[BDDnode] = [self.root]

        while len(stack) > 0:
            node: BDDnode = stack.pop()
            if node is None:
                continue

            if node.value == symbol:
                counter += 1

            stack.append(node.high)
            stack.append(node.low)

        return counter

    def count_nodes(self) -> int:
        counter: int = 0
        for _ in self.iterate_dfs():
            counter += 1
        return counter

    def reformat_nodes(self, prefix="n"):
        """
        Reformat node names using counting during a BFS-like traversal starting from 0.
        Node name prefix can be specified.
        """
        if self.root is None:
            return
        counter: int = 0
        visited: Set[BDDnode] = set()
        queue: List[BDDnode] = [self.root]

        while len(queue) > 0:
            node: BDDnode = queue.pop(0)
            if node is None:
                continue
            if node in visited:
                continue

            node.rename_node(f"{prefix}{counter}")
            counter += 1

            visited.add(node)
            if node.low is not None:
                queue.append(node.low)
            if node.high is not None:
                queue.append(node.high)

    def is_valid(self) -> bool:
        """
        Return true whether the BDD structure is okay (otherwise false). This means:
        - each node either has 2 child nodes (is an inner node) or 0 child nodes (is a leaf).
        - inner nodes have a consistent value type (either a string or an integer)
        - from root to leaf nodes, the node value (order of the variable) has a consistent order (is increasing).
        """

        def var_check(val1: Union[str, int], val2: Union[str, int]) -> bool:
            type_str: bool = type(val1) is int and type(val2) is int
            type_int: bool = type(val1) is str and type(val2) is str
            # short-circuit evaluation is utilized to check type consistency first:
            return (type_str or type_int) and val1 <= val2

        if self.root is None:
            return

        visited: Set[BDDnode] = set()
        stack: List[BDDnode] = [self.root]

        while len(stack) > 0:
            node: BDDnode = stack.pop()
            if node is None:
                continue
            if node in visited:
                continue
            visited.add(node)

            if node.high is not None and not node.high.is_leaf() and var_check(node.high.value, node.value):
                print("INVALID", node, node.high)
                return False
            if node.low is not None and not node.low.is_leaf() and var_check(node.low.value, node.value):
                print("INVALID", node, node.low)
                return False
            stack.append(node.high)
            stack.append(node.low)
        return True


def compare_bdds(bdd1: BDD, bdd2: BDD) -> bool:
    """
    Deep recursive check if two BDD structures are equal.
    Does not check names of the nodes, only values and overall structure.

    Note:
    This function does not account for BDDs that are isomorphic,
    but do not share the variable/node value ordering.
    """

    def compare_nodes(node1: Optional[BDDnode], node2: Optional[BDDnode]) -> bool:
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


# End of file bdd.py
