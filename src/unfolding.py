from ta_classes import *
from ta_functions import *
from test_data import *

boxes = boxCatalogue


def findPortStates(ta: TTreeAut):
    # {portName: stateName}
    result = {}
    for edgeList in ta.transitions.values():
        for edge in edgeList.values():
            label: str = edge.info.label
            if label.startswith("Port") and label not in result:
                result[label] = edge[0]
    # print([result[key] for key in sorted(result.keys())])
    return [result[key] for key in sorted(result.keys())]


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
        box = copy.deepcopy(boxes[boxName])

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


def unfold(ta: TTreeAut) -> TTreeAut:
    # print(ta)
    result = TTreeAut(
        ta.rootStates,
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
                result.transitions[edge.src][key] = edge
                continue

            boxesCount, newEdge = unfoldEdge(result, edge, unfoldCounter, subTable)
            result.transitions[edge.src][key] = newEdge
            unfoldCounter += boxesCount

    for placeState, contentState in subTable.items():
        newDict = {}
        for edge in result.transitions[contentState].values():
            newEdge = copy.copy(edge)
            newEdge.src = placeState
            newKey = f"{newEdge.src}-{newEdge.info.label}-{newEdge.children}"
            newDict[newKey] = newEdge
        result.transitions[placeState] = newDict

    return removeUselessStates(result)


# possibly not needed
def fixKeys(ta: TTreeAut):
    for state, edgeDict in ta.transitions.items():
        newEdgeDict = {}
        for edge in edgeDict.values():
            newKey = f"{edge.src}-{edge.info.label}-{edge.children}"
            newEdgeDict[newKey] = edge
        ta.transitions[state] = newEdgeDict
