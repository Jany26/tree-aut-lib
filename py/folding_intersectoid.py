"""
[file] folding_intersectoid.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for manipulating intersectoid construction used in folding.
"""

from ta_classes import *
from ta_functions import *
from test_data import *

import copy
import itertools
from folding_helpers import *



def intersectoidEdgeKey(e1: list, e2: list) -> str:
    """
    [description]
    Creates a "key" for transition dictionary modified for working with
    an "intersectoid" tree automaton.
    """
    state = f"({e1.src}, {e2.src})"
    symb = e2.info.label
    var = ""
    if e1.info.variable != "" and not symb.startswith("Port"):
        var = f",{e1.info.variable}"

    children = f""
    if not e2.info.label.startswith("Port"):
        for i in range(len(e1.children)):
            children += f"({e1.children[i]},{e2.children[i]}),"
        children = children[:-1]

    key = f"{state}-<{symb}{var}>-({children})"
    return key



def createIntersectoid(
    ta: TTreeAut,
    box: TTreeAut,
    root: str,
    helper: FoldingHelper
) -> TTreeAut:
    """
    [description]
    Funtion produces an intersectoid from the 'ta' UBDA and 'box' TA.
    This intersectoid is used in boxFinding() to determine the result mapping.
    Intersectoid is similar to a 'product' or an 'intersection' tree automaton.
    state set: Q' = Q_v x Q_b (v = normalized BDA, b = box)

    types of transitions and how they came to be:

    1) (q,s)-{LH}->[(q1,s1),(q2,s2)] | q-{LH}->(q1,q2) is in transition
        dictionary (trd.) of v and s-{LH}->(s1,s2) is in tr.dict. of b

    2) (q,s)-{LH,var}->[(q1,s1),(q2,s2)] | q-{LH,var}->(q1,q2) is in trd.
        of v and s-{LH}->(s1,s2) is in trd. of b

    3) (q,s)-{a}->() | q-{a}->() in trd. of v and s-{a}->() in trd. of b
        // a is a terminal symbol (e.g. '0' or '1') => output transition

    4) (q,s)-{Port_i}->() | s-{Port_i}->() in tr.d of b

    [parameters]
    'ta' - UBDA that is folded (first states of the tuples)
    'box' - TA representing reduction that is analysed (second states of the tuples)
    'root' - state from the UBDA ('ta') where the intersectoid is created from
    'helper' - FoldingHelper instance with additional information used during
    intersectoid creation

    [return]
    Tree automaton/UBDA representing the intersectoid (contains additional
    output symbols/output edges => port transitions), which is used later
    for finding the correct port-state mapping for applying folding reductions.
    """
    helper.keyCounter = 0
    edges = {}
    visited = set()
    worklist: list = [(root, b) for b in box.rootStates]
    helper.temp = []
    while worklist != []:
        currentTuple = worklist.pop(0)
        state = tupleName(currentTuple)
        if state not in edges:
            edges[state] = {}
        if state in visited:
            continue
        for key, te in ta.transitions[currentTuple[0]].items():  # ta edges
            # skipping edges with already applied reductions
            skip = False
            for b in te.info.boxArray:
                if b is not None:
                    # skipping when trying to reach through a reduced edge, BUT
                    # NOT when the source state can create a port transition
                    skip = True
            for be in box.transitions[currentTuple[1]].values():  # box edges
                # skipping differently labeled (e.g. LH and 0) edges
                if (
                    te.info.label != be.info.label and
                    not be.info.label.startswith("Port")
                ):
                    continue
                if len(te.children) == 2 and len(be.children) == 2:
                    if te.children[0] != te.children[1] and be.children[0] == be.children[1]:
                        continue
                # ports are exceptions to the different labeled exclusion
                # if one of the mismatched labels is a port label,
                # than that "overrules" any other label
                if be.info.label.startswith("Port"):
                    edgeObj = TEdge(be.info.label, [], "")
                    edge = TTransition(state, edgeObj, [])
                    edges[state][intersectoidEdgeKey(te, be)] = edge
                elif not skip:
                    children = []
                    for i in range(len(te.children)):
                        child = (te.children[i], be.children[i])
                        children.append(tupleName(child))
                        worklist.append(child)
                    edgeObj = TEdge(be.info.label, [], f"{te.info.variable}")
                    if len(children) != 0:
                        helper.temp.append((splitTupleName(state), key))
                    edge = TTransition(state, edgeObj, children)
                    edges[state][intersectoidEdgeKey(te, be)] = edge
            # for box edge
        # for tree automaton edge
        visited.add(state)
    # end while loop
    roots = [f"({root},{b})" for b in box.rootStates]
    name = f"intersectoid({box.name}, {root})"
    result = TTreeAut(roots, edges, name, box.portArity)
    return result


