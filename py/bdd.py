# bdd.py
# Module for implementing basic BDD operations.
# Needed in order to parse DIMACS format (read as DNF* for simplification).
#
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from typing import Union

from ta_classes import *
from unfolding import isUnfolded


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
        if self.isLeaf():
            if self.value == 0:
                return f"({self.name}, [0])"
            else:
                return f"({self.name}, [1])"
        return f"({self.name}, {self.value})"

    def isRoot(self):
        if self is None:
            return False
        return True if self.parents is None else False

    def isLeaf(self):
        if (self is not None and (self.low is None or self.high is None)):
            return True
        return False

    def attach(self, lowNode=None, highNode=None):
        if self is None:
            return
        self.low = lowNode
        if lowNode is not None:
            lowNode.parents.append(self)
        self.high = highNode
        if highNode is not None:
            highNode.parents.append(self)

    def renameNode(self, newName):
        if self is None:
            return
        oldName = self.name
        self.name = newName
        if not self.isLeaf():
            try:
                self.low.parents.remove(oldName)
                self.high.parents.remove(oldName)
            except:
                pass
            self.low.parents.append(newName)
            self.high.parents.append(newName)

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
        nLen = len("node")  # max Node length
        vLen = len("<var>")  # max Variable length
        cLen = max(len('low'), len('high'))  # max Child length
        for i in self.iterateDFS():
            nLen = max(len(str(i.name)) + 2, nLen)
            vLen = max(len(str(i.value)) + 2, vLen)
            cLen = max(len(str(i.value)), cLen)
            if i.isLeaf():
                cLen = max(len(f"<{i.value}>"), cLen)
        result = f"  [BDD]: '{self.name}'\n"
        result += f"  [root]: {self.root.name}\n"
        headerString = "  > %-*s - %-*s -> %-*s %-*s" % (
            nLen, 'node', vLen, '<var>', cLen, 'low', cLen, 'high'
        )
        result += headerString + '\n'
        result += '  ' + '-' * (len(headerString) - 2) + '\n'

        for i in self.iterateBFS():
            if i.isLeaf():
                continue
            ln = i.low.name if type(i.low.value) != int else f"[{i.low.value}]"
            hn = i.high.name if type(i.high.value) != int else f"[{i.high.value}]"
            result += "  > %-*s - %-*s -> %-*s %-*s\n" % (
                nLen, i.name, vLen, f"<{i.value}>", cLen, ln, cLen, hn
            )
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
        def getVar(node: BDDnode, result: set):
            if node.isLeaf():
                return
            result.add(node.value)
            if node.low is not None:
                getVar(node.low, result)
            if node.high is not None:
                getVar(node.high, result)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        result = set()
        getVar(self.root, result)
        result = list(result)
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

    def countNodes(self) -> int:
        counter = 0
        for node in self.iterateDFS():
            counter += 1
        return counter

    def reformatNodes(self, prefix='n'):
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

            node.renameNode(f"{prefix}{cnt}")
            cnt += 1

            visited.add(node)
            if node.low is not None:
                queue.append(node.low)
            if node.high is not None:
                queue.append(node.high)

    def isValid(self) -> bool:
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

            if node.high is not None and not node.high.isLeaf() and int(node.high.value) <= int(node.value):
                print("INVALID", node, node.high)
                return False
            if node.low is not None and not node.low.isLeaf() and int(node.low.value) <= int(node.value):
                print("INVALID", node, node.low)
                return False
            stack.append(node.high)
            stack.append(node.low)
        return True


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


# WIP ...
# unfolding self-loops and partial-loops is needed.
def createBDDfromTA(ta: TTreeAut) -> BDD:
    if not isUnfolded(ta):
        raise Exception('convertTAtoBDD(): folded input')
    if len(ta.rootStates) != 1:
        raise Exception('convertTAtoBDD(): more than 1 root state')

    root = BDDnode(ta.rootStates[0], ta.transitions[ta.rootStates])

    visited = set()
    stack = [ta.rootStates[0]]

    while len(stack) > 0:
        node = stack.pop()
        if node is None:
            continue

        if node in visited:
            continue
        visited.add(node)

        yield node
        stack.append(node.high)
        stack.append(node.low)


# Convert a BDD to a tree automaton.
def createTAfromBDD(bdd: BDD) -> TTreeAut:
    roots = [bdd.root.name]
    transitions = {}
    key = 0
    for node in bdd.iterateBFS():
        transitions[node.name] = {}
        edge = None
        children = []
        if node.isLeaf():
            edge = TEdge(str(node.value), [], '')
        else:
            edge = TEdge('LH', [], node.value)
            children = [node.low.name, node.high.name]
        newTransition = TTransition(node.name, edge, children)
        transitions[node.name][f'k{key}'] = newTransition

        key += 1
    result = TTreeAut(roots, transitions, bdd.name, 0)
    result.portArity = result.getPortArity()
    return result


def getVarPrefix(varList: list) -> str:
    if varList == []:
        return ""
    prefixLen = 0
    for i in range(len(varList[0])):
        if not varList[0][i:].isnumeric():
            prefixLen += 1
    prefix = varList[0][:prefixLen]
    return prefix


# Parses the tree automaton (freshly after dimacs parsing) and adds X boxes
# to the places which make sense.
#   - case 1: when an edge skips some variables
#       * e.g. node deciding by x1 leads to x4 (as opposed to x2)
#   - case 2: when a node that does not contain last variable
#       leads straight to a leaf node 
#       * e.g deciding by var x5, but there are 10 variables)
def addDontCareBoxes(ta: TTreeAut, vars: int) -> TTreeAut:
    result = copy.deepcopy(ta)
    varVis = {i: int(list(j)[0]) for i, j in ta.getVariableVisibility().items()}
    leaves = set(ta.getOutputStates())
    counter = 0
    skippedVarEdges = []
    varPrefix = ta.getVariablePrefix()
    for edge in iterateEdges(result):
        if edge.isSelfLoop():
            continue
        for idx, child in enumerate(edge.children):
            if (
                child in leaves and varVis[edge.src] != vars or
                child not in leaves and varVis[child] - varVis[edge.src] >= 2
            ):
                if len(edge.info.boxArray) < idx + 1:
                    edge.info.boxArray = [None] * len(edge.children)
                edge.info.boxArray[idx] = 'X'
                # print(f"adding box-X to {'H' if idx else 'L'} in edge {edge}")
            # if (child not in leaves and varVis[child] - varVis[edge.src] == 2):
            #     # print(f"  > bad edge = {edge}, state {child} has var {varVis[child]}")
            #     newState = f"temp{counter}"
            #     edge.children[idx] = newState
            #     newEdge = TTransition(
            #         newState, 
            #         TEdge('LH', [], f"{varPrefix}{varVis[edge.src] + 1}"),
            #         [child, child]
            #     )
            #     newKey = f"tempKey{counter}"
            #     counter += 1
            #     # print(f"  > edited edge {edge}")
            #     # print(f"  > adding extra ({counter}) edge = {newEdge}")
            #     skippedVarEdges.append((newState, newKey, newEdge))
    for newState, newKey, newEdge in skippedVarEdges:
        if newState not in result.transitions:
            result.transitions[newState] = {}
        if newKey not in result.transitions[newState]:
            result.transitions[newState][newKey] = newEdge

    return result

# End of file bdd.py
