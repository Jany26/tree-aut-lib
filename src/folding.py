from ta_classes import *
from ta_functions import *
from test_data import *

import re
from copy import deepcopy
from utils import stateNameSort
from render_dot import exportToFile


class FoldingHelper:
    def __init__(self, ta: TTreeAut, verbose: bool, export: bool, output, exportPath):
        # Helpful for storing (state, edgeKey) tuples during intersectoid
        # construction. If the intersectoid has non-empty language, the items
        # from this list are moved to the final softFlaggedEdges dictionary
        self.softFlaggedEdges = {}
        self.flaggedEdges = set()
        self.intersectoids = []
        self.name = ""
        match = re.search(r"\(([^()]*)\)", ta.name)
        if match is None:
            self.name = f"{ta.name}"
        else:
            self.name = f"{match.group(1)}"
        self.verbose = verbose
        self.export = export
        self.output = output
        self.path = exportPath
        self.counter = 0

    def __repr__(self):
        result = "FoldingHelper:\n"
        srcLen = 0
        keyLen = 0
        childLen = 0
        for state, edges in self.softFlaggedEdges.items():
            srcLen = max(srcLen, len(state))
            for childStr, (key, edge) in edges.items():
                childLen = max(childLen, len(childStr))
                keyLen = max(keyLen, len(key))
        for state, edges in self.softFlaggedEdges.items():
            for childStr, (key, edge) in edges.items():
                result += "%-*s -> %-*s : %-*s : %s\n" % (
                    srcLen, state, childLen, childStr, keyLen, key, edge
                )
        return result

    def write(self, s):
        # if helper.verbose:
        #     space = f"{0 * ' '}"
        #     sym = 'L' if edgePart[1] == 0 else 'H'
        #     if helper.output is None:
        #         print()
        #     else:
        #         helper.output.write("%s> boxFinding(%s-[%s:%s]->%s => %s)\n\n" % (
        #             space, state, sym, box.name, edgePart[2], mapping
        #         ))

        # if helper.verbose:
        #     if helper.output is None:
        #         print(A)
        #     else:
        #         helper.output.write(f"{A}\n")
        if self.verbose:
            if self.output is None:
                print(s)
            else:
                self.output.write(f"{s}\n")

    def flagEdge(self, key: str, edge: TTransition):
        if edge.src not in self.softFlaggedEdges:
            self.softFlaggedEdges[edge.src] = {}
        childStr = ""
        for i in edge.children:
            childStr += i + " | "
        childStr = childStr[:-3]
        if childStr not in self.softFlaggedEdges[edge.src]:
            self.softFlaggedEdges[edge.src][childStr] = (key, edge)

    def printFlaggedEdges(self):
        for j in self.softFlaggedEdges.values():
            for (l, m) in j.values():
                print(l, m)

    # ta -> intersectoid
    def getFlaggedEdgesFrom(self, ta: TTreeAut):
        for edge in transitions(ta):
            if len(edge.children) == 0:
                continue
            taState = splitTupleName(edge.src)
            children = [splitTupleName(i) for i in edge.children]
            childrenStr = ','.join(children)
            key = f"{taState}-{edge.info.variable}-{childrenStr}"
            self.flaggedEdges.add(key)


def removeFlaggedEdgesFix(ta: TTreeAut, helper: FoldingHelper):
    keyDict = {}
    for state, edges in ta.transitions.items():
        keyDict[state] = set()
        for key, edge in edges.items():
            if len(edge.children) == 0:
                continue
            childStr = ','.join(edge.children)
            if f"{edge.src}-{edge.info.variable}-{childStr}" in helper.flaggedEdges:
                keyDict[state].add(key)
    for state, keySet in keyDict.items():
        for key in keySet:
            ta.transitions[state].pop(key)


