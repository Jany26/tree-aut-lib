# testData.py
# Test variables used in testSuite.py for better readability
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *
from taClasses import *
from testTAs import *
from testTrees import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# first argument is a list of all "root" states
# "leaf" states are recognized by having at least one transition which
# has an empty tuple at the end (descendants) -> "output edge"

boxX    = TTreeAut(["q0"], testTransitionsBoxX)
boxL0   = TTreeAut(["r0"], testTransitionsBoxL0)
boxL1   = TTreeAut(["s0"], testTransitionsBoxL1)
boxH0   = TTreeAut(["t0"], testTransitionsBoxH0)
boxH1   = TTreeAut(["u0"], testTransitionsBoxH1)
boxLPort = TTreeAut(["v0"], testTransitionsBoxLPort)

# # output edge array for createPrefix()

outputEdgesX = boxX.getOutputEdges()
outputEdgesL0 = boxL0.getOutputEdges()
outputEdgesL1 = boxL1.getOutputEdges()
outputEdgesH0 = boxH0.getOutputEdges()
outputEdgesH1 = boxH1.getOutputEdges()
outputEdgesLPort = boxLPort.getOutputEdges()

# reachability and useless state removal test data
testBox1 = TTreeAut(['q0'], unreachableTest1)
testBox2a = TTreeAut(['q0'], unreachableTest2a)
testBox2b = TTreeAut(['q0'], unreachableTest2b)
testBox3 = copy.deepcopy(boxL0)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

boxesDict = {
    "boxX" : TTreeAut(["q0"], testTransitionsBoxX),
    "boxL0" : TTreeAut(["r0"], testTransitionsBoxL0),
    "boxL1" : TTreeAut(["s0"], testTransitionsBoxL1),
    "boxH0" : TTreeAut(["t0"], testTransitionsBoxH0),
    "boxH1" : TTreeAut(["u0"], testTransitionsBoxH1),
    "boxLPort" : TTreeAut(["v0"], testTransitionsBoxLPort),

    "unionXL0" : treeAutUnion(boxX, boxL0),
    "unionXL1" : treeAutUnion(boxX, boxL1),
    "unionXH0" : treeAutUnion(boxX, boxH0),
    "unionXH1" : treeAutUnion(boxX, boxH1),
    "unionL0H0" : treeAutUnion(boxL0, boxH0),
    "unionL0H1" : treeAutUnion(boxL0, boxH1),
    "unionL0L1" : treeAutUnion(boxL0, boxL1),
    "unionL1H0" : treeAutUnion(boxL1, boxH0),
    "unionL1H1" : treeAutUnion(boxL1, boxH1),
    "unionH0H1" : treeAutUnion(boxH0, boxH1),

    "intersectionXL0" :  treeAutIntersection(boxX, boxL0),
    "intersectionXL1" :  treeAutIntersection(boxX, boxL1),
    "intersectionXH0" :  treeAutIntersection(boxX, boxH0),
    "intersectionXH1" :  treeAutIntersection(boxX, boxH1),
    "intersectionL0H0" : treeAutIntersection(boxL0, boxH0),
    "intersectionL0H1" : treeAutIntersection(boxL0, boxH1),
    "intersectionL0L1" : treeAutIntersection(boxL0, boxL1),
    "intersectionL1H0" : treeAutIntersection(boxL1, boxH0),
    "intersectionL1H1" : treeAutIntersection(boxL1, boxH1),
    "intersectionH0H1" : treeAutIntersection(boxH0, boxH1),

    "complementX" : treeAutComplement(boxX),
    "complementL0" : treeAutComplement(boxL0),
    "complementL1" : treeAutComplement(boxL1),
    "complementH0" : treeAutComplement(boxH0),
    "complementH1" : treeAutComplement(boxH1),
    "complementLPort" : treeAutComplement(boxLPort),
    
    "Xsuffix" : boxX.createSuffix(),
    "L0suffix" : boxL0.createSuffix(),
    "L1suffix" : boxL1.createSuffix(),
    "H0suffix" : boxH0.createSuffix(),
    "H1suffix" : boxH1.createSuffix(),

    "XprefixForL0" : boxX.createPrefix(outputEdgesL0),
    "XprefixForL1" : boxX.createPrefix(outputEdgesL1),
    "XprefixForH0" : boxX.createPrefix(outputEdgesH0),
    "XprefixForH1" : boxX.createPrefix(outputEdgesH0),
    "L0prefixForX"  : boxL0.createPrefix(outputEdgesX),
    "L0prefixForL1" : boxL0.createPrefix(outputEdgesL1),
    "L0prefixForH0" : boxL0.createPrefix(outputEdgesH0),
    "L0prefixForH1" : boxL0.createPrefix(outputEdgesH0),
    "L1prefixForX"  : boxL1.createPrefix(outputEdgesX),
    "L1prefixForL0" : boxL1.createPrefix(outputEdgesL0),
    "L1prefixForH0" : boxL1.createPrefix(outputEdgesH0),
    "L1prefixForH1" : boxL1.createPrefix(outputEdgesH0),
    "H0prefixForX"  : boxH0.createPrefix(outputEdgesX),
    "H0prefixForL0" : boxH0.createPrefix(outputEdgesL0),
    "H0prefixForL1" : boxH0.createPrefix(outputEdgesL1),
    "H0prefixForH1" : boxH0.createPrefix(outputEdgesH0),
    "H1prefixForX"  : boxH1.createPrefix(outputEdgesX),
    "H1prefixForL0" : boxH1.createPrefix(outputEdgesL0),
    "H1prefixForL1" : boxH1.createPrefix(outputEdgesL1),
    "H1prefixForH0" : boxH1.createPrefix(outputEdgesH0)
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

functionPtrs = {
    "matchTreeBU" : matchTreeBU,
    "matchTreeTD" : matchTreeTD,
    
    "treeAutUnion" : treeAutUnion,
    "treeAutIntersection" : treeAutIntersection,
    "treeAutDeterminize" : treeAutDeterminize,
    "treeAutComplement" : treeAutComplement,
    
    "nonEmptyTD" : nonEmptyTD,
    "nonEmptyBU" : nonEmptyBU,
    
    "reachableTD" : reachableTD,
    "reachableBU" : reachableBU,
    "removeUselessStates" : removeUselessStates
}

# End of file testData.py
