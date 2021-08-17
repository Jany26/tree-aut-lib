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

def DOTtransitionHandle(graph, edge):
    name = f"{edge[0]}-{edge[1].label}->"
    # handle output edge
    if len(edge[2]) == 0:
        graph.node(name, shape='point', width='0.001', height='0.001')
        graph.edge(edge[0], name,
            penwidth='2.0', arrowsize='0.5', label=f"{edge[1].label}")
        return
    
    # handle regular edge
    for i in edge[2]:
        name += str(i)
    
    graph.node(name, label='', shape='point', width='0.05', height='0.05')
    graph.edge(edge[0], name, 
        splines='true', overlap='false', penwidth='1.0', arrowhead='empty')
    for i in range(len(edge[2])):
        graph.edge(name, edge[2][i], 
            penwidth='1.0', arrowsize='0.5', arrowhead='vee', label=f"{edge[1].label}:{i}")
    


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def createDOTfromTA(ta:TTreeAut) -> Digraph:
    dot = Digraph(comment=f"Tree Automaton {ta.name}")

    for state in ta.getStates():
        dot.node(f"{state}", shape='circle')
        if state in ta.rootStates:
            dot.node(f"->{state}", label='', shape='point', width='0.001', height='0.001')
            dot.edge(f"->{state}", f"{state}", penwidth='2.0', arrowsize='0.5')

    for edgeDict in ta.transitions.values():
        for edge in edgeDict.values():
            DOTtransitionHandle(dot, edge)

    return dot

def createDOTfromFile(fileName:str):
    if fileName.endswith(".vtf"):
        ta = importTreeAutFromVTF(fileName)
        return createDOTfromTA(ta)
    elif fileName.endswith(".tmb"):
        ta = importTreeAutFromTMB(fileName)
        return createDOTfromTA(ta)
    else:
        Exception("unsupported format")

# G = nx.cycle_graph(4, create_using=nx.DiGraph())
# draw(G)

# End of file jupyter.py
