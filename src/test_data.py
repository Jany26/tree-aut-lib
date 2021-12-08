# test_data.py
# Test variables used in testSuite.py for better readability
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_functions import *
from test_trees import *
from format_vtf import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# first argument is a list of all "root" states
# "leaf" states are recognized by having at least one transition which
# has an empty tuple at the end (descendants) -> "output edge"

fullAlphabet = {
    "LH" : 2,
    "0" : 0,
    "1" : 0,
    "Port_X" : 0,
    "Port_L0" : 0,
    "Port_L1" : 0,
    "Port_H0" : 0,
    "Port_H1" : 0,
    "Port_LPort0" : 0,
    "Port_LPort1" : 0,
    "Port_HPort0" : 0,
    "Port_HPort1" : 0,
}

boxCatalogue = {
    "X"     : importTAfromVTF("tests/boxX.vtf"),
    "L0"    : importTAfromVTF("tests/boxL0.vtf"),
    "L1"    : importTAfromVTF("tests/boxL1.vtf"),
    "H0"    : importTAfromVTF("tests/boxH0.vtf"),
    "H1"    : importTAfromVTF("tests/boxH1.vtf"),
    "LPort" : importTAfromVTF("tests/boxLPort.vtf"),
    "HPort" : importTAfromVTF("tests/boxHPort.vtf"),
}

boxX = boxCatalogue["X"]
boxL0 = boxCatalogue["L0"]
boxL1 = boxCatalogue["L1"]
boxH0 = boxCatalogue["H0"]
boxH1 = boxCatalogue["H1"]
boxLPort = boxCatalogue["LPort"]
boxHPort = boxCatalogue["HPort"]

# output edge array for createPrefix()

outputEdgesX = boxX.getOutputSymbols()
outputEdgesL0 = boxL0.getOutputSymbols()
outputEdgesL1 = boxL1.getOutputSymbols()
outputEdgesH0 = boxH0.getOutputSymbols()
outputEdgesH1 = boxH1.getOutputSymbols()
outputEdgesLPort = boxLPort.getOutputSymbols()
outputEdgesHPort = boxHPort.getOutputSymbols()

# reachability and useless state removal test data
testUnreachable1 = importTAfromVTF("tests/testUnreachable1.vtf")
testUnreachable2 = importTAfromVTF("tests/testUnreachable2.vtf")
testUnreachable3 = importTAfromVTF("tests/testUnreachable3.vtf")

testNonEmpty1    = importTAfromVTF("tests/testNonEmpty1.vtf")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