def removeFlaggedEdges(ta: TTreeAut, helper: FoldingHelper):
    keyList = []
    for state, edges in helper.softFlaggedEdges.items():
        for childStr, (key, edge) in edges.items():
            originalChildren = childStr.split(" | ")
            onlyBoxed = True
            childrenStayed = True
            for i in range(len(edge.children)):
                if originalChildren[i] != edge.children[i]:
                    childrenStayed = False
                if not hasOnlyBoxedEdges(ta, edge.children[i]):
                    onlyBoxed = False
            if childrenStayed and not onlyBoxed:
                keyList.append(key)
                ta.transitions[state].pop(key)
    # print(stateNameSort(keyList))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Helper functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def trim(ta: TTreeAut) -> TTreeAut:
    workTA = removeUselessStates(ta)

    # remove transitions over variables which are clearly unnecessary
    # TODO: define/explain ^^
    # get all paths from roots to leaves ---> make a function

    return workTA


# creates a "key" for transition dictionary modified for working with
# an "intersectoid" tree automaton
def intersectoidEdgeKey(e1: list, e2: list) -> str:
    state = f"({e1.src}, {e2.src})"
    symb = e2.info.label
    var = ""
    if e1.info.variable != "" and not symb.startswith("Port"):
        var = f",{e1.info.variable}"

    children = f""
    if not e2.info.label.startswith("Port"):
        for i in range(len(e1.children)):
            children += f"({e1.children[i]},{e2.children[i]}),"
        children = children[:-1]

    key = f"{state}-<{symb}{var}>-({children})"
    return key


# Helper function to create a list of states and some data about them,
# which will be helpful during main folding procedure.
# list of all sub-edges (parts of hyper-edge), with indexes to the child.
#
# e.g. key-transition pair "key": q0 -> (q1, q2) will be divided into:
# ["key", 0, q1] and ["key", 1, q2]
def prepareEdgeInfo(ta: TTreeAut, state: str) -> list:
    result = []
    for key, edge in ta.transitions[state].items():
        for i in range(len(edge.children)):
            result.append([key, i, edge.children[i]])
    return result


def tupleName(tuple) -> str:
    return f"({tuple[0]},{tuple[1]})"


def splitTupleName(string):
    match = re.search("^\(.*,", string)
    result = match.group(0)[1:-1]
    return result


def hasOnlyBoxedEdges(ta: TTreeAut, state: str):
    arityDict = ta.getSymbolArityDict()
    for edge in ta.transitions[state].values():
        arity = arityDict[edge.info.label]
        if arity == 0:
            return False
        boxCount = 0
        for box in edge.info.boxArray:
            if box is not None and box != "":
                boxCount += 1
        if arity != boxCount:
            return False
    return True


