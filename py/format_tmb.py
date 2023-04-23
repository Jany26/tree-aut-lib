# format_tmb.py
# Functions for exporting tree automaton into TMB format (.tmb)
# for generating a graphical representation of the TA.
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>


from format_vtf import *
from ta_classes import *
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB IMPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def replaceCommasIn(line: str) -> str:
    stack = []
    temp = ""
    for i in range(len(line)):
        if line[i] == "(":
            if len(stack) != 0:
                temp += "("
            stack.append("(")
        elif line[i] == ")":
            stack.pop()
            if len(stack) != 0:
                temp += ")"
        elif line[i] == "," and len(stack) == 1:
            temp += ";"
        else:
            temp += line[i]
    if len(stack) != 0:
        raise Exception("unbalanced parentheses")
    return temp


def loadSymbol(line: str):
    symbol = ""
    rest = ""
    for i in range(len(line)):
        if line[i] == "(":
            symbol = line[:i]
            rest = line[i:]
            break
    if symbol == "":
        symbol = line.strip()
        rest = ""
    return symbol, rest


def loadTransitionFromTMB(line: str) -> TTransition:
    line = line.strip()
    transitionData = line.split("->")
    srcState = transitionData[1].strip()
    rest = transitionData[0].strip()
    symbol, childrenString = loadSymbol(rest)
    childStates = replaceCommasIn(childrenString.strip())
    childStates = childStates.split(';')
    children = [state for state in childStates if state != ""]
    return TTransition(srcState, TEdge(symbol, [None] * len(children), ""), children)


def loadArityFromTMB(line: str) -> dict:
    words = line.strip().split()

    result = {}
    for i in words[1:]:
        items = i.split(":")
        symbol = str(items[0].strip())
        arity = int(items[1].strip())
        result[symbol] = arity
    return result


def consistencyCheckTMB(edges, states, arities) -> bool:
    # print(states)
    for stateName, edgeDict in edges.items():
        if stateName not in states:
            return False
        for edge in edgeDict.values():
            if (
                edge.src not in states
                or edge.info.label not in arities
                or len(edge.children) != int(arities[edge.info.label])
            ):
                return False
            for child in edge.children:
                if child not in states:
                    return False
    return True

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORT TA FROM TMB FILE/STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def importTAfromTMB(source: str, sourceType='f') -> TTreeAut:
    if sourceType == 'f':
        inputStream = open(source, "r")
    elif sourceType == 's':
        inputStream = source.split('\n')
    else:
        raise Exception(f"importTAfromTMB(): unsupported source type '{sourceType}'")

    arityDict = {}
    rootStates = []
    transitionDict = {}
    allStates = []
    rootsProcessed = False
    arityProcessed = False
    stateListProcessed = False
    transitionProcessing = False
    name = ""

    for line in inputStream:

        # skipping comments and empty lines
        line = line.strip()
        if line == "" or line.startswith("#") or line.startswith("//"):
            continue

        if transitionProcessing and not line.startswith('\n'):
            edge = loadTransitionFromTMB(line)
            if edge == []:
                continue
            # if arityProcessed and stateListProcessed:
            #     consistencyCheckTMB(edge, allStates, arityDict)
            key = generateKeyFromEdge(edge)
            if str(edge.src) not in transitionDict:
                transitionDict[str(edge.src)] = {}
            transitionDict[str(edge.src)][key] = edge
            continue

        if line.startswith("Automaton"):
            name = line[len("Automaton"):].strip()
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
            raise Exception(f"importTAfromTMB(): Unknown items in TMB file")
    # end for loop

    if arityProcessed and stateListProcessed:
        if not consistencyCheckTMB(transitionDict, allStates, arityDict):
            raise Exception(f"importTAfromTMB(): Inconsistent transition data with info in preamble")

    if not rootsProcessed:
        print("exception M")
        raise Exception(f"List of root states missing")
    return TTreeAut(rootStates, transitionDict, name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB EXPORT - FILE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writeAritiesTMBfile(arities, tgt):
    tgt.write("Ops")
    for i in arities:
        tgt.write(f" {i}:{arities[i]}")
    tgt.write("\n\n")


def writeNameTMBfile(name, tgt):
    tgt.write("Automaton ")
    tgt.write(f"{name}") if name != "" else tgt.write("unnamed")
    tgt.write("\n\n")


def writeStatesTMBfile(states, tgt):
    tgt.write("States")
    for i in states:
        tgt.write(f" {i}:0")
    tgt.write("\n\n")


def writeRootsTMBfile(states, tgt):
    tgt.write("Final States")
    for i in states:
        tgt.write(f" {i}")
    tgt.write("\n\n")


def writeTransitionsTMBfile(ta, tgt):
    tgt.write("Transitions\n")
    for transitionDict in ta.transitions.values():
        for edge in transitionDict.values():
            tgt.write(f"{edge.info.label}(")
            arity = len(edge.children)
            for i in range(arity):
                tgt.write(f"{edge.children[i]}")
                tgt.write("," if i < arity - 1 else "")
            tgt.write(f") -> {edge.src}\n")
    tgt.write("\n\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB EXPORT - STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writeAritiesTMBstr(arities):
    result = "Ops"
    for i in arities:
        result += f" {i}:{arities[i]}"
    result += "\n\n"
    return result


def writeNameTMBstr(name):
    return "Automaton " + (f"{name}" if name != "" else "unnamed") + "\n\n"


def writeStatesTMBstr(states):
    result = "States"
    for i in states:
        result += f" {i}:0"
    result += "\n\n"
    return result


def writeRootsTMBstr(states):
    result = "Final States"
    for i in states:
        result += f" {i}"
    result += "\n\n"
    return result


def writeTransitionsTMBstr(ta):
    result = "Transitions\n"
    for transitionDict in ta.transitions.values():
        for edge in transitionDict.values():
            temp = f"{edge.info.label}("
            for i in range(len(edge.children)):
                temp += f"{edge.children[i]}"
                temp += ", " if (i < len(edge.children) - 1) else ""
            temp += f") -> {edge.src}\n"
            result += temp
    result += "\n\n"
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TA TO TMB FILE/STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def exportTAtoTMB(ta: TTreeAut, fileName):
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    result = open(fileName, "w")
    writeAritiesTMBfile(ta.getSymbolArityDict(), result)
    writeNameTMBfile(ta.name, result)
    writeStatesTMBfile(ta.getStates(), result)
    writeRootsTMBfile(ta.rootStates, result)
    writeTransitionsTMBfile(ta, result)
    result.close()

# End of file format_tmb.py
