# all_tests.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from test_data import *
from format_vtf import *
from format_dot import *
import os

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
    vataExportTests()
    # vataImportTests() # time consuming

    print(">> UNIT TEST: DOT format export ...")
    dotExportTests()
    dotExportFromVTFTests()

    print(">> UNIT TESTS DONE!")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TEST SUITES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def printFailedTests(failedTestsArray):
    try:
        assert failedTestsArray == []
    except:
        print("   ## Tests failed (" + str(len(failedTestsArray)) + "):")
        for i in failedTestsArray:
            print("      " + i)

def matchTest(function:str, ta:str, tree:str, expectingMatch, failures):
    func = functionPtrs[function]
    box = boxesDict[ta]
    testTree = testTreeDict[tree]
    if (expectingMatch and not func(box, testTree)) or (not expectingMatch and func(box, testTree)):
        failures.append(f"{function}({ta}, {tree})")

def nonEmptyTest(function:str, ta:str, expectedResult, failures):
    func = functionPtrs[function]
    box = boxesDict[ta]
    testTree, testString = func(box)

    if expectedResult and (testTree is None or testString == ""):
        failures.append(f"{function}({ta})")
    if not expectedResult and (testTree is not None or testString != ""):
        failures.append(f"{function}({ta})")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTS FOR SUBFUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def getOuptutStatesTests():
    print(" > SUBUNIT TEST: testing getOutputStates() ...")
    failures = []

    if not boxX.getOutputStates() == ['q1']:
        failures.append("boxX.getOutputStates()")
    if not boxH1.getOutputStates() == ['u1', 'u2']:
        failures.append("boxH1.getOutputStates()")
    
    printFailedTests(failures)

def getArityDictTests():
    print(" > SUBUNIT TEST: testing getArityDict() ...")
    failures = []

    if boxX.getSymbolArityDict() != {'LH': 2, 'Port_X': 0}:
        failures.append("boxX.getSymbolArityDict()")
    if boxL0.getSymbolArityDict() != {'LH': 2, '0': 0, 'Port_L0': 0}:
        failures.append("boxL0.getSymbolArityDict()")
    if boxL1.getSymbolArityDict() != {'LH': 2, '1': 0, 'Port_L1': 0}:
        failures.append("boxL1.getSymbolArityDict()")
    if boxH0.getSymbolArityDict() != {'LH': 2, 'Port_H0': 0, '0': 0}:
        failures.append("boxH0.getSymbolArityDict()")
    if boxH1.getSymbolArityDict() != {'LH': 2, 'Port_H1': 0, '1': 0}:
        failures.append("boxH1.getSymbolArityDict()")
    if boxLPort.getSymbolArityDict() != {'LH': 2, 'Port_LPort0': 0, 'Port_LPort1': 0}:
        failures.append("boxLPort.getSymbolArityDict()")

    printFailedTests(failures)

def removeStateTests():
    print(" > SUBUNIT TEST: testing removeState() ...")
    failures = []
       
    boxL0withoutR2 = copy.deepcopy(boxL0)
    boxL0withoutR2.removeState('r2')
    boxesDict["boxL0withoutR2"] = boxL0withoutR2
    boxL1withoutS0 = copy.deepcopy(boxL1)
    boxL1withoutS0.removeState('s0')
    boxesDict["boxL1withoutS0"] = boxL1withoutS0

    matchTest("matchTreeTD", "boxL0withoutR2", "treeL0test1", False, failures)
    matchTest("matchTreeTD", "boxL0withoutR2", "treeL0test2", False, failures)
    matchTest("matchTreeTD", "boxL0withoutR2", "treeL0test3", False, failures)
    matchTest("matchTreeTD", "boxL0withoutR2", "treeL0test4", False, failures)

    matchTest("matchTreeTD", "boxL1withoutS0", "treeL1test1", False, failures)
    matchTest("matchTreeTD", "boxL1withoutS0", "treeL1test2", False, failures)
    matchTest("matchTreeTD", "boxL1withoutS0", "treeL1test3", False, failures)
    matchTest("matchTreeTD", "boxL1withoutS0", "treeL1test4", False, failures)
    
    printFailedTests(failures)