# Funtion produces an intersectoid from the 'ta' UBDA and 'box' TA.
# This intersectoid is used in boxFinding() to determine the result mapping.
# Intersectoid is similar to a 'product' or an 'intersection' tree automaton.
# state set: Q' = Q_v x Q_b (v = normalized BDA, b = box)
#
# types of transitions and how they came to be:
#
# 1) (q,s)-{LH}->[(q1,s1),(q2,s2)] | q-{LH}->(q1,q2) is in transition
#       dictionary (trd.) of v and s-{LH}->(s1,s2) is in tr.dict. of b
#
# 2) (q,s)-{LH,var}->[(q1,s1),(q2,s2)] | q-{LH,var}->(q1,q2) is in trd.
#       of v and s-{LH}->(s1,s2) is in trd. of b
#
# 3) (q,s)-{a}->() | q-{a}->() in trd. of v and s-{a}->() in trd. of b
#       // a is a terminal symbol (e.g. '0' or '1') => output transition
#
# 4) (q,s)-{Port_i}->() | s-{Port_i}->() in tr.d of b
def createIntersectoid(
    ta: TTreeAut,
    box: TTreeAut,
    root: str,
    helper: FoldingHelper
) -> TTreeAut:
    edges = {}
    visited = set()
    worklist: list = [(root, b) for b in box.rootStates]
    helper.temp = []
    while worklist != []:
        currentTuple = worklist.pop(0)
        state = tupleName(currentTuple)
        if state not in edges:
            edges[state] = {}
        if state in visited:
            continue
        for key, te in ta.transitions[currentTuple[0]].items():  # ta edges
            # skipping edges with already applied reductions
            skip = False
            for b in te.info.boxArray:
                if b is not None:
                    # skipping when trying to reach through a reduced edge, BUT
                    # NOT when the source state can create a port transition
                    skip = True
            for be in box.transitions[currentTuple[1]].values():  # box edges
                # skipping differently labeled (e.g. LH and 0) edges
                if (
                    te.info.label != be.info.label and
                    not be.info.label.startswith("Port")
                ):
                    continue
                # ports are exceptions to the different labeled exclusion
                # if one of the mismatched labels is a port label,
                # than that "overrules" any other label
                if be.info.label.startswith("Port"):
                    edgeObj = TEdge(be.info.label, [], '')
                    edge = TTransition(state, edgeObj, [])
                    edges[state][intersectoidEdgeKey(te, be)] = edge
                elif not skip:
                    children = []
                    for i in range(len(te.children)):
                        child = (te.children[i], be.children[i])
                        children.append(tupleName(child))
                        worklist.append(child)
                    edgeObj = TEdge(be.info.label, [], te.info.variable)
                    if len(children) != 0:
                        helper.temp.append((splitTupleName(state), key))
                        helper.flagEdge(key, te)
                    edge = TTransition(state, edgeObj, children)
                    edges[state][intersectoidEdgeKey(te, be)] = edge
            # for box edge
        # for tree automaton edge
        visited.add(state)
    # end while loop
    roots = [f"({root},{b})" for b in box.rootStates]
    name = f"intersectoid({box.name}, {root})"
    result = TTreeAut(roots, edges, name, box.portArity)
    # result.reformatKeys()
    return result


# This function parses an intersectoid and creates a dictionary with all
# port transitions and all states that begin with them.
# input:
# - an intersectoid "TA"
# output:
def portToStateMapping(intersectoid: TTreeAut) -> dict:
    result = {}
    for edge in transitions(intersectoid):
        if edge.info.label.startswith("Port"):
            if edge.info.label not in result:
                result[edge.info.label] = []
            result[edge.info.label].append(edge.src)
    return result


# finds a state furthest from the root so that the mapping is "maximal"
# input:
# - an intersectoid "TA",
# - dictionary of ports and states with port output transitions
# output:
def getMaximalMapping(intersectoid: TTreeAut, ta: TTreeAut, ports: dict) -> dict:
    mapping = {}
    for port, stateList in ports.items():
        mapping[port] = None
        currentDistance = 0  # state, rootDistance
        for state in stateList:
            dist = intersectoid.getRootDistance(state)
            if dist > currentDistance:
                mapping[port] = state
                currentDistance = dist
            elif dist == currentDistance:
                currentState = splitTupleName(mapping[port])
                possibleNewState = splitTupleName(state)
                currDist = ta.getRootDistance(currentState)
                newDist = ta.getRootDistance(possibleNewState)
                if newDist > currDist:
                    mapping[port] = state
        if mapping[port] is None:
            raise Exception(f"getMaximalMapping: {port} mapping not found")
    return mapping


def getMapping(intersectoid: TTreeAut, ta: TTreeAut) -> dict:
    ports = {}
    for edge in transitions(intersectoid):
        if edge.info.label.startswith("Port"):
            if edge.info.label not in ports:
                ports[edge.info.label] = []
            ports[edge.info.label].append(edge.src)

    reach: dict[str, set] = getAllStateReachability(ta, reflexive=False)
    mapping = {}
    for port, stateList in ports.items():
        mapping[port] = None
        for state in stateList:
            s = splitTupleName(state)
            infimum = True
            for state2 in stateList:
                if state == state2:
                    continue
                s2 = splitTupleName(state2)
                if s in reach[s2] and not s2 in reach[s]:
                    continue
                else:
                    infimum = False
            if infimum:
                mapping[port] = s
        if mapping[port] == None:
            return {}
    return mapping


