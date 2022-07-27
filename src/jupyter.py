# jupyter.py
# Module for integration of TreeAutLib into Jupyter Notebook (IPython)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from graphviz import *

from ta_classes import *
from ta_functions import *

from format_dot import *
from format_tmb import *
from format_vtf import *
from test_trees import *
from test_data import boxCatalogue

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORT/EXPORT INTEGRATION WITH JUPYTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def importTA(source: str, fmtType: str = "", srcType: str = 'f') -> TTreeAut:
    if fmtType == "" and srcType == 'f':
        if source.endswith(".vtf"):
            fmtType = 'vtf'
        elif source.endswith(".tmb"):
            fmtType = 'tmb'
        else:
            raise Exception(f"importTA(): unknown fmtType")

    if fmtType == 'vtf':
        return importTAfromVTF(source, srcType)
    elif fmtType == 'tmb':
        return importTAfromTMB(source, srcType)
    else:
        raise Exception(f"importTA(): unsupported format '{fmtType}'")


# target can be either a filePath or a string variable, where
def exportTA(ta: TTreeAut, fmtType: str, tgtType: str, filePath: str = ""):
    if fmtType != 'vtf' and fmtType != 'tmb':
        raise Exception(f"exportTA(): unsupported fmtType '{fmtType}'")
    if tgtType != 'f' and tgtType != 's':
        raise Exception(f"exportTA(): unsupported tgtType '{tgtType}'")

    if tgtType == 'f':
        ta.name = "unnamed" if ta.name == "" else ta.name
        filePath = f"./{ta.name}.{fmtType}" if filePath == "" else filePath

    if fmtType == 'vtf':
        return exportTAtoVTF(ta, tgtType, filePath)
    else:
        return exportTAtoTMB(ta, tgtType, filePath)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREE AUTOMATA = GRAPHVIZ INTEGRATION WITH DOT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def DOTtransitionHandle(graph, edge, key, verbose=False):
    if verbose:
        print("{:<60} {:<120}".format(
            f"KEY = {key}",
            f"EDGE = {edge}",
        ))
    name = f"{edge.src}-{edge.info.label}->"

    # case 1 : output edge
    if len(edge.children) == 0:
        # NODE: arbitrary output point
        graph.node(name,
                   shape='point',
                   width='0.001',
                   height='0.001'
                   )
        # EDGE: outputState -> arbitrary output point
        graph.edge(edge.src, name,
                   penwidth='2.0',
                   arrowsize='0.5',
                   label=f"<<B>[{edge.info.label}]</B>>")

        if verbose:
            print(" > arbitrary output point", name)
        if verbose:
            print(" > arbitrary output edge", edge.src, "->", name)
        return

    # case 2 : regular edge (connector node needed)
    for curr_child in edge.children:
        name += str(curr_child) + "==="
    name = name[:-3]

    # NODE: middle/connector node
    graph.node(name,
               label='',
               shape='point',
               width='0.05',
               height='0.05'
               )
    if verbose:
        print("middle/connector node", name)

    # EDGE: srcState -> connector node
    connectorLabel = ""
    if edge.info.variable != "":
        connectorLabel += f"[{edge.info.variable}] "
    connectorLabel += f"{edge.info.label}"

    graph.edge(edge.src, name,
               splines='true',
               overlap='false',
               penwidth='1.0',
               arrowhead='empty',
               label=connectorLabel
               )

    if verbose:
        print("connector edge", edge.src, "->", name)

    # EDGE: connector node -> children
    curr_child = 0
    curr_box = 0
    while curr_child < len(edge.children):
        edgeLabel = f"{curr_box}"
        hasBox = False
        if edge.info.boxArray != [] and edge.info.boxArray[curr_box] is not None:
            hasBox = True
            edgeLabel += f": {edge.info.boxArray[curr_box].name}"

        # box handling (mapping more children to one edge (portArity > 1))
        if hasBox:
            if type(edge.info.boxArray[curr_box]) == type(str):
                boxName = edge.info.boxArray[curr_box]
            else:
                boxName = edge.info.boxArray[curr_box].name
            arity = boxCatalogue[boxName].portArity
            if arity > 1:
                temp = f"{name}_{curr_child}_{curr_box}"

                graph.node(temp,
                           label='',
                           shape='point',
                           width='0.05',
                           height='0.05'
                           )
                graph.edge(name, temp,
                           penwidth='1.0',
                           arrowsize='0.5',
                           arrowhead='vee',
                           label=edgeLabel
                           )

                if verbose:
                    print(f" > > box handling node {temp}")
                if verbose:
                    print(f" > > box handling edge {name}->{temp} label={edgeLabel}")

                for j in range(arity):
                    graph.edge(temp, edge.children[curr_child],
                               label=f"⊕{j}",
                               penwidth='1.0',
                               arrowsize='0.5',
                               arrowhead='vee'
                               )

                    if verbose:
                        print(" > > > arity handling edge", temp, "->", edge.children[curr_child], f"label=port{j}")
                    curr_child += 1
            else:
                graph.edge(name, edge.children[curr_child],
                           label=edgeLabel,
                           penwidth='1.0',
                           arrowsize='0.5',
                           arrowhead='vee'
                           )
                if verbose:
                    print(" > > nobox handling edge", name, "->", edge.children[curr_child], f"label={edgeLabel}")
                curr_child += 1

        else:
            graph.edge(name, edge.children[curr_child],
                       label=f"{curr_box}",
                       penwidth='1.0',
                       arrowsize='0.5',
                       arrowhead='vee'
                       )
            if verbose:
                print(f" > normal edge {name} ->", {edge.children[curr_child]}, f"label={curr_box}")
            curr_child += 1
        curr_box += 1


