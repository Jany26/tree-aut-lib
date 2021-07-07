"""
    Basic classes needed for implementing tree automata

"""

def main():
    return

import sys
# import os

# class TAlphabetSymbol:
#     def __init__(self, name, arity:int):
#         self.name = name
#         self.arity = arity

# class TTreeTransition:
#     def __init__(self, initialState, symbol:TAlphabetSymbol, nextStates):
#         self.initialState = initialState
#         self.symbol = symbol
#         self.nextStates = nextStates

# class TTreeAut:
#     def __init__(self, states, alphabet, transitions:TTreeTransition, rootStates): # A = (Q, Sigma, Delta, R)
#         self.states = states
#         self.alphabet = alphabet
#         self.transitions = transitions # TODO define leaf transitions 
#         self.rootStates = rootStates
#         # how to perform top-down run for checking if the TA accepts a language

"""
    Node of a basic tree (general, does not have to be binary)
"""
class TTreeNode:
    def __init__(self, value):
        self.value = value
        self.parent = None # if None = the node is a root
        self.children = []

    # def connectChild(self, childPtr):
    #     childPtr.parent = self # connecting the children to the parent node
    #     self.children.append(childPtr)
    
    def createChild(self, value):
        childPtr = TTreeNode(value)
        childPtr.parent = self
        self.children.append(childPtr)
    
    def removeChild(self, value): # removes 1 child with specified value
        for i in range(len(self.children)):
            if (self.children[i].value == value):
                self.children.pop(i)
                return

def match(node, state):
    return True
    # TODO

"""
    transitions = dictionary (A) of dictionaries (B) referenced by state name
    inner dictionaries (B) are then referenced by some transitions
    the transitions are then tuples of input state, 
    type of transition and output states
"""
class TTreeAut:
    def __init__(self, rootStates, transitions):
        self.rootStates = rootStates
        self.transitions = transitions

    def makePrefix(self, prefixSelf):
        pass # TODO
    
    def makeSuffix(self, suffixSelf):
        pass # TODO

    def matchTree(self, someTreeRoot):
        for ptr in self.rootStates:
            if match(someTreeRoot, ptr) == True:
                return True
        return False

if __name__ == '__main__':
    main()
# End of file