def getMaximalMappingFixed(intersectoid: TTreeAut, ta: TTreeAut, ports: dict) -> dict:
    mapping = {}
    for port, stateList in ports.items():
        temp = {}
        mapping[port] = None
        for state in stateList:
            taState = splitTupleName(state)
            dist = ta.getRootDistance(taState)
            if dist not in temp:
                temp[dist] = set()
            temp[dist].add(state)
        maxDist = 0
        for dist in temp.keys():
            maxDist = max(maxDist, dist)
        if len(temp[maxDist]) > 1:
            return {}
        mapping[port] = list(temp[maxDist])[0]
    return mapping


# Main implementation of one step of the folding procedure.
# Function tries to apply tree automaton reduction starting from the specific
# state in the normalized (and well-specified) UBDA.
# inputs:
#   'ta' - UBDA on which we try to apply reduction
#   'box' - specifies which tree automaton should be applied
#   'root' - which state is the starting point of the procedure
# output:
#   - dictionary which specifies mapping of the output ports of the 'box'
#     TA to the states of the initial 'ta' (UBDA)
#   - if no mapping is found, empty dictionary {} is returned
def boxFinding(
    ta: TTreeAut,
    box: TTreeAut,
    root: str,
    helper: FoldingHelper,
    source: str
) -> dict:
    A: TTreeAut = createIntersectoid(ta, box, root, helper)
    tree, string = nonEmptyBU(A)
    if tree is None:
        return {}
    # copy = deepcopy(A)
    helper.intersectoids.append(A)
    if helper.export:
        temp = f"{helper.counter}-{source}-{box.name}-{root}"
        if helper.path is None:
            path = f"results/{helper.name}/intersectoids/{temp}"
        else:
            path = f"{helper.path}/intersectoids/{temp}"
        exportToFile(A, path)
        exportTAtoVTF(A, format='f', filePath=f"{path}.vtf")
    A = trim(A)  # additional functionality maybe needed?
    helper.write(A)
    helper.getFlaggedEdgesFrom(A)

    # mapping = portToStateMapping(A)
    # # oldMapping = getMaximalMapping(A, ta, mapping)
    # maxMapping = getMaximalMappingFixed(A, ta, mapping)
    # # ^^ largest rootDistance of "port" nodes (inside intersectoid)
    # finalMapping = {i: splitTupleName(j) for i, j in maxMapping.items()}

    finalMapping = getMapping(A, ta)

    return finalMapping


def createVariableVisibilityCache(ta: TTreeAut) -> dict:
    result = {state: "" for state in ta.getStates()}
    for state in ta.getStates():
        for edge in ta.transitions[state].values():
            if edge.info.variable != "":
                result[state] = edge.info.variable
    return result


# Creates a list of all edge-parts across all transitions from 1 source state.
# e.g. transition q0 -> (q1, q2) has 2 edge-parts, q0->q1 and q0->q2
# Each edge-part item in the list contains 4 pieces of information:
# - 0: edge key for lookup,
# - 1: index of the child,
# - 2: child name,
# - 3: source state name
def newPrepareEdgeInfo(ta: TTreeAut, state: str):
    result = []
    for key, edge in ta.transitions[state].items():
        # we do not fold edges that are self-loops
        if edge.src in edge.children:
            continue
        # ... or are not labeled with a variable
        if edge.info.variable == "":
            continue
        for i in range(len(edge.children)):
            result.append([key, i, edge.children[i], state])
    return result