def DOTstateHandle(graph, state, leaves, roots):
    # NODE: inner node (state of TA)
    graph.node(f"{state}",
               shape='circle',
               style='filled',
               fillcolor='khaki' if state in leaves else 'bisque'
               )

    if state in roots:
        # NODE: arbitrary root point
        graph.node(f"->{state}",
                   label='',
                   shape='point',
                   width='0.001',
                   height='0.001'
                   )
        # EDGE: arbitrary root point -> root node
        graph.edge(f"->{state}", f"{state}",
                   label='',
                   penwidth='2.0',
                   arrowsize='0.5'
                   )
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def convertToDOT(src, type='a', verbose=False) -> Digraph:
    if type == 'a':
        return TAtoDOT(src, verbose)
    elif type == 'n':
        return treeToDOT(src)
    elif type == 's':
        return treeToDOT(convertStringToTree(str(src)))


def TAtoDOT(ta: TTreeAut, verbose=False) -> Digraph:
    dot = Digraph(comment=f"Tree Automaton {ta.name}")
    outputStates = ta.getOutputStates()

    for state in ta.getStates():
        DOTstateHandle(dot, state, outputStates, ta.rootStates)

    for edgeDict in ta.transitions.values():
        for key, edge in edgeDict.items():
            DOTtransitionHandle(dot, edge, key, verbose)

    return dot

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREES = INTEGRATION WITH DOT/GRAPHVIZ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def drawChildren(graph: Digraph, root: TTreeNode, rootIdx: int) -> int:
    nodeIdx = rootIdx + 1
    for i in range(len(root.children)):
        currIdx = nodeIdx
        graph.node(str(currIdx),
                   label=f"{root.children[i].value}",
                   style='filled'
                   )
        nodeIdx = drawChildren(graph, root.children[i], nodeIdx)
        graph.edge(str(rootIdx), str(currIdx),
                   label=f"{i}",
                   penwidth='1.0',
                   arrowsize='0.5',
                   arrowhead='vee'
                   )
    return nodeIdx


def treeToDOT(root: TTreeNode) -> Digraph:
    dot = Digraph()

    if root is None:
        return dot
    # arbitrary root node (for extra arrow)
    dot.node(f"->{root.value}",
             label=f"->{root.value}",
             shape='point',
             width='0.001',
             height='0.001'
             )

    # the actual root node
    dot.node(str(0),
             label=f"{root.value}",
             style='filled'
             )

    dot.edge(f"->{root.value}", str(0),
             penwidth='1.0',
             arrowsize='0.5',
             arrowhead='vee'
             )
    drawChildren(dot, root, 0)
    return dot

# End of file jupyter.py
