# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

import sys
import os
import re

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
    inner dictionaries (B) are then referenced by some transitions (arbitrary name)
    the transitions are then tuples of input state, 
    type of transition and output states
"""
class TTreeAut:
    def __init__(self, rootStates, transitions):
        self.rootStates = rootStates
        self.transitions = transitions

    def printTreeAut(self):
        for state, content in self.transitions.items():
            print("--- State " + state + " ---")
            # needs polishing
            for key, transition in content.items():
                print(  "  from  '" + transition[0] + 
                        "'  through  '" + transition[1] + 
                        "'  to  " + str(transition[2]))

    def makePrefix(self, additionalTransitions):
        prefixSelf = self
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


# Functions for testing purposes

def getNodeFromString(string:str):
    string = string.strip()
    nodeName = re.match("^[\w]+", string).group()
    string = string.lstrip(str(nodeName))
    node = TTreeNode(nodeName)
    return node, string

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
