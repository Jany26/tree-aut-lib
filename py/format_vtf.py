"""
[file] format_vtf.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Import/Export into VATA format for tree automata/UBDA/ABDDs
used in this project.
[note] See VATA (documentation and source files for the format information and
where and how it was initially used. 'libVATA' is a C++ library for efficient
manipulation with non-deterministic finite (tree) automata.
[link] https://github.com/ondrik/libvata
"""
# format_vtf.py
# Functions for loading/saving tree automaton from/to VATA format (.vtf)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# import sys
# import os
from ta_functions import *
import re
import os
# from test_data import box_catalogue

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def load_roots_from_vtf(line: str) -> list:
    return [i for i in line.strip().split() if i != "%Root"]


def load_states_from_vtf(line: str) -> list:
    words = line.strip().split()
    return [i.split(":")[0].strip() for i in words if i != "%States"]


def load_arity_from_vtf(line: str) -> dict:
    words = line.strip().split()
    result = {}

    for i in words:
        if i.startswith("%Alphabet"):
            continue
        items = i.split(":")
        symbol = str(items[0].strip())
        arity = int(items[1].strip())
        result[symbol] = arity
    return result

# def load_transition_from_vtf(line:str, treeaut_type='ta') -> list:
#     line = line.strip()
#     if line == "":
#         return []
#     words = line.split()
#     state = words.pop(0)
#     symbol = words.pop(0)

#     children = []
#     for i in words[0:]:
#         temp = words.pop(0)
#         if i == "(": continue
#         if i == ")": break
#         children.append(str(temp))

#     boxes = []
#     if words != [] and words[0] == "[":
#         for i in words[0:]:
#             temp = words.pop(0)
#             if i == "[": continue
#             if i == "]": break
#             boxes.append(str(temp)) if i != "_" else boxes.append(None)

#     var = str(words.pop()) if words != [] else ""
#     # print([state, TEdge(symbol, boxes, var), children])
#     return [state, TEdge(symbol, boxes, var), children]


def process_edge(edge_info: list) -> Tuple[list, str]:
    if len(edge_info) == 0:
        return [], ""

    string = " ".join(edge_info)
    string = string.lstrip("<").lstrip().rstrip(">").rstrip()
    boxes_match = re.search("\[.*\]", string)

    boxes = []
    var_string = ""

    if boxes_match:
        match_string = boxes_match.group(0)
        box_array_string = match_string.lstrip("[").rstrip("]")
        var_string = string.replace(match_string, "")
        box_array = box_array_string.lstrip().rstrip().split()

        var_string = var_string.lstrip().rstrip()
        boxes = [str(box) if box != "_" else None for box in box_array]
    else:
        var_string = string

    return boxes, var_string


def load_transition_from_vtf(line: str, taType='ta') -> TTransition:
    line = line.strip()
    if line == "":
        return None
    words = line.split()
    state = words.pop(0)
    symbol = words.pop(0)

    edge_info = []
    for i in words[0:]:
        if i.startswith("("):
            break
        edge_info.append(i)
        words.pop(0)
    boxes, var = process_edge(edge_info)

    rest_of_string = " ".join(words[0:])
    # print(restOfString)
    rest_of_string = rest_of_string.rstrip().lstrip("(").rstrip(")")
    children = rest_of_string.split()
    # for i in words[0:]:
    #     temp = words.pop(0)
    #     if i == "(": continue
    #     if i == ")": break
    #     children.append(str(temp))

    return TTransition(state, TEdge(symbol, boxes, var), children)


def consistency_check(data: list, states: list, arity_dict: dict):
    if data.src not in states:
        raise Exception(f"consistency_check(): src state '{data.src}' not in preamble")
    if data.info.label not in arity_dict:
        raise Exception(f"consistency_check(): symbol '{data.info}' not in preamble")
    if len(data.children) != arity_dict[data.info.label]:
        raise Exception(f"consistency_check(): inconsistent arity for symbol '{data.info.label}'")
    for i in data.children:
        if i not in states:
            raise Exception(f"consistency_check(): child state '{i}' not in preamble")


# def check_children_arity(edge: TTransition, arity_dict: dict):
#     # NOTE: cannot be used - cyclical dependencies of initial box_catalogue imports
#     arity = arity_dict[edge.info.label]
#     box_port_count = 0
#     box_count = 0
#     for box in edge.info.box_array:
#         box_count += 1
#         box_port_count += box_catalogue[box].port_arity if box is not None else 1
#     if box_count != arity:
#         return False
#     if box_port_count != len(edge.children):
#         return False
#     return True


def consistency_check_vtf(edges, states, arities, verbose=False) -> bool:
    # print(states)
    for state_name, edge_dict in edges.items():

        if state_name not in states:
            if verbose:
                print(f"{state_name} not in states = {states}")
            return False

        for edge in edge_dict.values():
            if (
                edge.src not in states
                or edge.info.label not in arities
                or len(edge.children) != int(arities[edge.info.label])
                # or not check_children_arity(edge, arities)
            ):
                if verbose:
                    if edge.src not in states:
                        print(f"edge.src = {edge.src} not in states = [{states}]")
                    elif edge.info.label not in arities:
                        print(f"edge.info.label = {edge.info.label} not in arities = [{arities}]")
                    else:
                        print(f"children = {edge.children} inconsistent with arity of {edge.info.label} = {int(arities[edge.info.label])}")
                    print(f"EDGE = {edge}")
                return False
            for child in edge.children:
                if child not in states:
                    if verbose:
                        print(f"child {child} not in states = {states}")
                        print(f"EDGE = {edge}")
                    return False
    return True


