# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

import sys
import copy
# sys.path.append('../')

from treeAut import *
from boxes import *
from treeExamples import *

def main():
    print("\n1)\ttesting match() ... \n")
    matchTests()
    print("\n2)\ttesting suffix() ... \n")
    suffixTests()
    print("\n3)\ttesting prefix() ... \n")
    prefixTests()
    # print("\n4)\ttesting complement() ... \n")
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
    suffixH0 = copy.deepcopy(boxH0)
    suffixH0.makeSuffix()
    suffixH0.printTreeAut()

def prefixTests():
    outputEdgesL0 = boxL0.getOutputEdges()
    outputEdgesL1 = boxL1.getOutputEdges()
    outputEdgesH0 = boxH0.getOutputEdges()
    outputEdgesH1 = boxH1.getOutputEdges()
    outputEdgesLPort = boxLPort.getOutputEdges()
    outputEdgesX = boxX.getOutputEdges()

    prefixL0withX = copy.deepcopy(boxL0)
    prefixL0withL1 = copy.deepcopy(boxL0)
    prefixL0withH0 = copy.deepcopy(boxL0)
    prefixL0withH1 = copy.deepcopy(boxL0)

    prefixL0withX.makePrefix(outputEdgesX)
    prefixL0withL1.makePrefix(outputEdgesL1)
    prefixL0withH0.makePrefix(outputEdgesH0)
    prefixL0withH1.makePrefix(outputEdgesH1)

    prefixL0withX.printTreeAut()
    prefixL0withL1.printTreeAut()
    prefixL0withH0.printTreeAut()
    prefixL0withH1.printTreeAut()
    

def complementTests():
    # print("\n- L0 complement\n")
    complementL0 = treeAutComplement(boxL0)
    # complementL0.printTreeAut()

    # print("\n- L1 complement\n")
    complementL1 = treeAutComplement(boxL1)
    # complementL1.printTreeAut()

    # print("\n- H0 complement\n")
    complementH0 = treeAutComplement(boxH0)
    # complementH0.printTreeAut()

    # print("\n- H1 complement\n")
    complementH1 = treeAutComplement(boxH1)
    # complementH1.printTreeAut()

    # print("\n- X complement\n")
    complementX = treeAutComplement(boxX)
    # complementX.printTreeAut()

    

if __name__ == '__main__':
    main()

# End of file
