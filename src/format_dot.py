# format_dot.py
# Functions for exporting tree automaton into DOT format (.dot) 
# for generating a graphical representation of the TA.
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_functions import *
from test_data import boxCatalogue

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DOT FORMAT IMPORT/EXPORT
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
        endName = f"{edge[0]}-{edge[1].label}->"
        file.write(f"\t\"{endName}\"\n")
        file.write(f"\t\"{edge[0]}\" -> \"{endName}\" [ penwidth=2.0, arrowsize=0.5, label = \"{edge[1].label}\" ] \n\n")
        return True
    return False

def allStatesHandle(stateList, file):
    file.write("\tnode [ shape = circle ];\n")
    for i in stateList:
        file.write(f"\t\"{i}\"\n")
    file.write("\n")

def edgeHandle(edge:list, file):
    # if outputEdgeHandle(edge, file):
    #     return

    # BUG: trying to make a nicer self-loop 
    # (using same rank for the node and arbitrary node) 
    # creates an unexpected error for Graphviz in some cases 
    # - solution was to remove special treatment of self-loops

    tempName = f"{edge[0]}-{edge[1].label}->"

    # case 1 : output edge
    if len(edge[2]) == 0:
        file.write(f"\t\"{tempName}\" [ shape=point, width=0.001, height=0.001 ];\n")
        file.write(f"\t\"{edge[0]}\" -> \"{tempName}\" [ label=<<B>[{edge[1].label}]</B>>, penwidth=2.0, arrowsize=0.5 ]\n")
        return

    # case 2 : regular edge (connector node needed)
    for i in edge[2]:
        tempName += str(i) + "_"
    tempName = tempName[:-1]

    # connector node
    file.write(f"\t\"{tempName}\" [ shape=point, width=0.05, height=0.05 ];\n")
    
    connectorLabel = "\""
    if edge[1].variable != "":
        connectorLabel += f"[{edge[1].variable}] "
    connectorLabel += f"{edge[1].label}\""
    
    # edge: srcState -> connector node
    file.write(f"\t\"{edge[0]}\" -> \"{tempName}\" [ label={connectorLabel}, splines=true, overlap=false, penwidth=1.0, arrowhead=empty ]\n")
    
    # edge: connector node -> children
    current_child = 0
    current_box = 0
    while current_child < len(edge[2]):
        edgeLabel = f"\"{current_box}"
        hasBox = False;
        if edge[1].boxArray != [] and edge[1].boxArray[current_box] is not None:
            hasBox = True;
            edgeLabel += f": {edge[1].boxArray[current_box]}"
        edgeLabel += f"\""

        # box handling (mapping more child states to one edge (portArity can be > 1))
        if hasBox:
            boxName = edge[1].boxArray[current_box]
            arity = boxCatalogue[boxName].portArity
            if arity > 1:
                temp = f"{tempName}_{current_child}_{current_box}"
                
                file.write(f"\t\"{temp}\" [ shape=point, width=0.05, height=0.05 ];\n")
                file.write(f"\t\"{tempName}\" -> \"{temp}\" [ label={edgeLabel}, penwidth=1.0, arrowsize=0.5, arrowhead=vee ]\n")
                
                for j in range(arity):
                    file.write(f"\t\"{temp}\" -> \"{edge[2][current_child]}\" [ label=⊕{j}, penwidth=1.0, arrowsize=0.5, arrowhead=vee ]\n")
                    current_child += 1
            else:
                file.write(f"\t\"{tempName}\" -> \"{edge[2][current_child]}\" [ label={edgeLabel}, penwidth=1.0, arrowsize=0.5, arrowhead=vee ]\n")
                current_child += 1
            current_box += 1

        else:
            file.write(f"\t\"{tempName}\" -> \"{edge[2][current_child]}\" [ label={current_child}, penwidth=1.0, arrowsize=0.5, arrowhead=vee ]\n")
            current_child += 1

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

# End of file format_dot.py
