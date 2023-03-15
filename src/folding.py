from ta_classes import *
from ta_functions import *
from test_data import *

import re
from copy import deepcopy
from utils import stateNameSort
from render_dot import exportToFile


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
        
        # folding options
        self.maxVar = maxVar
        self.minVar = 0
        self.varPrefix = ta.getVariablePrefix()
        self.stateMap = {}
        self.counter = 0
        self.counter2 = 0

        # export/debug options
        self.intersectoids = []
        self.verbose = verbose
        self.png = export_png
        self.vtf = export_vtf
        self.output = output
        self.path = exportPath


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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Main Folding algorithm functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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
                    edgeObj = TEdge(be.info.label, [], "")
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
    return result


# This function finds all different port types in intersectoid and assigns
# one state from the original ta to be mapped to the port.
# It uses a reachability relation (similar to Floyd-Warshall algorithm) to
# determine the state that is "infimum" wrt. reachability, i.e. a state 'q', that
# can be reached from all 'suspect' states of the particular port and no
# 'suspect' state can reach the state 'q'. If no such state exists, mapping 
# fails and thus no box folding should be applied.
#
# note: 'suspect' states (a,b) from the intersectoid contain a Port output
# transition. (state 'a' from the original TA is compared wrt. the reachability)
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
                mapping[port] = state
        if mapping[port] == None:
            return {}
    return mapping


