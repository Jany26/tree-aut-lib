from sre_parse import State
from ta_classes import *
from ta_functions import *
from test_data import *

from normalization import compressVariables


# TBD
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
    var = f",{e1.info.variable}" if e1.info.variable != "" else ""

    children = f""
    for i in range(len(e1.children)):
        children += f"({e1.children[i]},{e2.children[i]}),"
    children = children[:-1]

    key = f"{state}-<{symb}{var}>-({children})"
    return key


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
def createIntersectoid(ta: TTreeAut, box: TTreeAut, root: str) -> TTreeAut:

    resultTransitions = {}
    for boxEdge in transitions(box):
        for taEdge in transitions(ta):
            if len(taEdge.children) != len(boxEdge.children):
                continue

            # skipping edges with already applied reductions
            skip = False
            for b in taEdge.info.boxArray:
                if b is not None:
                    skip = True
            if skip:
                continue

            # skipping different labeled edges (except the output port edges)
            aSymb = taEdge.info.label
            bSymb = boxEdge.info.label
            aVar = taEdge.info.variable
            if aSymb != bSymb and not bSymb.startswith("Port"):
                continue

            state = (taEdge.src, boxEdge.src)
            key = intersectoidEdgeKey(taEdge, boxEdge)
            if state not in resultTransitions:
                resultTransitions[state] = {}

            children = [(taEdge.children[i], boxEdge.children[i])
                        for i in range(len(taEdge.children))]
            edge = TTransition(state, TEdge(bSymb, [], aVar), children)
            resultTransitions[state][key] = edge
    resultRootstates = [(root, b) for b in box.rootStates]
    resultName = f"intersectoid({ta.name}, {box.name}, {root})"
    result = TTreeAut(resultRootstates, resultTransitions,
                      resultName, box.portArity)
    return result


# This function parses an intersectoid and creates a dictionary with all
# port transitions and all states that begin with them.
# input:
# - an intersetoid "TA"
# output:
def portToStateMapping(ta: TTreeAut) -> dict:
    result = {e.info.label: []
              for e in transitions(ta)
              if e.info.label.startswith("Port")}
    for edge in transitions(ta):
        symb = edge.info.label
        if not symb.startswith("Port"):
            continue
        result[symb].append(edge.src)
    return result


# finds a state furthest from the root so that the mapping is "maximal"
# input:
# - an intersectoid "TA",
# - dictionary of ports and states with port output transitions
# output:
def getMaximalMapping(ta: TTreeAut, ports: dict) -> dict:
    mapping = {}
    for port, stateList in ports.items():
        mapping[port] = None
        currentDistance = 0  # state, rootDistance
        for state in stateList:
            dist = ta.getRootDistance(state)
            if dist > currentDistance:
                mapping[port] = state
                currentDistance = dist
        if mapping[port] is None:
            raise Exception(f"getMaximalMapping: {port} mapping not found")
    return mapping


# Main implementation of folding procedure (one step)
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
def boxFinding(ta: TTreeAut, box: TTreeAut, root: str, midResults: list) -> dict:
    A: TTreeAut = createIntersectoid(ta, box, root)
    A = trim(A)  # additional functionality maybe needed?
    # print("intersectoid")
    # print(A)
    tree, string = nonEmptyBU(A)
    # ^^ this is based on the rootDistances of nodes from "ports"
    if tree is None:
        return {}
    B: TTreeAut = copy.deepcopy(A)
    B.name = f"({box.name}, {root})"

    mapping = portToStateMapping(A)
    maxMapping = getMaximalMapping(A, mapping)
    finalMapping = {i: j for i, (j, _) in maxMapping.items()}
   
    # print("\nINTERSECTOID")
    # print(B)
    # print("first", mapping)
    # print("max", maxMapping)
    # print("final", finalMapping, "\n")

    # midResults.append((B, finalMapping))
    return finalMapping


# Main function implementing process of folding.
# Applying separate folding steps implemented in boxFinding() funtion.
# Respects the chosen box order.
# inputs:
#   'ta' - UBDA that we want to apply folding on,
#   'boxes' - ordered list of box names, which can be used to reduce the 'ta'
# output: (folded) UBDA with applied reductions (same language as the input)
def fold(ta: TTreeAut, boxes: list) -> TTreeAut:
    result = copy.deepcopy(ta)
    midResults = []
    fillBoxArrays(result)  # in case of [None, None] and [] discrepancies
    reductions = 0
    for boxName in boxes:
        box = boxCatalogue[boxName]
        for state in iterateDFS(result):
            edgesToChildren = prepareEdgeInfo(result, state)
            for edgeInfo in edgesToChildren:
                # edgeInfo contains three items: [key, child-index, child]

                if isAlreadyReduced(result, state, edgeInfo):
                    continue
                mapping = boxFinding(result, box, edgeInfo[2], midResults)
                # print(f"boxFinding({box.name}, {edgeInfo[2]}) = {mapping}")

                # applying reduction HERE
                if mapping != {}:
                    reductions += 1
                    e = result.transitions[state][edgeInfo[0]]
                    boxList = e.info.boxArray
                    symbol = e.info.label
                    tempBoxArray = [None] * ta.getSymbolArityDict()[symbol]
                    for idx in range(len(boxList)):
                        tempBoxArray[idx] = boxList[idx]
                    tempBoxArray[edgeInfo[1]] = box
                    e.info.boxArray = tempBoxArray
                    idx = getStateIndexFromBoxIndex(e, edgeInfo[1])
                    e.children.pop(idx)
                    for i, mapState in enumerate(mapping.values()):
                        e.children.insert(idx + i, mapState)
                    midResults.append(copy.deepcopy(result))
                    # print(f"\nMID-RESULT {reductions}")
                    # print(f"boxFinding({box.name}, {edgeInfo[2]}) = {mapping}")
                    # print(compressVariables(result))
    result = removeUselessStates(result)
    return result, midResults


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
    for i, box in enumerate(edge.info.boxArray):
        if i == idx:
            return result
        result += box.portArity if box is not None else 1
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
    idx = edge.children.index(edgeInfo[2])
    # if box is None => short edge => arity = 1 (1 target state)
    arities = [(box, box.portArity) if box is not None else (None, 1) for box in edge.info.boxArray]

    i = 0
    for tuple in arities:
        if idx < i + tuple[1]:
            if tuple[0] is not None:
                # print(f"TRUE : st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge.children}, arities = {[i[1] for i in arities]}")
                return True
            else:
                # print(f"FALSE: st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge.children}, arities = {[i[1] for i in arities]}")
                return False
        i += tuple[1]

    # print(f"FALSE: st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge.children}, arities = {[i[1] for i in arities]}")
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
    pathList.sort()  # debug
    for i, j in pathDict.items():  # debug
        print(f"{i}{(6-len(i)) * ' '}: {j}") # debug
    result = []
    for path in pathList:
        result.extend(reversePathDict[path])
    return result


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

# End of folding.py
