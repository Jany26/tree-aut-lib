# normalization.py
# Module for normalization implementation - necessary for canonical form
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_classes import *
from ta_functions import *
from test_data import *
from utils import *


class NormalizationHelper:
    def __init__(self, treeaut: TTreeAut, variables: list):
        self.treeaut = treeaut  # copy of the initial TA (un-normalized)
        self.roots = []
        self.states = []
        self.transitions = []  # these will be in the final TA/UBDA
        self.worklist = []  # currently considered (macro)states
        self.symbols = {}
        for symbol, arity in treeaut.getSymbolArityDict().items():
            if arity > 0:
                self.symbols[symbol] = arity
        self.variables = variables
        # self.reachability = getAllStateReachability(self.treeaut)
        # self.variableVision = self.treeaut.getVariablesVisibility()

    def __repr__(self):
        result = ""
        result += f"roots     = {self.roots}\n"
        result += f"states    = {self.states}\n"
        result += f"symbols   = {self.symbols}\n"
        result += f"worklist  = {self.worklist}\n"
        result += f"variables = {self.variables}\n"
        result += f"transitions ----------------\n"
        for i in self.transitions:
            result += f" > {i[0]} -- {i[1]} "
            result += f"<{i[2]}> " if i[2] != "" else ""
            result += f"--> {i[3]}\n"
        return result


# This funtion filters out transitions from the UBDA, which allow for creation
# of "bad" trees (those which allow e.g. repetition of variables,
# or wrong order of variables)
def filterBadTransitions(ta: TTreeAut, norm: NormalizationHelper):
    varIndex = {j: i for i, j in enumerate(norm.variables, start=1)}
    cacheVarVision = ta.getVariablesVisibility()
    # cacheVarVisionReverse = ta.getVariablesVisibility(reverse=True)
    cacheReachability = getAllStateReachability(ta)

    filter: dict[str, set] = {}

    for edgeDict in ta.transitions.values():
        for key, edge in edgeDict.items():
            canChildrenSeeVar = False
            canSeeSource = False
            selfLoop = True
            isSrcChild = False
            childrenVisibleVariables = set()
            for child in edge.children:
                if child == edge.src:
                    isSrcChild = True
                if child in cacheVarVision:
                    canChildrenSeeVar = True
                    for var in cacheVarVision[child]:
                        childrenVisibleVariables.add(var)
                if edge.src in cacheReachability[child]:
                    canSeeSource = True
                if child != edge.src:
                    selfLoop = False

            # CASE 1: q without var cant go to p,
            # if p "sees" another variable and can get to "q"
            case1 = False
            if (
                edge.info.variable == "" and
                canChildrenSeeVar and
                canSeeSource and
                not selfLoop
            ):
                case1 = True

            # CASE 2: q cant go to p, if they both see the same variable,
            # or if q sees a higher variable (x2 is higher than x1)

            # NOTE: might be too robust and some change is needed
            # when the state with the "higher" variable is the state itself,
            # the transition should not be filtered out
            case2 = False
            srcVisibleVariable = None
            if edge.src in cacheVarVision:
                for var in cacheVarVision[edge.src]:
                    if (
                        srcVisibleVariable is None or
                        varIndex[var] > varIndex[srcVisibleVariable]
                    ):
                        srcVisibleVariable = var
                for var in childrenVisibleVariables:
                    if (
                        varIndex[srcVisibleVariable] >= varIndex[var] and
                        not selfLoop
                    ):

                        case2 = True

            # CASE 3: q cant go to p, if p sees a variable, and the transition
            # also leads back to q, which does not see the variable
            case3 = False
            if (
                edge.src not in cacheVarVision and
                isSrcChild and
                childrenVisibleVariables != set()
            ):
                case3 = True

            # FINALIZATION ...
            if (case1 or case2 or case3):
                if edge.src not in filter:
                    filter[edge.src] = set()
                filter[edge.src].add(key)
                # case1str = "1" if case1 else "_"
                # case2str = "2" if case2 else "_"
                # case3str = "3" if case3 else "_"
                # print(f"CASE [{case1str}][{case2str}][{case3str}]: {edge}")
    for state, keys in filter.items():
        for key in keys:
            ta.transitions[state].pop(key)