## temporarily copied from simulation.py
def computeAdditionalVariablesFolding(ta: TTreeAut, minVar: int):
    def convertVars(varList: list, prefix: str) -> dict:
        return {i: int(i[len(prefix):]) for i in varList}

    varPrefix = ta.getVariablePrefix()
    varLookup = convertVars(ta.getVariableOrder(), varPrefix)
    # varVis = {i: minVar for i in ta.rootStates}
    varVis = {}
    for edge in transitions(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src not in varVis:
            varVis[edge.src] = f"{varPrefix}{varLookup[edge.info.variable]}"
    for edge in transitions(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        for child in edge.children:
            if child in varVis:
                continue
            varVis[child] = f"{varPrefix}{varLookup[varVis[edge.src]] + 1}"

    for edge in transitions(ta):
        if edge.info.variable != "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src in varVis:
            edge.info.variable = varVis[edge.src]
        pass # doSth()

def addVariablesRecursive(ta: TTreeAut, helper: FoldingHelper):
    # var = int(edge.info.variable[len(helper.varPrefix):])
    # edge.info.variable = f"{helper.varPrefix}{var}"
    def addVariables(ta: TTreeAut, var: int, state: str, helper: FoldingHelper):
        if var > helper.maxVar + 1:
            return
        for edge in ta.transitions[state].values():
            if edge.src in edge.children:
                return
        for edge in ta.transitions[state].values():
            if edge.info.variable != "":
                edgeVar = int(edge.info.variable[len(helper.varPrefix):])
                if edgeVar != var:
                    print(f"WARNING: addVariables(): edge {edge} does not agree with var {var}")
                return
            edge.info.variable = f"{helper.varPrefix}{var}"
    # if root has no var-labeled edges and has no self-loops,
    # minVar is used to label edges starting from root
    for root in ta.rootStates:
        selfLooping = False
        noVars = True
        for edge in ta.transitions[root].values():
            if edge.src in edge.children:
                selfLooping = True
            if edge.info.variable != "":
                noVars = False
        # if not selfLooping and noVars:
        if selfLooping or not noVars:
            continue
        for edge in ta.transitions[root].values():
            edge.info.variable = f"{helper.varPrefix}{helper.minVar}"

    for edge in transitions(ta):
        if edge.src in edge.children: # or edge.info.variable == "":
            continue
        if edge.info.variable == "":
            continue
        var = int(edge.info.variable[len(helper.varPrefix):])
        for child in edge.children:
            addVariables(ta, var + 1, child, helper)


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
    if box.name in ['boxX', 'X'] and root == 'q1':
        print(A)
    tree, string = nonEmptyBU(A)
    if tree is None:
        return {}

    A = trim(A)  # additional functionality maybe needed?
    helper.intersectoids.append(A)

    if helper.png or helper.vtf:
        temp = f"{helper.counter}-{source}-{box.name}-{root}"
        if helper.path is None:
            path = f"results/{helper.name}/intersectoids/{temp}"
        else:
            path = f"{helper.path}/intersectoids/{temp}"
        if helper.vtf:
            exportTAtoVTF(A, format='f', filePath=f"{path}.vtf")
        if helper.png:
            exportToFile(A, path)

    addVariablesRecursive(A, helper)
    # computeAdditionalVariablesFolding(ta, helper.minVar)
    if helper.png:
        exportToFile(A, f"{path}-trimmed")
    helper.write(A)
    helper.getFlaggedEdgesFrom(A)

    # mapping = portToStateMapping(A)
    # # oldMapping = getMaximalMapping(A, ta, mapping)
    # maxMapping = getMaximalMappingFixed(A, ta, mapping)
    # # ^^ largest rootDistance of "port" nodes (inside intersectoid)
    # finalMapping = {i: splitTupleName(j) for i, j in maxMapping.items()}

    finalMapping = getMapping(A, ta)
    varVis = createVariableVisibilityCache(A)
    splitMapping = {p: (splitTupleName(s), varVis[s]) for p,s in finalMapping.items()}
    return splitMapping


# Main function implementing process of folding.
# Applying separate folding steps implemented in boxFinding() funtion.
# Respects the chosen box order.
# inputs:
#   'ta' - UBDA that we want to apply folding on,
#   'boxes' - ordered list of box names, which can be used to reduce the 'ta'
# output: (folded) UBDA with applied reductions (same language as the input)
def treeAutFolding(ta: TTreeAut, boxes: list, maxVar: int,
    verbose=False,
    export_vtf=False,
    export_png=False,
    output=None,
    exportPath=None,
) -> TTreeAut:
    result = copy.deepcopy(ta)
    fillBoxArrays(result)  # in case of [None, None] and [] discrepancies
    helper = FoldingHelper(ta, verbose, export_vtf, export_png, output, exportPath, maxVar)
    if helper.vtf or helper.png:
        if not os.path.exists(f"{helper.path}/ubdas/"):
            os.makedirs(f"{helper.path}/ubdas/")
        if not os.path.exists(f"{helper.path}/intersectoids/"):
            os.makedirs(f"{helper.path}/intersectoids/")
    for boxName in boxes:
        box = boxCatalogue[boxName]
        worklist = [root for root in ta.rootStates]
        visited = set()
        while worklist != []:
            state = worklist.pop(0)
            if state in visited:
                continue
            edgesToChildren = newPrepareEdgeInfo(result, state)
            for edgePart in edgesToChildren:
                # edgePart contains 5 items: [key, child-index, child-state, source-state, edge]
                part = 'L' if edgePart[1] == 0 else 'H'
                if isAlreadyReduced(result, state, edgePart):
                    # print(f"edgePart ({edgePart[0]}): {edgePart[3]} --[{part}]--> {edgePart[2]}")
                    continue
                helper.minVar = int(edgePart[4].info.variable[len(helper.varPrefix):]) + 1
                if state in result.transitions[state][edgePart[0]].children:
                    continue
                print("%s> boxFinding(%s-[%s:%s]->%s)" % (
                    f"{0 * ' '}", state, 'L' if edgePart[1] == 0 else 'H',
                    box.name, edgePart[2]
                ))
                mapping = boxFinding(result, box, edgePart[2], helper, state)

                if mapping == {}:
                    continue
                # print(mapping)
                noneVar = False
                for mapState, var in mapping.values():
                    if var == "":
                        noneVar = True
                if noneVar: continue
                helper.write("%s> boxFinding(%s-[%s:%s]->%s => %s)\n" % (
                    f"{0 * ' '}", state, 'L' if edgePart[1] == 0 else 'H',
                    box.name, edgePart[2], mapping
                ))
                exportUBDA(result, state, edgePart, box, helper)
                biggerVar = False
                varVis = createVariableVisibilityCache(result)
                for i, (mapState, var) in enumerate(mapping.values()):
                    # print(f"var = '{var}', mapState = '{mapState}', varVis[{mapState}] = '{varVis[mapState]}'")
                    originalVar = int(varVis[mapState][len(helper.varPrefix):])
                    intersectoidVar = int(var[len(helper.varPrefix):])
                    if intersectoidVar > originalVar:
                        biggerVar = True
                if biggerVar:
                    continue
                # phase 1: putting the box in the box array
                edge = result.transitions[edgePart[3]][edgePart[0]]
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

                for i, (mapState, var) in enumerate(mapping.values()):
                    edge.children.insert(idx + i, mapState)
                    if var == varVis[mapState]:
                        # TODO: here, possibly remove self-loop(s) in mapState
                        # in case of identical variables (ta, intersectoid)
                        continue
                    newState = f"{mapState}-{var}"
                    if newState in result.transitions:
                        edge.children[idx + i] = newState
                    result.transitions[newState] = {}
                    edge.children[idx + i] = newState
                    newEdge = TTransition(newState, TEdge('LH', [], var), [mapState, mapState])
                    helper.counter += 1
                    key = f"temp_{helper.counter2}"
                    helper.counter2 += 1
                    result.transitions[newState][key] = newEdge

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

                # for state in mapping
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


def exportUBDA(result: TTreeAut, state:str, edgePart: list, box: TTreeAut, helper: FoldingHelper):
    if helper.png or helper.vtf:
        temp = f"{state}-{edgePart[1]}:{box.name}-{edgePart[2]}"
        temp = f"{helper.counter}-{temp}"
        if helper.path is None:
            path = f"results/{helper.name}/ubdas/{temp}"
        else:
            path = f"{helper.path}/ubdas/{temp}"
        if helper.vtf:
            exportTAtoVTF(result, format='f', filePath=f"{path}.vtf")
        if helper.png:
            exportToFile(result, path)
        helper.counter += 1
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
    for edge in transitions(ta):
        newBoxArray = []
        for box in edge.info.boxArray:
            if type(box) == type(TTreeAut):
                newBoxArray.append(box.name)
            else:
                newBoxArray.append(box)
        edge.info.boxArray = newBoxArray


def createVariableVisibilityCache(ta: TTreeAut) -> dict:
    result = {state: "" for state in ta.getStates()}
    for state in ta.getStates():
        for edge in ta.transitions[state].values():
            if edge.info.variable != "":
                result[state] = edge.info.variable
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

# End of folding.py
