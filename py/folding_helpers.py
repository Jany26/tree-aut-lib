"""
[file] folding_helpers.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Helper functions and FoldingHelper class used during all
essential algorithms/operations regarding folding.

[note] mostly redundant or self-explanatory functions
"""


from ta_classes import *
from ta_functions import *
from test_data import *

import re
import copy

from render_dot import exportToFile

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Folding Helper class:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FoldingHelper:
    def __init__(
        self,
        ta: TTreeAut,
        verbose: bool,
        export_vtf: bool,
        export_png: bool,
        output,
        exportPath,
        maxVar
    ):
        self.name = ""
        match = re.search(r"\(([^()]*)\)", ta.name)
        if match is None:
            self.name = f"{ta.name}"
        else:
            self.name = f"{match.group(1)}"

        # Helpful for storing (state, edgeKey) tuples during intersectoid
        # construction. If the intersectoid has non-empty language, the items
        # from this list are moved to the final softFlaggedEdges dictionary
        self.softFlaggedEdges = {}
        self.flaggedEdges = set()
        
        self.keyCounter = 0

        # folding options
        self.maxVar = maxVar
        self.minVar = 0
        self.varPrefix = ta.getVariablePrefix()
        self.stateMap = {}
        self.counter = 0
        self.counter2 = 0
        self.reach: dict[str, set] = getAllStateReachability(ta, reflexive=False)

        # export/debug options
        self.intersectoids = []
        self.verbose = verbose
        self.png = export_png
        self.vtf = export_vtf
        self.output = output
        self.path = exportPath


    def __repr__(self):
        result = "[FoldingHelper]\n"
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
        result += f"minvar = {self.minVar}, maxvar = {self.maxVar}\n"
        result += f"keycounter = {self.keyCounter}, counter = {self.counter}, counter2 = {self.counter2}\n"
        result += f"statemap = {self.stateMap}\n"
        # result += f"{}\n"
        # result += f"{}\n"
        return result

    def write(self, s):
        if self.verbose:
            if self.output is None:
                print(s)
            else:
                self.output.write(f"{s}\n")

    # def flagEdge(self, key: str, edge: TTransition):
    #     if edge.src not in self.softFlaggedEdges:
    #         self.softFlaggedEdges[edge.src] = {}
    #     childStr = ""
    #     for i in edge.children:
    #         childStr += i + " | "
    #     childStr = childStr[:-3]
    #     if childStr not in self.softFlaggedEdges[edge.src]:
    #         self.softFlaggedEdges[edge.src][childStr] = (key, edge)

    # def printFlaggedEdges(self):
    #     for j in self.softFlaggedEdges.values():
    #         for (l, m) in j.values():
    #             print(l, m)

    # # ta -> intersectoid
    # def getFlaggedEdgesFrom(self, ta: TTreeAut):
    #     for edge in transitions(ta):
    #         if len(edge.children) == 0:
    #             continue
    #         taState = splitTupleName(edge.src)
    #         children = [splitTupleName(i) for i in edge.children]
    #         childrenStr = ','.join(children)
    #         key = f"{taState}-{edge.info.variable}-{childrenStr}"
    #         self.flaggedEdges.add(key)
    
    def exportUBDA(self, result: TTreeAut, state: str, edgePart: list, box: TTreeAut):
        if self.png or self.vtf:
            temp = f"{state}-{edgePart[1]}:{box.name}-{edgePart[2]}"
            temp = f"{self.counter}-{temp}"
            if self.path is None:
                path = f"results/{self.name}/ubdas/{temp}"
            else:
                path = f"{self.path}/ubdas/{temp}"
            if self.vtf:
                exportTAtoVTF(result, format='f', filePath=f"{path}.vtf")
            if self.png:
                exportToFile(result, path)
            self.counter += 1
    
    # helper.exportIntersectoid(A, root, source, box.name)
    def exportIntersectoid(self, treeaut: TTreeAut,
                           source: str, root: str, box: str):
        self.intersectoids.append(treeaut)
        temp = f"{self.counter}-{source}-{box}-{root}"
        if self.path is None:
            path = f"results/{self.name}/intersectoids/{temp}"
        else:
            path = f"{self.path}/intersectoids/{temp}"
        if self.vtf:
            exportTAtoVTF(treeaut, format='f', filePath=f"{path}.vtf")
        if self.png:
            exportToFile(treeaut, f"{path}")
        self.write(treeaut)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Helper functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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


