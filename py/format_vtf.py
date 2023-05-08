# format_vtf.py
# Functions for loading/saving tree automaton from/to VATA format (.vtf)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# import sys
# import os
from ta_functions import *
import re
import os
# from test_data import boxCatalogue

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


def loadTransitionFromVTF(line: str, taType='ta') -> TTransition:
    line = line.strip()
    if line == "":
        return None
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

    return TTransition(state, TEdge(symbol, boxes, var), children)


def consistencyCheck(data: list, allStates: list, arityDict: dict):
    if data.src not in allStates:
        raise Exception(f"consistencyCheck(): src state '{data.src}' not in preamble")
    if data.info.label not in arityDict:
        raise Exception(f"consistencyCheck(): symbol '{data.info}' not in preamble")
    if len(data.children) != arityDict[data.info.label]:
        raise Exception(f"consistencyCheck(): inconsistent arity for symbol '{data.info.label}'")
    for i in data.children:
        if i not in allStates:
            raise Exception(f"consistencyCheck(): child state '{i}' not in preamble")


# def checkChildrenArity(edge: TTransition, arityDict: dict):
#     # NOTE: cannot be used - cyclical dependencies of initial boxCatalogue imports
#     arity = arityDict[edge.info.label]
#     boxPortCount = 0
#     boxCount = 0
#     for box in edge.info.boxArray:
#         boxCount += 1
#         boxPortCount += boxCatalogue[box].portArity if box is not None else 1
#     if boxCount != arity:
#         return False
#     if boxPortCount != len(edge.children):
#         return False
#     return True


def consistencyCheckVTF(edges, states, arities, verbose=False) -> bool:
    # print(states)
    for stateName, edgeDict in edges.items():

        if stateName not in states:
            if verbose:
                print(f"{stateName} not in states = {states}")
            return False

        for edge in edgeDict.values():
            if (
                edge.src not in states
                or edge.info.label not in arities
                or len(edge.children) != int(arities[edge.info.label])
                # or not checkChildrenArity(edge, arities)
            ):
                if verbose:
                    if edge.src not in states:
                        print(f"edge.src = {edge.src} not in states = [{states}]")
                    elif edge.info.label not in arities:
                        print(f"edge.info.label = {edge.info.label} not in arities = [{arities}]")
                    else:
                        print(f"children = {edge.children} inconsistent with arity of {edge.info.label} = {int(arities[edge.info.label])}")
                    print(f"EDGE = {edge}")
                return False
            for child in edge.children:
                if child not in states:
                    if verbose:
                        print(f"child {child} not in states = {states}")
                        print(f"EDGE = {edge}")
                    return False
    return True


def generateKeyFromEdge(edge: list) -> str:
    children = ""
    for i in range(len(edge.children)):
        children += str(edge.children[i])
        if i < len(edge.children) - 1:
            children += ","
    # children.rstrip(",")
    return f"{edge.src}-{edge.info.label}-[{children}]"

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
                raise Exception(f"importTAfromVTF(): unexpected preamble '{line.strip()}'")
        else:
            edge = loadTransitionFromVTF(line, taType)
            if edge is None:
                continue
            # checking state and arity consistency - comparing with data from "preamble"
            key = generateKeyFromEdge(edge)
            if str(edge.src) not in transitions:
                transitions[str(edge.src)] = {}
            transitions[str(edge.src)][key] = edge
    if not rootsProcessed:
        raise Exception(f"importTAfromVTF(): List of root states missing")
    if arityProcessed and stateListProcessed:
        if not consistencyCheckVTF(transitions, allStates, arityDict, verbose=True):
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
            boxArray = []
            foundBox = False
            for box in data.info.boxArray:
                if box is None:
                    boxArray.append("_")
                else:
                    foundBox = True
                    if type(box) == str:
                        boxArray.append(box)
                    else:
                        boxArray.append(box.name)
            boxString = ""
            if foundBox:
                boxString += "["
                for box in boxArray:
                    boxString += box + " "
                boxString = boxString[:-1]
                boxString += "]"

            edgeString = ""
            if boxArray != [] or data.info.variable != "":
                edgeString = f"<{boxString}"
                if boxString != "":
                    edgeString += " "
                edgeString += f"{data.info.variable}> "
            
            tgt.write(f"{data.src} {data.info.label} {edgeString}(")
            for child in data.children:
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
            result += f"{data.src} {data.info.label} ("
            for i in data.children:
                result += f" {i}"
            result += " )\n"
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def exportTAtoVTF(ta: TTreeAut, filePath="", format='f'):
    if format != 'f' or format != 's':
        Exception("exportTAtoVTF(): unsupported format")

    if format == 'f' and filePath == "":
        Exception("exportTAtoVTF(): fileName needed")

    file = open(filePath, "w") if format == 'f' else ""

    if format == 'f':
        file.write("@NTA\n")
        file.write(f"# Automaton {ta.name}\n")
        writeRootsVTFfile(ta.rootStates, file)
        writeStatesVTFfile(ta.getStates(), file)
        writeAritiesVTFfile(ta.getSymbolArityDict(), file)
        writeEdgesVTFfile(ta.transitions, file)
        file.close()
    else:
        file += "@NTA\n"
        file += f"# Automaton {ta.name}\n"
        file += writeRootsVTFstr(ta.rootStates)
        file += writeStatesVTFstr(ta.getStates())
        file += writeAritiesVTFstr(ta.getSymbolArityDict())
        file += writeEdgesVTFstr(ta.transitions)
        return file
    return

# End of file format_vtf.py
