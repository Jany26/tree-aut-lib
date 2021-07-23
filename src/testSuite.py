# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from testData import *

def main():
    helperFuncTests()

    matchTestsTD()
    matchTestsBU()
    nonEmptinessTestsTD()
    nonEmptinessTestsBU()
    witnessGenTestsTD()
    witnessGenTestsBU()

    unionTests()
    intersectionTests()
    complementTests()

    reachabilityTDTests()
    reachabilityBUTests()
    removeUselessStatesTests()
    
    suffixTests()
    prefixTests()

    print(">> UNIT TESTS DONE!")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def printFailedTests(failedTestsArray):
    try:
        assert failedTestsArray == []
    except:
        print("Tests failed (" + str(len(failedTestsArray)) + "):")
        for i in failedTestsArray:
            print("    " + i)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def helperFuncTests():
    print(">> UNIT TEST: testing helper functions...")
    
    getOuptutStatesTests()
    getArityDictTests()
    removeStateTests()
    generateTuplesTest()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def getOuptutStatesTests():
    print(">>>> SUBUNIT TEST: testing getOutputStates()...")
    failures = []

    if not boxX.getOutputStates() == ['q1']:
        failures.append("boxX.getOutputStates()")
    if not boxH1.getOutputStates() == ['u1', 'u2']:
        failures.append("boxH1.getOutputStates()")
    
    printFailedTests(failures)

def getArityDictTests():
    print(">>>> SUBUNIT TEST: testing getArityDict()...")
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
    print(">>>> SUBUNIT TEST: testing removeState()...")
    failures = []

    testL0 = copy.deepcopy(boxL0)
    testL0.removeState('r2')
    
    if matchTreeTD(testL0, treeL0test1):
        failures.append("matchTreeTD(testL0, treeL0test1)")
    if matchTreeTD(testL0, treeL0test2):
        failures.append("matchTreeTD(testL0, treeL0test2)")
    if matchTreeTD(testL0, treeL0test3):
        failures.append("matchTreeTD(testL0, treeL0test3)")
    if matchTreeTD(testL0, treeL0test4):
        failures.append("matchTreeTD(testL0, treeL0test4)")

    testL1 = copy.deepcopy(boxL1)
    testL1.removeState('s0')

    if matchTreeTD(testL1, treeL1test1):
        failures.append("matchTreeTD(testL1, treeL1test1)")
    if matchTreeTD(testL1, treeL1test2):
        failures.append("matchTreeTD(testL1, treeL1test2)")
    if matchTreeTD(testL1, treeL1test3):
        failures.append("matchTreeTD(testL1, treeL1test3)")
    if matchTreeTD(testL1, treeL1test4):
        failures.append("matchTreeTD(testL1, treeL1test4)")

    printFailedTests(failures)

