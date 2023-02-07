from utils import *
from ta_classes import *
from ta_functions import *
from test_data import *


# Returns a list of states which have a port transition.
# NOTE: assuming each port only appears once - for one state
def findPortStates(ta: TTreeAut):
    # {portName: stateName}
    result = {}
    for edge in transitions(ta):
        label: str = edge.info.label
        if label.startswith("Port") and label not in result:
            result[label] = edge.src
    # print([result[key] for key in sorted(result.keys())])
    return [result[key] for key in sorted(result.keys())]


# Performs an unfolding operation for one edge (edge with box reductions).
# Adds the transitions from box on the unfolded edge to the resulting TA.
# - counter = for unique state names (if >1 identical boxes are on one edge)
# - subTable = remembers which states ("states with ports" from the box)
# should be substituted for the initial TA states
def unfoldEdge(result: TTreeAut, foldedEdge: TTransition, counter: int, subTable: dict):
    newEdgeInfo = TEdge(foldedEdge.info.label, [], foldedEdge.info.variable)
    newEdge = TTransition(foldedEdge.src, newEdgeInfo, [])
    edge = copy.deepcopy(foldedEdge)
    unfolded = 0

    while edge.info.boxArray != []:
        srcState = edge.src
        boxName = edge.info.boxArray[0]
        edge.info.boxArray.pop(0)
        box = None

        if boxName is None:
            newEdge.children.append(edge.children[0])
            edge.children.pop(0)
            continue
        box = copy.deepcopy(boxCatalogue[boxName])

        children = edge.children[:box.portArity]
        edge.children = edge.children[box.portArity:]

        # unfold the box content into result
        # print(result.name, srcState, box.name, children, counter + unfolded)
        for stateName in box.getStates():
            newName = f"{counter+unfolded}_{stateName}_{srcState}"
            result.transitions[newName] = copy.copy(box.transitions[stateName])
            box.renameState(stateName, newName)
        newEdge.children.extend(box.rootStates)
        connectorList = findPortStates(box)

        for index, state in enumerate(connectorList):
            subTable[state] = children[index]

        unfolded += 1
    return unfolded, newEdge


# The whole 'unfolding' cycle. This function goes through all transitions of
# the tree automaton, searching for 'non-short' edges (or edges labeled with
# boxes) and 'unfolds' them (replaces the part of the edge with corresponding
# box = tree automaton). The cycle creates a new TA from scratch.
def unfold(ta: TTreeAut, reformat=True) -> TTreeAut:
    # stringification of boxes
    result = TTreeAut(
        [i for i in ta.rootStates],
        {s: {} for s in ta.rootStates},
        "unfolded(" + ta.name + ")",
        ta.portArity
    )

    unfoldCounter = 1
    subTable = {}
    for edgeList in ta.transitions.values():
        for key, edge in edgeList.items():
            if edge.src not in result.transitions:
                result.transitions[edge.src] = {}

            # no boxes on transition (all short edges)
            if edge.info.boxArray == []:
                result.transitions[edge.src][key] = copy.deepcopy(edge)
                continue

            boxesCount, newEdge = unfoldEdge(result, edge, unfoldCounter, subTable)
            result.transitions[edge.src][key] = newEdge
            unfoldCounter += boxesCount

    for placeState, contentState in subTable.items():
        newDict = {}
        for edge in result.transitions[contentState].values():
            newEdge = copy.deepcopy(edge)
            newEdge.src = placeState
            newKey = f"{newEdge.src}-{newEdge.info.label}-{newEdge.children}"
            newDict[newKey] = newEdge

        # this line is left in only for testing purposes, it is bugged,
        # as port states got all their initial transitions removed
        # result.transitions[placeState] = newDict

        # it is assumed that only one port transition at a time
        # can be reached from one state
        keyToPop = ""
        for key, edge in result.transitions[placeState].items():
            if edge.info.label.startswith("Port"):
                keyToPop = key
        # merging the transitions from box and initial transitions
        result.transitions[placeState].update(newDict)
        # but also removing the initial port transition
        result.transitions[placeState].pop(keyToPop)

    if reformat is True:
        result.reformatStates()
        result.reformatKeys()
    result = removeUselessStates(result)
    return result


# Goes through all edges and "updates" their keys in the transition lookup
# dictionary. After unfolding, some edges could be labeled incorrectly.
# NOTE: probably obsolete
def fixKeys(ta: TTreeAut):
    for state, edgeDict in ta.transitions.items():
        newEdgeDict = {}
        for edge in edgeDict.values():
            newKey = f"{edge.src}-{edge.info.label}-{edge.children}"
            newEdgeDict[newKey] = edge
        ta.transitions[state] = newEdgeDict


# This function checks if there are any boxes in the tree automaton (UBDA),
# if no boxes are found, the UBDA is unfolded. For testing purposes.
def isUnfolded(ta: TTreeAut) -> bool:
    for edge in transitions(ta):
        for box in edge.info.boxArray:
            if box is not None:
                eprint(f"isUnfolded[ {ta.name} ]: found a box: {edge}")
                return False
    return True


def stringifyBoxes(ta: TTreeAut):
    for edge in transitions(ta):
        newArray = []
        for box in edge.info.boxArray:
            if box is None:
                newArray.append(None)
            elif type(box) == TTreeAut:
                newArray.append(box.name)
            else:
                newArray.append(box)
        edge.info.boxArray = newArray

# End of file unfolding.py
