from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from bdd import *
from apply import *
from utils import *
from dimacs import *


def testFold():
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


def bddTest():

    failures = []

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
    # (BDD('test1', a)).printBDD()


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

def foldTest():
    # print("INITIAL:")
    ta = importTAfromVTF("tests/newNormTest4.vtf", 'f')
    # print(ta)

    # print("\nUNFOLDING:")
    ta = unfold(ta)
    # print(ta)
    # print("\nUNFOLDING RENAMED:")
    ta.reformatStates()
    print(ta)

    print("\nNORMALIZATION:")
    ta = treeAutNormalize(ta, createVarOrder('x', 9))
    # ta.reformatStates()
    # ta.name = "unfoldingTest1"
    # print(compressVariables(ta))
    # for state in iterateDFS(ta):
    #     print(state)
    print(ta)

    print("\nFOLDING:")
    ta = fold(ta, boxOrder)
    print("\nFINAL RESULT:")
    print(ta)
    # for edge in transitions(ta):
    #     for box in edge.info.boxArray:
    #         if box is not None:
    #             print(box.name)
    # for intersectoid, mapping in midResults:
    #     print(f"\nMAPPING = {mapping}")
    #     print("\nINTERSECTOID")
    #     print(intersectoid)


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


def dimacsTest():
    dnf = dimacsRead("./dimacs/test.dnf")
    dnf.printBDD()
    dimacsWrite(dnf, "dimacs-out/output.dnf")

def normalizationTest():
    # ta1 = importTAfromVTF("tests/unfoldingTest1.vtf")
    # ta1 = unfold(ta1)
    # ta1.reformatStates()
    # ta1 = treeAutNormalize(ta, ['x1', 'x2', 'x3', 'x4'])
    # print(ta1)

    # ta2 = importTAfromVTF("tests/newNormTest5.vtf")  # already unfolded
    # ta2 = copy.deepcopy(ta2)
    # ta2 = treeAutNormalize(ta2, ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])
    # print(ta2)

    ta3 = importTAfromVTF("tests/newNormTest4-loops.vtf")
    ta3 = unfold(ta3)
    ta3.reformatStates()
    ta3 = treeAutNormalize(ta3, createVarOrder('x', 9))
    print(ta3)


if __name__ == '__main__':
    # bddTest()
    # applyTest()
    foldTest()
    # lexicographicOrderTest()
    # dimacsTest()
    # normalizationTest()
# End of file main.py
