from re import L
from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from bdd import *
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


def bddTests():
    
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

    # print(BDD('test1', a))
    # (BDD('test1', a)).printBDD()


def tidyUpNames(ta: TTreeAut):
    result = copy.deepcopy(ta)
    i = 0
    for state in iterateBFS(ta):
        result.renameState(state, f"q{i}")
        i += 1
    return result

if __name__ == '__main__':
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

# End of file main.py
