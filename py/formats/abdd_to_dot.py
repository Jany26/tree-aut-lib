"""
[file] abdd_to_dot.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for exporting tree automaton into DOT format (.dot)
for generating a graphical representation of the TA. (IMAGE OUTPUT)
[note] see graphviz library for python documentation
[link] https://graphviz.readthedocs.io/en/stable/manual.html
"""

import os
from typing import Optional

import graphviz

from apply.abdd import ABDD
from apply.abdd_node import ABDDNode


box_labels = {
    "X": "X",
    "L0": "<L<sub>0</sub>>",
    "L1": "<L<sub>1</sub>>",
    "H0": "<H<sub>0</sub>>",
    "H1": "<H<sub>1</sub>>",
    "LPort": "<L<sub>⊕</sub>>",
    "HPort": "<H<sub>⊕</sub>>",
    None: "S",
}


def draw_abdd_node(
    graph: graphviz.Digraph, parent: ABDDNode, box: Optional[str], tgtlist: list[ABDDNode], cache: set[str], dir=False
) -> None:
    if tgtlist == []:
        return

    parentid = f"{parent.node}({parent.var})" if not parent.is_leaf else f"{parent.leaf_val}"
    if parentid in cache:
        return
    sourceid = parentid
    multiedge = False
    if len(tgtlist) > 1:
        # print(f'node {helperid} {type(helperid)}')
        multiedge = True
        helperid = f"{parentid}_{'H' if dir else 'L'}"
        graph.node(helperid, shape="point", width="0.001", height="0.001")
        # print(f'edge {parentid} -> {helperid} label={box} {[type(parentid), type(helperid), type(box)]}')
        graph.edge(
            parentid,
            helperid,
            label=box_labels[box],
            penwidth="1.0",
            arrowsize="0.5",
            arrowhead="none",
            style="solid" if dir else "dashed",
        )
        sourceid = helperid

    for i, tgt in enumerate(tgtlist):
        tgtname = f"{tgt.node}({tgt.var})" if not tgt.is_leaf else f"{tgt.leaf_val}"
        graph.node(
            tgtname,
            label=f"{tgt.var}" if not tgt.is_leaf else f"{tgt.leaf_val}",
            shape="box" if tgt.is_leaf else "circle",
            style="filled" if tgt.is_leaf else "solid",
        )

        edgelabel = f"{i}" if multiedge else box_labels[box]

        # print(sourceid, edgelabel, tgtname)
        # print(type(sourceid), type(edgelabel), type(tgtname))

        graph.edge(
            sourceid,
            tgtname,
            label=edgelabel,
            penwidth="1.0",
            arrowsize="0.5",
            arrowhead="vee",
            style="solid" if dir else "dashed",
        )
        draw_abdd_node(graph, tgt, tgt.low_box, tgt.low, cache, dir=False)
        draw_abdd_node(graph, tgt, tgt.high_box, tgt.high, cache, dir=True)
        cache.add(tgtname)

    return


def abdd_to_dot(abdd: ABDD) -> graphviz.Digraph:
    dot = graphviz.Digraph()
    # dot.attr(fontname="Helvetica")
    dot.graph_attr["fontname"] = "Helvetica"
    dot.node_attr["fontname"] = "Helvetica"
    dot.edge_attr["fontname"] = "Helvetica"
    dot.attr(label=f"ABDD - {abdd.name}")

    # dictionary: "node_name": set of nodes, to which there exists an edge
    # in the currently drawn BDD -> this is to avoid duplicate drawing
    cache: set[str] = set()

    n = abdd.root
    if n is None:
        return dot

    rootid = f"{n.node}({n.var})" if not n.is_leaf else f"{n.leaf_val}"
    helperid = f"->{rootid}"

    dot.node(helperid, shape="point", width="0.001", height="0.001")

    dot.node(
        rootid,
        label=f"{n.var}" if not n.is_leaf else n.leaf_val,
        shape="box" if n.is_leaf else "circle",
        style="filled" if n.is_leaf else "solid",
    )
    rootlabel = f"{abdd.root_rule}" if abdd.root_rule is not None else "S"
    dot.edge(helperid, rootid, label=rootlabel, penwidth="1.0", arrowsize="0.5", arrowhead="vee")

    draw_abdd_node(dot, n, n.low_box, n.low, cache, dir=False)
    draw_abdd_node(dot, n, n.high_box, n.high, cache, dir=True)
    cache.add(rootid)
    return dot


# End of file abdd_to_dot.py
