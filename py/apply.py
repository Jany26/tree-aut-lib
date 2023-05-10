"""
[file] apply.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Module for implementing apply operation of two BDDs.
[note] Needed in order to parse DIMACS format and for creating BDDs
for further testing/experimenting with tree automata.
"""

from bdd import *
from utils import *

def createVarOrder(variables: list, terminals: list) -> dict:
    """
        Makes the list into a dictionary for easy lookup of indexing
    """
    if variables is not None:
        variables = stateNameSort(variables)
    result = {}
    i = 1
    for var in variables:
        if var not in result:
            result[var] = i
            i += 1
    # for t in terminals:
    #     result[str(t)] = i
    return result


# This class is for saving and accessing data important for apply function
# across recursive calls.
# Since there is more information needed, a structured data type (this class)
# is used for lookup and caching.
# - count = node counter, for unique node names
# - cache = cache allows us to lookup nodes based on the data about them,
#           it makes sure that there are no two same nodes in the BDD,
#           thus satisfying the BDD reduction rule
# - terminals = list of terminal symbols (most likely obsolete),
#               maybe usable in case of MTBDDs ???
# - vars = variable lookup table = each variable is indexed, the indices then
#          create a variable order based on the initial boolean function
class ApplyHelper:
    def __init__(self, bdd1: BDD, bdd2: BDD, vars):
        self.count: int = 0
        self.cache: 'dict[str, BDDnode]' = {}
        temp = bdd1.getTerminalSymbolsList()
        temp.extend(bdd2.getTerminalSymbolsList())
        self.terminals = list(set(temp))
        self.vars: dict = vars
        self.spacing = 0
        if vars is None or type(vars) == list:
            if vars is None:
                temp = bdd1.getVariableList()
                temp.extend(bdd2.getVariableList())
            self.vars = createVarOrder(temp, self.terminals)

    # for debugging purposes
    def __repr__(self):
        str = "Apply Helper info:\n"
        str += f"count = {self.count}\n"
        str += f"terminals = {self.terminals}\n"
        str += f"variables = {self.vars}\n"
        str += f"cache = {self.cache}"
        return str

# Creates a new BDD by applying some logic function on two BDDs.
def applyFunction(func: str, bdd1: BDD, bdd2: BDD, varOrder=None) -> BDD:

    class scenario:
        """
            scenario a: both trees are leaves
            scenario b: node1 is leaf, node2 is tree
            scenario c: node1 is tree, node2 is leaf
            scenario d: both trees are trees
        """
        a = False
        b = False
        c = False
        d = False
        def __init__(self, letter):
            self.__setattr__(letter, True)

    def decideScenario(node1:BDDnode, node2:BDDnode, data:ApplyHelper) -> scenario:
        """
        compares node1 node2 and decides according to which scenario
        should continue function apply     
        """
        if node1.isLeaf() and node2.isLeaf():
            return scenario("a")

        if not node1.isLeaf() and node2.isLeaf():
            return scenario("c")

        if node1.isLeaf() and not node2.isLeaf():
            return scenario("b")

        if data.vars[str(node1.value)] > data.vars[str(node2.value)]:
            return scenario("b")
        
        if data.vars[str(node1.value)] < data.vars[str(node2.value)]:
            return scenario("c")
        
        return scenario("d")


    def applyFrom(func: str, node1: BDDnode, node2: BDDnode,
                  data: ApplyHelper) -> BDDnode:
        currScenario = decideScenario(node1, node2, data)
        data.spacing += 2

        # scenario A - both are leaves
        if currScenario.a:
            terminal = leafApplyOp(func, node1, node2)
            # print(f"{data.spacing * ' '}[{node1.value}] {func} [{node2.value}] = {terminal}")
            name = f"t{terminal}"
            if name in data.cache:
                data.spacing -= 2
                return data.cache[name]
            result = BDDnode(name, terminal)
            data.cache[name] = result
            data.spacing -= 2
            return result
        
        # otherwise (at least one is not leaf) ...
        node1val = f"[{node1.value}]" if node1.isLeaf() else f"v{node1.value}"
        node2val = f"[{node2.value}]" if node2.isLeaf() else f"v{node2.value}"
        # print(f"{data.spacing * ' '}{node1val}, {node2val}")
        low: BDDnode = None
        high: BDDnode = None
        value = None

        # scenario B - node1 lower than node2
        if currScenario.b:
            # print(f"  > descend RIGHT [{node1.value} > {node2.value}]")
            low = applyFrom(func, node1, node2.low, data)
            high = applyFrom(func, node1, node2.high, data)
            value = node2.value
        
        # scenario C - node1 higher than node2
        if currScenario.c:
            # print(f"  > descend LEFT [{node1.value} < {node2.value}]")
            low = applyFrom(func, node1.low, node2, data)
            high = applyFrom(func, node1.high, node2, data)
            value = node1.value
        
        # scenario D - node1 same level as node2 (but non-leaves)
        if currScenario.d:
            # print(f"  > same level")
            low = applyFrom(func, node1.low, node2.low, data)
            high = applyFrom(func, node1.high, node2.high, data)
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
    data = ApplyHelper(bdd1, bdd2, varOrder)
    # print(data.vars)
    newRoot = applyFrom(func, bdd1.root, bdd2.root, data)


    return BDD("BDD", newRoot)


# "Wrapper" for boolean functions
def leafApplyOp(operator, bdd1, bdd2) -> int:
    def orOperator(val1, val2):
        return val1 or val2

    def andOperator(val1, val2):
        return val1 and val2

    def xorOperator(val1, val2):
        return val1 ^ val2

    def nandOperator(val1, val2):
        return not (val1 and val2)

    def norOperator(val1, val2):
        return not (val1 or val2)

    lookup = {
        'or': orOperator,
        'and': andOperator,
        'xor': xorOperator,
        'nor': norOperator,
        'nand': nandOperator,
    }
    func = lookup[str(operator)]
    result = func(bdd1.value, bdd2.value)
    return result

# End of file apply.py
