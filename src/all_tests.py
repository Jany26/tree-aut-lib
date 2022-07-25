# all_tests.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# from _typeshed import FileDescriptor
from io import TextIOWrapper
from jupyter import convertToDOT
from test_data import *
from format_vtf import *
from format_tmb import *
from format_dot import *
import os
import gc

from coocurrence import *
from unfolding import *
from normalization import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TEST SUITES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def printFailedTests(failedTestsArray):
    try:
        assert failedTestsArray == []
    except AssertionError:
        print("   ## Tests failed (" + str(len(failedTestsArray)) + "):")
        for i in failedTestsArray:
            print("      " + i)


def matchTest(function: str, ta: str, tree: str, expectedResult, failures):
    func = functionPtrs[function]
    box = boxesDict[ta]
    testTree = testTreeDict[tree]
    actualResult = func(box, testTree)
    if expectedResult != actualResult:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"{function}({ta}, {tree})", str(expectedResult), str(actualResult)
        ))


def nonEmptyTest(function: str, ta: str, expectedResult, failures):
    func = functionPtrs[function]
    box = boxesDict[ta]
    testTree, testString = func(box)
    actualResult = False if (testTree is None or testString == "") else True
    if expectedResult != actualResult:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"{function}({ta})", str(expectedResult), str(actualResult)
        ))


def wellDefinedTest(ta: str, expectedResult, errDisplay, failures):
    box = boxesDict[ta]
    actualResult = isWellDefined(box, errDisplay)
    if actualResult != expectedResult:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"isWellDefined({ta})", str(expectedResult), str(actualResult)
        ))

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

    if len(generatePossibleChildren('q0', ['q0', 'q1', 'q2'], 3)) != 19:
        failures.append("generatePossibleChildren('q0', ['q0', 'q1', 'q2'], 3)")
    if len(generatePossibleChildren('q0', ['q0', 'q1'], 3)) != 7:
        failures.append("generatePossibleChildren('q0', ['q0', 'q1'], 3)")
    if len(generatePossibleChildren('q0', ['q0', 'q1'], 2)) != 3:
        failures.append("generatePossibleChildren('q0', ['q0', 'q1'], 2)")
    if len(generatePossibleChildren('q0', ['q0', 'q1', 'q2', 'q3', 'q4'], 3)) != 61:
        failures.append("generatePossibleChildren('q0', ['q0', 'q1', 'q2', 'q3', 'q4'], 3)")
    if len(generatePossibleChildren('q0', ['q0', 'q1'], 4)) != 15:
        failures.append("generatePossibleChildren('q0', ['q0', 'q1'], 4)")

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


def sanityUnitTest(box: TTreeAut, f: TextIOWrapper):
    f.write(f"\ncomplement({box.name}) ... ")
    f.flush()
    print(f"complement({box.name}) ... ", flush=True)

    comp = treeAutComplement(box, box.getSymbolArityDict(), verbose=False)

    f.write(f"\nintersection({box.name}, {comp.name}) ... ")
    f.flush()
    print(f"intersection({box.name}, {comp.name}) ... ", flush=True)

    inter = treeAutIntersection(box, comp, verbose=False)

    f.write(f"\nnonEmptiness({inter.name}) ... ")
    f.flush()
    print(f"nonEmptiness({inter.name}) ... ", flush=True)

    witnessT, witnessS = nonEmptyTD(inter, verbose=False)

    f.write(f"\nsanityTest({str(box.name)}) result = ")
    f.write("OK" if witnessT is None else "ERROR")
    f.write("\n")
    f.flush()


