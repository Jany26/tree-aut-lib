from ta_classes import *
from ta_functions import *
from test_data import *

boxes = boxCatalogue


class NormalizationHelper:
    def __init__(self, treeaut, transitions, roots,
                 states, worklist, variables):
        self.treeaut = treeaut
        self.roots = roots
        self.states = states
        self.transitions = transitions
        self.worklist = worklist
        self.variables = variables

    def __repr__(self):
        result = f"roots     = {self.roots}\n"
        result += f"edges     = {self.states}\n"
        result += f"worklist  = {self.worklist}\n"
        result += f"variables = {self.variables}\n"
        result += f"transitions ----------------\n"
        for i in self.transitions:
            result += f" > {i[0]} -- {i[1]} "
            result += f"<{i[2]}>" if i[2] != "" else ""
            result += f" -- {i[3]}\n"
        return result


def createEdgeList(tr: list) -> list:
    if tr == []:
        return []
    helpDict = {}
    for i in tr:
        if i[2] not in helpDict:
            helpDict[i[2]] = {}
        if i[1] not in helpDict[i[2]]:
            helpDict[i[2]][i[1]] = set()
        helpDict[i[2]][i[1]].add(i[0])
    result = []
    for var, cont in helpDict.items():
        for sym, states in cont.items():
            result.append([list(states), sym, var])
    return result


def normalizeEdges(tr: list, vars: list) -> list:
    helpDict = {i: {} for i in vars}
    for var in vars:
        for e in tr:
            if e[2] != "" and e[2] != var:
                continue
            if e[1] not in helpDict[var]:
                helpDict[var][e[1]] = set()
            helpDict[var][e[1]].add(e[0])
    result = []
    for var, cont in helpDict.items():
        for sym, states in cont.items():
            result.append([list(states), sym, var])
    return result


def normalize(ta: TTreeAut, alphabet: dict, varOrder: list) -> TTreeAut:

    # NOTE: wellDefined might be different here
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
    for symbol, stateList in ta.getOutputEdges().items():
        # stateName = detCreateName(stateList)
        transitions.append([stateList, symbol, "", []])
        states.append(stateList)
        worklist.append(stateList)

    symbols = {s: a for s, a in alphabet.items() if a > 0}

    norm = NormalizationHelper(ta, transitions, roots, states, worklist, varOrder)

    processed = []
    while worklist != []:
        for sym in symbols:
            ms = worklist.pop()  # macrostate
            # print(ms)
            tuples = generatePossibleChildren(ms, states, symbols[sym])
            # for i in tuples:
            #     print(f"  > {i}")
            for t in tuples:
                if t in processed:
                    continue
                processed.append(t)
                # print(f"procTransitions({t})")
                procTransitions(norm, t)
    for statelist in states:
        for root in ta.rootStates:
            if root in statelist:
                norm.roots.append(statelist)
    newRoots = [detCreateName(i) for i in norm.roots]
    newName = f"normalized({ta.name})"
    newTransitions = normalizationGetTransitions(norm.transitions)
    result = TTreeAut(newRoots, newTransitions, newName, ta.portArity)
    # print(result)
    return result


def normalizationGetTransitions(transitions: list) -> dict:
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
            result[srcState][key] = TTransition(srcState, edge, children)
    return result


def procTransitions(data: NormalizationHelper, childrenStates: list):
    tr = []
    for edge in transitions(data.treeaut):
        if len(edge.children) != len(childrenStates):
            continue
        childsAreInMacroStates = True
        for i in range(len(edge.children)):
            if edge.children[i] not in childrenStates[i]:
                childsAreInMacroStates = False
        if childsAreInMacroStates:
            tr.append([edge.src, edge.info.label, edge.info.variable, edge.children])

    varEdge = False
    novarEdge = False
    for i in tr:
        if i[2] == "":
            novarEdge = True
        if i[2] != "":
            varEdge = True
            if i[2] not in data.variables:
                raise Exception("insufficient variable ordering for TA")

    if varEdge and novarEdge:
        edgesToAdd = normalizeEdges(tr, data.variables)
    else:
        edgesToAdd = createEdgeList(tr)

    # edgevars = [i[2] for i in edgesToAdd]
    # stateset = []
    # for i in edgesToAdd:
    #     stateset.extend(i[0])
    # stateset = set(stateset)
    # print("vars =", edgevars)
    # print("states =", stateset)
    # if edgevars == ['x1', 'x2', 'x3', 'x4', 'x5']:
    #     if len(stateset) == 1:
    #         print("ERROR")
    #         print("edgesToAdd")
    #         for i in edgesToAdd:
    #             print(i)
    #         print("varEdge =", varEdge)
    #         print("novarEdge =", novarEdge)
    #         print("tr =", tr)
    #         print(childrenStates)
    for edge in edgesToAdd:
        stateList = edge[0]
        stateList.sort()
        data.transitions.append([stateList, edge[1], edge[2], childrenStates])
        if stateList not in data.states:
            data.states.append(stateList)
            data.worklist.append(stateList)


def compressVariables(ta: TTreeAut) -> TTreeAut:
    temp = {}
    for edgeDict in ta.transitions.values():
        for edge in edgeDict.values():
            tempKey = f"{edge.src}-{edge.info.label}-{edge.children}"
            if tempKey not in temp:
                temp[tempKey] = [[], []]
            temp[tempKey][0] = [edge.src, edge.info.label, edge.children]
            temp[tempKey][1].append(edge.info.variable)

    transitions = {}
    for key, edgeData in temp.items():
        src = edgeData[0][0]
        symb = edgeData[0][1]
        children = edgeData[0][2]
        vars = ",".join(edgeData[1])
        edge = TEdge(symb, [], vars)
        if src not in transitions:
            transitions[src] = {}
        transitions[src][key] = TTransition(src, edge, children)
    result = TTreeAut(ta.rootStates, transitions, f"compressed({ta.name})", ta.portArity)
    return result

# End of normalization.py