# Main function implementing process of folding.
# Applying separate folding steps implemented in boxFinding() funtion.
# Respects the chosen box order.
# inputs:
#   'ta' - UBDA that we want to apply folding on,
#   'boxes' - ordered list of box names, which can be used to reduce the 'ta'
# output: (folded) UBDA with applied reductions (same language as the input)
def newFold(ta: TTreeAut, boxes: list, verbose=False, export=False, output=None, exportPath=None) -> TTreeAut:
    result = copy.deepcopy(ta)
    fillBoxArrays(result)  # in case of [None, None] and [] discrepancies
    variableVisibility = createVariableVisibilityCache(ta)
    helper = FoldingHelper(ta, verbose, export, output, exportPath)
    for boxName in boxes:
        box = boxCatalogue[boxName]
        worklist = [root for root in ta.rootStates]
        visited = set()
        while worklist != []:
            state = worklist.pop(0)
            if state in visited:
                continue
            edgesToChildren = newPrepareEdgeInfo(result, state)
            # print(box.name, state, edgesToChildren)
            for edgePart in edgesToChildren:
                # edgePart contains three items: [key, child-index, child]
                if isAlreadyReduced(result, state, edgePart):
                    continue
                if state in result.transitions[state][edgePart[0]].children:
                    continue
                mapping = boxFinding(result, box, edgePart[2], helper, state)
                if mapping != {}:
                    helper.write("%s> boxFinding(%s-[%s:%s]->%s => %s)\n" % (
                        f"{0 * ' '}", state, 'L' if edgePart[1] == 0 else 'H',
                        box.name, edgePart[2], mapping
                    ))
                    if helper.export:
                        temp = f"{state}-{edgePart[1]}:{box.name}-{edgePart[2]}"
                        temp = f"{helper.counter}-{temp}"
                        if helper.path is None:
                            path = f"results/{helper.name}/ubdas/{temp}"
                        else:
                            path = f"{helper.path}/ubdas/{temp}"
                        exportToFile(result, path)
                        exportTAtoVTF(result, format='f', filePath=f"{path}.vtf")
                        helper.counter += 1
                    # skip = False
                    # for mappedState in mapping.values():
                    #     if variableVisibility[mappedState] == "":
                    #         skip = True
                    #         print(f"skipping mapping {mapping} because {mappedState} has no variable visible")
                    # if skip:
                    #     continue
                    # phase 1: putting the box in the box array
                    edge = result.transitions[edgePart[3]][edgePart[0]]
                    # print(edge)
                    initialBoxList = edge.info.boxArray
                    symbol = edge.info.label
                    boxList = [None] * ta.getSymbolArityDict()[symbol]
                    for idx in range(len(initialBoxList)):
                        boxList[idx] = initialBoxList[idx]
                    boxList[edgePart[1]] = box.name
                    edge.info.boxArray = boxList

                    # phase 2: fill the box-port children in the child array
                    idx = getStateIndexFromBoxIndex(edge, edgePart[1])
                    edge.children.pop(idx)
                    for i, mapState in enumerate(mapping.values()):
                        edge.children.insert(idx + i, mapState)
                # if mapping != {}
            # for edgeInfo
            visited.add(state)
            for edge in transitionsFrom(result, state):
                for child in edge.children:
                    if child not in visited:
                        worklist.append(child)
            # worklist update
        # while worklist != []

    match = re.search(r"\(([^()]*)\)", result.name)
    if match is None:
        result.name = f"folded({ta.name})"    
    else:
        result.name = f"folded({match.group(1)})"
    return result


# changes box objects on edges to strings of their names ???
# initial try for compatability with dot/vtf format modules
# NOTE: redundant
def stringifyBoxes(ta: TTreeAut):
    for edge in transitions(ta):
        newBoxArray = []
        for box in edge.info.boxArray:
            if type(box) == type(TTreeAut):
                newBoxArray.append(box.name)
            else:
                newBoxArray.append(box)
        edge.info.boxArray = newBoxArray


