# format_dot.py
# Functions for exporting tree automaton into DOT format (.dot) 
# for generating a graphical representation of the TA.
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_lib import *
from format_vtf import importTreeAutFromVTF

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def rootHandle(rootList:list, file):
    file.write("\tnode [ label=\"\", shape=point, width=0.001, height=0.001 ];\n")
    for root in rootList:
        file.write(f"\t\"->{root}\"\n")
    file.write("\n\tnode [ shape=circle ];\n")
    for root in rootList:
        file.write(f"\t\"->{root}\" -> \"{root}\" [ penwidth=2.0, arrowsize=0.5 ] ;\n")
    file.write("\n")

def outputEdgeHandle(edge:list, file):
    if len(edge[2]) == 0:
        file.write(f"\tnode [ label=\"\", shape=point, width=0.001, height=0.001 ];\n")
        endName = f"{edge[0]}-{edge[1]}->"
        file.write(f"\t\"{endName}\"\n")
        file.write(f"\t\"{edge[0]}\" -> \"{endName}\" [ penwidth=2.0, arrowsize=0.5, label = \"{edge[1]}\" ] \n\n")
        return True
    return False

def allStatesHandle(stateList, file):
    file.write("\tnode [ shape = circle ];\n")
    for i in stateList:
        file.write(f"\t\"{i}\"\n")
    file.write("\n")

def edgeHandle(edge:list, file):
    if outputEdgeHandle(edge, file):
        return

    # BUG: making a nicer self-loops creates an unexpected error for Graphviz
    # in some cases - solution was to remove special treatment of self-loops
    tempName = f"{edge[0]}-{edge[1]}->"
    for i in edge[2]:
        tempName += str(i)

    file.write(f"\t\"{tempName}\" [ label=\"\", shape=point, width=0.05, height=0.05 ];\n")
    file.write(f"\t\"{edge[0]}\" -> \"{tempName}\" [ penwidth=1.0, arrowhead = None ]\n")
    for i in range(len(edge[2])):
        file.write(f"\t\"{tempName}\" -> \"{edge[2][i]}\" [ penwidth=1.0, arrowsize=0.5, label = \"{edge[1][i]}\" ]\n")
    file.write(f"\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def exportTreeAutToDOT(ta:TTreeAut, fileName:str):
    file = open(fileName, "w")
    file.write("digraph G {\n")
    allStatesHandle(ta.getStates(), file)
    rootHandle(ta.rootStates, file)
    for edgesDict in ta.transitions.values():
        for edge in edgesDict.values():
            edgeHandle(edge, file)
    file.write("}\n")
    file.close()
    pass

# Unnecessary most probably
## Explicitly reads all data from VATA format and creates a DOT format from it.
# -- could be easily done thru importTreeAutFromVTF() and exportTreeAutToDOT()
# This is a more optimized version though.
def exportVTFToDOT(fileNameVTF:str, fileNameDOT:str):
    temp = importTreeAutFromVTF(fileNameVTF)
    exportTreeAutToDOT(temp, fileNameDOT)
    pass

# End of file format_dot.py
