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
        print("exception A")
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
        print("exception B")
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
        print("exception C")
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
    if data[0] not in allStates:
        print("exception D")
        raise Exception(f"state '{data[0]}' not in preamble")
    if data[1] not in arityDict:
        print("exception E")
        raise Exception(f"symbol '{data[1]}' not in preamble")
    if len(data[2]) != arityDict[data[1]]:
        print("exception F")
        raise Exception(f"inconsistent arity for symbol '{data[1]}'")
    for i in data[2]:
        if i not in allStates:
            print("exception G")
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
                print("exception H")
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
                print("exception I")
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
        print("exception J")
        raise Exception(f"List of root states missing")
    
    file.close()
    
    # # checking state and arity consistency - comparing with data from "preamble"
    return TTreeAut(rootStates, transitions)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# helper functions


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def saveAutomatonToFile(fileName:str, ta:TTreeAut):
    file = open(fileName, "w")
    file.write("@NTA\n")

    file.write("%Root")
    for root in ta.rootStates:
        file.write(f" {root}")
    file.write("\n")
    
    states = ta.getStates()
    file.write("%States")
    for i in states:
        file.write(f" {i}")
    file.write("\n")

    arityDict = ta.getSymbolArityDict()
    file.write("%Alphabet")
    for symbol in arityDict:
        file.write(f" {symbol}:{arityDict[symbol]}")
    file.write("\n\n")
    
    for edge in ta.transitions.values():
        for data in edge.values():
            file.write(f"{data[0]} {data[1]} (")
            for child in data[2]:
                file.write(f" {child}")
            file.write(" )\n")
            
    file.close()
    return


# End of file vata.py