boxesDict = {
    "boxX"      : boxX,
    "boxL0"     : boxL0,
    "boxL1"     : boxL1,
    "boxH0"     : boxH0,
    "boxH1"     : boxH1,
    "boxLPort"  : boxLPort,
    "boxHPort"  : boxHPort,

    "unionXL0"  : treeAutUnion(boxX, boxL0),
    "unionXL1"  : treeAutUnion(boxX, boxL1),
    "unionXH0"  : treeAutUnion(boxX, boxH0),
    "unionXH1"  : treeAutUnion(boxX, boxH1),
    "unionL0H0" : treeAutUnion(boxL0, boxH0),
    "unionL0H1" : treeAutUnion(boxL0, boxH1),
    "unionL0L1" : treeAutUnion(boxL0, boxL1),
    "unionL1H0" : treeAutUnion(boxL1, boxH0),
    "unionL1H1" : treeAutUnion(boxL1, boxH1),
    "unionH0H1" : treeAutUnion(boxH0, boxH1),

    "intersectionXL0"   : treeAutIntersection(boxX, boxL0),
    "intersectionXL1"   : treeAutIntersection(boxX, boxL1),
    "intersectionXH0"   : treeAutIntersection(boxX, boxH0),
    "intersectionXH1"   : treeAutIntersection(boxX, boxH1),
    "intersectionL0H0"  : treeAutIntersection(boxL0, boxH0),
    "intersectionL0H1"  : treeAutIntersection(boxL0, boxH1),
    "intersectionL0L1"  : treeAutIntersection(boxL0, boxL1),
    "intersectionL1H0"  : treeAutIntersection(boxL1, boxH0),
    "intersectionL1H1"  : treeAutIntersection(boxL1, boxH1),
    "intersectionH0H1"  : treeAutIntersection(boxH0, boxH1),

    "complementX"       : treeAutComplement(boxX, fullAlphabet),
    "complementL0"      : treeAutComplement(boxL0, fullAlphabet),
    "complementL1"      : treeAutComplement(boxL1, fullAlphabet),
    "complementH0"      : treeAutComplement(boxH0, fullAlphabet),
    "complementH1"      : treeAutComplement(boxH1, fullAlphabet),
    "complementLPort"   : treeAutComplement(boxLPort, fullAlphabet),
    "complementHPort"   : treeAutComplement(boxHPort, fullAlphabet),

    "determinizedX"     : treeAutDeterminization(boxX, fullAlphabet),
    "determinizedL0"    : treeAutDeterminization(boxL0, fullAlphabet),
    "determinizedL1"    : treeAutDeterminization(boxL1, fullAlphabet),
    "determinizedH0"    : treeAutDeterminization(boxH0, fullAlphabet),
    "determinizedH1"    : treeAutDeterminization(boxH1, fullAlphabet),
    "determinizedLPort" : treeAutDeterminization(boxLPort, fullAlphabet),
    "determinizedHPort" : treeAutDeterminization(boxHPort, fullAlphabet),
    
    "Xsuffix"       : boxX.createSuffix(),
    "L0suffix"      : boxL0.createSuffix(),
    "L1suffix"      : boxL1.createSuffix(),
    "H0suffix"      : boxH0.createSuffix(),
    "H1suffix"      : boxH1.createSuffix(),
    "LPortsuffix"   : boxLPort.createSuffix(),

    "XprefixForL0"      : boxX.createPrefix(outputEdgesL0),
    "XprefixForL1"      : boxX.createPrefix(outputEdgesL1),
    "XprefixForH0"      : boxX.createPrefix(outputEdgesH0),
    "XprefixForH1"      : boxX.createPrefix(outputEdgesH0),
    "XprefixForLPort"   : boxX.createPrefix(outputEdgesLPort),
    "XprefixForHPort"   : boxX.createPrefix(outputEdgesHPort),

    "L0prefixForX"      : boxL0.createPrefix(outputEdgesX),
    "L0prefixForL1"     : boxL0.createPrefix(outputEdgesL1),
    "L0prefixForH0"     : boxL0.createPrefix(outputEdgesH0),
    "L0prefixForH1"     : boxL0.createPrefix(outputEdgesH0),
    "L0prefixForLPort"  : boxL0.createPrefix(outputEdgesLPort),
    
    "L1prefixForX"      : boxL1.createPrefix(outputEdgesX),
    "L1prefixForL0"     : boxL1.createPrefix(outputEdgesL0),
    "L1prefixForH0"     : boxL1.createPrefix(outputEdgesH0),
    "L1prefixForH1"     : boxL1.createPrefix(outputEdgesH0),
    "L1prefixForLPort"  : boxL1.createPrefix(outputEdgesLPort),
    
    "H0prefixForX"      : boxH0.createPrefix(outputEdgesX),
    "H0prefixForL0"     : boxH0.createPrefix(outputEdgesL0),
    "H0prefixForL1"     : boxH0.createPrefix(outputEdgesL1),
    "H0prefixForH1"     : boxH0.createPrefix(outputEdgesH0),
    "H0prefixForLPort"  : boxH0.createPrefix(outputEdgesLPort),
    
    "H1prefixForX"      : boxH1.createPrefix(outputEdgesX),
    "H1prefixForL0"     : boxH1.createPrefix(outputEdgesL0),
    "H1prefixForL1"     : boxH1.createPrefix(outputEdgesL1),
    "H1prefixForH0"     : boxH1.createPrefix(outputEdgesH0),
    "H1prefixForLPort"  : boxH1.createPrefix(outputEdgesLPort),
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

functionPtrs = {
    "matchTreeBU" : matchTreeBU,
    "matchTreeTD" : matchTreeTD,
    
    "treeAutUnion" : treeAutUnion,
    "treeAutIntersection" : treeAutIntersection,
    "treeAutDeterminization" : treeAutDeterminization,
    "treeAutComplement" : treeAutComplement,
    
    "nonEmptyTD" : nonEmptyTD,
    "nonEmptyBU" : nonEmptyBU,
    
    "reachableTD" : reachableTD,
    "reachableBU" : reachableBU,
    "removeUselessStates" : removeUselessStates
}

# End of file test_data.py
