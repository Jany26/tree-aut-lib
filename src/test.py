from re import L
from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from test_data import fullAlphabet, boxCatalogue

def noSameChildrenEdgeCheck(ta: TTreeAut) -> bool:
    result = {}
    for edge in transitions(ta):
        if edge[2] == []:
            continue
        child0 = edge[2][0]
        child1 = edge[2][1]
        if child0 not in result:
            result[child0] = {}
        if child1 not in result[child0]:
            result[child0][child1] = 0
        result[child0][child1] += 1
    
    for i, j in result.items():
        for k, l in j.items():
            if l > 1:
                print(i, k, l)
    return True


def testNormalization():
    ta = importTAfromVTF("tests/unfoldingTest5.vtf", 'f')
    symbols = ta.getSymbolArityDict()
    variables = [f"x" + f"{i+1}" for i in range(8)]
    ta = unfold(ta)
    # print(ta)
    ta = normalize(ta, symbols, variables)
    # print(ta)
    ta = compressVariables(ta)
    print(ta)
    print(noSameChildrenEdgeCheck(ta))


def testBoxFinding():
    ta = importTAfromVTF("tests/normalizationTest4.vtf", 'f')
    boxFinding(ta, boxCatalogue['L0'], ta.rootStates[0])


def testHelpers():
    ...


if __name__ == '__main__':
    testNormalization()
    # ta = importTAfromVTF("tests/normalizationTest5.vtf", 'f')
    # symbols = ta.getSymbolArityDict()
    # variables = [f"x" + f"{i+1}" for i in range(5)]
    # print(ta)
    # ta = normalize(ta, symbols, variables)


    # ta1 = importTAfromVTF("tests/normalizationTest1.vtf", 'f')
    # ta2 = importTAfromVTF("tests/tddetX.vtf", 'f')
    # print(ta1)
    # print(ta2)
    # boxFinding(ta1, ta2, ta1.rootStates[0])
# End of file main.py
