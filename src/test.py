from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from bdd import *
from apply import *
from utils import *
from dimacs import *
from simulation import *


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BDD testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def bddTest():

    a = BDDnode('a', 'x1')
    b = BDDnode('b', 'x2')
    c = BDDnode('c', 'x3')
    d = BDDnode('d', 'x4')
    e = BDDnode('0', 'x5')
    f = BDDnode('1', 'x6')

    a.attach(b, c)
    b.attach(e, f)
    c.attach(d, e)
    d.attach(f, f)

    bdd1 = BDD('test1', a)

    q0 = BDDnode('e', 'x1')
    q1 = BDDnode('f', 'x2')
    q2 = BDDnode('g', 'x3')
    q3 = BDDnode('h', 'x4')
    q4 = BDDnode('0', 'x5')
    q5 = BDDnode('1', 'x6')

    q0.attach(q1, q2)
    q1.attach(q4, q5)
    q2.attach(q3, q4)
    q3.attach(q5, q5)

    bdd2 = BDD('test2', q0)
    print(compareBDDs(bdd1, bdd2))
    bdd1.printBDD()
    bdd2.printBDD()
    print(bdd1.getVariableList())
    # print(BDD('test1', a))
    # BDD('test1', a).printBDD()


def applyTest():
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x4', t0, t1)
    n2 = BDDnode('n2', 'x2', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd1 = BDD('test1', n3)
    # bdd1.printBDD()
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x2', t0, t1)
    n2 = BDDnode('n2', 'x4', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd2 = BDD('test2', n3)
    # bdd2.printBDD()
    bdd3 = applyFunction('or', bdd1, bdd2, varOrder=None)
    print(bdd3)


def dimacsTest(file: str, override='dnf', verbose=True, horizontalCut=10, maxClausules=30):
    dnf = dimacsRead(file, override=override, verbose=verbose, horizontalCut=horizontalCut, maxClausules=maxClausules)
    print(dnf)
    ta = createTAfromBDD(dnf)
    print(ta)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# normalization testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def normalizationTest():
    ta1 = importTAfromVTF("tests/unfoldingTest1.vtf")
    ta1 = unfold(ta1)
    ta1.reformatStates()
    ta1 = treeAutNormalize(ta1, ['x1', 'x2', 'x3', 'x4'])
    print(ta1)

    ta2 = importTAfromVTF("tests/newNormTest5.vtf")  # already unfolded
    ta2 = copy.deepcopy(ta2)
    ta2 = treeAutNormalize(ta2, ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])
    print(ta2)

    ta3 = importTAfromVTF("tests/newNormTest4-loops.vtf")
    ta3 = unfold(ta3)
    ta3.reformatStates()
    ta3 = treeAutNormalize(ta3, createVarOrder('x', 9))
    print(ta3)


def lexicographicOrderTest():
    ta = importTAfromVTF("../nta/vtf/A0053.vtf", 'f')
    ta = treeAutDeterminization(ta, ta.getSymbolArityDict())
    ta.rootStates = [ta.rootStates[0]]
    ta.reformatStates()
    ta = removeUselessStates(ta)
    ta = normalize(ta, ta.getSymbolArityDict(), createVarOrder('x', 5))
    print(ta)
    test = lexicographicalOrder(ta)
    print(test)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# folding testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def foldTest(variables: int, debug=False):
    # print("INITIAL:")
    ta = importTAfromVTF("tests/newNormTest4.vtf", 'f')
    ta = unfold(ta)
    ta.reformatStates()
    # print(ta)

    # print("\nNORMALIZATION:")
    normta = treeAutNormalize(ta, createVarOrder('x', variables), verbose=debug)
    # print(normta)

    # print("\nFOLDING:")
    foldedta = newFold(normta, boxOrder, verbose=debug)
    # print("\nFINAL RESULT:")
    # ta.printKeys = True
    foldedta.printKeys = True
    # print(foldedta)
    return foldedta

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# simulations
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def dimacsBenchmarkTest():
    bdd1 = dimacsRead("dimacs/uf20-01-simplified.cnf", override='dnf', verbose=True)
    # print(bdd1)
    bdd1.reformatNodes()
    print(bdd1)
    bdd1 = dimacsRead("dimacs/test.cnf", override='dnf', verbose=True)
    print(bdd1)


def simulationTest():
    bdd1 = dimacsRead("dimacs/test.cnf", override='dnf')
    bdd2 = dimacsRead("dimacs/test2.cnf", override='cnf')
    result = simulateAndCompare(bdd1, bdd2, len(bdd1.getVariableList()))
    print("they are same =", result)
    dnf = dimacsRead("dimacs/uf20/uf20-01.cnf", override='dnf', maxClausules=20, verbose=True)
    print(dnf)
    ta = createTAfromBDD(dnf)
    print(ta)


def removeTransition(ta: TTreeAut, state: str, key: str):
    if state in ta.transitions:
        if key in ta.transitions[state]:
            ta.transitions[state].pop(key)


def TAsimulationTest():
    ta = importTAfromVTF("tests/newNormTest4.vtf", 'f')
    ta = unfold(ta)
    taNorm = treeAutNormalize(ta, createVarOrder('x', 8))

    ta2 = newFold(taNorm, boxOrder)
    ta2 = unfold(ta2)
    print(ta2)

    # varAssign = assignVariables(int("00110010", 2), 8)
    result = simulateAndCompare(ta, ta2, 8)
    print("they are same =", result)


def foldTestWithDifferentNormalizations():
    print("\n_____________ initial version _____________\n")
    ta = importTAfromVTF("tests/newNormTest4.vtf", 'f')
    print(ta)
    print("\n_____________ foldTest() version 1 _____________\n")
    ta1 = foldTest(9)  # worklist x worklist
    print(ta1)

    print("\n_____________ unfolded version _____________\n")

    ta = importTAfromVTF("tests/newNormTest4.vtf", 'f')
    ta = unfold(ta)
    ta.printKeys = True
    print(ta)
    varAssign = assignVariables(int("00110010", 2), 8)
    simulateRunTA(ta, varAssign)

    ta1 = unfold(ta1)
    ta1.reformatStates()
    print("ta and ta1 are same =", simulateAndCompare(ta, ta1, 8))


def dimacsDebug():
    # foldTestWithDifferentNormalizations()
    # dimacsTest("./dimacs/test.cnf")
    # dnf = dimacsRead("./dimacs/uf20-01-simplified.cnf", verbose=False, maxClausules=10)
    dnf1 = dimacsRead("./dimacs/apply1.dnf", verbose=False)
    # print(dnf1)
    dnf2 = dimacsRead("./dimacs/apply2.dnf", verbose=False)
    # print(dnf2)
    dnf = applyFunction('or', dnf1, dnf2)
    dnf.name = 'apply'
    # print(res)
    # dnf = dimacsRead("./dimacs/uf20-01-simplified.cnf", verbose=False, maxClausules=10)

    print(f"BDD is valid = {dnf.isValid()}, # of nodes = {dnf.countNodes()}")
    ta = createTAfromBDD(dnf)
    print(ta)
    # taNorm = treeAutNormalize(ta, createVarOrder('', 20))
    # print(taNorm)
    taFold = newFold(ta, boxOrder, verbose=True)
    print(taFold)
    print(len(taFold.transitions))


def testDimacsBenchmark(id: int):
    benchmarkID = id
    dnf = dimacsRead(f"./dimacs/uf20/uf20-0{benchmarkID}.cnf", override='dnf')
    cnf = dimacsRead(f"./dimacs/uf20/uf20-0{benchmarkID}.cnf", override='cnf')
    simulateAndCompare(cnf, dnf, 20, debug=True)
    print(f"{id}, cnf nodes = {cnf.countNodes()}, dnf nodes = {dnf.countNodes()}, same? = {compareBDDs(cnf, dnf)}")


if __name__ == '__main__':
    ta = importTAfromVTF("tests/newNormTest4.vtf")
    ta = unfold(ta)
    ta.reformatKeys()
    ta.reformatStates()
    taNorm = treeAutNormalize(ta, createVarOrder('x', 9))
    print(taNorm)


# End of file main.py
