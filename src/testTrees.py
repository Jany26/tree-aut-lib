# testTrees.py
# Some basic trees for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *
import re

# maybe load trees from this template form instead of calling class methods manually ???

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS FOR TESTING PURPOSES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## Does not cover edge cases! (e.g. wrong string structure)
def getNodeFromString(string:str):
    string = string.strip()
    nodeName = re.match("^[\w]+", string).group()
    string = string.lstrip(str(nodeName))
    node = TTreeNode(nodeName)
    return node, string

## Recursive function to generate a tree from a structured string
# XYZ [...] = node with list of children following (can be nested)
# [ node1 ; node2 [...] ; node3 ; ... ] = list of children of a previous node
def buildTreeFromString(currentNode:TTreeNode, string:str):
    string = string.strip() # skipping whitespaces

    # empty string - ending recursion
    if len(string) == 0:
        return currentNode
    
    # starting children generation (down a level)
    if string.startswith("["):
        node, string = getNodeFromString(string[1:]) 
        currentNode.connectChild(node)
        return buildTreeFromString(node, string)

    # continuing children generation (same level)
    elif string.startswith(";"):
        node, string = getNodeFromString(string[1:])
        currentNode.parent.connectChild(node)
        return buildTreeFromString(node, string)

    # ending children generation - returning to a parent (up a level)
    elif string.startswith("]"):
        return buildTreeFromString(currentNode.parent, string[1:])

    # start of a string - root creation (initial case - no special character at the beginning)
    else:
        root, string = getNodeFromString(string)
        return buildTreeFromString(root, string)

## Reverse of the buildTreeFromString function
# Creates a concise (string) representation of a tree from its structure
def buildStringFromTree(currentNode:TTreeNode) -> str:
    if len(currentNode.children) == 0:
        return str(currentNode.value)
    else:
        temp = currentNode.value + "["
        for i in range(len(currentNode.children)):
            temp += str(buildStringFromTree(currentNode.children[i]))
            if i < len(currentNode.children) - 1: 
                temp += ";"
        temp += "]"
        return temp

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTING DATA (trees represented by structured strings)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

XTreeExample1 = "LH[Port_X;Port_X]"
XTreeExample2 = "LH[LH[LH[Port_X;Port_X];Port_X];LH[Port_X;LH[Port_X;Port_X]]]"
XTreeExample3 = "LH[LH[Port_X;Port_X];LH[LH[LH[Port_X;Port_X];LH[Port_X;Port_X]];LH[Port_X;Port_X]]]"

L0TreeExample1 = "LH[0;LH[0;Port_L0]]"
L0TreeExample2 = "LH[0;LH[LH[LH[0;0];LH[0;0]];LH[0;Port_L0]]]"
L0TreeExample3 = "LH[LH[LH[0;0];LH[0;0]];LH[LH[0;0];LH[0;Port_L0]]]"
L0TreeExample4 = "LH[0;Port_L0]"

L1TreeExample1 = "LH[1;LH[1;Port_L1]]"
L1TreeExample2 = "LH[1;LH[LH[LH[1;1];LH[1;1]];LH[1;Port_L1]]]"
L1TreeExample3 = "LH[LH[LH[1;1];LH[1;1]];LH[LH[1;1];LH[1;Port_L1]]]"
L1TreeExample4 = "LH[1;Port_L1]"

H0TreeExample1 = "LH[LH[Port_H0;0];0]"
H0TreeExample2 = "LH[LH[LH[Port_H0;0];LH[LH[0;0];LH[0;0]]];0]"
H0TreeExample3 = "LH[LH[LH[Port_H0;0];LH[0;0]];LH[LH[0;0];LH[0;0]]]"
H0TreeExample4 = "LH[Port_H0;0]"

H1TreeExample1 = "LH[LH[Port_H1;1];1]"
H1TreeExample2 = "LH[LH[LH[Port_H1;1];LH[LH[1;1];LH[1;1]]];1]"
H1TreeExample3 = "LH[LH[LH[Port_H1;1];LH[1;1]];LH[LH[1;1];LH[1;1]]]"
H1TreeExample4 = "LH[Port_H1;1]"

treeXtest1 = buildTreeFromString(None, XTreeExample1)
treeXtest2 = buildTreeFromString(None, XTreeExample2)
treeXtest3 = buildTreeFromString(None, XTreeExample3)

treeL0test1 = buildTreeFromString(None, L0TreeExample1)
treeL0test2 = buildTreeFromString(None, L0TreeExample2)
treeL0test3 = buildTreeFromString(None, L0TreeExample3)
treeL0test4 = buildTreeFromString(None, L0TreeExample4)

treeL1test1 = buildTreeFromString(None, L1TreeExample1)
treeL1test2 = buildTreeFromString(None, L1TreeExample2)
treeL1test3 = buildTreeFromString(None, L1TreeExample3)
treeL1test4 = buildTreeFromString(None, L1TreeExample4)

treeH0test1 = buildTreeFromString(None, H0TreeExample1)
treeH0test2 = buildTreeFromString(None, H0TreeExample2)
treeH0test3 = buildTreeFromString(None, H0TreeExample3)
treeH0test4 = buildTreeFromString(None, H0TreeExample4)

treeH1test1 = buildTreeFromString(None, H1TreeExample1)
treeH1test2 = buildTreeFromString(None, H1TreeExample2)
treeH1test3 = buildTreeFromString(None, H1TreeExample3)
treeH1test4 = buildTreeFromString(None, H1TreeExample4)

# End of file testTrees.py
