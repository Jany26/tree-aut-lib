from re import L
from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from test_data import fullAlphabet, boxCatalogue


boxOrder = ['LPort', 'HPort', 'L0', 'L1', 'H0', 'H1', 'X']


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


def testFold():
    # ta = importTAfromVTF("tests/normalizationTest5.vtf", 'f')
    ta = importTAfromVTF("tests/unfoldingTest5.vtf", 'f')
    symbols = ta.getSymbolArityDict()
    variables = [f"x" + f"{i+1}" for i in range(8)]
    ta = unfold(ta)
    ta = normalize(ta, symbols, variables)

    i = 0
    ta1 = copy.deepcopy(ta)
    for state in iterateBFS(ta1):
        ta.renameState(state, f"q{i}")
        i += 1

    print(ta)
    fold(ta, boxOrder)


def testHelpers():
    ta = importTAfromVTF("tests/unfoldingTest3.vtf", 'f')
    for i in iterateDFS(ta):
        print(i)


if __name__ == '__main__':
    ta = importTAfromVTF("tests/foldingTest1.vtf", 'f')
    ta = unfold(ta)
    symbols = ta.getSymbolArityDict()
    variables = [f"x" + f"{i+1}" for i in range(8)]
    ta = normalize(ta, symbols, variables)
    # print(ta)
    xy = fold(ta, boxOrder)
    # print(xy)
# End of file main.py
