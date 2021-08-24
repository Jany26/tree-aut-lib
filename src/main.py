# main.py
# All unit tests "control panel".
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from all_tests import *

def main():
    print(">> UNIT TEST: helper functions ...")
    getOuptutStatesTests()
    getArityDictTests()
    removeStateTests()
    generateTuplesTest()

    print(">> UNIT TEST: matching trees to TAs ...")
    matchTestsTD()
    matchTestsBU()

    print(">> UNIT TEST: empty language check ...")
    nonEmptyTDTests()
    nonEmptyBUTests()

    print(">> UNIT TEST: basic automata operations ...")
    determinizationTests()
    unionTests()
    intersectionTests()
    complementTests()

    print(">> UNIT TEST: reachable states ...")
    reachabilityTDTests()
    reachabilityBUTests()
    removeUselessStatesTests()
    
    print(">> UNIT TEST: partial order finding ...")
    suffixTests()
    prefixTests()

    print(">> UNIT TEST: VATA format parsing ...")
    vtfExportTests()
    # vtfImportTests() # time consuming

    print(">> UNIT TEST: TMB format parsing ...")
    tmbExportTests()
    # tmbImportTests() # time consuming
    
    print(">> UNIT TEST: DOT format export ...")
    dotExportTests()
    dotExportFromVTFTests()

    # print(">> UNIT TEST: extra tests ...")
    # extraTests()

    print(">> UNIT TESTS DONE!")


if __name__ == '__main__':
    main()

# End of file main.py
