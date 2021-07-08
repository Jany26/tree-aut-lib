# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

import sys
# sys.path.append('../')

from treeAut import *
from boxes import *

def main():
    # basicTests()
    treeAutTests()

def treeAutTests():
    # test tree for H1 box
    testForH1 = TTreeNode("LH")
    testForH1.addChild("LH")
    testForH1.addChild("1")
    testForH1.children[0].addChild("Port_H1")
    testForH1.children[0].addChild("1")

    # boxH1.printTreeAut()
    # testForH1.printNode()

    print(matchTree(boxH1, testForH1))


def basicTests():
    # some tests ... 
    x = TTreeNode(10)
    x.addChild(5)
    x.addChild(15)
    x.children[0].addChild(1)
    x.children[0].addChild(4)
    x.children[0].addChild(2)
    x.children[1].addChild(3)
    x.children[1].addChild(4)
    x.printNode()
    y = x.findFromLeft(4)
    print("")
    y.printNode()
    y.parent.printNode()
    z = x.findFromRight(4)
    print("")
    z.printNode()
    z.parent.printNode()

if __name__ == '__main__':
    main()

# End of file
