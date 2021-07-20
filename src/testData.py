# testData.py
# Test variables used in testSuite.py for better readability
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *
from boxes import *
from treeExamples import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# first argument is a list of all "root" states
# "leaf" states are recognized by having at least one transition which
# has an empty tuple at the end (descendants) -> "output edge"

boxX    = TTreeAut(["q0"], testTransitionsBoxX)
boxL0   = TTreeAut(["r0"], testTransitionsBoxL0)
boxL1   = TTreeAut(["s0"], testTransitionsBoxL1)
boxH0   = TTreeAut(["t0"], testTransitionsBoxH0)
boxH1   = TTreeAut(["u0"], testTransitionsBoxH1)
boxLPort= TTreeAut(["v0"], testTransitionsBoxLPort)

# output edge array for createPrefix()

outputEdgesX = boxX.getOutputEdges()
outputEdgesL0 = boxL0.getOutputEdges()
outputEdgesL1 = boxL1.getOutputEdges()
outputEdgesH0 = boxH0.getOutputEdges()
outputEdgesH1 = boxH1.getOutputEdges()
outputEdgesLPort = boxLPort.getOutputEdges()

# createSuffix() test data

Xsuffix = boxX.createSuffix()
L0suffix = boxL0.createSuffix()
L1suffix = boxL1.createSuffix()
H0suffix = boxH0.createSuffix()
H1suffix = boxH1.createSuffix()

# createprefix() test data

XprefixForL0 = boxX.createPrefix(['0', 'Port_L0'])
XprefixForL1 = boxX.createPrefix(['1', 'Port_L1'])
XprefixForH0 = boxX.createPrefix(['0', 'Port_H0'])
XprefixForH1 = boxX.createPrefix(['1', 'Port_H1'])

L0prefixForX = boxL0.createPrefix(['Port_X'])
L0prefixForL1 = boxL0.createPrefix(['1', 'Port_L1'])
L0prefixForH0 = boxL0.createPrefix(['0', 'Port_H0'])
L0prefixForH1 = boxL0.createPrefix(['1', 'Port_H1'])

L1prefixForX = boxL1.createPrefix(['Port_X'])
L1prefixForL0 = boxL1.createPrefix(['0', 'Port_L0'])
L1prefixForH0 = boxL1.createPrefix(['0', 'Port_H0'])
L1prefixForH1 = boxL1.createPrefix(['1', 'Port_H1'])

H0prefixForX = boxH0.createPrefix(['Port_X'])
H0prefixForL0 = boxH0.createPrefix(['0', 'Port_L0'])
H0prefixForL1 = boxH0.createPrefix(['1', 'Port_L1'])
H0prefixForH1 = boxH0.createPrefix(['1', 'Port_H1'])

H1prefixForX = boxH1.createPrefix(['Port_X'])
H1prefixForL0 = boxH1.createPrefix(['0', 'Port_L0'])
H1prefixForL1 = boxH1.createPrefix(['1', 'Port_L1'])
H1prefixForH0 = boxH1.createPrefix(['0', 'Port_H0'])

# treeAutUnion() test data

unionXL0 = treeAutUnion(boxX, boxL0)
unionXL1 = treeAutUnion(boxX, boxL1)
unionXH0 = treeAutUnion(boxX, boxH0)
unionXH1 = treeAutUnion(boxX, boxH1)
unionL0H0 = treeAutUnion(boxL0, boxH0)
unionL0H1 = treeAutUnion(boxL0, boxH1)
unionL0L1 = treeAutUnion(boxL0, boxL1)
unionL1H0 = treeAutUnion(boxL1, boxH0)
unionL1H1 = treeAutUnion(boxL1, boxH1)
unionH0H1 = treeAutUnion(boxH0, boxH1)

# treeAutIntersection() test data

intersectionXL0 = treeAutIntersection(boxX, boxL0)
intersectionXL1 = treeAutIntersection(boxX, boxL1)
intersectionXH0 = treeAutIntersection(boxX, boxH0)
intersectionXH1 = treeAutIntersection(boxX, boxH1)
intersectionL0H0 = treeAutIntersection(boxL0, boxH0)
intersectionL0H1 = treeAutIntersection(boxL0, boxH1)
intersectionL0L1 = treeAutIntersection(boxL0, boxL1)
intersectionL1H0 = treeAutIntersection(boxL1, boxH0)
intersectionL1H1 = treeAutIntersection(boxL1, boxH1)
intersectionH0H1 = treeAutIntersection(boxH0, boxH1)

# End of file testData.py