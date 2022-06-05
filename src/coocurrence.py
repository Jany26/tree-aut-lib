
from ta_classes import *
from ta_functions import *

from itertools import product
# from typing import Tuple
# import copy


def getCoOccurrentStatesTD(ta: TTreeAut) -> list:

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
                # print(f"process_results {state}: {process_results}")
                result.extend([merge(state, macroList) for macroList in product(*process_results)])
        return result

    # -------------------------------------

    temp = []
    for i in ta.rootStates:
        temp.extend(process(i, ta, []))

    result = []
    for i in temp:
        x = list(i)
        x.sort()
        if x not in result:
            result.append(x)
    return result


def produceOutputTuples(ta1: TTreeAut, ta2: TTreeAut) -> dict:
    outEdges1 = ta1.getOutputEdges(inverse=True)
    outEdges2 = ta2.getOutputEdges(inverse=True)
    result = {}
    for state1 in ta1.transitions:
        for state2 in ta2.transitions:
            key = f"({state1},{state2})"
            entry1 = outEdges1[state1] if state1 in outEdges1 else []
            entry2 = outEdges2[state2] if state2 in outEdges2 else []
            result[key] = (entry1, entry2)
    return result


def isExtension(ta1: TTreeAut, ta2: TTreeAut) -> bool:
    debug = False
    product = removeUselessStates(treeAutProduct(ta1, ta2))
    cooccurrentList = getCoOccurrentStatesTD(product)
    outputTuples = produceOutputTuples(ta1, ta2)
    outEdges = product.getOutputEdges(inverse=True)

    if debug:
        ta1.printTreeAut()
        ta2.printTreeAut()
        product.printTreeAut()
    fullList = []
    for i in cooccurrentList:
        tempList = []
        for j in i:
            tempList.append((j, outputTuples[j]))
        fullList.append(tempList)

    if debug:
        for i in fullList:
            for j in i:
                print(j)
            print()

    # CHECKING LEAF-EDGE CONSISTENCY
    for coocurrence in fullList:
        checkDict = {}
        for state, edgeTuple in coocurrence:
            edges1, edges2 = edgeTuple

            # TODO: GENERALISATION NEEDED
            # e.g. going over all possible leaf-transitions in 1 state

            # for symbol1 in edges1:
            #     if symbol1.startswith("Port"):
            #         print(edgeTuple)
            #         # checkEdgeConsistency(symbol1, edges2, coocurence)

            symbol1 = edges1[0] if edges1 != [] else ""
            symbol2 = edges2[0] if edges2 != [] else ""
            if symbol1 == "" or symbol2 == "":
                continue
            if symbol2 not in checkDict:
                checkDict[symbol2] = []
            if symbol1 not in checkDict[symbol2]:
                checkDict[symbol2].append(symbol1)
        for port, possibleLeafEdges in checkDict.items():
            if len(possibleLeafEdges) != 1:
                # print("False")
                return False

    # print(outEdges)
    fullList = []
    for stateSet in cooccurrentList:
        tupleList = []
        for state in stateSet:
            symbols = outEdges[state] if state in outEdges else []
            # print(symbols)
            if (state, symbols) not in tupleList:
                tupleList.append((state, symbols))
            # print(tupleList)
        if tupleList not in fullList:
            fullList.append(tupleList)

    # print(fullList)
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
            if witnessTree is not None:
                # witnessTree.printNode()
                # print("True")
                return True
    # print("False")
    return False

# End of cooccurrence.py
