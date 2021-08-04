# format_tmb.py
# Functions for exporting tree automaton into TMB format (.tmb) 
# for generating a graphical representation of the TA.
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>


from format_vtf import *
from ta_classes import *

def loadTransitionFromTMB(line:str) -> list:
    line = line.strip()
    transitionData = line.split("->")
    srcState = transitionData[1].strip()
    rest = transitionData[0].strip()
    transitionData = rest.split("(", 1)
    if len(transitionData) != 1:
        symbol = transitionData[0].strip()
        childStates = transitionData[1].strip()
        childStates = childStates[:-1].split(',')
    else:
        symbol = transitionData[0].strip()
        childStates = []
    return [srcState, TEdge(symbol, [None] * len(childStates), ""), childStates]    

def loadArityFromTMB(line:str) -> dict:
    words = line.strip().split()
    
    result = {}
    for i in words[1:]:
        items = i.split(":")
        symbol = str(items[0].strip())
        arity = int(items[1].strip())
        result[symbol] = arity
    return result

def consistencyCheckTMB(states, arities, edges) -> bool:
    # print(states)
    for stateName, edgeDict in edges.items():
        if stateName not in states:
            return False
        for edgeData in edgeDict.values():
            if (edgeData[0] not in states
                or edgeData[1].label not in arities
                or len(edgeData[2]) != arities[edgeData[1].label]
            ):
                return False
            for child in edgeData[2]:
                if child not in states:
                    return False
    return True

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def importTreeAutFromTMB(fileName:str) ->TTreeAut:
    file = open(fileName, "r")

    arityDict = {}
    rootStates = []
    transitionDict = {}
    allStates = []
    rootsProcessed = False
    arityProcessed = False
    stateListProcessed = False
    transitionProcessing = False

    for line in file:
        if transitionProcessing and not line.startswith('\n'):
            edge = loadTransitionFromTMB(line)
            if edge == []:
                continue
            if arityProcessed and stateListProcessed:
                consistencyCheck(edge, allStates, arityDict)
            key = generateKeyFromEdge(edge)
            if str(edge[0]) not in transitionDict:
                transitionDict[str(edge[0])] = {}
            transitionDict[str(edge[0])][key] = edge
            continue

        if line.startswith("#") or line.startswith("//") or line.startswith("\n"):
            continue
        elif line.startswith("Automaton"):
            continue
        elif line.startswith("Ops"):
            arityDict = loadArityFromTMB(line)
            arityProcessed = True
            # print(arityDict)
        elif line.startswith("States"):
            words = line.strip().split()
            allStates = [i.split(":")[0].strip() for i in words[1:]]
            stateListProcessed = True
            # print(allStates)
        elif line.startswith("Final States"):
            words = line.strip().split()
            rootStates = [str(i.strip()) for i in words[2:]]
            rootsProcessed = True
            # print(rootStates)
        elif line.startswith("Transitions"):
            transitionProcessing = True
        else:
            raise Exception(f"Unknown items in TMB file")
    # end for loop

    if arityProcessed and stateListProcessed:
        if not consistencyCheckTMB(allStates, arityDict, transitionDict):
            raise Exception(f"Inconsistent transition data with info in preamble")

    if not rootsProcessed:
        print("exception J")
        raise Exception(f"List of root states missing")
    return TTreeAut(rootStates, transitionDict)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def writeAritiesTMB(arities, file):
    file.write("Ops")
    for i in arities:
        file.write(f" {i}:{arities[i]}")
    file.write("\n\n")

def writeStatesTMB(states, file):
    file.write("States")
    for i in states:
        file.write(f" {i}:0")
    file.write("\n\n")

def writeRootsTMB(states, file):
    file.write("Final States")
    for i in states:
        file.write(f" {i}")
    file.write("\n\n")

def writeTransitionTMB(edge, file):
    file.write(f"{edge[1].label}(")
    arity = len(edge[2])
    for i in range(arity):
        file.write(f"{edge[2][i]}")
        if i < arity - 1:
            file.write(",")
    file.write(f") -> {edge[0]}\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def exportTreeAutToTMB(ta: TTreeAut, fileName:str):
    file = open(fileName, "w")
    writeAritiesTMB(ta.getSymbolArityDict(), file)
    
    file.write("Automaton ")
    file.write(f"{ta.name}") if ta.name != "" else file.write("Unknown_Name")
    file.write("\n\n")
    
    writeStatesTMB(ta.getStates(), file)
    writeRootsTMB(ta.rootStates, file)
    file.write("Transitions\n")
    
    for transitionDict in ta.transitions.values():
        for edge in transitionDict.values():
            writeTransitionTMB(edge, file)

    file.write("\n\n")
    file.close()
    pass


# End of file format_tmb.py
