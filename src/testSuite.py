# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

import sys
# sys.path.append('../')

from treeAut import *
from boxes import *
from treeExamples import *

def main():
    print("testing match() ... \n\t" + matchTests())

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
    
    if not matchTree(boxH1, treeH1test1):
        failedTests += "H1-1, "
    if not matchTree(boxH1, treeH1test2):
        failedTests += "H1-2, "
    if not matchTree(boxH1, treeH1test3):
        failedTests += "H1-3, "
    
    if not matchTree(boxL0, treeL0test1):
        failedTests += "L0-1, "
    if not matchTree(boxL0, treeL0test2):
        failedTests += "L0-2, "
    if not matchTree(boxL0, treeL0test3):
        failedTests += "L0-3, "

    if not matchTree(boxL1, treeL1test1):
        failedTests += "L1-1, "
    if not matchTree(boxL1, treeL1test2):
        failedTests += "L1-2, "
    if not matchTree(boxL1, treeL1test3):
        failedTests += "L1-3, "

    if failedTests == "":
        failedTests = "None"
    return "Failed tests: " + failedTests
    

if __name__ == '__main__':
    main()

# End of file
