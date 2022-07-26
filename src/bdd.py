# bdd.py
# Module for implementing basic BDD operations.
# Needed in order to parse DIMACS format (read as DNF* for simplification).
#
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>


# One node of a binary decision diagram.
class BDDnode:

    def __init__(self, name, value, low=None, high=None):
        self.name = name  # name / label of the node
        self.value = value  # variable (value) symbolizing the node (e.g. 'x1')
        self.parent = None  # root node has parent None
        self.low = low  # low descendant ('False' branch   "....")
        self.high = high  # high descendant ('True' branch "____")

    def __repr__(self):
        if self is None:
            return ""
        return f"({self.name}, {self.value})"

    def attach(self, low, high):
        self.attachLow(low)
        self.attachHigh(high)

    def attachLow(self, node):
        if node is None:
            return
        self.low = node
        node.parent = self

    def attachHigh(self, node):
        if node is None:
            return
        self.high = node
        node.parent = self

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
        
        result = []
        getNodesFromLevelHelper(self, level, result)
        return result


# Binary decision diagram. open for expansion (more attributes etc.)
class BDD:
    def __init__(self, name: str, root: BDDnode):
        self.name = name
        self.root = root

    def __repr__(self):
        result = ""
        for i in self.iterateDFS(allowRepeats=True):
            result += f"{i} [{i.height()}] -> [{i.low}, {i.high}]\n"
        return result

    # Breadth first traversal of BDD nodes (iterator)
    # if allowRepeats=False: each node is only visited once (leaf nodes etc.)
    # by having repeats on, the tree traversal may be more understandable
    def iterateBFS(self, allowRepeats=False):
        node = self.root
        if node is None:
            return
        
        visited = set()
        queue = [node]

        while len(queue) > 0:
            node = queue.pop(0)

            if not allowRepeats:
                if node in visited:
                    return
                visited.add(node)

            yield node
            
            if node.low is not None:
                queue.append(node.low)
            
            if node.high is not None:
                queue.append(node.high)

    # Depth first traversal of BDD nodes (iterator)
    # see iterateBFS() for explanation of allowRepeats
    def iterateDFS(self, allowRepeats=False):
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

        visited = set()
        return DFS(self.root, visited, allowRepeats)
    

# Creates a new BDD by applying some logic function on two BDDs.
def applyFunction(bdd1: BDD, bdd2: BDD, func) -> BDD:
    pass
