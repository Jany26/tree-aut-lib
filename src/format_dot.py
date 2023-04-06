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


helpPoint = "shape=point, width=0.001, height=0.001"
smallPoint = "shape=point, width=0.05, height=0.05"
connEdge = "splines=true, overlap=false, penwidth=1.0, arrowhead=empty"
outEdge = "penwidth=2.0, arrowsize=0.5"
innerEdge = "penwidth=1.0, arrowsize=0.5, arrowhead=vee"


def rootHandle(rootList: list, file):
    file.write(f"\tnode [ label=\"\", {helpPoint} ];\n")
    for root in rootList:
        file.write(f"\t\"->{root}\"\n")
    file.write("\n\tnode [ shape=circle ];\n")
    for root in rootList:
        file.write(f"\t\"->{root}\" -> \"{root}\" [ {outEdge} ] ;\n")
    file.write("\n")


def outputEdgeHandle(edge: TTransition, file, debug=False):
    if len(edge.children) == 0:
        file.write(f"\tnode [ label=\"\", {helpPoint} ];\n")
        endName = f"{edge.src}-{edge.info.label}->"
        file.write(f"\t\"{endName}\"\n")
        file.write(f"\t\"{edge.src}\" -> \"{endName}\" [ {outEdge}, label = \"{edge.info.label}\" ] \n\n")
        return True
    return False


def allStatesHandle(ta: TTreeAut, file):
    stateList = ta.getStates()
    leaves = {state: None for state in ta.getOutputStates()}
    file.write("\tnode [ shape=circle, style=filled ];\n")

    for state in stateList:
        color = 'khaki' if state in leaves else 'bisque'
        file.write(f"\t\"{state}\" [fillcolor={color}];\n")
    file.write("\n")


def edgeHandle(edge: TTransition, file, debug=False):
    if debug:
        print(f"- - edgeHandle {edge} - -")
    # if outputEdgeHandle(edge, file, debug):
        # return

    # BUG: trying to make a nicer self-loop
    # (using same rank for the node and arbitrary node)
    # creates an unexpected error for Graphviz in some cases
    # - solution was to remove special treatment of self-loops

    tempName = f"{edge.src}-{edge.info.label}->"

    # case 1 : output edge
    if len(edge.children) == 0:
        file.write(f"\t\"{tempName}\" [ {helpPoint} ];\n")
        if debug:
            print(f"helpPOINT {tempName}")
        file.write(f"\t\"{edge.src}\" -> \"{tempName}\" [ label=<<B>[{edge.info.label}]</B>>, {outEdge} ]\n")
        if debug:
            print(f"[{edge.src}] -- {edge.info.label} --> [{tempName}]", "outEdge")
        return

    # case 2 : regular edge (connector node needed)
    for i in edge.children:
        tempName += str(i) + "_"
    tempName = tempName[:-1]

    # connector node
    file.write(f"\t\"{tempName}\" [ {smallPoint} ];\n")
    if debug:
        print(f"NODE {tempName}")

    connectorLabel = "\""
    if edge.info.variable != "":
        connectorLabel += f"[{edge.info.variable}] "
    connectorLabel += f"{edge.info.label}\""

    # edge: srcState -> connector node
    file.write(f"\t\"{edge.src}\" -> \"{tempName}\" [ label={connectorLabel}, {connEdge} ]\n")
    if debug:
        print(f"[{edge.src}] -> [{tempName}]", "connEdge")

    # edge: connector node -> children
    current_child = 0
    current_box = 0
    while current_child < len(edge.children):
        edgeLabel = f"\"{current_box}"
        hasBox = False
        if edge.info.boxArray != [] and edge.info.boxArray[current_box] is not None:
            hasBox = True
            edgeLabel += f": {edge.info.boxArray[current_box]}"
        edgeLabel += f"\""

        # box handling (mapping more child states to one edge (portArity can be > 1))
        if hasBox:
            boxName = edge.info.boxArray[current_box]
            arity = boxCatalogue[boxName].portArity
            if arity > 1:
                temp = f"{tempName}_{current_child}_{current_box}"

                file.write(f"\t\"{temp}\" [ {smallPoint} ];\n")
                if debug:
                    print(f"NODE {temp}")
                file.write(f"\t\"{tempName}\" -> \"{temp}\" [ label={edgeLabel}, {innerEdge} ]\n")
                if debug:
                    print(f"[{tempName}] -> [{temp}]")

                for j in range(arity):
                    file.write(f"\t\"{temp}\" -> \"{edge.children[current_child]}\" [ label=⊕{j}, {innerEdge} ]\n")
                    if debug:
                        print(f"[{temp}] -> [{edge.children[current_child]}]", f"curr_child = {current_child}")
                    current_child += 1
            else:
                file.write(f"\t\"{tempName}\" -> \"{edge.children[current_child]}\" [ label={edgeLabel}, {innerEdge} ]\n")
                if debug:
                    print(f"[{tempName}] -> [{edge.children[current_child]}]", f"curr_child = {current_child}")
                current_child += 1
        else:
            file.write(f"\t\"{tempName}\" -> \"{edge.children[current_child]}\" [ label={current_box}, {innerEdge} ]\n")
            if debug:
                print(f"[{tempName}] -> [{edge.children[current_child]}]", f"curr_child = {current_box}")
            current_child += 1

        current_box += 1

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def exportTreeAutToDOT(ta: TTreeAut, fileName: str):
    file = open(fileName, "w")
    file.write("digraph G {\n")
    allStatesHandle(ta, file)
    rootHandle(ta.rootStates, file)
    for edge in iterateEdges(ta):
        edgeHandle(edge, file, debug=False)
    file.write("}\n")
    file.close()
    pass

# End of file format_dot.py
