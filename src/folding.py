from sre_parse import State
from ta_classes import *
from ta_functions import *
from test_data import *


from collections import deque


# TBD
def trim(ta: TTreeAut) -> TTreeAut:
    workTA = removeUselessStates(ta)

    # remove transitions over variables which are clearly unnecessary
    # TODO: define/explain ^^
    # get all paths from roots to leaves ---> make a function

    return workTA


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
def boxFinding(ta: TTreeAut, box: TTreeAut, root: str) -> dict:
    A = createIntersectoid(ta, box, root)
    A = trim(A)  # additional functionality maybe needed?
    # print("intersectoid")
    # print(A)
    tree, string = nonEmptyBU(A)
    # ^^ this is based on the rootDistances of nodes from "ports"
    if tree is None:
        return {}

    mapping = portToStateMapping(A)
    maxMapping = getMaximalMapping(A, mapping)
    finalMapping = {i: j for i, (j, _) in maxMapping.items()}
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
                mapping = boxFinding(result, box, edgeInfo[2])
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
    result = removeUselessStates(result)
    stringifyBoxes(result)
    return result


def stringifyBoxes(ta:TTreeAut):
    for edge in transitions(ta):
        newBoxArray = []
        for box in edge.info.boxArray:
            if type(box) == type(TTreeAut):
                newBoxArray.append(box.name)
            else:
                newBoxArray.append(box)
        edge.info.boxArray = newBoxArray
            


def getStateIndexFromBoxIndex(edge: list, idx: int) -> int:
    if idx >= len(edge.info.boxArray):
        raise Exception("getStateIndexFromBoxIndex(): idx out of range")
    result = 0
    for i, box in enumerate(edge.info.boxArray):
        if i == idx:
            return result
        result += box.portArity
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


# NOTE: might be buggy (consider different index in edgeInfo and boxes with
# different port arities)
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


def prepareEdgeInfo(ta: TTreeAut, state: str) -> list:
    result = []
    for key, edge in ta.transitions[state].items():
        for i in range(len(edge.children)):
            result.append([key, i, edge.children[i]])
    return result

# End of folding.py
