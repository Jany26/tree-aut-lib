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

def exportTreeAutToTMB(ta: TTreeAut, fileName:str):
    pass


# End of file format_tmb.py
