import sys
import copy
from ta_classes import *


# boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']
boxOrder = ['L0', 'L1', 'H0', 'H1', 'LPort', 'HPort', 'X']
testVarOrder = [f"x{i+1}" for i in range(10)]
testVarOrder5 = [f"x{i+1}" for i in range(5)]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Creates a better readable state names for more clear images (DOT).
# Useful after unfolding, determinization/normalization, etc.
def tidyUpNames(ta: TTreeAut, prefix='q'):
    result = copy.deepcopy(ta)
    temp = {}
    i = 0
    for state in iterateBFS(ta):
        if state not in temp:
            temp[state] = i
            i += 1

    for state, idx in temp.items():
        result.renameState(state, f"temporaryName{idx}")
    for idx in temp.values():
        result.renameState(f"temporaryName{idx}", f"{prefix}{idx}")
    return result


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
    result = TTreeAut(ta.rootStates, transitions, f"compressed({ta.name})", ta.portArity)
    return result