def normalizationGetTransitions(transitions: list) -> dict:
    result = {}
    for i in transitions:
        srcState = detCreateName(i[0])
        edge = TEdge(i[1], [], i[2])
        children = [detCreateName(j) for j in i[3]]
        if srcState not in result:
            result[srcState] = {}
        edgeData = f"{edge.label}"
        if edge.variable != "":
            edgeData = f"<{edge.label},{edge.variable}>"
        key = f"{srcState}-{edgeData}-{children}"
        if key not in result[srcState]:
            result[srcState][key] = TTransition(srcState, edge, children)
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
    norm = NormalizationHelper(ta, varOrder)
    for symbol, stateList in ta.getOutputEdges().items():
        norm.transitions.append([stateList, symbol, "", []])
        norm.worklist.append(stateList)

    symbols = {s: a for s, a in alphabet.items() if a > 0}

    processed = set()
    while norm.worklist != []:
        ms = norm.worklist.pop()  # macrostate
        for sym in symbols:
            tuples = generatePossibleChildren(ms, norm.states, symbols[sym])
            for t in tuples:
                if str(t) in processed:
                    continue
                processed.add(str(t))
                procTransitions(norm, t)
    for statelist in norm.states:
        for root in ta.rootStates:
            if root in statelist:
                norm.roots.append(statelist)
    newRoots = [detCreateName(i) for i in norm.roots]
    newName = f"normalized({ta.name})"
    newTransitions = normalizationGetTransitions(norm.transitions)
    result = TTreeAut(newRoots, newTransitions, newName, ta.portArity)
    filterBadTransitions(result, norm)
    return result


def procTransitions(data: NormalizationHelper, childrenStates: list):
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
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    tr = []
    for edge in transitions(data.treeaut):
        if len(edge.children) != len(childrenStates):
            continue
        childsAreInMacroStates = True
        for i in range(len(edge.children)):
            if edge.children[i] not in childrenStates[i]:
                childsAreInMacroStates = False
        if childsAreInMacroStates:
            tr.append([
                edge.src,
                edge.info.label,
                edge.info.variable,
                edge.children
            ])

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

    for edge in edgesToAdd:
        stateList = edge[0]
        stateList.sort()
        data.transitions.append([stateList, edge[1], edge[2], childrenStates])
        if stateList not in data.states:
            data.states.append(stateList)
            data.worklist.append(stateList)


