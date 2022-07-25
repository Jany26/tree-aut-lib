# format_vtf.py
# Functions for loading/saving tree automaton from/to VATA format (.vtf)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# import sys
# import os
from ta_functions import *
import re
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def loadRootsFromVTF(line: str) -> list:
    return [i for i in line.strip().split() if i != "%Root"]


def loadStatesFromVTF(line: str) -> list:
    words = line.strip().split()
    return [i.split(":")[0].strip() for i in words if i != "%States"]


def loadArityFromVTF(line: str) -> dict:
    words = line.strip().split()
    result = {}

    for i in words:
        if i.startswith("%Alphabet"):
            continue
        items = i.split(":")
        symbol = str(items[0].strip())
        arity = int(items[1].strip())
        result[symbol] = arity
    return result

# def loadTransitionFromVTF(line:str, taType='ta') -> list:
#     line = line.strip()
#     if line == "":
#         return []
#     words = line.split()
#     state = words.pop(0)
#     symbol = words.pop(0)

#     children = []
#     for i in words[0:]:
#         temp = words.pop(0)
#         if i == "(": continue
#         if i == ")": break
#         children.append(str(temp))

#     boxes = []
#     if words != [] and words[0] == "[":
#         for i in words[0:]:
#             temp = words.pop(0)
#             if i == "[": continue
#             if i == "]": break
#             boxes.append(str(temp)) if i != "_" else boxes.append(None)

#     var = str(words.pop()) if words != [] else ""
#     # print([state, TEdge(symbol, boxes, var), children])
#     return [state, TEdge(symbol, boxes, var), children]


def processEdge(edgeInfo: list) -> Tuple[list, str]:
    if len(edgeInfo) == 0:
        return [], ""

    string = " ".join(edgeInfo)
    string = string.lstrip("<").lstrip().rstrip(">").rstrip()
    boxesMatch = re.search("\[.*\]", string)

    boxes = []
    varString = ""

    if boxesMatch:
        matchString = boxesMatch.group(0)
        boxArrayString = matchString.lstrip("[").rstrip("]")
        varString = string.replace(matchString, "")
        boxArray = boxArrayString.lstrip().rstrip().split()

        varString = varString.lstrip().rstrip()
        boxes = [str(box) if box != "_" else None for box in boxArray]
    else:
        varString = string

    return boxes, varString


def loadTransitionFromVTF(line: str, taType='ta') -> list:
    line = line.strip()
    if line == "":
        return []
    words = line.split()
    state = words.pop(0)
    symbol = words.pop(0)

    edgeInfo = []
    for i in words[0:]:
        if i.startswith("("):
            break
        edgeInfo.append(i)
        words.pop(0)
    boxes, var = processEdge(edgeInfo)

    restOfString = " ".join(words[0:])
    # print(restOfString)
    restOfString = restOfString.rstrip().lstrip("(").rstrip(")")
    children = restOfString.split()
    # for i in words[0:]:
    #     temp = words.pop(0)
    #     if i == "(": continue
    #     if i == ")": break
    #     children.append(str(temp))

    return [state, TEdge(symbol, boxes, var), children]


def consistencyCheck(data: list, allStates: list, arityDict: dict):
    if data[0] not in allStates:
        raise Exception(f"consistencyCheck(): src state '{data[0]}' not in preamble")
    if data[1].label not in arityDict:
        raise Exception(f"consistencyCheck(): symbol '{data[1]}' not in preamble")
    if len(data[2]) != arityDict[data[1].label]:
        raise Exception(f"consistencyCheck(): inconsistent arity for symbol '{data[1].label}'")
    for i in data[2]:
        if i not in allStates:
            raise Exception(f"consistencyCheck(): child state '{i}' not in preamble")


def consistencyCheckTMB(edges, states, arities, verbose=False) -> bool:
    # print(states)
    for stateName, edgeDict in edges.items():

        if stateName not in states:
            if verbose:
                print(f"{stateName} not in states = {states}")
            return False

        for edgeData in edgeDict.values():
            if (edgeData[0] not in states
                or edgeData[1].label not in arities
                or len(edgeData[2]) != int(arities[edgeData[1].label])
                ):
                if verbose:
                    if edgeData[0] not in states:
                        print(f"edge[0] = {edgeData[0]} not in states = [{states}]")
                    elif edgeData[1].label not in arities:
                        print(f"edge[1].label = {edgeData[1].label} not in arities = [{arities}]")
                    else:
                        print(f"children = {edgeData[2]} inconsistent with arity of {edgeData[1].label} = {int(arities[edgeData[1].label])}")
                    print(f"EDGE = {edgeData}")
                return False
            for child in edgeData[2]:
                if child not in states:
                    if verbose:
                        print(f"child {child} not in states = {states}")
                        print(f"EDGE = {edgeData}")
                    return False
    return True


