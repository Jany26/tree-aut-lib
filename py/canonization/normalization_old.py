"""
[file] normalization.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] UBDA Normalization implementation.
Merges equivalent states (i.e. states with equivalent languages
if they were considered roots)
Basically a bottom-up determinization that takes variables into account (they
are considered a part of the edge-symbol).
"""

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from tree_automata.functions.helpers import generate_possible_children
from tree_automata.functions.reachability import get_all_state_reachability
from tree_automata.functions.determinization import det_create_name

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - old version -- redundant, kept for archiving purposess  - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# this version of normalization created too many useless transitions over variables
# and worked too much like determinization (did not take variable ordering and
# hierarchical structure of UBDAs into account)


class NormalizationHelperOld:
    def __init__(self, treeaut: TTreeAut, variables: list):
        self.treeaut = treeaut  # copy of the initial TA (un-normalized)
        self.roots = []
        self.states = []
        self.transitions = []  # these will be in the final TA/UBDA
        self.worklist = []  # currently considered (macro)states
        self.symbols = {}
        for symbol, arity in treeaut.get_symbol_arity_dict().items():
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


# This function filters out transitions from the UBDA, which allow for creation
# of "bad" trees (those which allow e.g. repetition of variables,
# or wrong order of variables)
def filterBadTransitions(ta: TTreeAut, norm: NormalizationHelperOld):
    varIndex = {j: i for i, j in enumerate(norm.variables, start=1)}
    cacheVarVision = ta.get_var_visibility()
    cacheReachability = get_all_state_reachability(ta)

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

            # CASE 1: q without var can't go to p,
            # if p "sees" another variable and can get to "q"
            case1 = False
            if edge.info.variable == "" and canChildrenSeeVar and canSeeSource and not selfLoop:
                case1 = True

            # CASE 2: q can't go to p, if they both see the same variable,
            # or if q sees a higher variable (x2 is higher than x1)

            # NOTE: might be too robust and some change is needed
            # when the state with the "higher" variable is the state itself,
            # the transition should not be filtered out
            case2 = False
            srcVisibleVariable = None
            if edge.src in cacheVarVision:
                for var in cacheVarVision[edge.src]:
                    if srcVisibleVariable is None or varIndex[var] > varIndex[srcVisibleVariable]:
                        srcVisibleVariable = var
                for var in childrenVisibleVariables:
                    if varIndex[srcVisibleVariable] >= varIndex[var] and not selfLoop:

                        case2 = True

            # CASE 3: q can't go to p, if p sees a variable, and the transition
            # also leads back to q, which does not see the variable
            case3 = False
            if edge.src not in cacheVarVision and isSrcChild and childrenVisibleVariables != set():
                case3 = True

            # FINALIZATION ...
            if case1 or case2 or case3:
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
        srcState = det_create_name(i[0])
        edge = TEdge(i[1], [], i[2])
        children = [det_create_name(j) for j in i[3]]
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
    norm = NormalizationHelperOld(ta, varOrder)
    for symbol, stateList in ta.get_output_edges().items():
        norm.transitions.append([stateList, symbol, "", []])
        norm.worklist.append(stateList)

    symbols = {s: a for s, a in alphabet.items() if a > 0}

    processed = set()
    while norm.worklist != []:
        ms = norm.worklist.pop()  # macrostate
        for sym in symbols:
            tuples = generate_possible_children(ms, norm.states, symbols[sym])
            for t in tuples:
                if str(t) in processed:
                    continue
                processed.add(str(t))
                procTransitions(norm, t)
    for statelist in norm.states:
        for root in ta.roots:
            if root in statelist:
                norm.roots.append(statelist)
    newRoots = [det_create_name(i) for i in norm.roots]
    newName = f"normalized({ta.name})"
    newTransitions = normalizationGetTransitions(norm.transitions)
    result = TTreeAut(newRoots, newTransitions, newName, ta.port_arity)
    filterBadTransitions(result, norm)
    return result


def procTransitions(data: NormalizationHelperOld, childrenStates: list):
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
    for edge in iterate_edges(data.treeaut):
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

    for edge in edgesToAdd:
        stateList = edge[0]
        stateList.sort()
        data.transitions.append([stateList, edge[1], edge[2], childrenStates])
        if stateList not in data.states:
            data.states.append(stateList)
            data.worklist.append(stateList)


# end of normalization_old.py
