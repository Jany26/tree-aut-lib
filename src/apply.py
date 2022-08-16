from bdd import *


# makes the list into a dictionary for easy lookup of indexing
def createVarOrder(variables: list, terminals: list, sorted=True) -> dict:
    if not sorted and variables is not None:
        variables.sort()
    result = {}
    i = 1
    for var in variables:
        if var not in result:
            result[var] = i
            i += 1
    for t in terminals:
        result[str(t)] = i
    return result


class ApplyHelper:
    def __init__(self, bdd1: BDD, bdd2: BDD, vars):
        self.count: int = 0  # node counter = for unique node names
        self.cache: 'dict[str, BDDnode]' = {}
        self.terminals = bdd1.getTerminalSymbolsList()
        self.terminals.extend(bdd2.getTerminalSymbolsList())
        self.terminals = list(set(self.terminals))
        self.vars: dict = vars
        if vars is None or type(vars) == list:
            if vars is None:
                temp = bdd1.getVariableList()
                temp.extend(bdd2.getVariableList())
            self.vars = createVarOrder(temp, self.terminals, sorted=False)

    def __repr__(self):
        str = "Apply Helper info:\n"
        str += f"count = {self.count}\n"
        str += f"terminals = {self.terminals}\n"
        str += f"variables = {self.vars}\n"
        str += f"cache = {self.cache}"
        return str


# Creates a new BDD by applying some logic function on two BDDs.
def applyFunction(func: str, bdd1: BDD, bdd2: BDD, varOrder=None) -> BDD:

    data = ApplyHelper(bdd1, bdd2, varOrder)

    def applyFrom(func: str, node1: BDDnode, node2: BDDnode,
                  data: ApplyHelper) -> BDDnode:
        if node1.isLeaf() and node2.isLeaf():
            # scenario A
            # print(f"A: {node1} leaf and {node2} leaf")
            terminal = leafApplyOp(func, node1, node2)
            name = f"t{terminal}"
            if name in data.cache:
                return data.cache[name]
            result = BDDnode(name, terminal)
            data.cache[name] = result
            return result
        else:
            low: BDDnode = None
            high: BDDnode = None
            value = None
            if (
                (node1.isLeaf() and not node2.isLeaf())
                or (data.vars[str(node1.value)] > data.vars[str(node2.value)])
            ):
                # scenario D
                # print(f"D: {node1} lower than {node2}")
                low = applyFrom(func, node1, node2.low, data)
                high = applyFrom(func, node1, node2.high, data)
                value = node2.value
            elif (
                (not node1.isLeaf() and node2.isLeaf())
                or (data.vars[node2.value] > data.vars[node1.value])
            ):
                # scenario C
                # print(f"C: {node1} higher than {node2}")
                low = applyFrom(func, node1.low, node2, data)
                high = applyFrom(func, node1.high, node2, data)
                value = node1.value
            elif (
                (not node1.isLeaf() and not node2.isLeaf())
                and data.vars[node1.value] == data.vars[node2.value]
            ):
                # scenario B
                # print(f"B: {node1} same level as {node2}")
                low = applyFrom(func, node1.low, node2.low, data)
                high = applyFrom(func, node1.high, node2.high, data)
                value = node1.value

            lookup = f"{value},{low.name},{high.name}"
            # in case both subtrees are isomorphic...
            if low.name == high.name and low.value == high.value:
                name = low.name
                data.cache[lookup] = low
                return low
            if lookup in data.cache:
                print(f" > lookup of {lookup}")
                return data.cache[lookup]
            name = f"n{data.count}"
            data.count += 1
            result = BDDnode(name, value)
            result.attach(low, high)
            data.cache[lookup] = result
            return result

    newRoot = applyFrom(func, bdd1.root, bdd2.root, data)
    print(data)
    return BDD("BDD", newRoot)


def leafApplyOp(operator, bdd1, bdd2) -> int:
    def orOperator(val1, val2):
        print(f"  >> {val1} or {val2} = {val1 or val2}")
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
