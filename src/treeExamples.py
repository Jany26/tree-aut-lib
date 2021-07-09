# treeExamples.py
# Some basic trees for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

from treeAut import *
import re

# maybe load trees from this template form instead of calling class methods manually ???
H1TreeExample1 = "LH[LH[Port_H1;1];1]"
H1TreeExample2 = "LH[LH[LH[Port_H1;1];LH[LH[1;1];LH[1;1]]];1]"


def getNodeFromString(string:str):
    nodeName = re.match("^[\w]+", string).group()
    string = string.lstrip(str(nodeName))
    node = TTreeNode(nodeName)
    return node, string

def buildTreeFromString(currentNode:TTreeNode, string:str):
    string = string.strip()
    if len(string) == 0:
        return currentNode
    if string.startswith("["):
        node, string = getNodeFromString(string[1:])
        currentNode.connectChild(node)
        return buildTreeFromString(node, string)
    elif string.startswith(";"):
        node, string = getNodeFromString(string[1:])
        currentNode.parent.connectChild(node)
        return buildTreeFromString(node, string)
    elif string.startswith("]"):
        return buildTreeFromString(currentNode.parent, string[1:])
    else: # empty string
        root, string = getNodeFromString(string)
        return buildTreeFromString(root, string)