def generateTuplesTest():
    print(">>>> SUBUNIT TEST: testing generator of possibleChildrenTuples...")
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
    print(">> UNIT TEST: testing top-down match() ...")
    failures = []
    if not matchTreeTD(boxX, treeXtest1):
        failures.append("matchTreeTD(boxX, treeXtest1)")
    if matchTreeTD(boxX, treeXtest2):
        failures.append("matchTreeTD(boxX, treeXtest2)")
    if not matchTreeTD(boxX, treeXtest3):
        failures.append("matchTreeTD(boxX, treeXtest3)")
    
    if not matchTreeTD(boxL0, treeL0test1):
        failures.append("matchTreeTD(boxL0, treeL0test1)")
    if not matchTreeTD(boxL0, treeL0test2):
        failures.append("matchTreeTD(boxL0, treeL0test2)")
    if not matchTreeTD(boxL0, treeL0test3):
        failures.append("matchTreeTD(boxL0, treeL0test3)")
    if not matchTreeTD(boxL0, treeL0test4):
        failures.append("matchTreeTD(boxL0, treeL0test4)")
    if matchTreeTD(boxL0, treeL1test1):
        failures.append("matchTreeTD(boxL0, treeL1test1)")
    if matchTreeTD(boxL0, treeL1test2):
        failures.append("matchTreeTD(boxL0, treeL1test2)")
    if matchTreeTD(boxL0, treeL1test3):
        failures.append("matchTreeTD(boxL0, treeL1test3)")
    if matchTreeTD(boxL0, treeL1test4):
        failures.append("matchTreeTD(boxL0, treeL1test4)")
    if matchTreeTD(boxL0, treeH0test1):
        failures.append("matchTreeTD(boxL0, treeH0test1)")
    if matchTreeTD(boxL0, treeH0test2):
        failures.append("matchTreeTD(boxL0, treeH0test2)")
    if matchTreeTD(boxL0, treeH0test3):
        failures.append("matchTreeTD(boxL0, treeH0test3)")
    if matchTreeTD(boxL0, treeH0test4):
        failures.append("matchTreeTD(boxL0, treeH0test4)")

    if not matchTreeTD(boxL1, treeL1test1):
        failures.append("matchTreeTD(boxL1, treeL0test1)")
    if not matchTreeTD(boxL1, treeL1test2):
        failures.append("matchTreeTD(boxL1, treeL0test2)")
    if not matchTreeTD(boxL1, treeL1test3):
        failures.append("matchTreeTD(boxL1, treeL0test3)")
    if not matchTreeTD(boxL1, treeL1test4):
        failures.append("matchTreeTD(boxL1, treeL0test4)")

    if not matchTreeTD(boxH0, treeH0test1):
        failures.append("matchTreeTD(boxH0, treeH0test1)")
    if not matchTreeTD(boxH0, treeH0test2):
        failures.append("matchTreeTD(boxH0, treeH0test2)")
    if not matchTreeTD(boxH0, treeH0test3):
        failures.append("matchTreeTD(boxH0, treeH0test3)")
    if not matchTreeTD(boxH0, treeH0test4):
        failures.append("matchTreeTD(boxH0, treeH0test4)")
    
    if not matchTreeTD(boxH1, treeH1test1):
        failures.append("matchTreeTD(boxH1, treeH1test1)")
    if not matchTreeTD(boxH1, treeH1test2):
        failures.append("matchTreeTD(boxH1, treeH1test2)")
    if not matchTreeTD(boxH1, treeH1test3):
        failures.append("matchTreeTD(boxH1, treeH1test3)")
    if not matchTreeTD(boxH1, treeH1test4):
        failures.append("matchTreeTD(boxH1, treeH1test4)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def matchTestsBU():
    print(">> UNIT TEST: testing bottom-up match() ...")
    failures = []

    if not matchTreeBU(boxX, treeXtest1):
        failures.append("matchTreeBU(boxX, treeXtest1)")
    if matchTreeBU(boxX, treeXtest2):
        failures.append("matchTreeBU(boxX, treeXtest2)")
    if not matchTreeBU(boxX, treeXtest3):
        failures.append("matchTreeBU(boxX, treeXtest3)")
    
    if not matchTreeBU(boxL0, treeL0test1):
        failures.append("matchTreeBU(boxL0, treeL0test1)")
    if not matchTreeBU(boxL0, treeL0test2):
        failures.append("matchTreeBU(boxL0, treeL0test2)")
    if not matchTreeBU(boxL0, treeL0test3):
        failures.append("matchTreeBU(boxL0, treeL0test3)")
    if not matchTreeBU(boxL0, treeL0test4):
        failures.append("matchTreeBU(boxL0, treeL0test4)")
    if matchTreeBU(boxL0, treeL1test1):
        failures.append("matchTreeBU(boxL0, treeL1test1)")
    if matchTreeBU(boxL0, treeL1test2):
        failures.append("matchTreeBU(boxL0, treeL1test2)")
    if matchTreeBU(boxL0, treeL1test3):
        failures.append("matchTreeBU(boxL0, treeL1test3)")
    if matchTreeBU(boxL0, treeL1test4):
        failures.append("matchTreeBU(boxL0, treeL1test4)")
    if matchTreeBU(boxL0, treeH0test1):
        failures.append("matchTreeBU(boxL0, treeH0test1)")
    if matchTreeBU(boxL0, treeH0test2):
        failures.append("matchTreeBU(boxL0, treeH0test2)")
    if matchTreeBU(boxL0, treeH0test3):
        failures.append("matchTreeBU(boxL0, treeH0test3)")
    if matchTreeBU(boxL0, treeH0test4):
        failures.append("matchTreeBU(boxL0, treeH0test4)")

    if not matchTreeBU(boxL1, treeL1test1):
        failures.append("matchTreeBU(boxL1, treeL0test1)")
    if not matchTreeBU(boxL1, treeL1test2):
        failures.append("matchTreeBU(boxL1, treeL0test2)")
    if not matchTreeBU(boxL1, treeL1test3):
        failures.append("matchTreeBU(boxL1, treeL0test3)")
    if not matchTreeBU(boxL1, treeL1test4):
        failures.append("matchTreeBU(boxL1, treeL0test4)")

    if not matchTreeBU(boxH0, treeH0test1):
        failures.append("matchTreeBU(boxH0, treeH0test1)")
    if not matchTreeBU(boxH0, treeH0test2):
        failures.append("matchTreeBU(boxH0, treeH0test2)")
    if not matchTreeBU(boxH0, treeH0test3):
        failures.append("matchTreeBU(boxH0, treeH0test3)")
    if not matchTreeBU(boxH0, treeH0test4):
        failures.append("matchTreeBU(boxH0, treeH0test4)")
    
    if not matchTreeBU(boxH1, treeH1test1):
        failures.append("matchTreeBU(boxH1, treeH1test1)")
    if not matchTreeBU(boxH1, treeH1test2):
        failures.append("matchTreeBU(boxH1, treeH1test2)")
    if not matchTreeBU(boxH1, treeH1test3):
        failures.append("matchTreeBU(boxH1, treeH1test3)")
    if not matchTreeBU(boxH1, treeH1test4):
        failures.append("matchTreeBU(boxH1, treeH1test4)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
def unionTests():
    print(">> UNIT TEST: testing union() ...")
    failures = []
    if not matchTreeTD(unionL0H0, treeL0test1):
        failures.append("matchTreeTD(unionL0H0, treeL0test1)")
    if not matchTreeTD(unionL0H0, treeL0test2):
        failures.append("matchTreeTD(unionL0H0, treeL0test2)")
    if not matchTreeTD(unionL0H0, treeL0test3):
        failures.append("matchTreeTD(unionL0H0, treeL0test3)")
    if not matchTreeTD(unionL0H0, treeL0test4):
        failures.append("matchTreeTD(unionL0H0, treeL0test4)")
    if not matchTreeTD(unionL0H0, treeH0test1):
        failures.append("matchTreeTD(unionL0H0, treeH0test1)")
    if not matchTreeTD(unionL0H0, treeH0test2):
        failures.append("matchTreeTD(unionL0H0, treeH0test2)")
    if not matchTreeTD(unionL0H0, treeH0test3):
        failures.append("matchTreeTD(unionL0H0, treeH0test3)")
    if not matchTreeTD(unionL0H0, treeH0test4):
        failures.append("matchTreeTD(unionL0H0, treeH0test4)")

    if not matchTreeTD(unionL0H1, treeL0test1):
        failures.append("matchTreeTD(unionL0H0, treeL0test1)")
    if not matchTreeTD(unionL0H0, treeL0test2):
        failures.append("matchTreeTD(unionL0H0, treeL0test2)")
    if not matchTreeTD(unionL0H0, treeL0test3):
        failures.append("matchTreeTD(unionL0H0, treeL0test3)")
    if not matchTreeTD(unionL0H0, treeL0test4):
        failures.append("matchTreeTD(unionL0H0, treeL0test4)")
    if not matchTreeTD(unionL0H0, treeH0test1):
        failures.append("matchTreeTD(unionL0H0, treeH0test1)")
    if not matchTreeTD(unionL0H0, treeH0test2):
        failures.append("matchTreeTD(unionL0H0, treeH0test2)")
    if not matchTreeTD(unionL0H0, treeH0test3):
        failures.append("matchTreeTD(unionL0H0, treeH0test3)")
    if not matchTreeTD(unionL0H0, treeH0test4):
        failures.append("matchTreeTD(unionL0H0, treeH0test4)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def intersectionTests():
    print(">> UNIT TEST: testing intersection() ...")
    failures = []

    treeAutIntersection(boxL0, boxH0)
    treeAutIntersection(L0prefixForH1, H1suffix)

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def complementTests():
    print(">> UNIT TEST: testing complement() ...")
    failures = []

    if matchTreeTD(boxX, treeXtest1):
        failures.append("matchTreeTD(boxX, treeXtest1)")
    if not matchTreeTD(boxX, treeXtest2):
        failures.append("matchTreeTD(boxX, treeXtest2)")
    if matchTreeTD(boxX, treeXtest3):
        failures.append("matchTreeTD(boxX, treeXtest3)")
    
    if matchTreeTD(boxL0, treeL0test1):
        failures.append("matchTreeTD(boxL0, treeL0test1)")
    if matchTreeTD(boxL0, treeL0test2):
        failures.append("matchTreeTD(boxL0, treeL0test2)")
    if matchTreeTD(boxL0, treeL0test3):
        failures.append("matchTreeTD(boxL0, treeL0test3)")
    if matchTreeTD(boxL0, treeL0test4):
        failures.append("matchTreeTD(boxL0, treeL0test4)")
    if not matchTreeTD(boxL0, treeL1test1):
        failures.append("matchTreeTD(boxL0, treeL1test1)")
    if not matchTreeTD(boxL0, treeL1test2):
        failures.append("matchTreeTD(boxL0, treeL1test2)")
    if not matchTreeTD(boxL0, treeL1test3):
        failures.append("matchTreeTD(boxL0, treeL1test3)")
    if not matchTreeTD(boxL0, treeL1test4):
        failures.append("matchTreeTD(boxL0, treeL1test4)")
    if not matchTreeTD(boxL0, treeH0test1):
        failures.append("matchTreeTD(boxL0, treeH0test1)")
    if not matchTreeTD(boxL0, treeH0test2):
        failures.append("matchTreeTD(boxL0, treeH0test2)")
    if not matchTreeTD(boxL0, treeH0test3):
        failures.append("matchTreeTD(boxL0, treeH0test3)")
    if not matchTreeTD(boxL0, treeH0test4):
        failures.append("matchTreeTD(boxL0, treeH0test4)")

    if matchTreeTD(boxL1, treeL1test1):
        failures.append("matchTreeTD(boxL1, treeL0test1)")
    if matchTreeTD(boxL1, treeL1test2):
        failures.append("matchTreeTD(boxL1, treeL0test2)")
    if matchTreeTD(boxL1, treeL1test3):
        failures.append("matchTreeTD(boxL1, treeL0test3)")
    if matchTreeTD(boxL1, treeL1test4):
        failures.append("matchTreeTD(boxL1, treeL0test4)")

    if matchTreeTD(boxH0, treeH0test1):
        failures.append("matchTreeTD(boxH0, treeH0test1)")
    if matchTreeTD(boxH0, treeH0test2):
        failures.append("matchTreeTD(boxH0, treeH0test2)")
    if matchTreeTD(boxH0, treeH0test3):
        failures.append("matchTreeTD(boxH0, treeH0test3)")
    if matchTreeTD(boxH0, treeH0test4):
        failures.append("matchTreeTD(boxH0, treeH0test4)")
    
    if matchTreeTD(boxH1, treeH1test1):
        failures.append("matchTreeTD(boxH1, treeH1test1)")
    if matchTreeTD(boxH1, treeH1test2):
        failures.append("matchTreeTD(boxH1, treeH1test2)")
    if matchTreeTD(boxH1, treeH1test3):
        failures.append("matchTreeTD(boxH1, treeH1test3)")
    if matchTreeTD(boxH1, treeH1test4):
        failures.append("matchTreeTD(boxH1, treeH1test4)")

    # printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def nonEmptinessTestsTD():
    print(">> UNIT TEST: testing top-down nonEmptiness() ...")
    failures = []
    if not nonEmptyTopDown(boxX):
        failures.append("nonEmptyTopDown(boxX)")
    if not nonEmptyTopDown(boxL0):
        failures.append("nonEmptyTopDown(boxL0)")
    if not nonEmptyTopDown(boxL1):
        failures.append("nonEmptyTopDown(boxL1)")
    if not nonEmptyTopDown(boxH0):
        failures.append("nonEmptyTopDown(boxH0)")
    if not nonEmptyTopDown(boxH1):
        failures.append("nonEmptyTopDown(boxH1)")
    if not nonEmptyTopDown(boxLPort):
        failures.append("nonEmptyTopDown(boxLPort)")
    
    if nonEmptyTopDown(treeAutIntersection(boxL0, boxX)):
        failures.append("nonEmptyTopDown(treeAutIntersection(boxL0, boxX))")
    if nonEmptyTopDown(treeAutIntersection(boxL0, boxL1)):
        failures.append("nonEmptyTopDown(treeAutIntersection(boxL0, boxL1))")
    if nonEmptyTopDown(treeAutIntersection(boxL0, boxH0)):
        failures.append("nonEmptyTopDown(treeAutIntersection(boxL0, boxH0))")
    if nonEmptyTopDown(treeAutIntersection(boxL0, boxH1)):
        failures.append("nonEmptyTopDown(treeAutIntersection(boxL0, boxH1))")

    if not nonEmptyTopDown(treeAutIntersection(L0prefixForX, Xsuffix)):
        failures.append("nonEmptyTopDown(treeAutIntersection(L0prefixForX, Xsuffix))")
    if not nonEmptyTopDown(treeAutIntersection(L0prefixForL1, L1suffix)):
        failures.append("nonEmptyTopDown(treeAutIntersection(L0prefixForL1, L1suffix))")
    if not nonEmptyTopDown(treeAutIntersection(L0prefixForH0, H0suffix)):
        failures.append("nonEmptyTopDown(treeAutIntersection(L0prefixForH0, H0suffix))")
    if nonEmptyTopDown(treeAutIntersection(L0prefixForH0, H1suffix)):
        failures.append("nonEmptyTopDown(treeAutIntersection(L0prefixForH0, H1suffix))")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def nonEmptinessTestsBU():
    print(">> UNIT TEST: testing bottom-up nonEmptiness() ...")
    failures = []

    if not nonEmptyBottomUp(boxX):
        failures.append("nonEmptyBottomUp(boxX)")
    if not nonEmptyBottomUp(boxL0):
        failures.append("nonEmptyBottomUp(boxL0)")
    if not nonEmptyBottomUp(boxL1):
        failures.append("nonEmptyBottomUp(boxL1)")
    if not nonEmptyBottomUp(boxH0):
        failures.append("nonEmptyBottomUp(boxH0)")
    if not nonEmptyBottomUp(boxH1):
        failures.append("nonEmptyBottomUp(boxH1)")
    if not nonEmptyBottomUp(boxLPort):
        failures.append("nonEmptyBottomUp(boxLPort)")
    
    if nonEmptyBottomUp(treeAutIntersection(boxL0, boxX)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(boxL0, boxX))")
    if nonEmptyBottomUp(treeAutIntersection(boxL0, boxL1)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(boxL0, boxL1))")
    if nonEmptyBottomUp(treeAutIntersection(boxL0, boxH0)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(boxL0, boxH0))")
    if nonEmptyBottomUp(treeAutIntersection(boxL0, boxH1)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(boxL0, boxH1))")

    if not nonEmptyBottomUp(treeAutIntersection(L0prefixForX, Xsuffix)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(L0prefixForX, Xsuffix))")
    if not nonEmptyBottomUp(treeAutIntersection(L0prefixForL1, L1suffix)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(L0prefixForL1, L1suffix))")
    if not nonEmptyBottomUp(treeAutIntersection(L0prefixForH0, H0suffix)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(L0prefixForH0, H0suffix))")
    if nonEmptyBottomUp(treeAutIntersection(L0prefixForH0, H1suffix)):
        failures.append("nonEmptyBottomUp(treeAutIntersection(L0prefixForH0, H1suffix))")


    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def witnessGenTestsTD():
    print(">> UNIT TEST: testing top-down witnessGeneration()...")
    failures = []

    printFailedTests(failures)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def witnessGenTestsBU():
    print(">> UNIT TEST: testing bottom-up witnessGeneration()...")
    failures = []
    # TODO: more tests

    temp1tree, temp1str = createWitnessBU(L0suffix)
    temp2tree, temp2str = createWitnessBU(boxL0)
    temp3tree, temp3str = createWitnessBU(intersectionL0H1)
    
    if temp1tree is None or temp1str == "":
        failures.append("createWitnessBU(L0suffix)")
    if temp2tree is None or temp2str == "":
        failures.append("createWitnessBU(boxL0)")
    if temp3tree is not None or temp3str != "":
        failures.append("createWitnessBU(intersectionL0H1)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def reachabilityTDTests():
    print(">> UNIT TEST: testing top-down reachability()...")
    failures = []
    
    if set(topDownReachable(testBox1)) != set(['q0','q1']):
        failures.append("topDownReachable(testBox1)")
    if set(topDownReachable(testBox2a)) != set(['q0','q1','q2','q3']):
        failures.append("topDownReachable(testBox2a")
    if set(topDownReachable(testBox2b)) != set(['q0','q1','q2','q3']):
        failures.append("topDownReachable(testBox2b)")
    if set(topDownReachable(testBox3)) != set(['r0','r1','r2']):
        failures.append("topDownReachable(testBox3)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def reachabilityBUTests():
    print(">> UNIT TEST: testing bottom-up reachability()...")
    failures = []
    
    if set(bottomUpReachable(testBox1)) != set(['q1']):
        failures.append("bottomUpReachable(testBox1)")
    if set(bottomUpReachable(testBox2a)) != set(['q0','q1','q2','q3']):
        failures.append("bottomUpReachable(testBox2a")
    if set(bottomUpReachable(testBox2b)) != set(['q0','q1','q2','q3']):
        failures.append("bottomUpReachable(testBox2b)")
    if set(topDownReachable(testBox3)) != set(['r0','r1','r2']):
        failures.append("bottomUpReachable(testBox3)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def removeUselessStatesTests():
    print(">> UNIT TEST: testing removeUselessStates()...")
    failures = []

    removeUselessStates(testBox1)
    removeUselessStates(testBox2a)
    removeUselessStates(testBox2b)
    removeUselessStates(testBox3)

    if set(testBox1.getStates()) != set([]):
        failures.append("removeUselessStates(testBox1)")
    if set(testBox2a.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testBox2a)")
    if set(testBox2b.getStates()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("removeUselessStates(testBox2b)")
    if testBox3.transitions != boxL0.transitions:
        failures.append("removeUselessStates(testBox3)")
    
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def suffixTests():
    print(">> UNIT TEST: testing suffix() ...")
    failures = []
    try: boxX.createSuffix()    
    except: failures.append("boxX.createSuffix()")
    
    try: boxL0.createSuffix()    
    except: failures.append("boxL0.createSuffix()")

    try: boxL0.createSuffix()    
    except: failures.append("boxL0.createSuffix()")

    try: boxL0.createSuffix()    
    except: failures.append("boxL0.createSuffix()")

    try: boxL0.createSuffix()    
    except: failures.append("boxL0.createSuffix()")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prefixTests():
    print(">> UNIT TEST: testing prefix() ...")
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

if __name__ == '__main__':
    main()

# End of file testSuite.py
