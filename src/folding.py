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
    state = f"({e1[0]}, {e2[0]})"
    symb = e2[1].label
    var = f",{e1[1].variable}" if e1[1].variable != "" else ""

    children = f""
    for i in range(len(e1[2])):
        children += f"({e1[2][i]},{e2[2][i]}),"
    children = children[:-1]

    key = f"{state}-<{symb}{var}>-({children})"
    return key


# Funtion produces an intersectoid from the 'ta' UBDA and 'box' TA.
# This intersectoid is used in boxFinding() to determine the result mapping.
def createIntersectoid(ta: TTreeAut, box: TTreeAut, root: str) -> TTreeAut:

    resultTransitions = {}
    for boxEdge in transitions(box):
        for taEdge in transitions(ta):
            if len(taEdge[2]) != len(boxEdge[2]):
                continue

            # skipping edges with already applied reductions
            skip = False
            for b in taEdge[1].boxArray:
                if b is not None:
                    skip = True
            if skip:
                continue

            # skipping different labeled edges (except the output port edges)
            aSymb = taEdge[1].label
            bSymb = boxEdge[1].label
            aVar = taEdge[1].variable
            if aSymb != bSymb and not bSymb.startswith("Port"):
                continue

            state = (taEdge[0], boxEdge[0])
            key = intersectoidEdgeKey(taEdge, boxEdge)
            if state not in resultTransitions:
                resultTransitions[state] = {}

            children = [(taEdge[2][i], boxEdge[2][i])
                        for i in range(len(taEdge[2]))]
            edge = [state, TEdge(bSymb, [], aVar), children]
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
    result = {e[1].label: []
              for e in transitions(ta)
              if e[1].label.startswith("Port")}
    for edge in transitions(ta):
        symb = edge[1].label
        if not symb.startswith("Port"):
            continue
        result[symb].append(edge[0])
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
    # print(A)
    A = trim(A)  # additional functionality maybe needed?
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
    print(result)
    fillBoxArrays(result)
    reductions = 0
    # boxes.reverse()
    for boxName in boxes:
        box = boxCatalogue[boxName]
        # print(box.name)
        for state in iterateDFS(result):
            edgesToChildren = prepareEdgeInfo(result, state)
            for edge in edgesToChildren:
                # edge = [key, child-index, child]

                if isAlreadyReduced(result, state, edge):
                    continue
                mapping = boxFinding(result, box, edge[2])
                # print(f"boxFinding({box.name}, {state}, {edge[2]}[{edge[1]}]) = {mapping}")

                # applying reduction HERE
                if mapping != {}:
                    reductions += 1
                    e = result.transitions[state][edge[0]]
                    boxList = e[1].boxArray
                    symbol = e[1].label
                    tempBoxArray = [None] * ta.getSymbolArityDict()[symbol]
                    for idx in range(len(boxList)):
                        tempBoxArray[idx] = boxList[idx]
                    tempBoxArray[edge[1]] = box
                    e[1].boxArray = tempBoxArray
                    idx = getStateIndexFromBoxIndex(e, edge[1])
                    e[2].pop(idx)
                    for i, mapState in enumerate(mapping.values()):
                        e[2].insert(idx + i, mapState)
                    # print(e[2])
                    print(result)
    for i in result.transitions.values():
        for e in i.values():
            print(e)
    result = removeUselessStates(result)
    print(result)
    return result


def getStateIndexFromBoxIndex(edge: list, idx: int) -> int:
    if idx >= len(edge[1].boxArray):
        raise Exception("getStateIndexFromBoxIndex(): idx out of range")
    result = 0
    for i, box in enumerate(edge[1].boxArray):
        if i == idx:
            return result
        result += box.portArity
    raise Exception("getStateIndexFromBoxIndex(): idx out of range")


def fillBoxArrays(ta: TTreeAut):
    arities = ta.getSymbolArityDict()
    for edge in transitions(ta):
        if edge[1].boxArray == []:
            edge[1].boxArray = [None] * len(edge[2])
        else:
            boxlen = len(edge[1].boxArray)
            symlen = arities[edge[1].label]
            if boxlen != symlen:
                edge[1].boxArray.extend([None] * (symlen - boxlen))


# NOTE: might be buggy (consider different index in edgeInfo and boxes with
# different port arities)
def isAlreadyReduced(ta: TTreeAut, state: str, edgeInfo: list) -> bool:
    edge = ta.transitions[state][edgeInfo[0]]  # edgeInfo[0] = key
    idx = edge[2].index(edgeInfo[2])
    # if box is None => short edge => arity = 1 (1 target state)
    arities = [(box, box.portArity) if box is not None else (None, 1) for box in edge[1].boxArray]

    i = 0
    for tuple in arities:
        if idx < i + tuple[1]:
            if tuple[0] is not None:
                # print(f"TRUE : st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge[2]}, arities = {[i[1] for i in arities]}")
                return True
            else:
                # print(f"FALSE: st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge[2]}, arities = {[i[1] for i in arities]}")
                return False
        i += tuple[1]

    # print(f"FALSE: st = {state}, tgt = {edgeInfo[2]} [{edgeInfo[1]}], edgeChildren = {edge[2]}, arities = {[i[1] for i in arities]}")
    return False


def prepareEdgeInfo(ta: TTreeAut, state: str) -> list:
    result = []
    for key, edge in ta.transitions[state].items():
        for i in range(len(edge[2])):
            result.append([key, i, edge[2][i]])
    return result

# End of folding.py