def generateTuplesTest():
    print(" > SUBUNIT TEST: testing generator of possibleChildrenTuples ...")
    failures = []

    if len(generatePossibleChildren('q0', ['q0','q1','q2'], 3)) != 19:
        failures.append("generatePossibleChildren('q0', ['q0','q1','q2'], 3)")
    if len(generatePossibleChildren('q0', ['q0','q1'], 3)) != 7:
        failures.append("generatePossibleChildren('q0', ['q0','q1'], 3)")
    if len(generatePossibleChildren('q0', ['q0','q1'], 2)) != 3:
        failures.append("generatePossibleChildren('q0', ['q0','q1'], 2)")
    if len(generatePossibleChildren('q0', ['q0','q1','q2','q3','q4'], 3)) != 61:
        failures.append("generatePossibleChildren('q0', ['q0','q1','q2','q3','q4'], 3)")
    if len(generatePossibleChildren('q0', ['q0','q1'], 4)) != 15:
        failures.append("generatePossibleChildren('q0', ['q0','q1'], 4)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def matchTestsTD():
    print(" > SUBUNIT TEST: testing top-down match() ...")
    failures = []

    matchTest("matchTreeTD", "boxX", "treeXtest1", True, failures)
    matchTest("matchTreeTD", "boxX", "treeXtest2", False, failures)
    matchTest("matchTreeTD", "boxX", "treeXtest3", True, failures)
    
    matchTest("matchTreeTD", "boxL0", "treeL0test1", True, failures)
    matchTest("matchTreeTD", "boxL0", "treeL0test2", True, failures)
    matchTest("matchTreeTD", "boxL0", "treeL0test3", True, failures)
    matchTest("matchTreeTD", "boxL0", "treeL0test4", True, failures)

    matchTest("matchTreeTD", "boxL0", "treeXtest1", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeXtest2", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeXtest3", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeL1test1", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeL1test2", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeL1test3", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeL1test4", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH0test1", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH0test2", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH0test3", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH0test4", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH1test1", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH1test2", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH1test3", False, failures)
    matchTest("matchTreeTD", "boxL0", "treeH1test4", False, failures)

    matchTest("matchTreeTD", "boxL1", "treeL1test1", True, failures)
    matchTest("matchTreeTD", "boxL1", "treeL1test2", True, failures)
    matchTest("matchTreeTD", "boxL1", "treeL1test3", True, failures)
    matchTest("matchTreeTD", "boxL1", "treeL1test4", True, failures)

    matchTest("matchTreeTD", "boxH0", "treeH0test1", True, failures)
    matchTest("matchTreeTD", "boxH0", "treeH0test2", True, failures)
    matchTest("matchTreeTD", "boxH0", "treeH0test3", True, failures)
    matchTest("matchTreeTD", "boxH0", "treeH0test4", True, failures)

    matchTest("matchTreeTD", "boxH1", "treeH1test1", True, failures)
    matchTest("matchTreeTD", "boxH1", "treeH1test2", True, failures)
    matchTest("matchTreeTD", "boxH1", "treeH1test3", True, failures)
    matchTest("matchTreeTD", "boxH1", "treeH1test4", True, failures)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def matchTestsBU():
    print(" > SUBUNIT TEST: testing bottom-up match() ...")
    failures = []

    matchTest("matchTreeBU", "boxX", "treeXtest1", True, failures)
    matchTest("matchTreeBU", "boxX", "treeXtest2", False, failures)
    matchTest("matchTreeBU", "boxX", "treeXtest3", True, failures)
    
    matchTest("matchTreeBU", "boxL0", "treeL0test1", True, failures)
    matchTest("matchTreeBU", "boxL0", "treeL0test2", True, failures)
    matchTest("matchTreeBU", "boxL0", "treeL0test3", True, failures)
    matchTest("matchTreeBU", "boxL0", "treeL0test4", True, failures)

    matchTest("matchTreeBU", "boxL0", "treeL1test1", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeL1test2", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeL1test3", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeL1test4", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH0test1", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH0test2", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH0test3", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH0test4", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH1test1", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH1test2", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH1test3", False, failures)
    matchTest("matchTreeBU", "boxL0", "treeH1test4", False, failures)

    matchTest("matchTreeBU", "boxL1", "treeL1test1", True, failures)
    matchTest("matchTreeBU", "boxL1", "treeL1test2", True, failures)
    matchTest("matchTreeBU", "boxL1", "treeL1test3", True, failures)
    matchTest("matchTreeBU", "boxL1", "treeL1test4", True, failures)

    matchTest("matchTreeBU", "boxH0", "treeH0test1", True, failures)
    matchTest("matchTreeBU", "boxH0", "treeH0test2", True, failures)
    matchTest("matchTreeBU", "boxH0", "treeH0test3", True, failures)
    matchTest("matchTreeBU", "boxH0", "treeH0test4", True, failures)

    matchTest("matchTreeBU", "boxH1", "treeH1test1", True, failures)
    matchTest("matchTreeBU", "boxH1", "treeH1test2", True, failures)
    matchTest("matchTreeBU", "boxH1", "treeH1test3", True, failures)
    matchTest("matchTreeBU", "boxH1", "treeH1test4", True, failures)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def determinizationTests():
    print(" > SUBUNIT TEST: testing determinization() ...")
    failures = []
    boxesDict["deterministicX"] = treeAutDeterminization(boxesDict["boxX"], fullAlphabet)
    boxesDict["deterministicL0"] = treeAutDeterminization(boxesDict["boxL0"], fullAlphabet)
    boxesDict["deterministicL1"] = treeAutDeterminization(boxesDict["boxL1"], fullAlphabet)
    boxesDict["deterministicH0"] = treeAutDeterminization(boxesDict["boxH0"], fullAlphabet)
    boxesDict["deterministicH1"] = treeAutDeterminization(boxesDict["boxH1"], fullAlphabet)
    boxesDict["deterministicLPort"] = treeAutDeterminization(boxesDict["boxLPort"], fullAlphabet)

    matchTest("matchTreeTD", "deterministicX", "treeXtest1", True, failures)
    matchTest("matchTreeTD", "deterministicX", "treeXtest2", False, failures)
    matchTest("matchTreeTD", "deterministicX", "treeXtest3", True, failures)

    matchTest("matchTreeTD", "deterministicL0", "treeL0test1", True, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL0test2", True, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL0test3", True, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL0test4", True, failures)

    matchTest("matchTreeTD", "deterministicL0", "treeXtest1", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeXtest2", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeXtest3", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL1test1", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL1test2", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL1test3", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeL1test4", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH0test1", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH0test2", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH0test3", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH0test4", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH1test1", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH1test2", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH1test3", False, failures)
    matchTest("matchTreeTD", "deterministicL0", "treeH1test4", False, failures)

    matchTest("matchTreeTD", "deterministicL1", "treeL1test1", True, failures)
    matchTest("matchTreeTD", "deterministicL1", "treeL1test2", True, failures)
    matchTest("matchTreeTD", "deterministicL1", "treeL1test3", True, failures)
    matchTest("matchTreeTD", "deterministicL1", "treeL1test4", True, failures)

    matchTest("matchTreeTD", "deterministicH0", "treeH0test1", True, failures)
    matchTest("matchTreeTD", "deterministicH0", "treeH0test2", True, failures)
    matchTest("matchTreeTD", "deterministicH0", "treeH0test3", True, failures)
    matchTest("matchTreeTD", "deterministicH0", "treeH0test4", True, failures)

    matchTest("matchTreeTD", "deterministicH1", "treeH1test1", True, failures)
    matchTest("matchTreeTD", "deterministicH1", "treeH1test2", True, failures)
    matchTest("matchTreeTD", "deterministicH1", "treeH1test3", True, failures)
    matchTest("matchTreeTD", "deterministicH1", "treeH1test4", True, failures)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def unionTests():
    print(" > SUBUNIT TEST: testing union() ...")
    failures = []
    matchTest("matchTreeTD", "unionL0H0", "treeL0test1", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL0test2", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL0test3", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL0test4", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH0test1", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH0test2", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH0test3", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH0test4", True, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL1test1", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL1test2", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL1test3", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeL1test4", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH1test1", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH1test2", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH1test3", False, failures)
    matchTest("matchTreeTD", "unionL0H0", "treeH1test4", False, failures)

    matchTest("matchTreeTD", "unionL0H1", "treeL0test1", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeL0test2", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeL0test3", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeL0test4", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeH1test1", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeH1test2", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeH1test3", True, failures)
    matchTest("matchTreeTD", "unionL0H1", "treeH1test4", True, failures)

    matchTest("matchTreeTD", "unionXL1", "treeXtest1", True, failures)
    matchTest("matchTreeTD", "unionXL1", "treeXtest2", False, failures)
    matchTest("matchTreeTD", "unionXL1", "treeXtest3", True, failures)
    matchTest("matchTreeTD", "unionXL1", "treeL1test1", True, failures)
    matchTest("matchTreeTD", "unionXL1", "treeL1test2", True, failures)
    matchTest("matchTreeTD", "unionXL1", "treeL1test3", True, failures)
    matchTest("matchTreeTD", "unionXL1", "treeL1test4", True, failures)
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def intersectionTests():
    print(" > SUBUNIT TEST: testing intersection() ...")
    failures = []

    matchTest("matchTreeTD", "intersectionL0H0", "treeL0test1", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeL0test2", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeL0test3", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeL0test4", False, failures)

    matchTest("matchTreeTD", "intersectionL0H0", "treeH0test1", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeH0test2", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeH0test3", False, failures)
    matchTest("matchTreeTD", "intersectionL0H0", "treeH0test4", False, failures)

    boxesDict["intersectionXX"] = treeAutIntersection(boxesDict["boxX"], boxesDict["boxX"])
    boxesDict["intersectionL0L0"] = treeAutIntersection(boxesDict["boxL0"], boxesDict["boxL0"])
    boxesDict["intersectionL1L1"] = treeAutIntersection(boxesDict["boxL1"], boxesDict["boxL1"])
    boxesDict["intersectionH0H0"] = treeAutIntersection(boxesDict["boxH0"], boxesDict["boxH0"])
    boxesDict["intersectionH1H1"] = treeAutIntersection(boxesDict["boxH1"], boxesDict["boxH1"])
    boxesDict["intersectionLPortLPort"] = treeAutIntersection(boxesDict["boxLPort"], boxesDict["boxLPort"])

    matchTest("matchTreeTD", "intersectionL0H0", "treeH0test4", False, failures)

    nonEmptyTest("nonEmptyTD", "intersectionXX",   True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL0L0", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL1L1", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionH0H0", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionH1H1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXX",   True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL0L0", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL1L1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionH0H0", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionH1H1", True, failures)

    # boxesDict["prefixXsuffixL0"] = treeAutIntersection(boxesDict["XprefixForL0"], boxesDict["L0suffix"])
    # boxesDict["prefixXsuffixL1"] = treeAutIntersection(boxesDict["XprefixForL0"], boxesDict["L0suffix"])
    # boxesDict["prefixXsuffixH0"] = treeAutIntersection(boxesDict["XprefixForL0"], boxesDict["L0suffix"])
    # boxesDict["prefixXsuffixH1"] = treeAutIntersection(boxesDict["XprefixForL0"], boxesDict["L0suffix"])
    # boxesDict["prefixL0suffixX"] = treeAutIntersection(boxesDict["L0prefixForX"], boxesDict["Xsuffix"])
    # boxesDict["prefixL1suffixX"] = treeAutIntersection(boxesDict["L1prefixForX"], boxesDict["Xsuffix"])
    # boxesDict["prefixH0suffixX"] = treeAutIntersection(boxesDict["H0prefixForX"], boxesDict["Xsuffix"])
    # boxesDict["prefixH1suffixX"] = treeAutIntersection(boxesDict["H1prefixForX"], boxesDict["Xsuffix"])

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def complementTests():
    print(" > SUBUNIT TEST: testing complement() ...")
    failures = []

    matchTest("matchTreeBU", "complementX", "treeXtest1",  False, failures)
    matchTest("matchTreeBU", "complementX", "treeXtest2",  True, failures)
    matchTest("matchTreeBU", "complementX", "treeXtest3",  False, failures)
    matchTest("matchTreeBU", "complementX", "treeL0test1", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL0test2", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL0test3", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL0test4", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL1test1", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL1test2", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL1test3", True, failures)
    matchTest("matchTreeBU", "complementX", "treeL1test4", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH0test1", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH0test2", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH0test3", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH0test4", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH1test1", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH1test2", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH1test3", True, failures)
    matchTest("matchTreeBU", "complementX", "treeH1test4", True, failures)

    matchTest("matchTreeBU", "complementL0", "treeXtest1",  True, failures)
    matchTest("matchTreeBU", "complementL0", "treeXtest2",  True, failures)
    matchTest("matchTreeBU", "complementL0", "treeXtest3",  True, failures)
    matchTest("matchTreeBU", "complementL0", "treeL0test1", False, failures)
    matchTest("matchTreeBU", "complementL0", "treeL0test2", False, failures)
    matchTest("matchTreeBU", "complementL0", "treeL0test3", False, failures)
    matchTest("matchTreeBU", "complementL0", "treeL0test4", False, failures)
    matchTest("matchTreeBU", "complementL0", "treeL1test1", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeL1test2", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeL1test3", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeL1test4", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH0test1", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH0test2", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH0test3", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH0test4", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH1test1", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH1test2", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH1test3", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeH1test4", True, failures)

    matchTest("matchTreeBU", "complementL1", "treeXtest1",  True, failures)
    matchTest("matchTreeBU", "complementL1", "treeXtest2",  True, failures)
    matchTest("matchTreeBU", "complementL1", "treeXtest3",  True, failures)
    matchTest("matchTreeBU", "complementL1", "treeL0test1", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeL0test2", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeL0test3", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeL0test4", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeL1test1", False, failures)
    matchTest("matchTreeBU", "complementL1", "treeL1test2", False, failures)
    matchTest("matchTreeBU", "complementL1", "treeL1test3", False, failures)
    matchTest("matchTreeBU", "complementL1", "treeL1test4", False, failures)
    matchTest("matchTreeBU", "complementL1", "treeH0test1", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH0test2", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH0test3", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH0test4", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH1test1", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH1test2", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH1test3", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeH1test4", True, failures)

    matchTest("matchTreeBU", "complementH0", "treeXtest1",  True, failures)
    matchTest("matchTreeBU", "complementH0", "treeXtest2",  True, failures)
    matchTest("matchTreeBU", "complementH0", "treeXtest3",  True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL0test1", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL0test2", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL0test3", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL0test4", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL1test1", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL1test2", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL1test3", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeL1test4", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeH0test1", False, failures)
    matchTest("matchTreeBU", "complementH0", "treeH0test2", False, failures)
    matchTest("matchTreeBU", "complementH0", "treeH0test3", False, failures)
    matchTest("matchTreeBU", "complementH0", "treeH0test4", False, failures)
    matchTest("matchTreeBU", "complementH0", "treeH1test1", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeH1test2", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeH1test3", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeH1test4", True, failures)

    matchTest("matchTreeBU", "complementH1", "treeXtest1",  True, failures)
    matchTest("matchTreeBU", "complementH1", "treeXtest2",  True, failures)
    matchTest("matchTreeBU", "complementH1", "treeXtest3",  True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL0test1", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL0test2", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL0test3", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL0test4", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL1test1", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL1test2", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL1test3", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeL1test4", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeH0test1", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeH0test2", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeH0test3", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeH0test4", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeH1test1", False, failures)
    matchTest("matchTreeBU", "complementH1", "treeH1test2", False, failures)
    matchTest("matchTreeBU", "complementH1", "treeH1test3", False, failures)
    matchTest("matchTreeBU", "complementH1", "treeH1test4", False, failures)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def nonEmptyTDTests():
    print(" > SUBUNIT TEST: testing top-down witnessGeneration() ...")
    failures = []

    nonEmptyTest("nonEmptyTD", "boxX",  True, failures)
    nonEmptyTest("nonEmptyTD", "boxL0", True, failures)
    nonEmptyTest("nonEmptyTD", "boxL1", True, failures)
    nonEmptyTest("nonEmptyTD", "boxH0", True, failures)
    nonEmptyTest("nonEmptyTD", "boxH1", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXL0",  False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXL1",  False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXH0",  False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXH1",  False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL0L1", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL0H0", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL0H1", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL1H0", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL1H1", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionH0H1", False, failures)

    printFailedTests(failures)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def nonEmptyBUTests():
    print(" > SUBUNIT TEST: testing bottom-up witnessGeneration() ...")
    failures = []

    nonEmptyTest("nonEmptyBU", "boxX",  True, failures)
    nonEmptyTest("nonEmptyBU", "boxL0", True, failures)
    nonEmptyTest("nonEmptyBU", "boxL1", True, failures)
    nonEmptyTest("nonEmptyBU", "boxH0", True, failures)
    nonEmptyTest("nonEmptyBU", "boxH1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXL0",  False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXL1",  False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXH0",  False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXH1",  False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL0L1", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL0H0", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL0H1", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL1H0", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL1H1", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionH0H1", False, failures)
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def reachabilityTDTests():
    print(" > SUBUNIT TEST: testing top-down reachability() ...")
    failures = []
    
    if set(reachableTD(testBox1)) != set(['q0','q1']):
        failures.append("reachableTD(testBox1)")
    if set(reachableTD(testBox2a)) != set(['q0','q1','q2','q3']):
        failures.append("reachableTD(testBox2a")
    if set(reachableTD(testBox2b)) != set(['q0','q1','q2','q3']):
        failures.append("reachableTD(testBox2b)")
    if set(reachableTD(testBox3)) != set(['r0','r1','r2']):
        failures.append("reachableTD(testBox3)")
  
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def reachabilityBUTests():
    print(" > SUBUNIT TEST: testing bottom-up reachability() ...")
    failures = []
    
    if set(reachableBU(testBox1)) != set(['q1']):
        failures.append("reachableBU(testBox1)")
    if set(reachableBU(testBox2a)) != set(['q0','q1','q2','q3']):
        failures.append("reachableBU(testBox2a")
    if set(reachableBU(testBox2b)) != set(['q0','q1','q2','q3']):
        failures.append("reachableBU(testBox2b)")
    if set(reachableBU(testBox3)) != set(['r0','r1','r2']):
        failures.append("reachableBU(testBox3)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def removeUselessStatesTests():
    print(" > SUBUNIT TEST: testing removeUselessStates() ...")
    failures = []

    removeUselessStates(testBox1)
    removeUselessStates(testBox2a)
    removeUselessStates(testBox2b)

    if set(testBox1.getStates()) != set([]):
        failures.append("removeUselessStates(testBox1)")
    if set(testBox2a.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testBox2a)")
    if set(testBox2b.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testBox2b)")

    # now this test will fail, as edges are not simply strings, 
    # but objects on different adresses (even though they contain the same data)
    # if testBox3.transitions != boxL0.transitions:
    #     failures.append("removeUselessStates(testBox3)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def suffixTests():
    print(" > SUBUNIT TEST: testing suffix() ...")
    failures = []

    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxL0.createSuffix()    
    except: failures.append("boxL0.createSuffix()")

    try: boxL1.createSuffix()    
    except: failures.append("boxL1.createSuffix()")

    try: boxH0.createSuffix()    
    except: failures.append("boxH0.createSuffix()")

    try: boxH1.createSuffix()    
    except: failures.append("boxH1.createSuffix()")

    printFailedTests(failures)    

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prefixTests():
    print(" > SUBUNIT TEST: testing prefix() ...")
    failures = []
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def vataImportTests():
    print(" > SUBUNIT TEST: importing from VATA format ...")
    failures = []
    for subdir, dirs, files in os.walk("../"):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            else:
                try:
                    testBox = importTreeAutFromVTF(filepath)
                    # print(f"      loading from file {filepath}")
                except:
                    failures.append(f"importFromVTF({filepath})")
    printFailedTests(failures)

def vataExportTests():
    print(" > SUBUNIT TEST: exporting to VATA format ...")
    failures = []

    for name, box in boxesDict.items():
        try:
            exportTreeAutToVTF(box, f"vtf/{name}.vtf")
        except:
            failures.append(f"exportToVTF(out/{name}.vtf)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def dotExportTests():
    print(" > SUBUNIT TEST: exporting to DOT format ...")
    failures = []

    for name, box in boxesDict.items():
        try:
            exportTreeAutToDOT(box, f"dot/{name}.dot")
        except:
            failures.append(f"exportToDOT(out/{name}.dot)")

    printFailedTests(failures)

def dotExportFromVTFTests():
    print(" > SUBUNIT TEST: exporting from VTF to DOT format ...")
    failures = []
    for subdir, dirs, files in os.walk("."):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            else:
                try:
                    dotFilepath = "." + os.sep + "vtf-to-dot" + os.sep + file
                    dotFilepath = dotFilepath[:-4] + ".dot"
                    exportVTFToDOT(filepath, dotFilepath)
                except:
                    failures.append(f"exportFromVTFtoDOT({filepath}, {dotFilepath})")

    printFailedTests(failures)

if __name__ == '__main__':
    main()

# End of file all_tests.py
