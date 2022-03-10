from ta_classes import *
from ta_functions import *
from test_data import *

boxes = boxCatalogue

class NormalizationHelper:
    def __init__(self, treeaut, transitions, roots, states, worklist, variables):
        self.treeaut = treeaut
        self.roots = roots
        self.states = states
        self.transitions = transitions
        self.worklist = worklist
        self.variables = variables
    def __repr__(self):
        result =  f"roots     = {self.roots}\n"
        result += f"edges     = {self.states}\n"
        result += f"worklist  = {self.worklist}\n"
        result += f"variables = {self.variables}\n"
        result += f"transitions ----------------\n"
        for i in self.transitions:
            result += f" > {i[0]} -- {i[1]} "
            result += f"<{i[2]}>" if i[2] != "" else ""
            result += f" -- {i[3]}\n"
        return result

def normalize(ta:TTreeAut, alphabet:dict, varOrder:list) -> TTreeAut:
    
    # if not isWellDefined(ta, errDisplay=False):
    #     raise Exception("Can not normalize TA, that is not well defined.")

    # list of temporary arrays representing transitions = array of 4 elements:
    #   source state list, 
    #   edge symbol/label, 
    #   edge variable, 
    #   list of children states
    transitions = []
    
    roots = []
    states = []
    worklist = []
    outputSymbols = ta.getOutputEdges()
    for symbol, stateList in outputSymbols.items():
        # stateName = detCreateName(stateList)
        transitions.append([stateList, symbol, "", []])
        states.append(stateList)
        worklist.append(stateList)

    symbols = {s: a for s, a in alphabet.items() if a > 0}

    norm = NormalizationHelper(ta, transitions, roots, states, worklist, varOrder)

    processed = []
    # print(worklist)
    while worklist != []:
        for sym in symbols:
            ms = worklist.pop() # macrostate
            tuples = generatePossibleChildren(ms, states, symbols[sym])
            for t in tuples:
                if t in processed:
                    continue
                processed.append(t)
                procTransitions(norm, t)
    for statelist in states:
        for root in ta.rootStates:
            if root in statelist:
                norm.roots.append(statelist)
    newRoots = [detCreateName(i) for i in norm.roots]
    newName = f"normalized({ta.name})"
    newTransitions = normalizationGetTransitions(norm.transitions)
    result = TTreeAut(newRoots, newTransitions, newName, portArity=ta.portArity)
    # print(result)
    return result


def normalizationGetTransitions(transitions:list) -> dict:
    result = {}
    for i in transitions:
        srcState = detCreateName(i[0])
        edge = TEdge(i[1], [], i[2])
        children = [detCreateName(j) for j in i[3]]
        if srcState not in result:
            result[srcState] = {}
        edgeData = f"{edge.label}" if edge.variable == "" else f"<{edge.label},{edge.variable}>"
        key = f"{srcState}-{edgeData}-{children}"
        if key not in result[srcState]:
            result[srcState][key] = [srcState, edge, children]
    return result


def procTransitions(data: NormalizationHelper, childrenStates:list):
    # print(childrenStates)
    varEdges = []
    plainEdges = []
    for edgeDict in data.treeaut.transitions.values():
        for edge in edgeDict.values():
            if len(edge[2]) != len(childrenStates):
                continue
            childsAreInMacroStates = True
            for i in range(len(edge[2])):
                if edge[2][i] not in childrenStates[i]:
                    childsAreInMacroStates = False
            if childsAreInMacroStates:
                temp = [edge[0], edge[1].label, edge[1].variable, edge[2]]
                if edge[1].variable != "":
                    varEdges.append(temp)
                else:
                    plainEdges.append(temp)

    edgesToAdd = []
    # print("var:", varEdges)
    # print("plain:", plainEdges)
    if (varEdges != []) ^ (plainEdges != []):
        edges = varEdges if varEdges != [] else plainEdges
        for edge in edges:
            childrenFromEdgeCorrespondToParameters = True
            for i in range(len(edge[3])):
                if edge[3][i] not in childrenStates[i]:
                    childrenFromEdgeCorrespondToParameters = False
                    break
            if childrenFromEdgeCorrespondToParameters:
                temp = [[edge[0]], edge[1], edge[2], childrenStates]
                edgesToAdd.append(temp)

    for vEdge in varEdges:
        for pEdge in plainEdges:
            # note: discussed with Ondrej 
            # -> this prevents unnecessary edge duplication in some cases
            if vEdge[0] == pEdge[0]:
                continue 
            
            for var in data.variables:
                srcState = [vEdge[0]]
                if vEdge[2] == var:
                    srcState.extend([pEdge[0]])
                symbol = vEdge[1]
                children = pEdge[2]
                edgesToAdd.append([srcState, symbol, var, children])

    for edge in edgesToAdd:
        stateList = edge[0]
        stateList.sort()
        data.transitions.append([stateList, edge[1], edge[2], childrenStates])
        if stateList not in data.states:
            data.states.append(stateList)
            data.worklist.append(stateList)


def compressVariables(ta:TTreeAut) -> TTreeAut:
    temp = {}
    for edgeDict in ta.transitions.values():
        for edge in edgeDict.values():
            tempKey = f"{edge[0]}-{edge[1].label}-{edge[2]}"
            if tempKey not in temp:
                temp[tempKey] = [[], []]
            temp[tempKey][0] = [edge[0], edge[1].label, edge[2]]
            temp[tempKey][1].append(edge[1].variable)
    
    transitions = {}
    for key, edgeData in temp.items():
        src = edgeData[0][0]
        symb = edgeData[0][1]
        children = edgeData[0][2]
        vars = ",".join(edgeData[1])
        edge = TEdge(symb, [], vars)
        if src not in transitions:
            transitions[src] = {}
        transitions[src][key] = [src, edge, children]
    result = TTreeAut(ta.rootStates, transitions, f"compressed({ta.name})", ta.portArity)
    return result

# End of normalization.py
