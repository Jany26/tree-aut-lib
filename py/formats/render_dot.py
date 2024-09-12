"""
[file] render_dot.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for exporting tree automaton into DOT format (.dot)
for generating a graphical representation of the TA. (IMAGE OUTPUT)
[note] see graphviz library for python documentation
[link] https://graphviz.readthedocs.io/en/stable/manual.html
"""

import graphviz

from tree_automata import TTreeAut, TTransition, TTreeNode
from tree_automata.tree_node import convert_string_to_tree
from bdd.bdd_class import BDD
from bdd.bdd_node import BDDnode

from formats.format_vtf import import_treeaut_from_vtf, export_treeaut_to_vtf
from formats.format_tmb import import_treeaut_from_tmb, export_treeaut_to_tmb

from utils import box_catalogue


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORT/EXPORT INTEGRATION WITH JUPYTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def import_treeaut(source: str, format_type: str = "", source_type: str = "f") -> TTreeAut:
    if format_type == "" and source_type == "f":
        if source.endswith(".vtf"):
            format_type = "vtf"
        elif source.endswith(".tmb"):
            format_type = "tmb"
        else:
            raise Exception(f"import_treeaut(): unknown format_type")

    if format_type == "vtf":
        return import_treeaut_from_vtf(source, source_type)
    elif format_type == "tmb":
        return import_treeaut_from_tmb(source, source_type)
    else:
        raise Exception(f"import_treeaut(): unsupported format '{format_type}'")


# target can be either a filepath or a string variable, where
def export_treeaut(ta: TTreeAut, format_type: str, target_type: str, filepath: str = ""):
    if format_type != "vtf" and format_type != "tmb":
        raise Exception(f"export_treeaut(): unsupported format_type '{format_type}'")
    if target_type != "f" and target_type != "s":
        raise Exception(f"export_treeaut(): unsupported target_type '{target_type}'")

    if target_type == "f":
        ta.name = "unnamed" if ta.name == "" else ta.name
        filepath = f"./{ta.name}.{format_type}" if filepath == "" else filepath

    if format_type == "vtf":
        return export_treeaut_to_vtf(ta, target_type, filepath)
    else:
        return export_treeaut_to_tmb(ta, target_type, filepath)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREE AUTOMATA = GRAPHVIZ INTEGRATION WITH DOT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def dot_transition_handle(graph, edge: TTransition, key: str, verbose=False):
    use_low_high = False
    if verbose:
        print(
            "{:<60} {:<120}".format(
                f"KEY = {key}",
                f"EDGE = {edge}",
            )
        )
    name = f"{edge.src}-{edge.info.label}->"

    # case 1 : output edge
    if len(edge.children) == 0:
        # NODE: arbitrary output point
        graph.node(name, shape="point", width="0.001", height="0.001")
        # EDGE: output_state -> arbitrary output point
        output_edge_label = edge.info.label
        if edge.info.label.startswith("Port_"):
            output_edge_label = f"⊕{edge.info.label[5:]}"
        var = f"[{edge.info.variable}]" if edge.info.variable != "" else ""
        graph.edge(edge.src, name, penwidth="2.0", arrowsize="0.5", label=f"<<B>{var} {output_edge_label}</B>>")

        if verbose:
            print(" > arbitrary output point", name)
        if verbose:
            print(" > arbitrary output edge", edge.src, "->", name)
        return

    # case 2 : regular edge (connector node needed)
    for current_child in edge.children:
        name += str(current_child) + ","
    name = name[:-1]

    # NODE: middle/connector node
    graph.node(name, label="", shape="point", width="0.05", height="0.05")
    if verbose:
        print("middle/connector node", name)

    # EDGE: src_state -> connector node
    connector_label = ""
    if edge.info.variable != "":
        connector_label += f"[{edge.info.variable}]"
    if use_low_high:
        if edge.info.label != "LH":
            connector_label += f" {edge.info.label}"
    else:
        connector_label += f" {edge.info.label}"

    graph.edge(
        edge.src, name, splines="true", overlap="false", penwidth="1.0", arrowhead="empty", label=connector_label
    )

    if verbose:
        print("connector edge", edge.src, "->", name)

    # EDGE: connector node -> children
    current_child = 0
    current_box = 0
    while current_child < len(edge.children):
        if edge.info.label == "LH" and use_low_high:
            edge_label = "L" if current_box == 0 else "H"
        else:
            # dead code - other non-nullar symbols other than LH are not used
            edge_label = f"{current_box}"
        has_box = False
        if edge.info.box_array != [] and edge.info.box_array[current_box] is not None:
            has_box = True
            if type(edge.info.box_array[current_box]) == str:
                box_name = box_catalogue[edge.info.box_array[current_box]].name
            else:
                box_name = edge.info.box_array[current_box].name
            if box_name.startswith("box"):
                box_name = box_name[len("box") :]
            if box_name.endswith("Port"):
                box_name = box_name[:-4]
                box_name += "⊕"
            edge_label += f": {box_name}"

        # box handling (mapping more children to one edge (port_arity > 1))
        if has_box:
            if type(edge.info.box_array[current_box]) == str:
                box_name = edge.info.box_array[current_box]
            else:
                box_name = edge.info.box_array[current_box].name
            arity = box_catalogue[box_name].port_arity
            if arity > 1:
                temp = f"{name}_{current_child}_{current_box}"

                graph.node(temp, label="", shape="point", width="0.05", height="0.05")
                graph.edge(name, temp, penwidth="1.0", arrowsize="0.5", arrowhead="vee", label=edge_label)

                if verbose:
                    print(f" > > box handling node {temp}")
                    print(f" > > box handling edge {name}->{temp}", end="")
                    print(f", label={edge_label}")

                for j in range(arity):
                    graph.edge(
                        temp,
                        edge.children[current_child],
                        label=f"⊕{j}",
                        penwidth="1.0",
                        arrowsize="0.5",
                        arrowhead="vee",
                    )

                    if verbose:
                        print(" > > > arity handling edge", temp, "->", edge.children[current_child], f"label=port{j}")
                    current_child += 1
            else:
                graph.edge(
                    name,
                    edge.children[current_child],
                    label=edge_label,
                    penwidth="1.0",
                    arrowsize="0.5",
                    arrowhead="vee",
                )
                if verbose:
                    print(" > > nobox handling edge", name, "->", edge.children[current_child], f"label={edge_label}")
                current_child += 1

        else:
            graph.edge(
                name,
                edge.children[current_child],
                label=f"{edge_label}",
                penwidth="1.0",
                arrowsize="0.5",
                arrowhead="vee",
            )
            if verbose:
                print(f" > normal edge {name} ->", {edge.children[current_child]}, f"label={current_box}")
            current_child += 1
        current_box += 1


