# boxes.py
# Some basic testing for tree implementation and tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

import sys
sys.path.append('../')

from src.treeAut import *

def main():
    basicTests()

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
