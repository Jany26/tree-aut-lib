
from ta_classes import *
from ta_functions import *

from itertools import product
# from typing import Tuple
# import copy

def getCoOccurrentStatesTD(ta:TTreeAut) -> list:
    
    def merge(state, macroList):
        # print(f"> merging {state} with {macroList}")
        result = [state]
        for item in macroList:
            result.extend(item)
        # print(f" - merged: {result}")
        return set(result)

    def process(state, ta, queue):
        # print(f"processing {state}")
        queue.append(state)
        result = []
        for edge in ta.transitions[state].values():
            process_results = []
            for child in edge[2]:
                if child == state:
                    continue
                if child in queue:
                    continue
                # print(f" adding {state}->{child}")
                process_results.append(process(child, ta, queue[:]))

            if edge[2] == [] or process_results != []:
                # print( f"process_results {state}: {process_results}")
                result.extend( [ merge(state, macroList) for macroList in product(*process_results) ])
        return result
    
    # -------------------------------------

    temp = []
    for i in ta.rootStates:
        temp.extend(process(i, ta, []))
    return temp


def isExtension(ta1:TTreeAut, ta2:TTreeAut) -> bool:
    product = treeAutProduct(ta1, ta2)
    product = removeUselessStates(product)
    setList = getCoOccurrentStatesTD(product)

    outEdges = product.getOutputEdges(inverse=True)
    # print(outEdges)
    fullList = []
    for stateSet in setList:
        tupleList = []
        for state in stateSet:
            symbols = outEdges[state] if state in outEdges else []
            # print(symbols)
            tupleList.append((state, symbols))
            # print(tupleList)
        fullList.append(tupleList)

    checkList = []
    for tupleList in fullList:
        check = {}
        for item in tupleList:
            for symbol in item[1]:
                if symbol.startswith("Port"):
                    if symbol not in check:
                        check[symbol] = []
                    check[symbol].append(item[0])
        checkList.append(check)
    # print(checkList)
    
    # print(checkList)
    for listSet in checkList:
        # print(">  ", listSet)
        for stateList in listSet.values():
            # print(">>>  ", stateList)
            intersection = None
            for state in stateList:
                product.rootStates = [state]
                intersection = treeAutIntersection(product, intersection)
            witnessTree, witnessStr = nonEmptyTD(intersection)
            # intersection.printTreeAut()
            if witnessTree != None:
                # witnessTree.printNode()
                # print("False")
                return True
    # print("True")1
    return False

# End of cooccurrence.py