def generate_key_from_edge(edge: list) -> str:
    children = ""
    for i in range(len(edge.children)):
        children += str(edge.children[i])
        if i < len(edge.children) - 1:
            children += ","
    # children.rstrip(",")
    return f"{edge.src}-{edge.info.label}-[{children}]"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VTF IMPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def import_treeaut_from_vtf(source, source_type='f', treeaut_type='ta') -> TTreeAut:
    if source_type == 'f':
        file = open(source, "r")
        treeaut_name = source.split(os.sep)[len(source.split(os.sep)) - 1][:-4]
    elif source_type == 's':
        file = source.split('\n')
        treeaut_name = "unnamed"
    else:
        Exception("import_treeaut_from_vtf(): unsupported source_type (only 'f'/'s')")

    arity_dict = {}
    roots = []
    transitions = {}
    all_states = []
    roots_done = False
    arity_done = False
    statelist_done = False

    for line in file:
        if line.startswith("#"):
            continue
        parts = line.split("#")
        line = parts[0]
        if line.startswith("@"):
            if not line.startswith("@NTA"):
                raise Exception(f"import_treeaut_from_vtf(): unexpected structure format {line}")
        elif line.startswith("%"):
            if line.startswith("%Root"):
                roots = load_roots_from_vtf(line)
                roots_done = True
            elif line.startswith("%Alphabet"):
                arity_dict = load_arity_from_vtf(line)
                arity_done = True
            elif line.startswith("%States"):
                all_states = load_states_from_vtf(line)
                statelist_done = True
            else:
                raise Exception(f"import_treeaut_from_vtf(): unexpected preamble '{line.strip()}'")
        else:
            edge = load_transition_from_vtf(line, treeaut_type)
            if edge is None:
                continue
            # checking state and arity consistency - comparing with data from "preamble"
            key = generate_key_from_edge(edge)
            if str(edge.src) not in transitions:
                transitions[str(edge.src)] = {}
            transitions[str(edge.src)][key] = edge
    if not roots_done:
        raise Exception(f"import_treeaut_from_vtf(): List of root states missing")
    if arity_done and statelist_done:
        if not consistency_check_vtf(transitions, all_states, arity_dict, verbose=True):
            raise Exception(f"import_treeaut_from_vtf(): inconsistent data with the preamble")

    if source_type == 'f':
        file.close()
    result = TTreeAut(roots, transitions, str(treeaut_name))
    result.port_arity = result.get_port_arity()
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF - HELPER FUNCTIONS (FILE)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def write_roots_vtf_file(roots, tgt):
    tgt.write("%Root")
    for root in roots:
        tgt.write(f" {root}")
    tgt.write("\n")


def write_states_vtf_file(states, tgt):
    tgt.write("%States")
    for i in states:
        tgt.write(f" {i}:0")
    tgt.write("\n")


def write_arities_vtf_file(arities, tgt):
    tgt.write("%Alphabet")
    for symbol in arities:
        tgt.write(f" {symbol}:{arities[symbol]}")
    tgt.write("\n\n")


def write_edges_vtf_file(edges, tgt):
    for edge in edges.values():
        for data in edge.values():
            box_array = []
            found_box = False
            for box in data.info.box_array:
                if box is None:
                    box_array.append("_")
                else:
                    found_box = True
                    if type(box) == str:
                        box_array.append(box)
                    else:
                        box_array.append(box.name)
            box_str = ""
            if found_box:
                box_str += "["
                for box in box_array:
                    box_str += box + " "
                box_str = box_str[:-1]
                box_str += "]"

            edge_str = ""
            if box_array != [] or data.info.variable != "":
                edge_str = f"<{box_str}"
                if box_str != "":
                    edge_str += " "
                edge_str += f"{data.info.variable}> "

            tgt.write(f"{data.src} {data.info.label} {edge_str}(")
            for child in data.children:
                tgt.write(f" {child}")
            tgt.write(" )\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF - HELPER FUNCTIONS (STRING)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def write_roots_vtf_str(roots):
    result = "%Root"
    for i in roots:
        result += f" {i}"
    result += "\n"
    return result


def write_states_vtf_str(states):
    result = "%States"
    for i in states:
        result += f" {i}:0"
    result += "\n"
    return result


def write_arities_vtf_str(arities):
    result = "%Alphabet"
    for symbol in arities:
        result += f" {symbol}:{arities[symbol]}"
    result += "\n\n"
    return result


def write_edges_vtf_str(edges):
    result = "# Transitions\n\n"
    for edge in edges.values():
        for data in edge.values():
            result += f"{data.src} {data.info.label} ("
            for i in data.children:
                result += f" {i}"
            result += " )\n"
    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def export_treeaut_to_vtf(ta: TTreeAut, filepath="", format='f'):
    if format != 'f' or format != 's':
        Exception("export_treeaut_to_vtf(): unsupported format")

    if format == 'f' and filepath == "":
        Exception("export_treeaut_to_vtf(): filepath needed")

    file = open(filepath, "w") if format == 'f' else ""

    if format == 'f':
        file.write("@NTA\n")
        file.write(f"# Automaton {ta.name}\n")
        write_roots_vtf_file(ta.roots, file)
        write_states_vtf_file(ta.get_states(), file)
        write_arities_vtf_file(ta.get_symbol_arity_dict(), file)
        write_edges_vtf_file(ta.transitions, file)
        file.close()
    else:
        file += "@NTA\n"
        file += f"# Automaton {ta.name}\n"
        file += write_roots_vtf_str(ta.roots)
        file += write_states_vtf_str(ta.get_states())
        file += write_arities_vtf_str(ta.get_symbol_arity_dict())
        file += write_edges_vtf_str(ta.transitions)
        return file
    return

# End of file format_vtf.py
