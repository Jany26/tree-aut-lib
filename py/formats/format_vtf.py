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

from io import TextIOWrapper
import re
import os
from typing import Optional, Tuple

from tree_automata import TTransition, TEdge, TTreeAut

box_arities: dict[str, int] = {
    "X": 1,
    "L0": 1,
    "L1": 1,
    "H0": 1,
    "H1": 1,
    "LPort": 2,
    "HPort": 2,
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def load_roots_from_vtf(line: str) -> list[str]:
    return [i for i in line.strip().split() if i != "%Root"]


def load_states_from_vtf(line: str) -> list[str]:
    words: list[str] = line.strip().split()
    return [i.split(":")[0].strip() for i in words if i != "%States"]


def load_arity_from_vtf(line: str) -> dict[str, int]:
    words: list[str] = line.strip().split()
    result: dict[str, int] = {}

    for i in words:
        if i.startswith("%Alphabet"):
            continue
        items: list[str] = i.split(":")
        symbol: str = str(items[0].strip())
        arity: int = int(items[1].strip())
        result[symbol] = arity
    return result


def process_edge(edge_info: list[str]) -> Tuple[list[Optional[str]], str]:
    if len(edge_info) == 0:
        return [], ""

    string: str = " ".join(edge_info)
    string = string.lstrip("<").lstrip().rstrip(">").rstrip()
    boxes_match = re.search("\[.*\]", string)

    boxes: list[str] = []
    var_string: str = ""

    if boxes_match:  # is not None
        match_string: str = boxes_match.group(0)
        box_array_string: str = match_string.lstrip("[").rstrip("]")
        var_string: str = string.replace(match_string, "")
        box_array: list[str] = box_array_string.lstrip().rstrip().split()

        var_string: str = var_string.lstrip().rstrip()

        # we assume we either get no information about the box array (input is a tree automaton, or unfolded, etc...)
        # or we get complete box-array information - for ABDDs that means two box names like:
        # <[ 'low_edge_box_name' 'high_edge_box_name' ] 'var_name'>
        # examples:
        # <[ LPort X ] 1>
        # <[ _ X ] 1>
        # <x3>
        # <[X L0] x4>
        # <[ _ _ ] x8>
        boxes: list[Optional[str]] = [str(box) if box != "_" else None for box in box_array]
    else:
        var_string = string

    return boxes, var_string


def load_transition_from_vtf(line: str) -> Optional[TTransition]:
    line: str = line.strip()
    if line == "":
        return None
    words: list[str] = line.split()
    state: str = words.pop(0)
    symbol: str = words.pop(0)

    edge_info: list[str] = []
    for i in words[0:]:
        if i.startswith("("):
            break
        edge_info.append(i)
        words.pop(0)
    box_var_tuple: tuple[list[Optional[str]], str] = process_edge(edge_info)
    boxes, var = box_var_tuple

    rest_of_string: str = " ".join(words[0:])
    rest_of_string = rest_of_string.rstrip().lstrip("(").rstrip(")")
    children: list[str] = rest_of_string.split()

    if len(boxes) == 0 and symbol == "LH":
        boxes = [None] * 2

    return TTransition(state, TEdge(symbol, boxes, var), children)


def consistency_check(data: TTransition, states: list[str], arity_dict: dict[str, int]) -> None:
    if data.src not in states:
        raise Exception(f"consistency_check(): src state '{data.src}' not in preamble")
    if data.info.label not in arity_dict:
        raise Exception(f"consistency_check(): symbol '{data.info}' not in preamble")
    if len(data.children) != arity_dict[data.info.label]:
        raise Exception(f"consistency_check(): inconsistent arity for symbol '{data.info.label}'")
    for i in data.children:
        if i not in states:
            raise Exception(f"consistency_check(): child state '{i}' not in preamble")


def check_children_arity(edge: TTransition, arity_dict: dict[str, int]) -> bool:
    arity: int = arity_dict[edge.info.label]
    box_port_count: int = 0
    box_count: int = 0
    for box in edge.info.box_array:
        box_count += 1
        box_port_count += box_arities[box] if box is not None else 1
    if box_count != arity:
        return False
    if box_port_count != len(edge.children):
        return False
    return True


def consistency_check_vtf(edges: dict, states, arities, verbose=False) -> bool:
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
                        print(
                            f"children = {edge.children} inconsistent with arity of {edge.info.label} = {int(arities[edge.info.label])}"
                        )
                    print(f"EDGE = {edge}")
                return False
            for child in edge.children:
                if child not in states:
                    if verbose:
                        print(f"child {child} not in states = {states}")
                        print(f"EDGE = {edge}")
                    return False
    return True


def generate_key_from_edge(edge: TTransition) -> str:
    children: str = ""
    for i in range(len(edge.children)):
        children += str(edge.children[i])
        if i < len(edge.children) - 1:
            children += ","
    # children.rstrip(",")
    return f"{edge.src}-{edge.info.label}-[{children}]"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VTF IMPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def import_treeaut_from_vtf(source: str, source_type="f", treeaut_type="ta") -> TTreeAut:
    if source_type == "f":
        file: TextIOWrapper = open(source, "r")
        treeaut_name = source.split(os.sep)[len(source.split(os.sep)) - 1][:-4]
    elif source_type == "s":
        file: str = source.split("\n")
        treeaut_name = "unnamed"
    else:
        Exception("import_treeaut_from_vtf(): unsupported source_type (only 'f'/'s')")

    arity_dict: dict[str, int] = {}
    roots: list[str] = []
    transitions: dict[str, dict[str, TTransition]] = {}
    all_states: list[str] = []
    roots_done: bool = False
    arity_done: bool = False
    statelist_done: bool = False
    root_rule: Optional[str] = None

    for line in file:
        if line.startswith("#"):
            continue
        parts: list[str] = line.split("#")
        line: str = parts[0]
        if line.startswith("@"):
            name = line.strip()
            if name not in ["@NTA", "@ABDD", "@UBDA"]:
                raise Exception(f"import_treeaut_from_vtf(): unexpected structure format {line}")
        elif line.startswith("%"):
            if line.startswith("%Rootrule"):
                rule = line.split()[1]
                if rule not in box_arities:
                    raise Exception(f"import_treeaut_from_vtf(): unexpected root rule '{root_rule}'")
                root_rule = rule
            elif line.startswith("%Root"):
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
            edge: TTransition = load_transition_from_vtf(line)
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

    if source_type == "f":
        file.close()
    result = TTreeAut(roots, transitions, str(treeaut_name))
    result.port_arity = result.get_port_arity()
    result.rootbox = root_rule
    return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TO VTF - HELPER FUNCTIONS (FILE)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def write_roots_vtf_file(roots: list[str], tgt: TextIOWrapper) -> None:
    tgt.write("%Root")
    for root in roots:
        tgt.write(f" {root}")
    tgt.write("\n")


def write_states_vtf_file(states: list[str], tgt: TextIOWrapper) -> None:
    tgt.write("%States")
    for i in states:
        tgt.write(f" {i}:0")
    tgt.write("\n")


def write_arities_vtf_file(arities: dict[str, int], tgt: TextIOWrapper) -> None:
    tgt.write("%Alphabet")
    for symbol, arity in arities.items():
        tgt.write(f" {symbol}:{arity}")
    tgt.write("\n\n")


def write_edges_vtf_file(edges: dict[str, dict[str, TTransition]], tgt: TextIOWrapper) -> None:
    for edge in edges.values():
        for data in edge.values():
            box_array: list[str] = []
            found_box: bool = False
            for box in data.info.box_array:
                if box is None:
                    box_array.append("_")
                else:
                    found_box = True
                    if type(box) == str:
                        box_array.append(box)
                    else:
                        box_array.append(box.name)
            box_str: str = ""
            if found_box:
                box_str += "["
                for box in box_array:
                    box_str += box + " "
                box_str = box_str[:-1]
                box_str += "]"

            edge_str: str = ""
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


def write_roots_vtf_str(roots: list[str]) -> str:
    result: str = "%Root"
    for i in roots:
        result += f" {i}"
    result += "\n"
    return result


def write_states_vtf_str(states: list[str]) -> str:
    result: str = "%States"
    for i in states:
        result += f" {i}:0"
    result += "\n"
    return result


def write_arities_vtf_str(arities) -> str:
    result: str = "%Alphabet"
    for symbol in arities:
        result += f" {symbol}:{arities[symbol]}"
    result += "\n\n"
    return result


def write_edges_vtf_str(edges) -> str:
    result: str = "# Transitions\n\n"
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


def export_treeaut_to_vtf(ta: TTreeAut, filepath="", format="f"):
    if format != "f" or format != "s":
        Exception("export_treeaut_to_vtf(): unsupported format")

    if format == "f" and filepath == "":
        Exception("export_treeaut_to_vtf(): filepath needed")

    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file = open(filepath, "w") if format == "f" else ""

    if format == "f":
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
