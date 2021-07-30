# formatDOT.py
# Functions for exporting tree automaton into DOT format (.dot) 
# for generating a graphical representation of the TA.
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *

def rootHandle(rootList:list, file):
    file.write("\tnode [ shape=point, width=0.001, height=0.001 ];\n")
    for root in rootList:
        file.write(f"\t\"start_{root}\"\n")
    file.write("\n\tnode [ shape=circle ];\n")
    for root in rootList:
        file.write(f"\t\"start_{root}\" -> \"{root}\";\n")
    file.write("\n")

def outputEdgeHandle(edge:list, file):
    if len(edge[2]) == 0:
        file.write(f"\tnode [ shape=point, width=0.001, height=0.001 ];\n")
        endName = f"end_{edge[0]}_{edge[1]}"
        file.write(f"\t\"{endName}\"\n")
        file.write(f"\t\"{edge[0]}\" -> \"{endName}\" [ label = \"{edge[1]}\" ] \n\n")
        return True
    return False

def edgeHandle(edge:list, file):
    if outputEdgeHandle(edge, file):
        return
    
    tempName = f"temp_{edge[0]}-{edge[1]}->[_"
    selfLoop = True 
    # if all children are the parent, then some adjustments have to be made
    for i in edge[2]:
        if i != edge[0]:
            selfLoop = False
        tempName += str(i) + "_"
    tempName += "]"

    if selfLoop:
        file.write(f"\t{{ rank = same; \"{edge[0]}\"; \"{tempName}\"; }};\n")   

    file.write(f"\t\"{tempName}\" [ shape=point, width=0.001, height=0.001 ];\n")
    file.write(f"\t\"{edge[0]}\" -> \"{tempName}\" [ arrowhead = None ]\n")
    for i in range(len(edge[2])):
        file.write(f"\t\"{tempName}\" -> \"{edge[2][i]}\" [ label = \"{edge[1][i]}\" ]\n")
    file.write(f"\n")

def exportTreeAutToDOT(ta:TTreeAut, fileName:str):
    file = open(fileName, "w")
    file.write("digraph G {\n")
    rootHandle(ta.rootStates, file)
    for edgesDict in ta.transitions.values():
        for edge in edgesDict.values():
            edgeHandle(edge, file)
    file.write("}\n")
    file.close()
    pass

def exportVTFToDOT(vtfFile:str, dotFile:str):
    
    pass

# End of file formatDOT.py