def dot_state_handle(graph, state, leaves, roots):
    # NODE: inner node (state of TA)
    graph.node(f"{state}", shape="circle", style="filled", fillcolor="khaki" if state in leaves else "bisque")

    if state in roots:
        # NODE: arbitrary root point
        graph.node(f"->{state}", label="", shape="point", width="0.001", height="0.001")
        # EDGE: arbitrary root point -> root node
        graph.edge(f"->{state}", f"{state}", label="", penwidth="2.0", arrowsize="0.5")
    return


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def convert_to_dot(src, source_type="a", verbose=False, caption=False) -> graphviz.Digraph:
    if type(src) is TTreeAut:
        return treeaut_to_dot(src, verbose, caption)
    elif type(src) is TTreeNode:
        return tree_to_dot(src)
    elif type(src) is str:
        return tree_to_dot(convert_string_to_tree(str(src)))
    elif type(src) is BDD:
        return bdd_to_dot(src)


def treeaut_to_dot(ta: TTreeAut, verbose=False, caption=False) -> graphviz.Digraph:
    dot = graphviz.Digraph(comment=f"Tree Automaton {ta.name}")
    if caption:
        dot.attr(label=f"{ta.name}")
    output_states = ta.get_output_states()

    for state in ta.get_states():
        dot_state_handle(dot, state, output_states, ta.roots)

    for edge_dict in ta.transitions.values():
        for key, edge in edge_dict.items():
            dot_transition_handle(dot, edge, key, verbose)

    return dot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREES = INTEGRATION WITH DOT/GRAPHVIZ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def draw_children(graph: graphviz.Digraph, root: TTreeNode, root_idx: int) -> int:
    node_idx = root_idx + 1
    for i in range(len(root.children)):
        current_idx = node_idx
        graph.node(str(current_idx), label=f"{root.children[i].value}", style="filled")
        node_idx = draw_children(graph, root.children[i], node_idx)
        graph.edge(str(root_idx), str(current_idx), label=f"{i}", penwidth="1.0", arrowsize="0.5", arrowhead="vee")
    return node_idx


def tree_to_dot(root: TTreeNode) -> graphviz.Digraph:
    dot = graphviz.Digraph()

    if root is None:
        return dot
    # arbitrary root node (for extra arrow)
    dot.node(f"->{root.value}", label=f"->{root.value}", shape="point", width="0.001", height="0.001")

    # the actual root node
    dot.node(str(0), label=f"{root.value}", style="filled")

    dot.edge(f"->{root.value}", str(0), penwidth="1.0", arrowsize="0.5", arrowhead="vee")
    draw_children(dot, root, 0)
    return dot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TREES = INTEGRATION WITH DOT/GRAPHVIZ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def draw_bdd_node(graph: graphviz.Graph, node: BDDnode, parent: BDDnode, cache: set, low=False):
    if node is None:
        return

    if node.name not in cache:
        graph.node(
            node.name,
            label=f"{node.value}",
            shape="box" if node.is_leaf() else "circle",
            style="filled" if node.is_leaf() else "solid",
        )
        cache.add(node.name)

    if f"{parent.name}->{node.name}" not in cache:
        graph.edge(
            parent.name,
            node.name,
            penwidth="1.0",
            arrowsize="0.5",
            arrowhead="vee",
            style="dotted" if low is True else "solid",
        )
        cache.add(f"{parent.name}->{node.name}")

    draw_bdd_node(graph, node.low, node, cache, low=True)
    draw_bdd_node(graph, node.high, node, cache, low=False)
    return


def bdd_to_dot(bdd: BDD) -> graphviz.Graph:
    dot = graphviz.Digraph()
    dot.attr(label=f"BDD - {bdd.name}")

    # dictionary: "node_name": set of nodes, to which there exists an edge
    # in the currently drawn BDD -> this is to avoid duplicate drawing
    cache: set = set()

    if bdd.root is None:
        return dot

    dot.node(f"->{bdd.root.name}", shape="point", width="0.001", height="0.001")

    dot.node(
        bdd.root.name,
        label=f"{bdd.root.value}",
        shape="box" if bdd.root.is_leaf() else "circle",
        style="filled" if bdd.root.is_leaf() else "solid",
    )
    dot.edge(f"->{bdd.root.name}", bdd.root.name, penwidth="1.0", arrowsize="0.5", arrowhead="vee")

    cache.add(bdd.root.name)
    draw_bdd_node(dot, bdd.root.low, bdd.root, cache, low=True)
    draw_bdd_node(dot, bdd.root.high, bdd.root, cache, low=False)
    return dot


def export_to_file(obj: object, path: str, format="png", caption=True):
    dot = convert_to_dot(obj, caption=caption)
    dot.render(path, format=format, cleanup=True)


# End of file render_dot.py
