from multiprocessing.sharedctypes import Value
import sys
import copy
from ta_classes import *


# boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']
boxOrder = ['L0', 'L1', 'H0', 'H1', 'LPort', 'HPort', 'X']


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# sorts the state names while ignoring the prefix
def stateNameSort(stateList: list) -> list:
    if stateList == []:
        return []
    
    prefixLen = 0
    for i in range(len(stateList[0])):
        if not stateList[0][i:].isnumeric():
            prefixLen += 1
    prefix = stateList[0][:prefixLen]
    try:
        myList = [int(i.lstrip(prefix)) for i in stateList]
        myList.sort()
        myList = [f"{prefix}{i}" for i in myList]
    except ValueError:
        myList = [i for i in stateList]
    return myList


def createVarOrder(prefix: str, count: int):
    return [f"{prefix}{i+1}" for i in range(count)]


# This is strictly for compacting the UBDA before output for testing purposes.
# Instead of many identical edges (with just different variables),
# the edges are merged into one where variables are compacted into one string.
# This provides much more readable format.
# Only use this function before outputting the UBDA.
def compressVariables(ta: TTreeAut) -> TTreeAut:
    temp = {}
    for edgeDict in ta.transitions.values():
        for edge in edgeDict.values():
            # boxNames parsing for the key:
            boxesStr = ""
            for box in edge.info.boxArray:
                if box is None:
                    boxName = "_"
                else:
                    boxName = box if type(box) == str else box.name
                    if boxName.startswith("box"):
                        boxName = boxName[len("box"):]
                boxesStr += "," + boxName
            boxesStr.lstrip(",")
            # end fo boxNames parsing
            tempKey = f"{edge.src}-{edge.info.label}{boxesStr}-{edge.children}"
            if tempKey not in temp:
                temp[tempKey] = [[], []]
            temp[tempKey][0] = [
                edge.src,
                edge.info.label,
                edge.info.boxArray,
                edge.children
            ]
            temp[tempKey][1].append(edge.info.variable)

    transitions = {}
    for key, edgeData in temp.items():
        src = edgeData[0][0]
        symb = edgeData[0][1]
        boxArray = edgeData[0][2]
        children = edgeData[0][3]
        vars = ",".join(edgeData[1])
        edge = TEdge(symb, boxArray, vars)
        if src not in transitions:
            transitions[src] = {}
        transitions[src][key] = TTransition(src, edge, children)
    result = TTreeAut(ta.rootStates, transitions, f"{ta.name}", ta.portArity)
    return result
