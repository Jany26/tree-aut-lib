"""
[file] coocurrence.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for computing coocurence relation between two tree automata.
[note] Part of a preliminary work on trying to find a total order over boxes
with regards to their language inclusion properties.
"""


from ta_classes import *
from ta_functions import *

from itertools import product


def getCoOccurrentStatesTD(ta: TTreeAut) -> list:

    def merge(state, macroList):
        result = [state]
        for item in macroList:
            result.extend(item)
        return set(result)

    def process(state, ta, queue):
        queue.append(state)
        result = []
        for edge in ta.transitions[state].values():
            process_results = []
            for child in edge.children:
                if child == state:
                    continue
                if child in queue:
                    continue
                process_results.append(process(child, ta, queue[:]))

            if edge.children == [] or process_results != []:
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
        print(ta1)
        print(ta2)
        print(product)
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
    fullList = []
    for stateSet in cooccurrentList:
        tupleList = []
        for state in stateSet:
            symbols = outEdges[state] if state in outEdges else []
            if (state, symbols) not in tupleList:
                tupleList.append((state, symbols))
        if tupleList not in fullList:
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
    for listSet in checkList:
        for stateList in listSet.values():
            intersection = None
            for state in stateList:
                product.rootStates = [state]
                intersection = treeAutIntersection(product, intersection)
            witnessTree, witnessStr = nonEmptyTD(intersection)
            if witnessTree is not None:
                return True
    return False

# End of cooccurrence.py
