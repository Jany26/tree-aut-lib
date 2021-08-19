# jupyter.py
# Module for integration of TreeAutLib into Jupyter Notebook (IPython)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from graphviz import *

from ta_classes import *
from ta_lib import *

from format_dot import *
from format_tmb import *
from format_vtf import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREE AUTOMATA = GRAPHVIZ INTEGRATION WITH DOT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def DOTtransitionHandle(graph, edge):
    name = f"{edge[0]}-{edge[1].label}->"
    
    # case 1 : output edge
    if len(edge[2]) == 0:
        # NODE: arbitrary output point
        graph.node(name, 
            shape='point', 
            width='0.001', 
            height='0.001'
        )
        # EDGE: outputState -> arbitrary output point
        graph.edge(edge[0], name,
            penwidth    = '2.0', 
            arrowsize   = '0.5', 
            label       = f"<<B>[{edge[1].label}]</B>>"
        )
        return
    
    # case 2 : regular edge (connector node needed)
    for i in edge[2]:
        name += str(i)
    
    # NODE: middle/connector node
    graph.node(name, 
        label   = '',
        shape   = 'point', 
        width   = '0.05', 
        height  = '0.05'
    )

    # EDGE: srcState -> connector node
    graph.edge(edge[0], name, 
        label       = f"{edge[1].label}",
        splines     = 'true', 
        overlap     = 'false', 
        penwidth    = '1.0', 
        arrowhead   = 'empty'
    )

    # EDGE: connector node -> children
    for i in range(len(edge[2])):
        graph.edge(name, edge[2][i], 
            label       = f"{i}",
            penwidth    = '1.0', 
            arrowsize   = '0.5', 
            arrowhead   = 'vee' 
        )

def DOTstateHandle(graph, state, leaves, roots):
    # NODE: inner node (state of TA)
    graph.node(f"{state}", 
        shape       = 'circle', 
        style       = 'filled',
        fillcolor   = 'khaki' if state in leaves else 'bisque'
    )

    if state in roots:
        # NODE: arbitrary root point
        graph.node(f"->{state}", 
            label   = '', 
            shape   = 'point', 
            width   = '0.001', 
            height  = '0.001'
        )
        # EDGE: arbitrary root point -> root node
        graph.edge(f"->{state}", f"{state}", 
            label       = '',
            penwidth    = '2.0', 
            arrowsize   = '0.5'
        )        
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def convertToDOT(ta:TTreeAut) -> Digraph:
    dot = Digraph(comment=f"Tree Automaton {ta.name}")
    outputStates = ta.getOutputStates()

    for state in ta.getStates():
        DOTstateHandle(dot, state, outputStates, ta.rootStates)

    for edgeDict in ta.transitions.values():
        for edge in edgeDict.values():
            DOTtransitionHandle(dot, edge)

    return dot

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORT/EXPORT INTEGRATION WITH JUPYTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def importTA(source:str, fmtType:str, srcType:str = 'f') -> TTreeAut:
    if fmtType == 'vtf':
        return importTAfromVTF(source, srcType)
    elif fmtType == 'tmb':
        return importTAfromTMB(source, srcType)
    else:
        raise Exception(f"importTAfrom(): unsupported format '{fmtType}'")


# target can be either a filePath or a string variable, where 
def exportTA(ta: TTreeAut, fmtType:str, tgtType:str, filePath:str=""):
    if fmtType != 'vtf' and fmtType != 'tmb':
        raise Exception(f"exportTAto(): unsupported fmtType '{fmtType}'")
    if tgtType != 'f' and tgtType != 's':
        raise Exception(f"exportTAto(): unsupported tgtType '{tgtType}'")

    if tgtType == 'f':
        ta.name = "unnamed" if ta.name == "" else ta.name
        filePath = f"./{ta.name}.{fmtType}" if filePath == "" else filePath
    
    if fmtType == 'vtf':
        return exportTAtoVTF(ta, tgtType, filePath)
    else:
        return exportTAtoTMB(ta, tgtType, filePath)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREES = INTEGRATION WITH DOT/GRAPHVIZ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def createDOTfromTreeNode(root:TTreeNode) -> Digraph:
    pass

def createDOTfromTreeString(string:str) -> Digraph:
    pass

# G = nx.cycle_graph(4, create_using=nx.DiGraph())
# draw(G)

# End of file jupyter.py