# Normalizes the box arrays within the ta,
# so that reducibility checks are consistent.
def fillBoxArrays(ta: TTreeAut):
    arities = ta.getSymbolArityDict()
    for edge in iterateEdges(ta):
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
    # idx = edge.children.index(edgeInfo[2])
    # print(edgeInfo[1])
    idx = edgeInfo[1]
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


def removeUselessStatesTD(ta: TTreeAut) -> TTreeAut:
    workTA = copy.deepcopy(ta)
    # reachableStatesBU = reachableBU(workTA)
    # workTA.shrinkTA(reachableStatesBU)
    reachableStatesTD = reachableTD(workTA)
    workTA.shrinkTA(reachableStatesTD)
    return workTA


def trim(ta: TTreeAut) -> TTreeAut:
    workTA = removeUselessStatesTD(ta)
    return removeUselessStates(workTA)

    # remove transitions over variables which are clearly unnecessary
    # TODO: define/explain ^^
    # get all paths from roots to leaves ---> make a function

    return workTA


class EdgePart:
    def __init__(self, key: str, edge: TTransition, index: int):
        assert(edge.src not in edge.children)
        assert(edge.info.variable != "")
        self.key = key
        self.edge = edge
        self.index = index
        self.src = edge.src
        self.target = edge.children[index]


# Creates a list of all edge-parts across all transitions from 1 source state.
# e.g. transition q0 -> (q1, q2) has 2 edge-parts, q0->q1 and q0->q2
# Each edge-part item in the list contains 4 pieces of information:
# - 0: edge key for lookup,
# - 1: index of the child,
# - 2: child name,
# - 3: source state name
# - 4: the whole edge itself
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
            result.append([key, i, edge.children[i], state, edge])
    return result


def tupleName(tuple) -> str:
    return f"({tuple[0]},{tuple[1]})"


def splitTupleName(string):
    match = re.search("^\(.*,", string)
    result = match.group(0)[1:-1]
    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# redundant edge removal - currently not included in implementation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# probably useless 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# NOTE: this function is redundant, a newer version is used (newPrepareEdgeInfo)
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



