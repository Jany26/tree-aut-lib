# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

# import sys
# import os
import re
from sys import prefix

class TTreeNode:
    def __init__(self, value):
        self.value = value
        self.parent = None # if None = the node is a root
        self.children = []
        self.depth = 0

    def addChild(self, value):
        childPtr = TTreeNode(value)
        childPtr.depth = self.depth + 1
        childPtr.parent = self
        self.children.append(childPtr)
    
    def connectChild(self, node): 
        self.children.append(node)
        node.parent = self
        node.depth = self.depth + 1
    
    def removeChild(self, value): # removes 1 child (starts from smallest index (left)) with specified value
        for i in range(len(self.children)):
            if self.children[i].value == value:
                self.children.pop(i)
                return
    
    # needed for testing
    def printNode(self):
        print(2 * self.depth * ' ' + str(self.value) + "   --> lv " + str(self.depth))
        for i in self.children:
            i.printNode()
    
    def findFromLeft(self, valueToFind):
        for i in self.children:
            x = i.findFromLeft(valueToFind)
            if x != None:
                return x
        return self if (self.value == valueToFind) else None

    def findFromRight(self, valueToFind):
        tempList = self.children[::-1]
        for i in tempList:
            x = i.findFromRight(valueToFind)
            if x != None:
                return x
        return self if (self.value == valueToFind) else None

"""
    transitions = dictionary (A) of dictionaries (B) referenced by state name
    inner dictionaries (B) are then referenced by transition names (arbitrary)
    the transition itself is then just a tuple of:
        - input state, 
        - transition label (edge name/type) 
        - array of output states (size of array = arity of the node)
    * all state and label names are considered as strings
"""
class TTreeAut:
    def __init__(self, rootStates, transitions):
        self.rootStates = rootStates
        self.transitions = transitions

    def printTreeAut(self):
        print("--- Root States ---")
        print(str(self.rootStates))

        for state, content in self.transitions.items():
            print("--- State " + state + " ---")
            # needs polishing
            for key, transition in content.items():
                print(  "  from  '" + transition[0] + 
                        "'  through  '" + transition[1] + 
                        "'  to  " + str(transition[2]))

    # needed for feeding makePrefix() function
    # generates all edge symbols labeling the output edges from the tree automaton
    def getOutputEdges(self):
        outputEdgeArray = []
        for state, content in self.transitions.items():
            for key, transition in content.items():
                if len(transition[2]) == 0:
                    outputEdgeArray.append(transition[1])
        return outputEdgeArray
    
    def makePrefix(self, additionalTransitions):
        prefixSelf = self
        for state, content in prefixSelf.transitions.items():
            tempDict = {}
            for symbol in additionalTransitions:
                tempString = str(state) + "-" + str(symbol) + "-()"
                tempTuple = (state, symbol, [])
                tempDict[tempString] = tempTuple
            for tempName, tempTransition in tempDict.items():
                # checking for non-port output edge
                nonPortOutput = False
                for name, transition in content.items():
                    if not transition[1].startswith('Port') and len(transition[2]) == 0:
                        nonPortOutput = True
                # skip adding non-port output edge if another non-port output present
                if not tempTransition[1].startswith('Port') and nonPortOutput:
                    continue
                else:
                    content[tempName] = tempTransition
        return prefixSelf
    
    def makeSuffix(self):
        suffixSelf = self
        for state, content in self.transitions.items():
            check = True
            # needs polishing
            for key, transition in content.items():
                if (transition[1].startswith("Port")):
                    check = False
                    break
            if check == True and state not in self.rootStates:
                suffixSelf.rootStates.append(state)
        return suffixSelf

def matchTree(treeAutomaton:TTreeAut, treeRootNode:TTreeNode):
    for rootPtr in treeAutomaton.rootStates:
        if match(treeAutomaton, treeRootNode, rootPtr) == True:
            return True
    return False

def match(treeaut:TTreeAut, node:TTreeNode, state:str):
    descendantTuples = []

    # definitely needs polishing
    for stateName, content in treeaut.transitions.items():
        for key, transition in content.items():
            if stateName == state and node.value == transition[1]:
                descendantTuples.append(transition[2])
    
    for tuple in descendantTuples:
        b = True
        for i in range(len(tuple)):
            if i not in range(len(node.children)):
                b = False # tree has less children than expected
                break
            b = match(treeaut, node.children[i], tuple[i])
            if not b:
                break
        if b:
            return True
    return False

# Basic operations on tree automata

def treeAutDetermize(treeAut1:TTreeAut) -> TTreeAut:
    pass

def treeAutUnion(treeAut1:TTreeAut, treeAut2:TTreeAut) -> TTreeAut:
    pass

def treeAutIntersection(treeAut1:TTreeAut, treeAut2:TTreeAut) -> TTreeAut:
    pass

def treeAutComplement(treeAut:TTreeAut) -> TTreeAut:
    pass

# Functions for testing purposes

# Does not cover edge cases (wrong string structure) !
def getNodeFromString(string:str):
    string = string.strip()
    nodeName = re.match("^[\w]+", string).group()
    string = string.lstrip(str(nodeName))
    node = TTreeNode(nodeName)
    return node, string

# Recursive function to generate a tree from a structured string
# XYZ [...] = node with list of children following (can be nested)
# [ node1 ; node2 [...] ; node3 ; ... ] = list of children of a previous node

def buildTreeFromString(currentNode:TTreeNode, string:str):
    # print(string)
    # currentNode.printNode()
    string = string.strip()
    if len(string) == 0: # empty string - ending recursion
        return currentNode
    if string.startswith("["): # starting children generation (down a level)
        node, string = getNodeFromString(string[1:])
        currentNode.connectChild(node)
        return buildTreeFromString(node, string)
    elif string.startswith(";"): # continuing children generation (same level)
        node, string = getNodeFromString(string[1:])
        currentNode.parent.connectChild(node)
        return buildTreeFromString(node, string)
    elif string.startswith("]"): # ending children generation - returning to a parent (up a level)
        return buildTreeFromString(currentNode.parent, string[1:])
    else: # start of a string - root creation
        root, string = getNodeFromString(string)
        return buildTreeFromString(root, string)

# End of file
