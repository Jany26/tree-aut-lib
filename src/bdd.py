# bdd.py
# Module for implementing basic BDD operations.
# Needed in order to parse DIMACS format (read as DNF* for simplification).
#
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from typing import Union


# One node of a binary decision diagram.
# - 'name'      - arbitrary name for a node (should be unique within a BDD)
# - 'value'     - variable (value) which symbolizes the node (e.g. 'x1')
#               - in case of leaves, the value is 0 or 1 (int)
# - 'parent'    - list of all parent nodes (root node has empty parent list)
# - 'low'       - points to a low descendant node (symbolizes 'False' branch)
# - 'high'      - points to a high descendant node (symbolizes 'True' branch)
# (* leaf node has both low and high descendants None)
class BDDnode:

    def __init__(self, name, value, low=None, high=None):
        self.name: str = name
        self.value: Union[int, str] = value
        self.parent: list = []
        self.low: BDDnode = low
        self.high: BDDnode = high
        if low is not None and high is not None:
            self.attach(low, high)

    def __repr__(self):
        if self is None:
            return ""
        return f"({self.name}, {self.value})"

    def isRoot(self):
        if self is None:
            return False
        return True if self.parent is None else False

    def isLeaf(self):
        if (self is not None and self.low is None and self.high is None):
            return True
        return False

    def attach(self, lowNode=None, highNode=None):
        if self is None:
            return
        self.low = lowNode
        if lowNode is not None:
            lowNode.parent.append(self)
        self.high = highNode
        if highNode is not None:
            highNode.parent.append(self)

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
    def findNode(self, name):
        if self is None:
            return None
        if self.name == name:
            return self
        lowChild = self.findNode(self.low)
        if lowChild is not None:
            return lowChild
        highChild = self.findNode(self.high)
        if highChild is not None:
            return highChild
        return None

    # may be obsolete => originally used in iterateBFS()
    def getNodesFromLevel(self, level: int) -> list:
        def getNodesFromLevelHelper(node, level, result):
            if self is None:
                return
            if level == 1:
                result.append(node)
            elif level > 1:
                getNodesFromLevelHelper(node.low, level - 1, result)
                getNodesFromLevelHelper(node.high, level - 1, result)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = []
        getNodesFromLevelHelper(self, level, result)
        return result


# Binary decision diagram. open for expansion (more attributes etc.)
class BDD:
    def __init__(self, name: str, root: BDDnode):
        self.name = name
        self.root = root

    # List-like output format for a BDD
    def __repr__(self):
        result = f"BDD '{self.name}'\n"
        for i in self.iterateDFS(allowRepeats=False):
            nodeVal = f"<{i.value }>"
            if type(i.value) == int:
                nodeVal = f"[{i.value}]"
            nodeName = f"\"{i.name}\""
            if i.isLeaf():
                nodeVal = f"[{i.value}]"
            lowName = i.low.value if i.low is not None else "_"
            highName = i.high.value if i.high is not None else "_"
            result += f"{nodeVal} {nodeName} -> ({lowName}, {highName})\n"
        return result

    # Tree-like format of outputting/printing a BDD
    def printBDD(self):
        def printBDDNode(node: BDDnode, lvl: int, prefix: str):
            if node is None:
                return
            spaces = " " * 2 * lvl
            value = f"<{node.value}>"
            if type(node.value) == int:
                value = f"[{node.value}]"
            isLeaf = "LEAF" if node.low is None or node.high is None else ""
            print(f"{spaces}{prefix} {value} {node.name} {isLeaf}")
            newPrefixLow = ""  # f"[{node.name}-L->]"
            newPrefixHigh = ""  # f"[{node.name}-H->]"
            printBDDNode(node.low, lvl + 1, newPrefixLow)
            printBDDNode(node.high, lvl + 1, newPrefixHigh)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print(f"> BDD {self.name}")
        printBDDNode(self.root, 0, "[root]")

    # Breadth first traversal of BDD nodes (iterator)
    # if allowRepeats=False: each node is only visited once (leaf nodes etc.)
    # by having repeats on, the tree traversal may be more understandable
    def iterateBFS(self, allowRepeats=False):
        if self.root is None:
            return

        visited = set()
        queue = [self.root]

        while len(queue) > 0:
            node = queue.pop(0)
            if node is None:
                continue
            if not allowRepeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            queue.append(node.low)
            queue.append(node.high)

    # Depth first traversal of BDD nodes (iterator)
    # see iterateBFS() for explanation of allowRepeats
    def iterateDFSrecurisve(self, allowRepeats=False):
        def DFS(node, visited, allowRepeats):
            if not allowRepeats:
                if node in visited:
                    return
                visited.add(node)

            yield node

            if node.low is not None:
                yield from DFS(node.low, visited, allowRepeats)

            if node.high is not None:
                yield from DFS(node.high, visited, allowRepeats)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        visited = set()
        return DFS(self.root, visited, allowRepeats)

    def iterateDFS(self, allowRepeats=False):
        if self.root is None:
            return

        visited = set()
        stack = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                continue

            if not allowRepeats:
                if node in visited:
                    continue
                visited.add(node)

            yield node
            stack.append(node.high)
            stack.append(node.low)

    def getVariableList(self) -> list:
        def getVar(node: BDDnode, result: list):
            if node.isLeaf():
                return
            result.append(node.value)
            if node.low is not None:
                getVar(node.low, result)
            if node.high is not None:
                getVar(node.high, result)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = []
        getVar(self.root, result)
        result = list(set(result))
        result.sort()
        return result

    def getTerminalNodesList(self) -> 'list[BDDnode]':
        def getTerminalNode(node: BDDnode, result: list):
            if node is None:
                return
            if node.isLeaf():
                result.append(node)
            getTerminalNode(node.low, result)
            getTerminalNode(node.high, result)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = []
        return getTerminalNode(self.root, result)

    def getTerminalSymbolsList(self) -> list:
        def getTerminal(node: BDDnode, result: set):
            if node is None:
                return
            if node.isLeaf():
                result.add(node.value)
            else:
                getTerminal(node.low, result)
                getTerminal(node.high, result)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = set()
        getTerminal(self.root, result)
        return list(result)

    # DFS counting the number of paths leading to a specific symbol - usually
    # a leaf. Used to count how many dimacs clausules is the BDD made of.
    def countBranchesIter(self, symbol) -> int:
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


# Deep recursive check if two BDD structures are equal.
# Does not check names of the nodes, only values and overall structure.
def compareBDDs(bdd1: BDD, bdd2: BDD) -> bool:
    def compareNodes(node1: BDDnode, node2: BDDnode) -> bool:
        if (node1 is None) != (node2 is None):
            return False
        if node1 is None and node2 is None:
            return True
        if (
            # node1.name != node2.name  # node names do not have to match
            node1.value != node2.value
            or compareNodes(node1.low, node2.low) is False
            or compareNodes(node1.high, node2.high) is False
        ):
            return False
        return True
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    return compareNodes(bdd1.root, bdd2.root)

# End of file bdd.py