# NOTE: function addVariablesTD is in use for folding
# temporarily copied from simulation.py
def addVariablesBUFolding(ta: TTreeAut, minVar: int):
    def convertVars(varList: list, prefix: str) -> dict:
        return {i: int(i[len(prefix):]) for i in varList}

    varPrefix = ta.getVariablePrefix()
    varLookup = convertVars(ta.getVariableOrder(), varPrefix)
    # varVis = {i: minVar for i in ta.rootStates}
    varVis = {}
    for edge in iterateEdges(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src not in varVis:
            varVis[edge.src] = f"{varPrefix}{varLookup[edge.info.variable]}"
    for edge in iterateEdges(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        for child in edge.children:
            if child in varVis:
                continue
            varVis[child] = f"{varPrefix}{varLookup[varVis[edge.src]] + 1}"

    for edge in iterateEdges(ta):
        if edge.info.variable != "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src in varVis:
            edge.info.variable = f"{varVis[edge.src]}"
        pass  # doSth()


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


# changes box objects on edges to strings of their names ???
# initial try for compatability with dot/vtf format modules
# NOTE: redundant
def stringifyBoxes(ta: TTreeAut):
    for edge in iterateEdges(ta):
        newBoxArray = []
        for box in edge.info.boxArray:
            if type(box) == type(TTreeAut):
                newBoxArray.append(box.name)
            else:
                newBoxArray.append(box)
        edge.info.boxArray = newBoxArray

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# old port-state map creating functions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def getMappingOld(intersectoid, treeaut):
    mapping = portToStateMapping(intersectoid)
    # oldMapping = getMaximalMapping(intersectoid, treeaut, mapping)
    maxMapping = getMaximalMappingFixed(intersectoid, treeaut, mapping)
    # ^^ largest rootDistance of "port" nodes (inside intersectoid)
    finalMapping = {i: splitTupleName(j) for i, j in maxMapping.items()}
    return finalMapping

# This function parses an intersectoid and creates a dictionary with all
# port transitions and all states that begin with them.
# input:
# - an intersectoid "TA"
# output:
def portToStateMapping(intersectoid: TTreeAut) -> dict:
    result = {}
    for edge in iterateEdges(intersectoid):
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# different versions of manipulating the edge targets
# after finding out the mapping (used in treeAutFolding function)
# ~~deprecated~~, kept for documenting/archiving purposes
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# for i, (mapState, var) in enumerate(mapping.values()):
#     edge.children.insert(idx + i, mapState)
#     if var != varVis[mapState]:
#         # create and assign state copy
#         if f"{mapState}{var}" in helper.stateMap:
#             mappedState = helper.stateMap[f"{mapState}{var}"]
#             edge.children[idx + i] = mappedState
#             # print(mapState, var, mappedState)
#             continue
#         newState = f"{mapState}_{helper.counter}"
#         helper.stateMap[f"{mapState}{var}"] = newState
#         # helper.stateMap[f"{mapState}{var}"] = newState
#         transitionsCopy = {}
#         result.transitions[newState] = transitionsCopy
#         for k, e in result.transitions[mapState].items():
#             if e.isFullSelfLoop():
#                 continue
#             edgeCopy: TTransition = copy.deepcopy(e)
#             edgeCopy.src += f'_{helper.counter}'
#             for index, child in enumerate(e.children):
#                 if child == e.src:
#                     edgeCopy.children[index] += f'_{helper.counter}'
#             transitionsCopy[f'{k}_{helper.counter}'] = edgeCopy
#         # for k, e in transitionsCopy.items():
#             # print("trCopyEdge", e)
#         edge.children[idx + i] = newState
#         # print(f"edge.children = {edge.children}, newState = {newState}")

#         newEdge = TTransition(newState, TEdge('LH', [], var), [mapState, mapState])
#         # print("newEdge", newEdge)
#         helper.counter += 1
#         key = f"temp_{helper.counter2}"
#         helper.counter2 += 1
#         # if newState not in result.transitions:
#         #     result.transitions[newState] = {}
#         result.transitions[newState][key] = newEdge


# for i, (mapState, var) in enumerate(mapping.values()):
#     print(mapping)
#     edge.children.insert(idx + i, mapState)
#     if var == varVis[mapState]:
#         continue
#     # if var == "":
#         # continue
#     print(f"mapstate = {mapState}, {type(mapState)}, var = {var}, {type(var)}, varvis = {varVis[mapState]}")
#     newState = f"{mapState}-{var}"
#     print(edge, idx+i, edge.children[idx+i], newState)
#     edge.children[idx+i] = newState
#     if newState not in result.transitions:
#         result.transitions[newState] = {}
#     newEdge = TTransition(newState, TEdge('LH', [], var), [mapState, mapState])
#     print(f"newEdge = {newEdge}")
#     result.transitions[newState][f'{helper.counter2}'] = newEdge
#     helper.counter2 += 1
#     originalVar = int(varVis[mapState][len(helper.varPrefix):])
#     intersectoidVar = int(var[len(helper.varPrefix):])
#     print(f'original = {originalVar}, intersectoid = {intersectoidVar}')
#     if originalVar > intersectoidVar + 1:
#         newEdge = TTransition(newState, TEdge('LH', [], ""), [newState, newState])
#         print(f"newEdge = {newEdge}")
#         result.transitions[newState][f'{helper.counter2}'] = newEdge
#         helper.counter2 += 1
