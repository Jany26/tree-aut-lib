from ta_classes import *
from ta_functions import *
from test_data import *

import re
import copy
from render_dot import exportToFile
from folding_helpers import *
from folding_intersectoid import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Main Folding algorithm functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def getStateWitnessRelation(intersectoid: TTreeAut, port: str):
    def isEdgeUnified(children: list):
        return len(set(children)) <= 1

    def getRelationStep(state: str, intersectoid: TTreeAut):
        res = []

        for edge in intersectoid.transitions[state].values():
            if edge.src in edge.children:
                continue
            if len(edge.children) == 0:
                if edge.info.label == port:
                    return [set([edge.src])]
                continue

            if isEdgeUnified(edge.children):
                res.extend(getRelationStep(edge.children[0], intersectoid))
                continue

            subResult = set()
            for child in edge.children:
                for child_set in getRelationStep(child, intersectoid):
                    subResult = subResult.union(child_set)

            res.append(subResult)
        return res

    result = []
    for root in intersectoid.rootStates:
        result.extend(getRelationStep(root, intersectoid))
    return result

# This function finds all different port types in intersectoid and assigns
# one state from the original ta to be mapped to the port.
# It uses a reachability relation (similar to Floyd-Warshall algorithm) to
# determine the state that is "infimum" wrt. reachability, i.e. a state 'q', that
# can be reached from all 'suspect' states of the particular port and no
# 'suspect' state can reach the state 'q'. If no such state exists, mapping 
# fails and thus no box folding should be applied.
#
# note: 'suspect' states (a,b) from the intersectoid contain a Port output
# transition. (state 'a' from the original TA is compared wrt. the reachability)
def getMapping(intersectoid: TTreeAut, ta: TTreeAut) -> dict:
    ports = {
        edge.info.label
        for edge in iterateEdges(intersectoid)
        if edge.info.label.startswith("Port")
    }
    reach: dict[str, set] = getAllStateReachability(ta, reflexive=False)
    varvis = intersectoid.getVariableVisibilityCache()
    mapping = {}
    for port in ports:
        try:
            relation = [(varvis[list(s)[0]], s) for s in getStateWitnessRelation(intersectoid, port)]
        except:
            print("exception")
            print(intersectoid)
            print(varvis)
            getStateWitnessRelation(intersectoid, port)
            print(s)
        # print(port, relation)
        relation.sort(reverse=True)
        for var, stateset in relation:
            skip = False
            for state in stateset:
                s = splitTupleName(state)
                infimum = True
                for state2 in stateset:
                    if state == state2:
                        continue
                    s2 = splitTupleName(state2)
                    if s in reach[s2] and not s2 in reach[s]:
                        continue
                    else:
                        infimum = False
                if infimum:
                    mapping[port] = state
                    skip = True
                    break
            if skip:
                break
        if port not in mapping:
            return {}
    return mapping

# Main implementation of one step of the folding procedure.
# Function tries to apply tree automaton reduction starting from the specific
# state in the normalized (and well-specified) UBDA.
# inputs:
#   'ta' - UBDA on which we try to apply reduction
#   'box' - specifies which tree automaton should be applied
#   'root' - which state is the starting point of the procedure
# output:
#   - dictionary which specifies mapping of the output ports of the 'box'
#     TA to the states of the initial 'ta' (UBDA)
#   - if no mapping is found, empty dictionary {} is returned
def boxFinding(
    ta: TTreeAut,
    box: TTreeAut,
    root: str,
    helper: FoldingHelper,
    source: str
) -> dict:
    intersectoid: TTreeAut = createIntersectoid(ta, box, root, helper)
    intersectoid = trim(intersectoid)  # additional functionality maybe needed?
    debug1 = len(intersectoid.getStates())
    debug2 = len(intersectoid.getStates())
    # print(f"{source}-{box.name}-{root} : {debug1}, {debug2}")
    tree, _ = nonEmptyBU(intersectoid)
    if tree is None:
        return {}

    helper.exportIntersectoid(intersectoid, root, source, box.name) 
    addVariablesRecursive(intersectoid, helper)
    # helper.getFlaggedEdgesFrom(intersectoid)
    # print(intersectoid)
    reach = intersectoidReachability(intersectoid)
    intersectoid.shrinkTA(reach)
    if intersectoid.getPortArity() > 1:
        reducePortableStates(intersectoid)
        intersectoid = trim(intersectoid)
    finalMapping = getMapping(intersectoid, ta)
    # print(finalMapping)
    if finalMapping == {}:
        return {}
    varVis = intersectoid.getVariableVisibilityCache()
    splitMapping = {p: (splitTupleName(s), varVis[s]) for p,s in finalMapping.items()}
    return splitMapping


def mappingIsCorrect(mapping: dict, ta: TTreeAut, varVis: dict):
    # varVis = ta.getVariableVisibilityCache()
    if mapping == {}:
        return False
    biggerVar = False
    noneVar = False
    for i, (mapState, var) in enumerate(mapping.values()):
        if var == "":
            noneVar = True
        originalVar = int(varVis[mapState])
        intersectoidVar = int(var)
        if intersectoidVar > originalVar:
            biggerVar = True
    if biggerVar or noneVar:
        return False
    return True

