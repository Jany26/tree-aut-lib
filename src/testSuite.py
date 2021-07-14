# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

# import sys
import copy
# sys.path.append('../')

from treeAut import *
from boxes import *
from treeExamples import *

def main():
    # print("TEST 1) testing match() ... \n")
    # matchTests()
    # print("TEST 2) testing suffix() ... \n")
    # suffixTests()
    # print("TEST 3) testing prefix() ... \n")
    # prefixTests()
    # print("TEST 4) testing union() ... \n")
    # unionTests()
    # print("TEST 5) testing intersection() ... \n")
    intersectionTests()
    # print("TEST 6) testing complement() ... \n")
    # complementTests()

def matchTests():
    failedTests = ""

    if not matchTree(boxX, treeXtest1):
        failedTests += "X-1, "
    if matchTree(boxX, treeXtest2):
        failedTests += "X-2, "
    if not matchTree(boxX, treeXtest3):
        failedTests += "X-3, "

    if not matchTree(boxH0, treeH0test1):
        failedTests += "H0-1, "
    if not matchTree(boxH0, treeH0test2):
        failedTests += "H0-2, "
    if not matchTree(boxH0, treeH0test3):
        failedTests += "H0-3, "
    if not matchTree(boxH0, treeH0test4):
        failedTests += "H0-4, "
    
    if not matchTree(boxH1, treeH1test1):
        failedTests += "H1-1, "
    if not matchTree(boxH1, treeH1test2):
        failedTests += "H1-2, "
    if not matchTree(boxH1, treeH1test3):
        failedTests += "H1-3, "
    if not matchTree(boxH1, treeH1test4):
        failedTests += "H1-4, "
    
    if not matchTree(boxL0, treeL0test1):
        failedTests += "L0-1, "
    if not matchTree(boxL0, treeL0test2):
        failedTests += "L0-2, "
    if not matchTree(boxL0, treeL0test3):
        failedTests += "L0-3, "
    if not matchTree(boxL0, treeL0test4):
        failedTests += "L0-4, "

    if not matchTree(boxL1, treeL1test1):
        failedTests += "L1-1, "
    if not matchTree(boxL1, treeL1test2):
        failedTests += "L1-2, "
    if not matchTree(boxL1, treeL1test3):
        failedTests += "L1-3, "
    if not matchTree(boxL1, treeL1test4):
        failedTests += "L1-4, "

    if failedTests == "":
        failedTests = "None"
    
    print("Failed tests: " + failedTests)
    
def suffixTests():
    suffixH0 = boxH0.createSuffix()
    suffixH0.printTreeAut()

def prefixTests():
    outputEdgesL0 = boxL0.getOutputEdges()
    outputEdgesL1 = boxL1.getOutputEdges()
    outputEdgesH0 = boxH0.getOutputEdges()
    outputEdgesH1 = boxH1.getOutputEdges()
    outputEdgesLPort = boxLPort.getOutputEdges()
    outputEdgesX = boxX.getOutputEdges()

    prefixL0withX = boxL0.createPrefix(outputEdgesX)
    prefixL0withL1 = boxL0.createPrefix(outputEdgesL1)
    prefixL0withH0 = boxL0.createPrefix(outputEdgesH0)
    prefixL0withH1 = boxL0.createPrefix(outputEdgesH1)

    prefixL0withX.printTreeAut()
    prefixL0withL1.printTreeAut()
    prefixL0withH0.printTreeAut()
    prefixL0withH1.printTreeAut()
    
def unionTests():
    errorString = ""
    test = treeAutUnion(boxL0, boxH0)
    tempResultArray = []
    tempResultArray.append(matchTree(test, treeL0test1))
    tempResultArray.append(matchTree(test, treeL0test2))
    tempResultArray.append(matchTree(test, treeL0test3))
    tempResultArray.append(matchTree(test, treeL0test4))
    tempResultArray.append(matchTree(test, treeH0test1))
    tempResultArray.append(matchTree(test, treeH0test2))
    tempResultArray.append(matchTree(test, treeH0test3))
    tempResultArray.append(matchTree(test, treeH0test4))
    for i in range(len(tempResultArray)):
        if tempResultArray[i] == False:
            errorString += "L0 U H0 test" + str(i) + ", "
    if errorString == "":
        errorString += "All passed"
    print(errorString)    

    # L0unionL1 = treeAutUnion(boxL0, boxL1)

def intersectionTests():
    test = treeAutIntersection(boxL0, boxH0)
    test.printTreeAut()
    # treeAutIntersection(boxL0, boxL1)
    # treeAutIntersection(boxX, boxL0)

def complementTests():
    complementL0 = treeAutComplement(boxL0)
    complementL1 = treeAutComplement(boxL1)
    complementH0 = treeAutComplement(boxH0)
    complementH1 = treeAutComplement(boxH1)
    complementX = treeAutComplement(boxX)

if __name__ == '__main__':
    main()

# End of file
