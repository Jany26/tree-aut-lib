# testExamples.py
# Some basic trees and basic TAs for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *
import re

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
# TESTING DATA - TREES (represented by structured strings)
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

testTreeDict = {
    "treeXtest1" : buildTreeFromString(None, XTreeExample1),
    "treeXtest2" : buildTreeFromString(None, XTreeExample2),
    "treeXtest3" : buildTreeFromString(None, XTreeExample3),

    "treeL0test1" : buildTreeFromString(None, L0TreeExample1),
    "treeL0test2" : buildTreeFromString(None, L0TreeExample2),
    "treeL0test3" : buildTreeFromString(None, L0TreeExample3),
    "treeL0test4" : buildTreeFromString(None, L0TreeExample4),

    "treeL1test1" : buildTreeFromString(None, L1TreeExample1),
    "treeL1test2" : buildTreeFromString(None, L1TreeExample2),
    "treeL1test3" : buildTreeFromString(None, L1TreeExample3),
    "treeL1test4" : buildTreeFromString(None, L1TreeExample4),

    "treeH0test1" : buildTreeFromString(None, H0TreeExample1),
    "treeH0test2" : buildTreeFromString(None, H0TreeExample2),
    "treeH0test3" : buildTreeFromString(None, H0TreeExample3),
    "treeH0test4" : buildTreeFromString(None, H0TreeExample4),

    "treeH1test1" : buildTreeFromString(None, H1TreeExample1),
    "treeH1test2" : buildTreeFromString(None, H1TreeExample2),
    "treeH1test3" : buildTreeFromString(None, H1TreeExample3),
    "treeH1test4" : buildTreeFromString(None, H1TreeExample4)
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTING DATA - TREE AUTOMATA (Basic boxes from the article)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

testTransitionsBoxX = {
    'q0': {
        'a': ['q0', 'LH', ['q0', 'q0']],
        'b': ['q0', 'LH', ['q1', 'q1']]
        }, 
    'q1': {
        'c': ['q1', 'Port_X', []]
    }
}

testTransitionsBoxL0 = {
    'r0': {
        'a': ['r0', 'LH', ['r1', 'r0']],
        'b': ['r0', 'LH', ['r1', 'r2']]
        }, 
    'r1': {
        'c': ['r1', 'LH', ['r1', 'r1']],
        'd': ['r1', '0', []]
    },
    'r2': {
        'e': ['r2', 'Port_L0', []]
    }
}

testTransitionsBoxL1 = {
    's0': {
        'a': ['s0', 'LH', ['s1', 's0']],
        'b': ['s0', 'LH', ['s1', 's2']]
        }, 
    's1': {
        'c': ['s1', 'LH', ['s1', 's1']],
        'd': ['s1', '1', []]
    },
    's2': {
        'e': ['s2', 'Port_L1', []]
    }
}

testTransitionsBoxH0 = {
    't0': {
        'a': ['t0', 'LH', ['t0', 't2']],
        'b': ['t0', 'LH', ['t1', 't2']]
        }, 
    't1': {
        'c': ['t1', 'Port_H0', []]
    },
    't2': {
        'd': ['t2', 'LH', ['t2', 't2']],
        'e': ['t2', '0', []]
    }
}

testTransitionsBoxH1 = {
    'u0': {
        'a': ['u0', 'LH', ['u0', 'u2']],
        'b': ['u0', 'LH', ['u1', 'u2']]
        }, 
    'u1': {
        'c': ['u1', 'Port_H1', []]
    },
    'u2': {
        'd': ['u2', 'LH', ['u2', 'u2']],
        'e': ['u2', '1', []]
    }
}

testTransitionsBoxLPort = {
    'v0': {
        'a': ['v0', 'LH', ['v1', 'v0']],
        'b': ['v0', 'LH', ['v1', 'v2']]
        }, 
    'v1': {
        'c': ['v1', 'LH', ['v1', 'v1']],
        'd': ['v1', 'Port_LPort0', []]
    },
    'v2': {
        'e': ['v2', 'Port_LPort1', []]
    }
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Testing boxes = with top-down/bottom-up unreachable states ...
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

unreachableTest1 = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q0']],
    },
    'q1': {
        'b': ['q1', '1', []]
    }
}

# basically H1 box with extra 2 states = q3, q4 and 3 transitions f-h
unreachableTest2a = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q2']],
        'b': ['q0', 'LH', ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1','Port', []],
    },
    'q2': {
        'd': ['q2', 'LH', ['q2', 'q2']],
        'e': ['q2', '1', []],
        'f': ['q2', 'LH', ['q2', 'q3']],
    },
    'q3': {
        'g': ['q3', '1', []],
    },
    'q4': {
        'h': ['q4', 'LH', ['q4','q3']],
    }
}

# same as unreachableTest2, but 'f' transition connects to root not to itself 
unreachableTest2b = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q2']],
        'b': ['q0', 'LH', ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1','Port', []],
    },
    'q2': {
        'd': ['q2', 'LH', ['q2', 'q2']],
        'e': ['q2', '1', []],
        'f': ['q2', 'LH', ['q0', 'q3']],
    },
    'q3': {
        'g': ['q3', '1', []],
    },
    'q4': {
        'h': ['q4', 'LH', ['q4','q3']],
    }
}

testTransitionscomplementL0 = {
    'sink': {
        'a': ['sink', 'LH', ['sink','q0']],
        'b': ['sink', 'LH', ['q0','sink']],
        'c': ['sink', 'LH', ['sink','q1']],
        'd': ['sink', 'LH', ['q1','sink']],
        'e': ['sink', 'LH', ['sink','q2']],
        'f': ['sink', 'LH', ['q2','sink']],
        'g': ['sink', 'LH', ['sink','sink']],
        'h': ['sink', '1', []],
        'k': ['sink', 'Port_X', []],
        'i': ['sink', 'Port_L1', []],
        'j': ['sink', 'Port_H0', []],
        'l': ['sink', 'Port_H1', []]
    },
    'q0': {
        'm': ['q0', 'LH', ['q1','q0']],
        'n': ['q0', 'LH', ['q1','q2']]
    },
    'q1': {
        'o': ['q1', '0', []]
    },
    'q2': {
        'p': ['q2', 'LH', ['q2','q2']],
        'q': ['q2', 'Port_L0', []]
    }
}

# End of file testExamples.py