# This function performs a bottom-up check of normalization.
# Each combination of children is supposed to meet parents through
# a few transitions. In normalized UBDA the transitions do not repeat the same
# variable. Either the edges to the specific children list have all
# the variables once or have one "variable-less" edge. (empty string as var)
def isNormalized(ta: TTreeAut) -> bool:
    # lookup = edge symbol -> children array key ->
    # set of variables over all transitions from parent to child
    result: 'dict[str, dict[str, set]]' = {}

    duplicateEdges: 'list[TTransition]' = []

    for symbol, arity in ta.getSymbolArityDict().items():
        if arity != 0:
            result[symbol] = {}
    queue = [i for i in ta.rootStates]
    visited = set()
    while queue != []:
        parent = queue.pop(0)
        if parent in visited:
            continue
        for edge in ta.transitions[parent].values():
            if edge.children == []:
                continue
            for child in edge.children:
                if child not in visited:
                    queue.append(child)
            symbol = edge.info.label
            childStr = str(edge.children)
            if childStr not in result[symbol]:
                result[symbol][childStr] = set()
            var = edge.info.variable
            if (
                var in result[symbol][childStr]
                or (var == "" and len(result[symbol][childStr]) != 0)
                or (var != "" and "" in result[symbol][childStr])
            ):
                duplicateEdges.append(edge)
            else:
                result[symbol][childStr].add(var)
        visited.add(parent)

    for edge in duplicateEdges:
        eprint("isNormalized():", end="")
        eprint(f"edge {str(edge)[4:-1]} disrupts normalized property")

    return duplicateEdges == []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class NewNormalizationHelper:
    def __init__(self, treeaut: TTreeAut, variables: list, verbose: bool, output):
        self.treeaut = treeaut  # copy of the initial TA (un-normalized)
        self.roots = {}
        self.transitions = []  # these will be in the final TA/UBDA
        self.worklist = []  # currently considered (macro)states
        self.nextWorklist = []  # which states are considered in next iteration
        self.symbols = {}
        self.varWorklist: 'dict[str, list]' = {var: [] for var in variables}
        for symbol, arity in treeaut.getSymbolArityDict().items():
            if arity > 0:
                self.symbols[symbol] = arity
        self.lookup = {}
        self.edgeLookup = self.edgesToProcessCacheInit()
        for edgeDict in treeaut.transitions.values():
            for key, edge in edgeDict.items():
                if str(edge.children) not in self.lookup:
                    self.lookup[str(edge.children)] = []
                self.lookup[str(edge.children)].append((key, edge))
        self.processedEdges = set()
        self.keys = set()
        for edgeDict in treeaut.transitions.values():
            for k in edgeDict.keys():
                self.keys.add(k)
        self.variables = variables[::-1]
        self.verbose = verbose
        self.output = output

    def __repr__(self):
        result = ""
        result += f"roots     = {self.roots}\n"
        result += f"symbols   = {self.symbols}\n"
        result += f"worklist  = {self.worklist}\n"
        result += f"variables = {self.variables}\n"
        result += f"transitions ----------------\n"
        for i in self.transitions:
            result += f" > {i[0]} -- {i[1]} "
            result += f"<{i[2]}> " if i[2] != "" else ""
            result += f"--> {i[3]}\n"
        return result

    def edgesToProcessCacheInit(self) -> 'dict[str, set[str]]':
        result = {}
        for edgeDict in self.treeaut.transitions.values():
            for key, edge in edgeDict.items():
                for child in edge.children:
                    if child not in result:
                        result[child] = set()
                    result[child].add(key)
        return result
    
    def checkForUnprocessedStates(self):
        """
            Checking if some macrostate from current worklist has not yet been fully
            processed = i.e. some edge leading to some state from the macrostate
            has not yet been encountered.
        """
        temp = []
        for macroState in self.worklist:
            # NOTE: check subset, (to not create redundant "single" states that can be represented by )
            # skip = False
            # for nextMacroState in norm.nextWorklist:
            #     ms = set(macroState)
            #     nextms = set(nextMacroState)
            #     if ms.issubset(nextms):
            #         skip = True
            # if skip:
            #     continue
            fullyProcessed = True
            for state in macroState:
                if len(self.edgeLookup[state]) != 0:
                    for k in self.edgeLookup[state]:
                        temp.append(k)
                    fullyProcessed = False
            if not fullyProcessed:
                if macroState not in self.nextWorklist:
                    self.nextWorklist.append(macroState)
                    # print(f"adding {macroState} cuz of {temp}")
            # norm.varWorklist[currentVariable].append(macroState)

    def optimizeRedundantStates(self):
        deleteList = []
        for ms in self.nextWorklist:
            keep = False
            for s in ms:
                if s not in self.edgeLookup:
                    continue
                if len(self.edgeLookup[s]) != 0:
                    keep = True
            if not keep:
                deleteList.append(ms)
        for ms in deleteList:
            self.nextWorklist.remove(ms)
        
    def printEdgeLookup(self):
        # cleaning norm.edgeLookup
        toPop = []
        for i,j in self.edgeLookup.items():
            if j == set():
                toPop.append(i)
        for item in toPop:
            self.edgeLookup.pop(item)
        
        result = ""
        for i,j in self.edgeLookup.items():
            result += f"{i} = ["
            for key in j:
                result += f"{key},"
            result = result[:-1]
            result += "] "
        # print(result)

    def printWorklist(self, var):
        if self.variables != []:
            oldVar = self.variables[0]
        worklistStr = f"var: {var}"
        # for i in norm.varWorklist[var]:
        for i in self.worklist:
            keySet = set()
            for j in i:
                if j not in self.edgeLookup:
                    continue
                for key in self.edgeLookup[j]:
                    keySet.add(key)
            keyList = list(keySet)
            # worklistStr += f" | {detCreateName(i)}={detCreateName(keyList)}"
            worklistStr += f" | {detCreateName(i)}"
        print(worklistStr)


def processPossibleEdges(
    tuple: list,
    norm: NewNormalizationHelper,
    currentVariable: str,
    symbol: str
):
    childrenLists = [list(i) for i in product(*tuple)]
    newMacroState = set()
    forceVar = False
    keysToProcess = []
    for c in childrenLists:
        if str(c) not in norm.lookup:   
            continue
        possibleEdges = norm.lookup[str(c)]
        for key, edge in possibleEdges:
            if norm.verbose:
                if norm.output is None:
                    print("      > EDGE =", edge)
                else:
                    norm.output.write(f"      > EDGE = {edge}\n")
            if edge.info.variable == "" or edge.info.variable == currentVariable:
                varString = ""
                if edge.info.variable == currentVariable:
                    varString = f" through {currentVariable}"
                    forceVar = True
                newMacroState.add(edge.src)
                for child in edge.children:
                    if key in norm.edgeLookup[child]:
                        # print(f"  [!] processed edge {key} leading to {child}{varString}")
                        norm.edgeLookup[child].remove(key)
                        if key in norm.keys:
                            # print(f"  [!] removing key {key}")
                            norm.keys.remove(key)
                            keysToProcess.append(key)
    if len(newMacroState) != 0:
        newMacroState = list(newMacroState)
        newMacroState = stateNameSort(newMacroState)
        if newMacroState not in norm.nextWorklist:
            # print(f"    > appending {newMacroState}")
            norm.nextWorklist.append(newMacroState)

        # if newMacroState not in norm.varWorklist[currentVariable]:
        #     norm.varWorklist[currentVariable].append(newMacroState)

        # if self-loop (even partial), then no variable on edge
        # variable appears only if that was the case in the original UBDA
        if newMacroState in tuple or not forceVar:
        # if newMacroState in tuple:
            addedVar = ""
        else:
            addedVar = currentVariable

        lookupStr = str([newMacroState, symbol, addedVar, tuple])
        if lookupStr not in norm.processedEdges:
            norm.processedEdges.add(lookupStr)
            norm.transitions.append([newMacroState, symbol, addedVar, tuple])
            if norm.verbose:
                if norm.output is None:
                    print("[!] edge =", [newMacroState, symbol, addedVar, tuple])
                else:
                    norm.output.write(f"[!] edge = {[newMacroState, symbol, addedVar, tuple]}\n")
                # print("  [keys] =", keysToProcess)
            for root in norm.treeaut.rootStates:
                if root in newMacroState:
                    norm.roots[str(newMacroState)] = newMacroState


