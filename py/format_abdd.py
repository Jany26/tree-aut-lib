# format_abdd.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_classes import *
from copy import deepcopy
from test_data import boxCatalogue
import os
from pathlib import Path

# @ABDD     # Automata-based reduction BDDs
# %Name example-abdd
# %Vars 100
# %Root 1
def ABDDpreamble(ta: TTreeAut, file, name: str):
    file.write("@ABDD\n")
    file.write(f"# imported from {ta.name}\n")
    finalName = ta.name if name == "" else name
    file.write(f"%Name {finalName}\n")
    maxVar = ta.getVariableOrder()[-1]
    file.write(f"%Vars {maxVar[ta.metaData.variablePrefix:]}\n")
    file.write(f"%Root {ta.rootStates[0][ta.metaData.statePrefix:]}\n\n")


# 1[0] (2, 3)[HPort] 3[X] # this denotes node id 1 with variable x0 going 
# over L to nodes id 2, id 3 with applying the reduction rule HPort (box with arity 2) 
# and over H to node id 3 applying reduction rule X (arity 1)
# 1[0] 2 3     # this denotes node id 1 with variable x0 going 
# over L (low) to node id 2 and over H (high) to node id 3
# 2[4] <0> 3   # in this case the node has variable x4, L goes to leaf *0*, and H goes to 3
# 3[6] <1> <0> # L goes to leaf *1* and H goes to leaf *0*
def ABDDtransition(ta: TTreeAut, edge: TTransition) -> str:
    def writeChild(ta, child) -> str:
        stateStr = f"{child}"
        if child in ta.getOutputStates():
            stateStr = "<" + ta.getOutputEdges(inverse=True)[child][0] + ">"
        return stateStr

    edgeString = ""
    if edge.src in ta.getOutputStates():
        return ""
    var = edge.info.variable[ta.metaData.variablePrefix:]
    edgeString += f"{edge.src}[{var}] "
    arity = 1
    childIndex = 0
    boxStr = ""
    for box in edge.info.boxArray:
        if box is not None and box != "_":
            arity = boxCatalogue[f"{box}"].getPortArity()
            boxStr = f"[{box[3:]}]" if box.startswith("box") else box
        if arity == 1:
            edgeString += writeChild(ta, edge.children[childIndex])
        if arity > 1:
            edgeString += f"("
            for idx in range(len(edge.children[childIndex:arity-1])):
                edgeString += writeChild(ta, edge.children[idx + childIndex])
                if idx < childIndex + arity:
                    edgeString += ', '
            edgeString += ')'
        childIndex += arity
        edgeString += boxStr
        edgeString += ' '
    edgeString = edgeString[:-1]
    return edgeString


def exportTAtoABDD(ta: TTreeAut, filePath: str, name="", comments=False):
    # variables are expected to have the same prefix
    # DAG as the input is assumed (output states with no transitions)
    # boxArray is expected to contain only strings (box names)
    taCopy = deepcopy(ta)
    taCopy.reformatKeys()
    taCopy.reformatStates(prefix='', startFrom=1)
    taCopy.metaData.recompute()
    file = open(filePath, 'w')
    ABDDpreamble(taCopy, file, name)
    edgeStringMaxLen = 0
    for edge in iterateEdges(taCopy):
        edgeLen = len(ABDDtransition(taCopy, edge))
        if edgeStringMaxLen < edgeLen:
            edgeStringMaxLen = edgeLen
    for state in iterateStatesBFS(taCopy):
        for edge in taCopy.transitions[state].values():
            edgeString = ABDDtransition(taCopy, edge)
            file.write(edgeString)
            if comments:
                file.write((edgeStringMaxLen - len(edgeString)) * ' ')
                file.write(f" # {edge}")
            if comments or edgeString != "":
                file.write('\n')

def importTAfromABDD(source) -> TTreeAut | list:
    # print(source)
    file = open(source, "r")
    name = Path(source).stem
    # ta = createTAfromABDD(file, name)
    results = []
    positions = []
    i = 0
    for l in file:
        if l.startswith("@BDD") or l.startswith("@ABDD"):
            positions.append(i)
        i += len(l)
    for pos in positions:
        file.seek(pos)
        results.append(createTAfromABDD(file, name))
    if len(results) == 1:
        return results[0]
    return results


def createTAfromABDD(file, name) -> TTreeAut:
    ta = TTreeAut([], {}, name)
    leaves = set()
    keyCounter = 0
    preamble = False
    for l in file:
        line = l.split('#')[0]  # strip comments
        line = line.strip()  # strip leading and trailing whitespaces
        if line == "":
            continue
        data = line.split()
        if line.startswith('@'):
            if line != "@ABDD" and line != "@BDD":
                raise Exception(f"importTAfromABDD(): unexpected header: {line}")
            if preamble:
                break
            else:
                preamble = True
                continue
        if line.startswith('%'):
            if data[0] not in ["%Name", "%Vars", "%Root"]:
                raise Exception(f"importTAfromABDD(): unexpected metadata: {data[0]}")
            if data[0] == "%Name":
                ta.name = data[1]
            if data[0] == "%Vars":
                maxVar = int(data[1])
            if data[0] == "%Root":
                ta.rootStates.append(data[1])
            continue
        if line == "":
            continue
        src, var = data[0].rstrip(']').split('[')
        if data[1].endswith(']'):
            child1, box1 = data[1].rstrip(']').split('[')
            if box1 == "":
                box1 = None
        else:
            child1, box1 = data[1], None
        if data[2].endswith(']'):
            child2, box2 = data[2].rstrip(']').split('[')
            if box2 == "":
                box2 = None
        else:
            child2, box2 = data[2], None
        edge = TTransition(src, TEdge('LH', [box1, box2], var), [child1, child2])
        if src not in ta.transitions:
            ta.transitions[src] = {}
        ta.transitions[src][f"k{keyCounter}"] = edge
        keyCounter += 1
        for state in [src, child1, child2]:
            if state.startswith('<') and state.endswith('>'):
                leaves.add(state)
    # print(ta)
    for leaf in leaves:
        symbol = leaf.lstrip("<").rstrip(">")
        edge = TTransition(leaf, TEdge(symbol, [], ""), [])
        ta.transitions[leaf] = {}
        ta.transitions[leaf][f"k{keyCounter}"] = edge
        keyCounter += 1

    return ta
   

    

# End of file format_abdd.py