def generateKeyFromEdge(edge: list) -> str:
    children = ""
    for i in range(len(edge[2])):
        children += str(edge[2][i])
        if i < len(edge[2])-1:
            children += ","
    # children.rstrip(",")
    return f"{edge[0]}-{edge[1].label}-[{children}]"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VTF IMPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def importTAfromVTF(source, sourceType='f', taType='ta') -> TTreeAut:
    if sourceType == 'f':
        file = open(source, "r")
        autName = source.split(os.sep)[len(source.split(os.sep)) - 1][:-4]
    elif sourceType == 's':
        file = source.split('\n')
        autName = "unnamed"
    else:
        Exception("importTAfromVTF(): unsupported sourceType (only 'f'/'s')")

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
                raise Exception(f"importTAfromVTF(): unexpected structure format {line}")
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
                raise Exception(f"importTAfromVTF(): unexpected preamble '{line}'")
        else:
            edge = loadTransitionFromVTF(line, taType)
            if edge == []:
                continue
            # checking state and arity consistency - comparing with data from "preamble"
            key = generateKeyFromEdge(edge)
            if str(edge[0]) not in transitions:
                transitions[str(edge[0])] = {}
            transitions[str(edge[0])][key] = edge
    if not rootsProcessed:
        raise Exception(f"importTAfromVTF(): List of root states missing")
    if arityProcessed and stateListProcessed:
        if not consistencyCheckTMB(transitions, allStates, arityDict, verbose=True):
            raise Exception(f"importTAfromVTF(): inconsistent data with the preamble")

    if sourceType == 'f':
        file.close()
    result = TTreeAut(rootStates, transitions, str(autName))
    result.portArity = result.getPortArity()
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF - HELPER FUNCTIONS (FILE)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writeRootsVTFfile(roots, tgt):
    tgt.write("%Root")
    for root in roots:
        tgt.write(f" {root}")
    tgt.write("\n")


def writeStatesVTFfile(states, tgt):
    tgt.write("%States")
    for i in states:
        tgt.write(f" {i}:0")
    tgt.write("\n")


def writeAritiesVTFfile(arities, tgt):
    tgt.write("%Alphabet")
    for symbol in arities:
        tgt.write(f" {symbol}:{arities[symbol]}")
    tgt.write("\n\n")


def writeEdgesVTFfile(edges, tgt):
    for edge in edges.values():
        for data in edge.values():
            tgt.write(f"{data[0]} {data[1].label} (")
            for child in data[2]:
                tgt.write(f" {child}")
            tgt.write(" )\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF - HELPER FUNCTIONS (STRING)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writeRootsVTFstr(roots):
    result = "%Root"
    for i in roots:
        result += f" {i}"
    result += "\n"
    return result


def writeStatesVTFstr(states):
    result = "%States"
    for i in states:
        result += f" {i}:0"
    result += "\n"
    return result


def writeAritiesVTFstr(arities):
    result = "%Alphabet"
    for symbol in arities:
        result += f" {symbol}:{arities[symbol]}"
    result += "\n\n"
    return result


def writeEdgesVTFstr(edges):
    result = "# Transitions\n\n"
    for edge in edges.values():
        for data in edge.values():
            result += f"{data[0]} {data[1].label} ("
            for i in data[2]:
                result += f" {i}"
            result += " )\n"
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def exportTAtoVTF(ta: TTreeAut, format, fileName=""):
    if format != 'f' or format != 's':
        Exception("exportTAtoVTF(): unsupported format")

    if format == 'f' and fileName == "":
        Exception("exportTAtoVTF(): fileName needed")

    result = open(fileName, "w") if format == 'f' else ""

    if format == 'f':
        result.write("@NTA\n")
        result.write(f"# Automaton {ta.name}\n")
        writeRootsVTFfile(ta.rootStates, result)
        writeStatesVTFfile(ta.getStates(), result)
        writeAritiesVTFfile(ta.getSymbolArityDict(), result)
        writeEdgesVTFfile(ta.transitions, result)
        result.close()
    else:
        result += "@NTA\n"
        result += f"# Automaton {ta.name}\n"
        result += writeRootsVTFstr(ta.rootStates)
        result += writeStatesVTFstr(ta.getStates())
        result += writeAritiesVTFstr(ta.getSymbolArityDict())
        result += writeEdgesVTFstr(ta.transitions)
        return result
    return

# End of file format_vtf.py
