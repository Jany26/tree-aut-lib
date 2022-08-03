from re import L
from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from bdd import *
from apply import *
from utils import *


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


def tidyUpNames(ta: TTreeAut):
    result = copy.deepcopy(ta)
    i = 0
    for state in iterateBFS(ta):
        result.renameState(state, f"q{i}")
        i += 1
    return result


def foldTest():
    print("INITIAL:")
    ta = importTAfromVTF("tests/unfoldingTest1.vtf", 'f')
    print(ta)

    print("\nUNFOLDING:")
    ta = unfold(ta)
    print(ta)

    print("\nNORMALIZATION:")
    ta = normalize(ta, ta.getSymbolArityDict(), testVarOrder)
    ta = tidyUpNames(ta)
    print(compressVariables(ta))

    print("\nFOLDING:")
    ta = fold(ta, boxOrder)
    print(ta)


if __name__ == '__main__':
    # bddTest()
    applyTest()
# End of file main.py