# Another approach to normalization. This approach also goes bottom-up,
# but remembers current variable, and always decreases the variable with each
# iteration until it reaches the root.
# This approach mostly does not create unnecessary transitions.
def treeAutNormalize(ta: TTreeAut, vars: list, verbose=False, output=None) -> TTreeAut:
    norm = NewNormalizationHelper(ta, vars, verbose, output)
    var = norm.variables.pop(0)  # discrepancy about variables on output edges
    for symbol, stateList in ta.getOutputEdges().items():
        norm.transitions.append([stateList, symbol, var, []])
        norm.worklist.append(stateList)
        # norm.varWorklist[var].append(stateList)
    if norm.verbose:
        if norm.output is None:
            print(f"var: {var} | {[detCreateName(i) for i in norm.worklist]}")
        else:
            norm.output.write(f"var: {var} | {[detCreateName(i) for i in norm.worklist]}\n")
    while norm.variables != []:
        oldVar = var
        var = norm.variables.pop(0)
        if norm.verbose:
            if norm.output is None:
                print(f"var: {var} | {[detCreateName(i) for i in norm.worklist]}")
            else:
                norm.output.write(f"var: {var} | {[detCreateName(i) for i in norm.worklist]}\n")
        for sym in norm.symbols:
            tuples = []
            # for i in product(norm.varWorklist[oldVar], repeat=norm.symbols[sym]):
            for i in product(norm.worklist, repeat=norm.symbols[sym]):
                tuples.append(list(i))
            for t in tuples:
                if norm.verbose:
                    if norm.output is None:
                        print(f"   > tuple = {t}\n")
                    else:
                        norm.output.write(f"   > tuple = {t}\n")
                processPossibleEdges(t, norm, var, sym)
            # norm.optimizeRedundantStates()
            # norm.checkForUnprocessedStates()
        norm.worklist = norm.nextWorklist
        norm.nextWorklist = []
        if norm.variables == []:
            break
    ta = createTaFromHelper(norm)
    removeBadTransitions(ta, vars, norm)
    return ta


# remove edges that do not comply with the "variable order"
#   - either edges that create a chain of same variable edges (x1, x1)
#   - or edges that create a chain of unordered variable edges (x2, x1)
def removeBadTransitions(ta: TTreeAut, vars: list, norm):
    varIndex = {j: i for i, j in enumerate(vars, start=1)}
    maxVarCache = {}
    for edge in transitions(ta):
        if edge.info.variable == "":
            continue
        if (
            edge.src not in maxVarCache or
            maxVarCache[edge.src] < varIndex[edge.info.variable]
        ):
            maxVarCache[edge.src] = varIndex[edge.info.variable]

    flaggedEdges = set()

    for edgeDict in ta.transitions.values():
        for key, edge in edgeDict.items():
            if edge.info.variable == "" or edge.src not in maxVarCache:
                continue
            for child in edge.children:
                if child not in maxVarCache:
                    continue
                if maxVarCache[child] <= maxVarCache[edge.src]:
                # if maxVarCache[child] < maxVarCache[edge.src]:
                    flaggedEdges.add((edge.src, key))
                    # if norm.verbose:
                    # print("[!] flagged edge =", edge)

    for src, key in flaggedEdges:
        ta.transitions[src].pop(key)


def createTaFromHelper(norm: NormalizationHelper) -> TTreeAut:
    name = f"normalized({norm.treeaut.name})"
    roots = [detCreateName(i) for i in norm.roots.values()]
    roots.sort()
    counter = 1
    transitionDict = {}
    for edge in norm.transitions:
        srcState = detCreateName(edge[0])
        edgeInfo = TEdge(edge[1], [], edge[2])
        children = [detCreateName(i) for i in edge[3]]
        transition = TTransition(srcState, edgeInfo, children)
        if srcState not in transitionDict:
            transitionDict[srcState] = {}
        transitionDict[srcState][f"k{counter}"] = transition
        counter += 1
    result = TTreeAut(roots, transitionDict, name, norm.treeaut.portArity)
    return result

# End of normalization.py