def intersectoidReachability(ta: TTreeAut, varVis) -> list:
    """
    [description]
    Computes bottom-up reachability within the intersectoid with regards to
    properly labeled port transitions with variables.
    Port transitions without variables are considered invalid.

    [parameters]
    'ta' - intersectoid to analyze

    [return]
    list of states that are reachable without invalid port transitions.

    [note]
    This function is used after creating the intersectoid and saturating the
    transitions with variables where possible.
    """
    def intersectoidTupleGen(state: str, parents: list, varVis: dict) -> list:
        possibilites = product(parents, repeat=2)
        result = []
        for k in possibilites:
            if state not in k:
                continue
            if k[0] in varVis and k[1] in varVis:
                if varVis[k[0]] != varVis[k[1]]:
                    continue
            result.append(list(k))
        return result

    copyta = copy.deepcopy(ta)
    copyta.reformatKeys()

    edgesToPop = []
    for edgeDict in copyta.transitions.values():
        for key, edge in edgeDict.items():
            # port edge should be labeled with a variable
            if len(edge.children) == 0:
                if edge.info.label.startswith("Port") and edge.info.variable == "":
                    edgesToPop.append((edge.src, key))
                continue
            bad = False
            # low = edge.children[0]
            # high = edge.children[1]
            if bad:
                edgesToPop.append((edge.src, key))

    for src, key in edgesToPop:
        copyta.transitions[src].pop(key)

    copyta = removeUselessStates(copyta)
    return reachableBU(copyta)


def addVariablesTD(treeaut: TTreeAut, helper: FoldingHelper):
    """
    [description]
    Top-down variable saturation. Can compute variables to edges where child
    states do not contain self looping transitions (so it is clear which variables
    can go there) and recursively propagates following variables down from
    each edge that was var-labeled beforehand.
    
    [parameters]
    'treeaut' - usually an intersectoid to saturate
    'helper' - contains additional information like minVar, maxVar, etc.,
    that are useful in this procedure

    [note]
    nothing is returned -> the variables are saturated in situ into 'treeaut'
    """
    def addVariables(ta: TTreeAut, var: int, state: str, helper: FoldingHelper):
        if var > helper.maxVar + 1:
            return
        for edge in ta.transitions[state].values():
            if edge.src in edge.children:
                return
        for edge in ta.transitions[state].values():
            if edge.info.variable != "":
                edgeVar = int(edge.info.variable[len(helper.varPrefix):])
                if edgeVar != var:
                    if helper.verbose:
                        print(f"WARNING: addVariables(): edge {edge} does not agree with var {var}")
                return
            if helper.verbose:
                print(f"addVariables(): adding {helper.varPrefix}{var} to {edge}")
            edge.info.variable = f"{helper.varPrefix}{var}"

    # edge-case 1:
    # if root has no var-labeled edges and has no self-loops,
    # minVar is used to label edges starting from root
    for root in treeaut.rootStates:
        selfLooping = False
        noVars = True
        for edge in treeaut.transitions[root].values():
            if edge.src in edge.children:
                selfLooping = True
            if edge.info.variable != "":
                noVars = False
        # if not selfLooping and noVars:
        if selfLooping or not noVars:
            continue
        for edge in treeaut.transitions[root].values():
            if helper.verbose:
                print(f"addVariables(): adding {helper.varPrefix}{helper.minVar} to {edge}")
            edge.info.variable = f"{helper.varPrefix}{helper.minVar}"

    # edge-case 2:
    # when using LPort, HPort, possibly even X port, sometimes the port-mapped state
    # can be reached through multiple vars
    varVis = treeaut.getVariableVisibilityCache()
    for edge in iterateEdges(treeaut):
        if edge.info.label.startswith("Port") and edge.info.variable == "":
            if edge.src in varVis:
                edge.info.variable = f"{helper.varPrefix}{varVis[edge.src]}"

    # propagating variable values to lower edges where possible
    for edge in iterateEdges(treeaut):
        if edge.src in edge.children: # or edge.info.variable == "":
            continue
        if edge.info.variable == "":
            continue
        var = int(edge.info.variable[len(helper.varPrefix):])
        for child in edge.children:
            addVariables(treeaut, var + 1, child, helper)


