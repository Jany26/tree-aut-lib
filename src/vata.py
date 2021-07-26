# vata.py
# Functions for loading/saving tree automaton from/to VATA format (.vtf)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# import sys
# import os
from taLib import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# helper functions


def loadRootsFromVTF(line:str) -> list:
    words = line.strip()
    result = []

    if not line.startswith("%Root"):
        raise Exception("unexpected preamble")

    words = line.split()
    for i in words:
        if i.startswith("%Root"):
            continue
        result.append(i)
    return result



def loadStatesFromVTF(line:str) -> list:
    words = line.strip()
    result = []

    if not line.startswith("%States"):
        raise Exception("unexpected preamble")

    words = line.split()
    for i in words:
        if i.startswith("%States"):
            continue
        items = i.split(":")
        result.append(str(items[0].strip()))
    return result



def loadArityFromVTF(line:str) -> dict:
    words = line.strip()
    result = {}

    if not line.startswith("%Alphabet"):
        raise Exception("unexpected preamble")

    words = line.split()
    for i in words:
        if i.startswith("%Alphabet"):
            continue
        items = i.split(":")
        symbol = str(items[0].strip())
        arity = int(items[1].strip())
        result[symbol] = arity
    return result



def loadTransitionFromVTF(line:str) -> list:
    line = line.strip()
    if line == "":
        return []
    words = line.split()
    state = words[0]
    symbol = words[1]
    children = []
    for i in words[2:]:
        if i == "(" or i == ")":
            continue
        else:
            children.append(str(i))
    return [state, symbol, children]


def consistencyCheck(data:list, allStates:list, arityDict:dict):
    # for stateName, edgeDict in transitions.items():
    #     if stateName not in allStates:
    #         raise Exception(f"state '{stateName}' not in preamble")
    #     for data in edgeDict.values():
    if data[0] not in allStates:
        raise Exception(f"state '{data[0]}' not in preamble")
    if data[1] not in arityDict:
        raise Exception(f"symbol '{data[1]}' not in preamble")
    if len(data[2]) != arityDict[data[1]]:
        raise Exception(f"inconsistent arity for symbol '{data[1]}'")
    for i in data[2]:
        if i not in allStates:
            raise Exception(f"state '{i}' not in preamble")



def generateKeyFromEdge(edge:list) -> str:
    children = ""
    for i in edge[2]:
        children += str(i)
        children += ", "
    children.rstrip(", ")  
    key = f"{edge[0]}-{edge[1]}-[{children}]"
    return key


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def loadAutomatonFromFile(fileName) -> TTreeAut:
    file = open(fileName, "r")

    arityDict = {}
    rootStates = []
    transitions = {}
    allStates = []
    rootsProcessed = False
    arityProcessed = False
    stateListProcessed = False

    for line in file:
        if line.startswith("#"):
            continue
        parts = line.split("#")
        line = parts[0]
        if line.startswith("@"):
            if not line.startswith("@NTA"):
                raise Exception(f"unexpected format {line}")
        elif line.startswith("%"):
            if line.startswith("%Root"):
                rootStates = loadRootsFromVTF(line)
                rootsProcessed = True
            elif line.startswith("%Alphabet"):
                arityDict = loadArityFromVTF(line)
                arityProcessed = True
            elif line.startswith("%States"):
                allStates = loadStatesFromVTF(line)
                stateListProcessed = True
            else:
                raise Exception(f"unexpected preamble '{line}'")
        else:
            edge = loadTransitionFromVTF(line)
            if edge == []:
                continue
            if arityProcessed and stateListProcessed:
                consistencyCheck(edge, allStates, arityDict)
            key = generateKeyFromEdge(edge)
            if str(edge[0]) not in transitions:
                transitions[str(edge[0])] = {}
            transitions[str(edge[0])][key] = edge
    if not rootsProcessed:
        raise Exception(f"List of root states missing")
    
    file.close()
    
    # # checking state and arity consistency - comparing with data from "preamble"
    return TTreeAut(rootStates, transitions)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# helper functions


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def saveAutomatonToFile(fileName:str, treeAut:TTreeAut):
    file = open(fileName, "w")
    file.write()
    
    
    file.close()
    return


# End of file vata.py
