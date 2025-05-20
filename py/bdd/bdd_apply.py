"""
[file] bdd_apply.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Module for implementing apply operation of two BDDs.
[note] Needed in order to parse DIMACS format and for creating BDDs
for further testing/experimenting with tree automata.
"""

from typing import Set, List, Dict, Tuple, Union

from bdd.bdd_class import BDD
from bdd.bdd_node import BDDnode

from helpers.string_manipulation import state_name_sort


def create_var_order_for_apply(variables: list[str], terminals: List[str | int]) -> Dict[Union[str, int], int]:
    """
    Makes the list of (ordered) variables into a dictionary for easy lookup (variable -> idx) of indexing.
    """
    if variables is not None:
        variables: List[str] = state_name_sort(variables)
    result: Dict[str | int, int] = {}
    idx: int = 1
    for var in variables:
        if var not in result:
            result[var] = idx
            idx += 1
    # for t in terminals:
    #     result[str(t)] = i
    return result


class ApplyHelper:
    """
    This class is for saving and accessing data important for apply function across recursive calls.
    Since there is more information needed, a structured data type (this class) is used for lookup and caching.
    - `count` = node counter, for unique node names
    - `cache` = cache allows us to lookup nodes based on the data about them,
    it makes sure that there are no two same nodes in the BDD, thus satisfying the BDD reduction rule
    - `terminals` = list of terminal symbols (most likely obsolete), maybe usable in case of MTBDDs ???
    - `vars` = variable lookup table = each variable is indexed,
    the indices then create a variable order based on the initial boolean function
    - `spacing` = for pretty printing (debug purposes), not a functionally necessary attribute
    """

    def __init__(self, bdd1: BDD, bdd2: BDD, vars):
        self.count: int = 0
        self.cache: Dict[str, BDDnode] = {}
        _temp: List[int | str] = bdd1.get_terminal_symbols_list()
        _temp.extend(bdd2.get_terminal_symbols_list())
        self.terminals: List[int | str] = list(set(_temp))
        self.vars: Dict[str | int, int] = vars
        self.spacing: int = 0
        if vars is None or type(vars) == list:
            if vars is None:
                _temp2 = bdd1.get_variable_list()
                _temp2.extend(bdd2.get_variable_list())
            self.vars = create_var_order_for_apply(_temp2, self.terminals)

    # for debugging purposes
    def __repr__(self):
        repr: str = "Apply Helper info:\n"
        repr += f"count = {self.count}\n"
        repr += f"terminals = {self.terminals}\n"
        repr += f"variables = {self.vars}\n"
        repr += f"cache = {self.cache}"
        return repr


def apply_function(func: str, bdd1: BDD, bdd2: BDD, var_order=None) -> BDD:
    """
    Creates a new BDD by applying (recursively) some logic function `func` on two BDDs.

    Example: If the function is logical 'and', the resulting BDD should
    evaluate to true iff both inputs are evaluated to true.
    """

    class ApplyCase:
        """
        Case a): both BDD nodes are leaves
        Case b): BDD node 1 is leaf, BDD node 2 is inner
        Case c): BDD node 1 is inner, BDD node 2 is leaf
        Case d): both BDD nodes are inner nodes
        """

        a: bool = False
        b: bool = False
        c: bool = False
        d: bool = False

        def __init__(self, case):
            self.__setattr__(case, True)

    def decide_case(node1: BDDnode, node2: BDDnode, data: ApplyHelper) -> ApplyCase:
        """
        Decides which "apply" case should be recursively happening from a certain point
        based on node1 and node2 properties.
        """
        if node1.is_leaf() and node2.is_leaf():
            return ApplyCase("a")
        if not node1.is_leaf() and node2.is_leaf():
            return ApplyCase("c")
        if node1.is_leaf() and not node2.is_leaf():
            return ApplyCase("b")
        if data.vars[str(node1.value)] > data.vars[str(node2.value)]:
            return ApplyCase("b")
        if data.vars[str(node1.value)] < data.vars[str(node2.value)]:
            return ApplyCase("c")
        return ApplyCase("d")

    def apply_from(func: str, node1: BDDnode, node2: BDDnode, data: ApplyHelper) -> BDDnode:
        """
        Recursive apply function on two BDD structures.
        Uses memoization (caching) to unify nodes representing the same Boolean functions.
        """
        current_case: ApplyCase = decide_case(node1, node2, data)
        data.spacing += 2
        name: str

        # scenario A - both are leaves
        if current_case.a:
            terminal: int = leaf_apply_op(func, node1, node2)
            name = f"t{terminal}"
            if name in data.cache:
                data.spacing -= 2
                return data.cache[name]
            result = BDDnode(name, terminal)
            data.cache[name] = result
            data.spacing -= 2
            return result

        # otherwise (at least one is not leaf) ...
        node1val = f"[{node1.value}]" if node1.is_leaf() else f"v{node1.value}"
        node2val = f"[{node2.value}]" if node2.is_leaf() else f"v{node2.value}"
        low: BDDnode = None
        high: BDDnode = None
        value = None

        # scenario B - node1 lower than node2
        if current_case.b:
            low = apply_from(func, node1, node2.low, data)
            high = apply_from(func, node1, node2.high, data)
            value = node2.value

        # scenario C - node1 higher than node2
        if current_case.c:
            low = apply_from(func, node1.low, node2, data)
            high = apply_from(func, node1.high, node2, data)
            value = node1.value

        # scenario D - node1 same level as node2 (but non-leaves)
        if current_case.d:
            low = apply_from(func, node1.low, node2.low, data)
            high = apply_from(func, node1.high, node2.high, data)
            value = node1.value

        lookup = f"{value},{low.name},{high.name}"
        # in case both subtrees are isomorphic...
        if low.name == high.name and low.value == high.value:
            name = low.name
            data.cache[lookup] = low
            data.spacing -= 2
            return low

        if lookup in data.cache:
            data.spacing -= 2
            return data.cache[lookup]

        name = f"n{data.count}"
        data.count += 1
        result = BDDnode(name, value)
        result.attach(low, high)
        data.cache[lookup] = result
        data.spacing -= 2
        return result

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if bdd1.root is None and bdd2.root is None:
        return BDD(None, None)
    if bdd1.root is None:
        return BDD(None, bdd2.root)
    if bdd2.root is None:
        return BDD(None, bdd1.root)
    data = ApplyHelper(bdd1, bdd2, var_order)
    new_root = apply_from(func, bdd1.root, bdd2.root, data)

    return BDD("BDD", new_root)


def leaf_apply_op(operator: str, bdd1: BDDnode, bdd2: BDDnode) -> int:
    """
    Wrapper for boolean functions
    """

    def or_operator(val1: int, val2: int):
        return val1 or val2

    def and_operator(val1: int, val2: int):
        return val1 and val2

    def xor_operator(val1: int, val2: int):
        return val1 ^ val2

    def nand_operator(val1: int, val2: int):
        return not (val1 and val2)

    def nor_operator(val1: int, val2: int):
        return not (val1 or val2)

    lookup = {
        "or": or_operator,
        "and": and_operator,
        "xor": xor_operator,
        "nor": nor_operator,
        "nand": nand_operator,
    }
    func: function = lookup[str(operator)]
    result: int = func(bdd1.value, bdd2.value)  # terminal nodes have int values
    return result


# End of file bdd_apply.py
