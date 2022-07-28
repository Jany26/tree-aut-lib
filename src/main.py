# main.py
# All unit tests "control panel".
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from all_tests import *

verbose = False  # printing more detailed info on output during tests


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

    print(">> UNIT TEST: VATA/TMB/DOT format import/export ...")
    vtfExportTests()
    # vtfImportTests() # time consuming
    tmbExportTests()
    # tmbImportTests() # time consuming
    dotExportTests()
    dotExportFromVTFTests()

    print(">> UNIT TEST: extra tests ...")
    wellDefinedTests(verbose)
    commutativityTests(verbose)
    # comparabilityTests()
    # productTests()
    # extensionTests()

    # sanityTests()
    unfoldingTests()
    normalizationTests()
    print(">> UNIT TESTS DONE!")


if __name__ == '__main__':
    main()
    extraTests()

# End of file main.py
