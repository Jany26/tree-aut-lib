"""
[file] format_dot.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for exporting tree automaton into DOT format (.dot)
for generating a graphical representation of the TA. (TEXT OUTPUT)
[note] see graphviz documentation for DOT format specification.
[link] https://graphviz.org/
"""

from ta_functions import *
from test_data import box_catalogue

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DOT FORMAT IMPORT/EXPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


help_point = "shape=point, width=0.001, height=0.001"
small_point = "shape=point, width=0.05, height=0.05"
connector_edge = "splines=true, overlap=false, penwidth=1.0, arrowhead=empty"
output_edge = "penwidth=2.0, arrowsize=0.5"
inner_edge = "penwidth=1.0, arrowsize=0.5, arrowhead=vee"


def root_handle(roots: list, file):
    file.write(f'\tnode [ label="", {help_point} ];\n')
    for root in roots:
        file.write(f'\t"->{root}"\n')
    file.write("\n\tnode [ shape=circle ];\n")
    for root in roots:
        file.write(f'\t"->{root}" -> "{root}" [ {output_edge} ] ;\n')
    file.write("\n")


def output_edge_handle(edge: TTransition, file, debug=False):
    if len(edge.children) == 0:
        file.write(f'\tnode [ label="", {help_point} ];\n')
        end_name = f"{edge.src}-{edge.info.label}->"
        file.write(f'\t"{end_name}"\n')
        file.write(f'\t"{edge.src}" -> "{end_name}" [ {output_edge}, label = "{edge.info.label}" ] \n\n')
        return True
    return False


def all_states_handle(ta: TTreeAut, file):
    states = ta.get_states()
    leaves = {s: None for s in ta.get_output_states()}
    file.write("\tnode [ shape=circle, style=filled ];\n")

    for s in states:
        color = "khaki" if s in leaves else "bisque"
        file.write(f'\t"{s}" [fillcolor={color}];\n')
    file.write("\n")


def edge_handle(edge: TTransition, file, debug=False):
    if debug:
        print(f"- - edge_handle {edge} - -")
    # if output_edge_handle(edge, file, debug):
    # return

    # BUG: trying to make a nicer self-loop
    # (using same rank for the node and arbitrary node)
    # creates an unexpected error for Graphviz in some cases
    # - solution was to remove special treatment of self-loops

    connector_node = f"{edge.src}-{edge.info.label}->"

    # case 1 : output edge
    if len(edge.children) == 0:
        file.write(f'\t"{connector_node}" [ {help_point} ];\n')
        if debug:
            print(f"connector_node {connector_node}")
        file.write(f'\t"{edge.src}" -> "{connector_node}" [ label=<<B>[{edge.info.label}]</B>>, {output_edge} ]\n')
        if debug:
            print(f"[{edge.src}] -- {edge.info.label} --> [{connector_node}]", "output_edge")
        return

    # case 2 : regular edge (connector node needed)
    for i in edge.children:
        connector_node += str(i) + "_"
    connector_node = connector_node[:-1]

    # connector node
    file.write(f'\t"{connector_node}" [ {small_point} ];\n')
    if debug:
        print(f"NODE {connector_node}")

    connector_label = '"'
    if edge.info.variable != "":
        connector_label += f"[{edge.info.variable}] "
    connector_label += f'{edge.info.label}"'

    # edge: src_state -> connector node
    file.write(f'\t"{edge.src}" -> "{connector_node}" [ label={connector_label}, {connector_edge} ]\n')
    if debug:
        print(f"[{edge.src}] -> [{connector_node}]", "connector_edge")

    # edge: connector node -> children
    current_child = 0
    current_box = 0
    while current_child < len(edge.children):
        edge_label = f'"{current_box}'
        has_box = False
        if edge.info.box_array != [] and edge.info.box_array[current_box] is not None:
            has_box = True
            edge_label += f": {edge.info.box_array[current_box]}"
        edge_label += f'"'

        # box handling (mapping more child states to one edge (port_arity can be > 1))
        if has_box:
            box_name = edge.info.box_array[current_box]
            arity = box_catalogue[box_name].port_arity
            if arity > 1:
                temp = f"{connector_node}_{current_child}_{current_box}"

                file.write(f'\t"{temp}" [ {small_point} ];\n')
                if debug:
                    print(f"NODE {temp}")
                file.write(f'\t"{connector_node}" -> "{temp}" [ label={edge_label}, {inner_edge} ]\n')
                if debug:
                    print(f"[{connector_node}] -> [{temp}]")

                for j in range(arity):
                    file.write(f'\t"{temp}" -> "{edge.children[current_child]}" [ label=⊕{j}, {inner_edge} ]\n')
                    if debug:
                        print(f"[{temp}] -> [{edge.children[current_child]}]", f"curr_child = {current_child}")
                    current_child += 1
            else:
                file.write(
                    f'\t"{connector_node}" -> "{edge.children[current_child]}" [ label={edge_label}, {inner_edge} ]\n'
                )
                if debug:
                    print(f"[{connector_node}] -> [{edge.children[current_child]}]", f"curr_child = {current_child}")
                current_child += 1
        else:
            file.write(
                f'\t"{connector_node}" -> "{edge.children[current_child]}" [ label={current_box}, {inner_edge} ]\n'
            )
            if debug:
                print(f"[{connector_node}] -> [{edge.children[current_child]}]", f"curr_child = {current_box}")
            current_child += 1

        current_box += 1


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def export_treeaut_to_dot(ta: TTreeAut, filepath: str):
    file = open(filepath, "w")
    file.write("digraph G {\n")
    all_states_handle(ta, file)
    root_handle(ta.roots, file)
    for edge in iterate_edges(ta):
        edge_handle(edge, file, debug=False)
    file.write("}\n")
    file.close()
    pass


# End of file format_dot.py
