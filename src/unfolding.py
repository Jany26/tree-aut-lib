from ta_classes import *
from ta_functions import *
from test_data import *

boxes = boxCatalogue

def findPortStates(ta: TTreeAut):
    # {portName: stateName}
    result = {}
    for edgeList in ta.transitions.values():
        for edge in edgeList.values():
            label: str = edge[1].label
            if label.startswith("Port") and label not in result:
                result[label] = edge[0]
    # print([result[key] for key in sorted(result.keys())])
    return [result[key] for key in sorted(result.keys())]


def unfoldEdge(result: TTreeAut, foldedEdge: TEdge, counter: int, subTable: dict):
    newEdgeInfo = TEdge(foldedEdge[1].label, [], foldedEdge[1].variable)
    newEdge = [foldedEdge[0], newEdgeInfo, []]
    edge = copy.deepcopy(foldedEdge)
    unfolded = 0
    
    while edge[1].boxArray != []:
        srcState = edge[0]
        boxName = edge[1].boxArray[0]
        edge[1].boxArray.pop(0)
        box = None 
        
        if boxName == None:
            newEdge[2].append(edge[2][0])
            edge[2].pop(0)
            continue
        box = copy.deepcopy(boxes[boxName])
   
        children = edge[2][:box.portArity]
        edge[2] = edge[2][box.portArity:]

        # unfold the box content into result
        # print(result.name, srcState, box.name, children, counter + unfolded)
        for stateName in box.getStates():
            newName = f"{counter+unfolded}_{stateName}_{srcState}"
            result.transitions[newName] = copy.copy(box.transitions[stateName])
            box.renameState(stateName, newName)
        newEdge[2].extend(box.rootStates)
        connectorList = findPortStates(box)

        for index, state in enumerate(connectorList):
            subTable[state] = children[index]


        unfolded += 1
    return unfolded, newEdge
    
def unfold(ta:TTreeAut) -> TTreeAut:
    # print(ta)
    result = TTreeAut(
        ta.rootStates, 
        {s:{} for s in ta.rootStates}, 
        ta.name + "_unfolded", 
        ta.portArity
    )

    unfoldCounter = 1
    subTable = {}
    for edgeList in ta.transitions.values():
        for key, edge in edgeList.items():
            if edge[0] not in result.transitions:
                result.transitions[edge[0]] = {}

            # no boxes on transition (all short edges)
            if edge[1].boxArray == []:
                result.transitions[edge[0]][key] = edge
                continue

            boxesCount, newEdge = unfoldEdge(result, edge, unfoldCounter, subTable)
            result.transitions[edge[0]][key] = newEdge
            unfoldCounter += boxesCount

    for placeState, contentState in subTable.items():
        newDict = {}
        for edge in result.transitions[contentState].values():
            newEdge = copy.copy(edge)
            newEdge[0] = placeState
            newKey = f"{newEdge[0]}-{newEdge[1].label}-{newEdge[2]}"
            newDict[newKey] = newEdge
        result.transitions[placeState] = newDict

    return removeUselessStates(result)

# possibly not needed
def fixKeys(ta:TTreeAut):
    for state, edgeDict in ta.transitions.items():
        newEdgeDict={}
        for edge in edgeDict.values():
            newKey = f"{edge[0]}-{edge[1].label}-{edge[2]}"
            newEdgeDict[newKey] = edge
        ta.transitions[state] = newEdgeDict