def sanityTests():
    print(" > SUBUNIT TEST: testing determinization() with sanity tests ...")
    fileArray = []
    f = open("../progress.txt", "w")
    f.write("---- SANITY TESTS START ----\n")
    for subdir, dirs, files in os.walk("../nta/"):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            fileArray.append(filepath)
    fileArray.sort()
    for i in fileArray:
        testBox = importTAfromVTF(i)
        sanityUnitTest(testBox, f)
        fileArray.remove(i)
        gc.collect()
    f.write("\n---- SANITY TESTS END ----\n")
    f.close()

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

    nonEmptyTest("nonEmptyTD", "intersectionXX", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL0L0", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionL1L1", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionH0H0", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionH1H1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXX", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL0L0", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionL1L1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionH0H0", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionH1H1", True, failures)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def complementTests():
    print(" > SUBUNIT TEST: testing complement() ...")
    failures = []

    matchTest("matchTreeBU", "complementX", "treeXtest1", False, failures)
    matchTest("matchTreeBU", "complementX", "treeXtest2", True, failures)
    matchTest("matchTreeBU", "complementX", "treeXtest3", False, failures)
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

    matchTest("matchTreeBU", "complementL0", "treeXtest1", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeXtest2", True, failures)
    matchTest("matchTreeBU", "complementL0", "treeXtest3", True, failures)
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

    matchTest("matchTreeBU", "complementL1", "treeXtest1", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeXtest2", True, failures)
    matchTest("matchTreeBU", "complementL1", "treeXtest3", True, failures)
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

    matchTest("matchTreeBU", "complementH0", "treeXtest1", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeXtest2", True, failures)
    matchTest("matchTreeBU", "complementH0", "treeXtest3", True, failures)
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

    matchTest("matchTreeBU", "complementH1", "treeXtest1", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeXtest2", True, failures)
    matchTest("matchTreeBU", "complementH1", "treeXtest3", True, failures)
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

    nonEmptyTest("nonEmptyTD", "boxX", True, failures)
    nonEmptyTest("nonEmptyTD", "boxL0", True, failures)
    nonEmptyTest("nonEmptyTD", "boxL1", True, failures)
    nonEmptyTest("nonEmptyTD", "boxH0", True, failures)
    nonEmptyTest("nonEmptyTD", "boxH1", True, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXL0", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXL1", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXH0", False, failures)
    nonEmptyTest("nonEmptyTD", "intersectionXH1", False, failures)
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

    nonEmptyTest("nonEmptyBU", "boxX", True, failures)
    nonEmptyTest("nonEmptyBU", "boxL0", True, failures)
    nonEmptyTest("nonEmptyBU", "boxL1", True, failures)
    nonEmptyTest("nonEmptyBU", "boxH0", True, failures)
    nonEmptyTest("nonEmptyBU", "boxH1", True, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXL0", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXL1", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXH0", False, failures)
    nonEmptyTest("nonEmptyBU", "intersectionXH1", False, failures)
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

    if set(reachableTD(testUnreachable1)) != set(['q0', 'q1']):
        failures.append("reachableTD(testUnreachable1)")
    if set(reachableTD(testUnreachable2)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachableTD(testUnreachable2")
    if set(reachableTD(testUnreachable3)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachableTD(testUnreachable3)")
    if set(reachableTD(copy.deepcopy(boxL0))) != set(['r0', 'r1', 'r2']):
        failures.append("reachableTD(boxL0copy)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def reachabilityBUTests():
    print(" > SUBUNIT TEST: testing bottom-up reachability() ...")
    failures = []

    if set(reachableBU(testUnreachable1)) != set(['q1']):
        failures.append("reachableBU(testUnreachable1)")
    if set(reachableBU(testUnreachable2)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachableBU(testUnreachable2")
    if set(reachableBU(testUnreachable3)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachableBU(testUnreachable3)")
    if set(reachableBU(copy.deepcopy(boxL0))) != set(['r0', 'r1', 'r2']):
        failures.append("reachableBU(boxL0copy)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def removeUselessStatesTests():
    print(" > SUBUNIT TEST: testing removeUselessStates() ...")
    failures = []

    cleanTestBox1 = removeUselessStates(testUnreachable1)
    cleanTestBox2a = removeUselessStates(testUnreachable2)
    cleanTestBox2b = removeUselessStates(testUnreachable3)

    if set(cleanTestBox1.getStates()) != set([]):
        failures.append("removeUselessStates(testUnreachable1)")
    if set(cleanTestBox2a.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testUnreachable2)")
    if set(cleanTestBox2b.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testUnreachable3)")

    # now this test will fail, as edges are not simply strings,
    # but objects on different adresses (even though they contain the same data)

    # if copy.deepcopy(boxL0).transitions != boxL0.transitions:
    #     failures.append("removeUselessStates(copy.deepcopy(boxL0))")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def vtfImportTests():
    print(" > SUBUNIT TEST: importing from VATA format ...")
    failures = []
    for subdir, dirs, files in os.walk("../"):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            else:
                try:
                    testBox = importTAfromVTF(filepath, 'f')
                except Exception as e:
                    failures.append(f"importFromVTF({filepath})")
    printFailedTests(failures)


def vtfExportTests():
    print(" > SUBUNIT TEST: exporting to VATA format ...")
    failures = []

    if not os.path.exists("vtf"):
        os.makedirs("vtf")

    for name, box in boxesDict.items():
        try:
            exportTAtoVTF(box, 'f', f"vtf/{name}.vtf")
        except Exception as e:
            failures.append(f"exportToVTF(out/{name}.vtf)")
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def dotExportTests():
    print(" > SUBUNIT TEST: exporting to DOT format ...")
    failures = []

    if not os.path.exists("dot"):
        os.makedirs("dot")

    for name, box in boxesDict.items():
        try:
            exportTreeAutToDOT(box, f"dot/{name}.dot")
        except Exception as e:
            failures.append(f"exportToDOT(out/{name}.dot)")
    printFailedTests(failures)


def dotExportFromVTFTests():
    print(" > SUBUNIT TEST: exporting from VTF to DOT format ...")
    failures = []

    if not os.path.exists("vtf-to-dot"):
        os.makedirs("vtf-to-dot")

    for subdir, dirs, files in os.walk("."):
        for file in files:
            filePath = subdir + os.sep + file
            if filePath.endswith(".vtf"):
                try:
                    dotFilePath = "." + os.sep + "vtf-to-dot" + os.sep + file
                    dotFilePath = dotFilePath[:-4] + ".dot"
                    ta = importTAfromVTF(filePath, 'f')
                    exportTreeAutToDOT(ta, dotFilePath)
                except Exception as e:
                    failures.append(f"exportFromVTFtoDOT({filePath}, {dotFilePath})")
    printFailedTests(failures)


def tmbImportTests():
    print(" > SUBUNIT TEST: importing from TMB format ...")
    failures = []

    for subdir, dirs, files in os.walk(".."):
        for file in files:
            filePath = subdir + os.sep + file
            if filePath.endswith(".tmb"):
                try:
                    testBox = importTAfromTMB(filePath)
                except Exception as e:
                    failures.append(f"importTAfromTMB({filePath})")

    printFailedTests(failures)


def tmbExportTests():
    print(" > SUBUNIT TEST: exporting to TMB format ...")

    if not os.path.exists("tmb"):
        os.makedirs("tmb")

    failures = []
    for name, box in boxesDict.items():
        try:
            exportTAtoTMB(box, 'f', f"tmb/{name}.tmb")
        except Exception as e:
            failures.append(f"exportTreeAutToTMB(tmb/{name}.tmb)")

    printFailedTests(failures)


def wellDefinedTests(verbose=False):
    print(" > SUBUNIT TEST: checking if the boxes are well-defined ...")
    failures = []

    wellDefinedTest("boxX", True, verbose, failures)
    wellDefinedTest("boxL0", True, verbose, failures)
    wellDefinedTest("boxL1", True, verbose, failures)
    wellDefinedTest("boxH0", True, verbose, failures)
    wellDefinedTest("boxH1", True, verbose, failures)
    wellDefinedTest("boxLPort", True, verbose, failures)

    wellDefinedTest("unionXL0", False, verbose, failures)
    wellDefinedTest("unionXL1", False, verbose, failures)
    wellDefinedTest("unionXH0", False, verbose, failures)
    wellDefinedTest("unionXH1", False, verbose, failures)
    wellDefinedTest("unionL0H0", False, verbose, failures)
    wellDefinedTest("unionL0H1", False, verbose, failures)
    wellDefinedTest("unionL0L1", False, verbose, failures)
    wellDefinedTest("unionL1H0", False, verbose, failures)
    wellDefinedTest("unionL1H1", False, verbose, failures)
    wellDefinedTest("unionH0H1", False, verbose, failures)

    wellDefinedTest("intersectionXL0", False, verbose, failures)
    wellDefinedTest("intersectionXL1", False, verbose, failures)
    wellDefinedTest("intersectionXH0", False, verbose, failures)
    wellDefinedTest("intersectionXH1", False, verbose, failures)
    wellDefinedTest("intersectionL0H0", False, verbose, failures)
    wellDefinedTest("intersectionL0H1", False, verbose, failures)
    wellDefinedTest("intersectionL0L1", False, verbose, failures)
    wellDefinedTest("intersectionL1H0", False, verbose, failures)
    wellDefinedTest("intersectionL1H1", False, verbose, failures)
    wellDefinedTest("intersectionH0H1", False, verbose, failures)

    wellDefinedTest("complementX", False, verbose, failures)
    wellDefinedTest("complementL0", False, verbose, failures)
    wellDefinedTest("complementL1", False, verbose, failures)
    wellDefinedTest("complementH0", False, verbose, failures)
    wellDefinedTest("complementH1", False, verbose, failures)
    wellDefinedTest("complementLPort", False, verbose, failures)

    wellDefinedTest("determinizedX", False, verbose, failures)
    wellDefinedTest("determinizedL0", False, verbose, failures)
    wellDefinedTest("determinizedL1", False, verbose, failures)
    wellDefinedTest("determinizedH0", False, verbose, failures)
    wellDefinedTest("determinizedH1", False, verbose, failures)
    wellDefinedTest("determinizedLPort", False, verbose, failures)

    wellDefinedTest("Xsuffix", True, verbose, failures)
    wellDefinedTest("L0suffix", False, verbose, failures)
    wellDefinedTest("L1suffix", False, verbose, failures)
    wellDefinedTest("H0suffix", False, verbose, failures)
    wellDefinedTest("H1suffix", False, verbose, failures)

    wellDefinedTest("XprefixForL0", False, verbose, failures)
    wellDefinedTest("XprefixForL1", False, verbose, failures)
    wellDefinedTest("XprefixForH0", False, verbose, failures)
    wellDefinedTest("XprefixForH1", False, verbose, failures)
    wellDefinedTest("L0prefixForX", False, verbose, failures)
    wellDefinedTest("L0prefixForL1", False, verbose, failures)
    wellDefinedTest("L0prefixForH0", False, verbose, failures)
    wellDefinedTest("L0prefixForH1", False, verbose, failures)
    wellDefinedTest("L1prefixForX", False, verbose, failures)
    wellDefinedTest("L1prefixForL0", False, verbose, failures)
    wellDefinedTest("L1prefixForH0", False, verbose, failures)
    wellDefinedTest("L1prefixForH1", False, verbose, failures)
    wellDefinedTest("H0prefixForX", False, verbose, failures)
    wellDefinedTest("H0prefixForL0", False, verbose, failures)
    wellDefinedTest("H0prefixForL1", False, verbose, failures)
    wellDefinedTest("H0prefixForH1", False, verbose, failures)
    wellDefinedTest("H1prefixForX", False, verbose, failures)
    wellDefinedTest("H1prefixForL0", False, verbose, failures)
    wellDefinedTest("H1prefixForL1", False, verbose, failures)
    wellDefinedTest("H1prefixForH0", False, verbose, failures)

    printFailedTests(failures)
    pass


def commutativityTest(ta1: str, ta2: str, expectedResult, verbose, failures):
    box1 = boxesDict[ta1]
    box2 = boxesDict[ta2]
    actualResult1 = areCommutative(box1, box2)
    actualResult2 = areCommutative(box2, box1)
    if expectedResult != actualResult1:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"areCommutative({ta1}, {ta2})", str(expectedResult), str(actualResult1)
        ))
    if expectedResult != actualResult2:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"areCommutative({ta2}, {ta1})", str(expectedResult), str(actualResult2)
        ))
    if verbose and actualResult1 != actualResult2:
        print("WARNING: commutativity test gives inconsistent results")


def commutativityTests(verbose=False):
    print(" > SUBUNIT TEST: testing commutativity ...")
    failures = []

    commutativityTest("boxX", "boxL0", False, verbose, failures)
    commutativityTest("boxX", "boxL1", False, verbose, failures)
    commutativityTest("boxX", "boxH0", False, verbose, failures)
    commutativityTest("boxX", "boxH1", False, verbose, failures)
    commutativityTest("boxX", "boxLPort", False, verbose, failures)
    commutativityTest("boxX", "boxHPort", False, verbose, failures)

    commutativityTest("boxL0", "boxL1", True, verbose, failures)  # True !
    commutativityTest("boxL0", "boxH0", False, verbose, failures)
    commutativityTest("boxL0", "boxH1", False, verbose, failures)
    commutativityTest("boxL0", "boxLPort", False, verbose, failures)
    commutativityTest("boxL0", "boxHPort", False, verbose, failures)

    commutativityTest("boxL1", "boxH0", False, verbose, failures)
    commutativityTest("boxL1", "boxH1", False, verbose, failures)
    commutativityTest("boxL1", "boxLPort", False, verbose, failures)
    commutativityTest("boxL1", "boxHPort", False, verbose, failures)

    commutativityTest("boxH0", "boxH1", True, verbose, failures)  # True !
    commutativityTest("boxH0", "boxLPort", False, verbose, failures)
    commutativityTest("boxH0", "boxHPort", False, verbose, failures)

    commutativityTest("boxH1", "boxLPort", False, verbose, failures)
    commutativityTest("boxH1", "boxHPort", False, verbose, failures)

    commutativityTest("boxLPort", "boxHPort", False, verbose, failures)

    printFailedTests(failures)


def comparabilityTestAdvanced(ta1, expectedResult, ta2, failures):
    box1 = boxesDict[ta1]
    box2 = boxesDict[ta2]
    res1 = areComparable(box1, box2)
    res2 = areComparable(box2, box1)
    print(f"\t res1 = {res1}, res2 = {res2}")
    if expectedResult == ">" and res1 is True and res2 is False:
        return
    if expectedResult == "<" and res1 is False and res2 is True:
        return
    if expectedResult == "?" and res1 is False and res2 is False:
        return
    failures.append("{:<50}".format(f"areComparable({ta1}, {ta2})"))


def comparabilityTestSimple(ta1, ta2, exp, failures):
    box1 = boxesDict[ta1]
    box2 = boxesDict[ta2]
    res = areComparable(box1, box2)
    # if res != exp:
    if res != exp:
        failures.append("{:<50} | {:>15} | {:>15}".format(
            f"comparing... {ta1} > {ta2} ?", f"expected = {exp}", f"result = {res}"
        ))
        # failures[len(failures)-1] += "   err"


def comparabilityTests():
    print(" > SUBUNIT TEST: testing comparability/partial order ...")
    failures = []

    # boxes = {"boxX":0, "boxLPort":1, "boxHPort":1, "boxL0":2, "boxL1":2, "boxH0":2, "boxH1":2}

    # print("    {:<30} => {:>10} | {:>10}".format("comparing", "result", "expected"))
    # print("-" * 100)
    # for i, ival in boxes.items():
    #     box1 = boxesDict[i]
    #     for j, jval in boxes.items():
    #         box2 = boxesDict[j]
    #         result = areComparable(box1, box2)
    #         expected = ival >= jval
    #         print("    {:<30} => {:>10} | {:>10} | {:>5}".format(f"{box1.name} > {box2.name} ?", f"{result}", f"{expected}", f"ERR" if result != expected else ""))

    comparabilityTestSimple("boxL0", "boxX", True, failures)
    comparabilityTestSimple("boxL1", "boxX", True, failures)
    comparabilityTestSimple("boxH0", "boxX", True, failures)
    comparabilityTestSimple("boxH1", "boxX", True, failures)
    comparabilityTestSimple("boxLPort", "boxX", True, failures)
    comparabilityTestSimple("boxHPort", "boxX", True, failures)

    comparabilityTestSimple("boxL0", "boxLPort", True, failures)
    comparabilityTestSimple("boxL1", "boxLPort", True, failures)
    comparabilityTestSimple("boxH0", "boxHPort", True, failures)
    comparabilityTestSimple("boxH1", "boxHPort", True, failures)

    comparabilityTestSimple("boxLPort", "boxL0", False, failures)
    comparabilityTestSimple("boxLPort", "boxL1", False, failures)
    comparabilityTestSimple("boxHPort", "boxH0", False, failures)
    comparabilityTestSimple("boxHPort", "boxH1", False, failures)

    comparabilityTestSimple("boxX", "boxL0", False, failures)
    comparabilityTestSimple("boxX", "boxL1", False, failures)
    comparabilityTestSimple("boxX", "boxH0", False, failures)
    comparabilityTestSimple("boxX", "boxH1", False, failures)

    comparabilityTestSimple("boxL0", "boxL1", False, failures)
    comparabilityTestSimple("boxL0", "boxH0", False, failures)
    comparabilityTestSimple("boxL0", "boxH1", False, failures)
    comparabilityTestSimple("boxL1", "boxL0", False, failures)
    comparabilityTestSimple("boxL1", "boxH0", False, failures)
    comparabilityTestSimple("boxL1", "boxH1", False, failures)
    comparabilityTestSimple("boxH0", "boxL0", False, failures)
    comparabilityTestSimple("boxH0", "boxL1", False, failures)
    comparabilityTestSimple("boxH0", "boxH1", False, failures)
    comparabilityTestSimple("boxH1", "boxL0", False, failures)
    comparabilityTestSimple("boxH1", "boxL1", False, failures)
    comparabilityTestSimple("boxH1", "boxH0", False, failures)

    comparabilityTestSimple("boxH0", "boxLPort", False, failures)
    comparabilityTestSimple("boxH1", "boxLPort", False, failures)
    comparabilityTestSimple("boxL0", "boxHPort", False, failures)
    comparabilityTestSimple("boxL1", "boxHPort", False, failures)
    comparabilityTestSimple("boxLPort", "boxHPort", False, failures)
    comparabilityTestSimple("boxHPort", "boxLPort", False, failures)

    printFailedTests(failures)


def productTests():
    def productUnitTest(ta1, ta2, expect, failures):
        result = treeAutProduct(ta1, ta2)
        witnessT, witnessS = nonEmptyTD(result)
        actual = (witnessT is not None)  # actual = can witness be produced?
        if expect != actual:
            failures.append("{:<50} {:<20} {:<15} {:<15}".format(
                f"product({ta1.name},{ta2.name})",
                f"has witness?",
                f"exp = {expect}",
                f"got = {actual}"
            ))

    X = importTAfromVTF("tests/tddetX.vtf")
    LPort = importTAfromVTF("tests/tddetLPort.vtf")
    HPort = importTAfromVTF("tests/tddetHPort.vtf")
    L0 = importTAfromVTF("tests/tddetL0.vtf")
    L1 = importTAfromVTF("tests/tddetL1.vtf")
    H0 = importTAfromVTF("tests/tddetH0.vtf")
    H1 = importTAfromVTF("tests/tddetH1.vtf")

    failures = []

    productUnitTest(X, LPort, True, failures)
    productUnitTest(X, HPort, True, failures)
    productUnitTest(X, L0, True, failures)
    productUnitTest(X, L1, True, failures)
    productUnitTest(X, H0, True, failures)
    productUnitTest(X, H1, True, failures)
    productUnitTest(LPort, X, False, failures)
    productUnitTest(HPort, X, False, failures)
    productUnitTest(L0, X, False, failures)
    productUnitTest(L1, X, False, failures)
    productUnitTest(H0, X, False, failures)
    productUnitTest(H1, X, False, failures)

    productUnitTest(LPort, L0, True, failures)
    productUnitTest(LPort, L1, True, failures)
    productUnitTest(HPort, H0, True, failures)
    productUnitTest(HPort, H1, True, failures)

    productUnitTest(LPort, H0, False, failures)
    productUnitTest(LPort, H1, False, failures)
    productUnitTest(HPort, L0, False, failures)
    productUnitTest(HPort, L1, False, failures)
    productUnitTest(LPort, HPort, False, failures)

    productUnitTest(L0, L1, False, failures)
    productUnitTest(L1, L1, True, failures)
    productUnitTest(H0, L1, False, failures)
    productUnitTest(H1, L1, False, failures)
    productUnitTest(L1, L0, False, failures)
    productUnitTest(L1, H0, False, failures)
    productUnitTest(L1, H1, False, failures)
    printFailedTests(failures)


def extensionTests():
    def extensionUnitTest(ta1, ta2, expect, failures):
        actual = isExtension(ta1, ta2)
        if expect != actual:
            failures.append("{:<50} {:<20} {:<15} {:<15}".format(
                f"extension({ta1.name},{ta2.name})",
                f"has witness?",
                f"exp = {expect}",
                f"got = {actual}"
            ))

    X = importTAfromVTF("tests/tddetX.vtf")
    LPort = importTAfromVTF("tests/tddetLPort.vtf")
    HPort = importTAfromVTF("tests/tddetHPort.vtf")
    L0 = importTAfromVTF("tests/tddetL0.vtf")
    L1 = importTAfromVTF("tests/tddetL1.vtf")
    H0 = importTAfromVTF("tests/tddetH0.vtf")
    H1 = importTAfromVTF("tests/tddetH1.vtf")

    failures = []
    # extension je specializovanejsi // mal by byt
    extensionUnitTest(X, LPort, True, failures)
    extensionUnitTest(X, HPort, True, failures)
    extensionUnitTest(X, L0, True, failures)
    extensionUnitTest(X, L1, True, failures)
    extensionUnitTest(X, H0, True, failures)
    extensionUnitTest(X, H1, True, failures)
    extensionUnitTest(LPort, X, False, failures)
    extensionUnitTest(HPort, X, False, failures)
    extensionUnitTest(L0, X, False, failures)
    extensionUnitTest(L1, X, False, failures)
    extensionUnitTest(H0, X, False, failures)
    extensionUnitTest(H1, X, False, failures)

    extensionUnitTest(LPort, L0, True, failures)
    extensionUnitTest(LPort, L1, True, failures)
    extensionUnitTest(HPort, H0, True, failures)
    extensionUnitTest(HPort, H1, True, failures)

    extensionUnitTest(LPort, H0, False, failures)
    extensionUnitTest(LPort, H1, False, failures)
    extensionUnitTest(HPort, L0, False, failures)
    extensionUnitTest(HPort, L1, False, failures)
    extensionUnitTest(LPort, HPort, False, failures)

    extensionUnitTest(L0, L1, False, failures)
    extensionUnitTest(L1, L1, True, failures)
    extensionUnitTest(H0, L1, False, failures)
    extensionUnitTest(H1, L1, False, failures)
    extensionUnitTest(L1, L0, False, failures)
    extensionUnitTest(L1, H0, False, failures)
    extensionUnitTest(L1, H1, False, failures)
    printFailedTests(failures)


def extraTests():
    ta = importTAfromVTF("tests/normalizationTest1.vtf", 'f')
    # ta = importTAfromVTF("tests/unfoldingTest4.vtf", 'f')
    # exportTreeAutToDOT(ta, "vtf-to-dot/unfoldingTest4.dot")
    print(ta)


# End of file all_tests.py
