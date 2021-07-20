# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from testData import *

# helperFuncTests()
# TODO: test removeState func

# removeUselessStates()
# TODO: test top down reachable func
# TODO: test bottom up reachable func


def main():
    helperFuncTests() #0
    # matchTests() #1
    # suffixTests() #2
    # prefixTests() #3
    # unionTests() #4
    # intersectionTests() #5
    # complementTests() #6
    # nonEmptinessTests() #7
    # print(">>> UNIT TESTS DONE!")

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
    print(">>> UNIT TEST 0) testing helper functions...")
    failures = []

    if not boxX.getOutputStates() == ['q1']:
        failures.append("boxX.getOutputStates()")
    if not boxH1.getOutputStates() == ['u1', 'u2']:
        failures.append("boxH1.getOutputStates()")

    print(boxX.getSymbolArityDict())
    print(boxL0.getSymbolArityDict())
    print(boxL1.getSymbolArityDict())
    print(boxH0.getSymbolArityDict())
    print(boxH1.getSymbolArityDict())
    print(boxLPort.getSymbolArityDict())

    testL0 = copy.deepcopy(boxL0)
    testL1 = copy.deepcopy(boxL1)

    testL0.printTreeAut()
    testL0.removeState('r1')
    testL0.printTreeAut()
    

    testL1.printTreeAut()
    testL1.removeState('r0')
    testL1.printTreeAut()

    printFailedTests(failures)

def matchTests():
    print(">>> UNIT TEST 1) testing match() ...")
    failures = []
    if not matchTree(boxX, treeXtest1):
        failures.append("matchTree(boxX, treeXtest1)")
    if matchTree(boxX, treeXtest2):
        failures.append("matchTree(boxX, treeXtest2)")
    if not matchTree(boxX, treeXtest3):
        failures.append("matchTree(boxX, treeXtest3)")
    
    if not matchTree(boxL0, treeL0test1):
        failures.append("matchTree(boxL0, treeL0test1)")
    if not matchTree(boxL0, treeL0test2):
        failures.append("matchTree(boxL0, treeL0test2)")
    if not matchTree(boxL0, treeL0test3):
        failures.append("matchTree(boxL0, treeL0test3)")
    if not matchTree(boxL0, treeL0test4):
        failures.append("matchTree(boxL0, treeL0test4)")

    if not matchTree(boxL1, treeL1test1):
        failures.append("matchTree(boxL1, treeL0test1)")
    if not matchTree(boxL1, treeL1test2):
        failures.append("matchTree(boxL1, treeL0test2)")
    if not matchTree(boxL1, treeL1test3):
        failures.append("matchTree(boxL1, treeL0test3)")
    if not matchTree(boxL1, treeL1test4):
        failures.append("matchTree(boxL1, treeL0test4)")

    if not matchTree(boxH0, treeH0test1):
        failures.append("matchTree(boxH0, treeH0test1)")
    if not matchTree(boxH0, treeH0test2):
        failures.append("matchTree(boxH0, treeH0test2)")
    if not matchTree(boxH0, treeH0test3):
        failures.append("matchTree(boxH0, treeH0test3)")
    if not matchTree(boxH0, treeH0test4):
        failures.append("matchTree(boxH0, treeH0test4)")
    
    if not matchTree(boxH1, treeH1test1):
        failures.append("matchTree(boxH1, treeH1test1)")
    if not matchTree(boxH1, treeH1test2):
        failures.append("matchTree(boxH1, treeH1test2)")
    if not matchTree(boxH1, treeH1test3):
        failures.append("matchTree(boxH1, treeH1test3)")
    if not matchTree(boxH1, treeH1test4):
        failures.append("matchTree(boxH1, treeH1test4)")
    
    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
def suffixTests():
    print(">>> UNIT TEST 2) testing suffix() ...")
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
    print(">>> UNIT TEST 3) testing prefix() ...")
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
    
def unionTests():
    print(">>> UNIT TEST 4) testing union() ...")
    failures = []
    if not matchTree(unionL0H0, treeL0test1):
        failures.append("matchTree(unionL0H0, treeL0test1)")
    if not matchTree(unionL0H0, treeL0test2):
        failures.append("matchTree(unionL0H0, treeL0test2)")
    if not matchTree(unionL0H0, treeL0test3):
        failures.append("matchTree(unionL0H0, treeL0test3)")
    if not matchTree(unionL0H0, treeL0test4):
        failures.append("matchTree(unionL0H0, treeL0test4)")
    if not matchTree(unionL0H0, treeH0test1):
        failures.append("matchTree(unionL0H0, treeH0test1)")
    if not matchTree(unionL0H0, treeH0test2):
        failures.append("matchTree(unionL0H0, treeH0test2)")
    if not matchTree(unionL0H0, treeH0test3):
        failures.append("matchTree(unionL0H0, treeH0test3)")
    if not matchTree(unionL0H0, treeH0test4):
        failures.append("matchTree(unionL0H0, treeH0test4)")

    if not matchTree(unionL0H1, treeL0test1):
        failures.append("matchTree(unionL0H0, treeL0test1)")
    if not matchTree(unionL0H0, treeL0test2):
        failures.append("matchTree(unionL0H0, treeL0test2)")
    if not matchTree(unionL0H0, treeL0test3):
        failures.append("matchTree(unionL0H0, treeL0test3)")
    if not matchTree(unionL0H0, treeL0test4):
        failures.append("matchTree(unionL0H0, treeL0test4)")
    if not matchTree(unionL0H0, treeH0test1):
        failures.append("matchTree(unionL0H0, treeH0test1)")
    if not matchTree(unionL0H0, treeH0test2):
        failures.append("matchTree(unionL0H0, treeH0test2)")
    if not matchTree(unionL0H0, treeH0test3):
        failures.append("matchTree(unionL0H0, treeH0test3)")
    if not matchTree(unionL0H0, treeH0test4):
        failures.append("matchTree(unionL0H0, treeH0test4)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def intersectionTests():
    print(">>> UNIT TEST 5) testing intersection() ...")
    failures = []

    treeAutIntersection(boxL0, boxH0)
    treeAutIntersection(L0prefixForH1, H1suffix)

    printFailedTests(failures)

def complementTests():
    print(">>> UNIT TEST 6) testing complement() ...")
    failures = []
    try: treeAutComplement(boxX)
    except: failures.append("treeAutComplement(boxX)")

    try: treeAutComplement(boxL0)
    except: failures.append("treeAutComplement(boxL0)")

    try: treeAutComplement(boxL1)
    except: failures.append("treeAutComplement(boxL1)")

    try: treeAutComplement(boxH0)
    except: failures.append("treeAutComplement(boxH0)")
    
    try: treeAutComplement(boxH1)
    except: failures.append("treeAutComplement(boxH1)")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def nonEmptinessTests():
    print(">>> UNIT TEST 7) testing nonEmptiness() ...")
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

if __name__ == '__main__':
    main()

# End of file testSuite.py
