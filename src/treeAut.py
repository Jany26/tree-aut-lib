# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

# import sys
# import os
import copy
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

        for stateName, content in self.transitions.items():
            print("--- State " + stateName + " ---")
            # needs polishing
            for key, transition in content.items():
                print(  "  from  '" + transition[0] + 
                        "'  through  '" + transition[1] + 
                        "'  to  " + str(transition[2]))

    # needed for feeding makePrefix() function
    # generates all edge symbols labeling the output edges from the tree automaton
    def getOutputEdges(self):
        outputEdgeArray = []
        for stateName, content in self.transitions.items():
            for key, transition in content.items():
                if len(transition[2]) == 0:
                    outputEdgeArray.append(transition[1])
        return outputEdgeArray
    
    def createPrefix(self, additionalOutputEdges): 
        result = copy.deepcopy(self)
        for stateName, content in result.transitions.items():
            tempDict = {}
            for symbol in additionalOutputEdges:
                tempString = str(stateName) + "-" + str(symbol) + "-()"
                tempTuple = (stateName, symbol, [])
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
        return result

    def createSuffix(self):
        result = copy.deepcopy(self)
        for stateName, content in result.transitions.items():
            check = True
            # needs polishing
            for key, transition in content.items():
                if (transition[1].startswith("Port")):
                    check = False
                    break
            if check == True and stateName not in result.rootStates:
                result.rootStates.append(stateName)
        return result

def matchTree(treeAutomaton:TTreeAut, treeRootNode:TTreeNode):
    for rootPtr in treeAutomaton.rootStates:
        if match(treeAutomaton, treeRootNode, rootPtr) == True:
            return True
    return False

def match(treeAut:TTreeAut, node:TTreeNode, state:str):
    descendantTuples = []

    # maybe needs polishing
    for stateName, content in treeAut.transitions.items():
        for key, transition in content.items():
            if stateName == state and node.value == transition[1]:
                descendantTuples.append(transition[2])
    
    for tuple in descendantTuples:
        b = True
        # when tree unexpected amount children than expected
        if len(tuple) != len(node.children):
            break
        for i in range(len(tuple)):
            # recursive matching for all children
            b = match(treeAut, node.children[i], tuple[i])
            if not b:
                break
        if b:
            return True
    return False

# Basic operations on tree automata

def treeAutDetermize(treeAut1:TTreeAut) -> TTreeAut:
    pass

# -- temporary notes --
# A1 U A2
#
# A1 = (Q1, delta1, R1), A2 = (Q2, delta2, R2)
# A1 U A2 = (Q1 U Q2 (with renaming at conflicts), delta1 U delta2, R1 U R2)


# find out how to change tuples and dictionary keys :(
def renameStateInTreeAut(oldName, newName, treeAut:TTreeAut):
    if oldName not in treeAut.transitions:
        return
    # supposing only one state with the oldName exists in treeAut
    # renaming state in the dictionary of states (1st layer)
    treeAut.transitions[newName] = treeAut.transitions.pop(oldName)

    # renaming name of the state inside transitions (2nd layer)
    for stateName, content in treeAut.transitions.items():
        for key, transition in content.items():
            if transition[0] == oldName:
                transition[0] = str(newName)
            # renaming state name inside 
            for i in range(len(transition[2])):
                if transition[2][i] == oldName:
                    transition[2][i] = newName
    if oldName in treeAut.rootStates:
        treeAut.rootStates.remove(oldName)
        treeAut.rootStates.append(newName)


# just merging transition dictionaries and set of rootstates
# before merging, name resolution is needed for states with the same name
def treeAutUnion(treeAut1:TTreeAut, treeAut2:TTreeAut) -> TTreeAut:
    result = copy.deepcopy(treeAut2)

    # remove name collisions by renaming states in a new automaton
    for stateName in treeAut1.transitions:
        if stateName in result.transitions:
            renameStateInTreeAut(stateName, str(stateName) + "_new", result)
    
    # merge
    result.transitions = {**result.transitions, **treeAut1.transitions}
    result.rootStates = result.rootStates + treeAut1.rootStates
    return result

# TODO: REFACTORING needed here
def treeAutIntersection(treeAut1:TTreeAut, treeAut2:TTreeAut) -> TTreeAut:
    result = TTreeAut([], {})
    for stateName1, content1 in treeAut1.transitions.items():
        for stateName2, content2 in treeAut2.transitions.items():
            newStateName = "(" + stateName1 + ", " + stateName2 + ")"
            if stateName1 in treeAut1.rootStates and stateName2 in treeAut2.rootStates:
                result.rootStates.append(newStateName)
            for key1, transition1 in content1.items():
                for key2, transition2 in content2.items():
                    # adding new transition to the intersection if possible
                    if transition1[1] == transition2[1]:
                        # check if the arity is consistent (for now we just assume it is)
                        if len(transition1[2]) != len(transition2[2]):
                            # TODO error handle
                            return result  
                        newTransition = []
                        newTransition.append("(" + transition1[0] + ", " + transition2[0] + ")")
                        newTransition.append(transition1[1])
                        childStates = []
                        for i in range(len(transition1[2])):
                            childStates.append("(" + transition1[2][i] + ", " + transition2[2][i] + ")")
                        newTransition.append(childStates)

                        newKey = "(" + key1 + ", " + key2 + ")"
                        if newStateName not in result.transitions:
                            # add state to transition dictionary
                            result.transitions[newStateName] = {}
                            pass
                        result.transitions[newStateName][newKey] = newTransition
                    pass
    print(str(result.rootStates))
    return result

def treeAutComplement(treeAut:TTreeAut) -> TTreeAut:

    # TODO: bottom-up determinization implementation needed
    # result = treeAutdeterminize(treeAut)

    rootStates = []
    for stateName, content in treeAut.transitions.items():
        if stateName not in treeAut.rootStates:
            rootStates.append(stateName)
    return TTreeAut(rootStates, treeAut.transitions)

# Functions for testing purposes

# Does not cover edge cases! (e.g. wrong string structure)
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

# End of file