def getBoxIndex(edgePart):
    # edgePart contains 5 items: [key, child-index, child-state, source-state, edge]
    currIdx = 0

    for idx, box in enumerate(edgePart[4].info.boxArray):
        if currIdx == edgePart[1]:
            return idx
        if box == None:
            currIdx += 1
        else:
            currIdx += boxCatalogue[box].portArity
    

# Main function implementing process of folding.
# Applying separate folding steps implemented in boxFinding() funtion.
# Respects the chosen box order.
# inputs:
#   'ta' - UBDA that we want to apply folding on,
#   'boxes' - ordered list of box names, which can be used to reduce the 'ta'
# output: (folded) UBDA with applied reductions (same language as the input)
def treeAutFolding(ta: TTreeAut, boxes: list, maxVar: int,
    verbose=False,
    export_vtf=False,
    export_png=False,
    output=None,
    exportPath=None,
) -> TTreeAut:
    result = copy.deepcopy(ta)
    fillBoxArrays(result)  # in case of [None, None] and [] discrepancies
    helper = FoldingHelper(ta, verbose, export_vtf, export_png, output, exportPath, maxVar)
    if helper.vtf or helper.png:
        if not os.path.exists(f"{helper.path}/ubdas/"):
            os.makedirs(f"{helper.path}/ubdas/")
        if not os.path.exists(f"{helper.path}/intersectoids/"):
            os.makedirs(f"{helper.path}/intersectoids/")
    varVis = result.getVariableVisibilityCache()
    for boxName in boxes:
        # print(boxName)
        box = boxCatalogue[boxName]
        worklist = [root for root in ta.rootStates]
        visited = set()
        while worklist != []:
            state = worklist.pop(0)
            if state in visited:
                continue
            edgesToChildren = newPrepareEdgeInfo(result, state)
            for edgePart in edgesToChildren:
                # edgePart contains 5 items: [key, child-index, child-state, source-state, edge]
                part = 'L' if edgePart[1] == 0 else 'H'
                if isAlreadyReduced(result, state, edgePart):
                    # print(f"edgePart ({edgePart[0]}): {edgePart[3]} --[{part}]--> {edgePart[2]}")
                    continue
                helper.minVar = int(edgePart[4].info.variable[len(helper.varPrefix):]) + 1

                # skipping self-loop
                if state in result.transitions[state][edgePart[0]].children:
                    continue
                if helper.verbose: print("%s> boxFinding(%s-[%s:%s]->%s)" % (
                    f"{0 * ' '}", state, part, box.name, edgePart[2]
                ))
                mapping = boxFinding(result, box, edgePart[2], helper, state)

                # phase 0: checking correctness of the mapping
                # checking if all mapped states have a visible variable
                # and have lower variables than states in the UBDA
                if not mappingIsCorrect(mapping, result, varVis):
                    continue
                helper.write("%s> boxFinding(%s-[%s:%s]->%s => %s)\n" % (
                    f"{0 * ' '}", state, 'L' if edgePart[1] == 0 else 'H',
                    box.name, edgePart[2], mapping
                ))
                helper.exportUBDA(result, state, edgePart, box)


                # phase 1: putting the box in the box array
                edge = result.transitions[edgePart[3]][edgePart[0]]
                initialBoxList = edge.info.boxArray
                symbol = edge.info.label
                boxList = [None] * ta.getSymbolArityDict()[symbol]
                for idx in range(len(initialBoxList)):
                    boxList[idx] = initialBoxList[idx]
                # print('a', edgePart, getBoxIndex(edgePart))
                # boxList[edgePart[1]] = box.name
                boxList[getBoxIndex(edgePart)] = box.name
                edge.info.boxArray = boxList
                # print('b', edge)

                # print(edgePart)
                # print(boxList)
                # print(edgePart)
                # phase 2: fill the box-port children in the child array
                idx = getStateIndexFromBoxIndex(edge, getBoxIndex(edgePart))
                edge.children.pop(idx)
                for i, (mapState, var) in enumerate(mapping.values()):
                    edge.children.insert(idx + i, mapState)
                    if var == varVis[mapState]:
                        # TODO: here, possibly remove self-loop(s) in mapState
                        # in case of identical variables (ta, intersectoid)
                        continue
                    newState = f"{mapState}-{var}"
                    if newState in result.transitions:
                        edge.children[idx + i] = newState
                    result.transitions[newState] = {}
                    edge.children[idx + i] = newState
                    newEdge = TTransition(newState, TEdge('LH', [], f"{var}"), [mapState, mapState])
                    varVis[newState] = var
                    helper.counter += 1
                    key = f"temp_{helper.counter2}"
                    helper.counter2 += 1
                    result.transitions[newState][key] = newEdge
                # for state in mapping
            # for edgeInfo
            visited.add(state)
            for edge in iterateEdgesFromState(result, state):
                for child in edge.children:
                    if child not in visited:
                        worklist.append(child)
            # worklist update
        # while worklist != []

    match = re.search(r"\(([^()]*)\)", result.name)
    if match is None:
        result.name = f"folded({ta.name})"    
    else:
        result.name = f"folded({match.group(1)})"
    # print(result)
    return result


# End of folding.py