def reducePortableStates(intersectoid: TTreeAut):
    """
    [description]
    This function is used to find out which tuples of port states
    (in multiport boxes => port arity > 1) can be used as a mapping.

    This is computed by trying out all different combinations of port transitions
    (the other port transitions of the same type are temporarily left out)
    and checking if the language of the intersectoid is non-empty.

    If the language of the intersectoid is empty for the particular combination
    of port transitions => the mapping would not be possible and thus these
    are then not considered.

    """
    def getPortEdgelookup(intersectoid: TTreeAut):
        # each port has paths to edge lookup (state, key)
        result: dict[str, list[tuple(str, str)]] = {}
        edges: dict[str, set[str]] = {}
        # intersectoid.getOutputSymbols()
        for key, edge in iterateKeyEdgePairs(intersectoid):
            if not edge.info.label.startswith("Port"):
                continue
            if edge.info.label not in result:
                result[edge.info.label] = []
            if edge.src not in edges:
                edges[edge.src] = set()
            edges[edge.src].add(key)
            result[edge.info.label].append((edge.src, key))
        return result, edges

    def iteratePortEdgePaths(inp):
        return (dict(zip(inp.keys(), values)) for values in product(*inp.values()))

    # portMapping - paths to port edges that stay in the intersectoid
    # portEdges - for each port there is a list of tuples, 
    #             which contain edge lookup info (state, edge-key)
    # edgeStorage - for storing/saving removed edges from the intersectoid,
    #               identical structure as TTreeAut transition dictionary
    def reduceIntersectoidEdges(intersectoid: TTreeAut,
                                portMapping: dict[str, tuple[str, str]],
                                portEdges: dict[str, list[tuple[str, str]]],
                                edgeStorage: dict[str, dict[str, TTransition]]
                                ):
        for port, pathList in portEdges.items():
            (stateToStay, keyToStay) = portMapping[port]
            for (state, key) in pathList:
                if state == stateToStay and key == keyToStay:
                    continue
                if state not in edgeStorage:
                    edgeStorage[state] = {}
                if key not in edgeStorage[state]:
                    edgeStorage[state][key] = intersectoid.transitions[state].pop(key)
        # for port1, state, key in portMapping.items():
    def returnReducedEdges(intersectoid: TTreeAut, edgeStorage: dict):
        for state, edges in edgeStorage.items():
            for key, edge in edges.items():
                intersectoid.transitions[state][key] = edge
            

    portEdges, edgePopper = getPortEdgelookup(intersectoid)
    edgeStorage: dict[str, dict[str, TTransition]] = {}
    candidates = [i for i in iteratePortEdgePaths(portEdges)]
    for i in candidates:
        reduceIntersectoidEdges(intersectoid, i, portEdges, edgeStorage)
        node, _ = nonEmptyTD(intersectoid)
        if node is not None:
            for port, (state, key) in i.items():
                edgePopper[state].remove(key)

        returnReducedEdges(intersectoid, edgeStorage)
        edgeStorage = {}
    for state, keySet in edgePopper.items():
        for key in keySet:
            intersectoid.transitions[state].pop(key)


# end folding_intersectoid.py