# Returns the first (important notice!) child state (index),
# to which does the transition lead through the box on index idx.
#
# E.g. q0 - [box1, box2] -> (q1, q2, q3, q4) ## consider box1 has portArity = 3
# idx = 1 (box2)... box1 has port arity 3, so box2 is on the sub-edge leading
# to state q4, as subedge with box1 encapsulates children q1, q2, q3
#
# NOTE: might not work in some special cases of port arity combinations etc.
def getStateIndexFromBoxIndex(edge: list, idx: int) -> int:
    if idx >= len(edge.info.boxArray):
        raise Exception("getStateIndexFromBoxIndex(): idx out of range")
    result = 0
    for i, boxStr in enumerate(edge.info.boxArray):
        if i == idx:
            return result
        if boxStr is None:
            result += 1
        else:
            result += boxCatalogue[boxStr].portArity
    raise Exception("getStateIndexFromBoxIndex(): idx out of range")


def fillBoxArrays(ta: TTreeAut):
    arities = ta.getSymbolArityDict()
    for edge in transitions(ta):
        if edge.info.boxArray == []:
            edge.info.boxArray = [None] * len(edge.children)
        else:
            boxlen = len(edge.info.boxArray)
            symlen = arities[edge.info.label]
            if boxlen != symlen:
                edge.info.boxArray.extend([None] * (symlen - boxlen))


# This function checks whether or not a certain subedge has a box reduction.
# (subedge is based on 'state' and 'edgeInfo')
#
# NOTE: might be buggy if box arities and boxArrays on edges are inconsistent
# (consider different index in edgeInfo and boxes with different port arities)
def isAlreadyReduced(ta: TTreeAut, state: str, edgeInfo: list) -> bool:
    edge = ta.transitions[state][edgeInfo[0]]  # edgeInfo[0] = key
    if edgeInfo[2] not in edge.children:
        return True
    idx = edge.children.index(edgeInfo[2])
    # if box is None => short edge => arity = 1 (1 target state)
    boxArities = []
    for boxStr in edge.info.boxArray:
        if boxStr is None:
            boxArities.append((None, 1))
        else:
            box = boxCatalogue[boxStr]
            boxArities.append((boxStr, box.portArity))

    i = 0
    for tuple in boxArities:
        if idx < i + tuple[1]:
            if tuple[0] is not None:
                return True
            else:
                return False
        i += tuple[1]
    return False


# In order to canonically and deterministically fold the unfolded and
# normalized UBDA, we need to determine an order in which the states will
# be checked for possible applicable reductions. Lexicographic order (ordered
# by the shortest path from root to the particular state),
# which is similar to DFS, provides such a way.
#
# e.g. path to q1 from root is: low(0), low(0), high(1) edges - 001
# path to q2 from root is: low(0), high(1), low(0) - 010
# thus, lexicographically, q1 comes before q2
#
# This function takes a
def lexicographicalOrder(ta: TTreeAut) -> list:
    def lexOrder(ta: TTreeAut, state: str, path: str, result, open):
        if state not in result:
            result[state] = path
        else:  # probably redundant, as we go depth first from the lowest path
            if path < result[state]:
                result[state] = path

        for edge in ta.transitions[state].values():
            for idx, child in enumerate(edge.children):
                if child in open:
                    continue
                open.add(child)
                lexOrder(ta, child, path + str(idx), result, open)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    pathDict = {}  # state -> path string
    open = set()
    for i in ta.rootStates:
        open.add(i)
        lexOrder(ta, i, '', pathDict, open)

    # because some states can be accessed through identical paths,
    # we need to have lists in the reverse path dict.
    reversePathDict: dict[str, list[str]] = {}  # path -> list of states
    for state, path in pathDict.items():
        if path not in reversePathDict:
            reversePathDict[path] = []
        reversePathDict[path].append(state)

    pathList = [path for path in reversePathDict.keys()]
    pathList.sort()
    result = []
    for path in pathList:
        result.extend(reversePathDict[path])
    return result

# End of folding.py
