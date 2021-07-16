# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

from testData import *

def main():
    matchTests()
    suffixTests()
    prefixTests()
    unionTests()
    intersectionTests()
    complementTests()
    nonEmptinessTests()
    print(">>> UNIT TESTS DONE!")

def printFailedTests(failedTestsArray):
    try:
        assert failedTestsArray == []
    except:
        print("Tests failed (" + str(len(failedTestsArray)) + "):")
        for i in failedTestsArray:
            print("\t" + i)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    if not nonEmptyTD(boxX):
        failures.append("nonEmptyTD(boxX)")
    if not nonEmptyTD(boxL0):
        failures.append("nonEmptyTD(boxL0)")
    if not nonEmptyTD(boxL1):
        failures.append("nonEmptyTD(boxL1)")
    if not nonEmptyTD(boxH0):
        failures.append("nonEmptyTD(boxH0)")
    if not nonEmptyTD(boxH1):
        failures.append("nonEmptyTD(boxH1)")
    if not nonEmptyTD(boxLPort):
        failures.append("nonEmptyTD(boxLPort)")
    
    if nonEmptyTD(treeAutIntersection(boxL0, boxX)):
        failures.append("nonEmptyTD(treeAutIntersection(boxL0, boxX))")
    if nonEmptyTD(treeAutIntersection(boxL0, boxL1)):
        failures.append("nonEmptyTD(treeAutIntersection(boxL0, boxL1))")
    if nonEmptyTD(treeAutIntersection(boxL0, boxH0)):
        failures.append("nonEmptyTD(treeAutIntersection(boxL0, boxH0))")
    if nonEmptyTD(treeAutIntersection(boxL0, boxH1)):
        failures.append("nonEmptyTD(treeAutIntersection(boxL0, boxH1))")

    if not nonEmptyTD(treeAutIntersection(L0prefixForX, Xsuffix)):
        failures.append("nonEmptyTD(treeAutIntersection(L0prefixForX, Xsuffix))")
    if not nonEmptyTD(treeAutIntersection(L0prefixForL1, L1suffix)):
        failures.append("nonEmptyTD(treeAutIntersection(L0prefixForL1, L1suffix))")
    if not nonEmptyTD(treeAutIntersection(L0prefixForH0, H0suffix)):
        failures.append("nonEmptyTD(treeAutIntersection(L0prefixForH0, H0suffix))")
    if not nonEmptyTD(treeAutIntersection(L0prefixForH0, H1suffix)):
        failures.append("nonEmptyTD(treeAutIntersection(L0prefixForH0, H1suffix))")

    printFailedTests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    main()

# End of file testSuite.py
