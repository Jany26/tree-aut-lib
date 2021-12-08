
from typing import NewType
from ta_classes import *
from ta_functions import *
from test_data import *

boxes = boxCatalogue

def unfoldEdge(refTa: TTreeAut, resultTa:TTreeAut, key:str, edge: list, index: int):
    # initialization phase
    boxArray = []
    for box in edge[1].boxArray:
        if box in boxes:
            boxArray.append(copy.deepcopy(boxes[box]))
        else:
            boxArray.append(None)
    
    currentIndex = 0
    # main cycle
    workEdge = copy.deepcopy(edge)
    # print(f"unfolding edge {edge}")
    # print(f"boxarray = {len(boxArray)}")
    for workBox in boxArray:
        if box == None:
            workEdge[1].boxArray.pop(0)
            continue

        # print(f"STEP {index}")
        
        portArity = workBox.portArity
        for state in workBox.getStates():
            workBox.renameState(state, f"{state}_{edge[0]}_{index}")
        
        # print(workBox)
        # print(f"BOXARRAY = {edge[1].boxArray}")
        # print(f"CURRENT BOX UNFOLDING #{currentIndex} = {edge[1].boxArray[currentIndex]}")
        # print(f"CHILDREN = {edge[2]}")
        
        # set output ports in the box which we are unfolding into the TA
        # such that they point to the children from initial edge structure of the TA
        portNo = 0
        doneSymbols = []
        for symbol, stateList in workBox.getOutputEdges().items():
            if symbol.startswith("Port") and symbol not in doneSymbols:
                for i in stateList:
                    # print(str(workEdge)[1:-1])
                    # print(f"port mapping '{i}' to '{edge[2][currentIndex]}'")
                    workBox.renameState(i, edge[2][currentIndex])
                doneSymbols.append(symbol)
                portNo += 1
        
        # adding all states from the box to the initial TA
        for state in workBox.getStates():
            resultTa.transitions[state] = workBox.transitions[state]
        
        # remove as many children as the box has ports
        for i in range(portArity):
            # print(f"popping {edge[2][curIndex]}")
            workEdge[2].pop(currentIndex)
        # connect sourceState from initial edge structure to rootstate of the box
        # assuming the rootState list only contains one state !!!
        workEdge[2].insert(currentIndex, workBox.rootStates[0])
        # remove a box from edge info
        workEdge[1].boxArray.pop(0)
        index += 1
        currentIndex += 1 # currentIndex is for indexing stuff alongside the currently unfolded edge
        resultTa.transitions[workEdge[0]][key] = workEdge
        # print(resultTa)
    return currentIndex

# function input is the object containing folded transitions
# the objective of unfold() is to unfold these transitions
# we dont want to have any edges labeled with boxes, only short edges (no reductions)
def unfold(ta:TTreeAut) -> TTreeAut:
    result = copy.deepcopy(ta) # result will be edited, because we iterate over ta
    
    # counter is needed for resolving state name conflicts
    unfold_counter = 1
    
    for edgeDict in ta.transitions.values():
        for key, edge in edgeDict.items():
            unfoldedAmount = unfoldEdge(ta, result, key, edge, unfold_counter)
            unfold_counter += unfoldedAmount
    # print("RESULT")
    # print(result)
    return result
    