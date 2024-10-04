"""
[file] format_tmb.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Import/Export into TMB (Timbuk) format for tree automata.
[note] See TIMBUK documentation for the format information and where and how
it was initially used.
[link] https://people.irisa.fr/Thomas.Genet/timbuk/
"""

from io import TextIOWrapper
import os

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from formats.format_vtf import generate_key_from_edge

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB IMPORT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def replace_commas_in(line: str) -> str:
    """
    TODO: ...
    """
    stack: list[str] = []
    temp = ""
    for i in range(len(line)):
        if line[i] == "(":
            if len(stack) != 0:
                temp += "("
            stack.append("(")
        elif line[i] == ")":
            stack.pop()
            if len(stack) != 0:
                temp += ")"
        elif line[i] == "," and len(stack) == 1:
            temp += ";"
        else:
            temp += line[i]
    if len(stack) != 0:
        raise Exception("unbalanced parentheses")
    return temp


def load_symbol(line: str) -> tuple[str, str]:
    symbol: str = ""
    rest: str = ""
    for i in range(len(line)):
        if line[i] == "(":
            symbol = line[:i]
            rest = line[i:]
            break
    if symbol == "":
        symbol = line.strip()
        rest = ""
    return symbol, rest


def load_transition_from_tmb(line: str) -> TTransition:
    """
    TODO:
    """
    line: str = line.strip()
    transition_data: list[str] = line.split("->")
    src_state: str = transition_data[1].strip()
    rest: str = transition_data[0].strip()
    symbol, children_str = load_symbol(rest)
    child_states: str = replace_commas_in(children_str.strip())
    child_states: list[str] = child_states.split(";")
    children: list[str] = [state for state in child_states if state != ""]
    return TTransition(src_state, TEdge(symbol, [None] * len(children), ""), children)


def load_arity_from_tmb(line: str) -> dict[str, int]:
    words: list[str] = line.strip().split()

    result: dict[str, int] = {}
    for i in words[1:]:
        items: list[str] = i.split(":")
        symbol: str = str(items[0].strip())
        arity: int = int(items[1].strip())
        result[symbol] = arity
    return result


def consistency_check_tmb(edges: dict[str, dict[str, TTransition]], states: set[str], arities: dict[str, int]) -> bool:
    for state_name, edge_dict in edges.items():
        if state_name not in states:
            return False
        for edge in edge_dict.values():
            if (
                edge.src not in states
                or edge.info.label not in arities
                or len(edge.children) != arities[edge.info.label]
            ):
                return False
            for child in edge.children:
                if child not in states:
                    return False
    return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORT TA FROM TMB FILE/STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def import_treeaut_from_tmb(source: str, source_type="f") -> TTreeAut:
    if source_type == "f":
        input_stream = open(source, "r")
    elif source_type == "s":
        input_stream = source.split("\n")
    else:
        raise Exception(f"import_treeaut_from_tmb(): unsupported source type '{source_type}'")

    arity_dict: dict[str, int] = {}
    roots: list[str] = []
    transition_dict: dict[str, dict[str, TTransition]] = {}
    all_states: set[str] = set()
    roots_done: bool = False
    arity_done: bool = False
    statelist_done: bool = False
    transition_done: bool = False
    name: str = ""

    for line in input_stream:

        # skipping comments and empty lines
        line = line.strip()
        if line == "" or line.startswith("#") or line.startswith("//"):
            continue

        if transition_done and not line.startswith("\n"):
            edge = load_transition_from_tmb(line)
            if edge == []:
                continue
            # if arity_done and statelist_done:
            #     consistency_check_tmb(edge, all_states, arity_dict)
            key = generate_key_from_edge(edge)
            if str(edge.src) not in transition_dict:
                transition_dict[str(edge.src)] = {}
            transition_dict[str(edge.src)][key] = edge
            continue

        if line.startswith("Automaton"):
            name = line[len("Automaton") :].strip()
            continue
        elif line.startswith("Ops"):
            arity_dict = load_arity_from_tmb(line)
            arity_done = True
            # print(arity_dict)
        elif line.startswith("States"):
            words = line.strip().split()
            all_states = set([i.split(":")[0].strip() for i in words[1:]])
            statelist_done = True
            # print(all_states)
        elif line.startswith("Final States"):
            words = line.strip().split()
            roots = [str(i.strip()) for i in words[2:]]
            roots_done = True
            # print(roots)
        elif line.startswith("Transitions"):
            transition_done = True
        else:
            raise Exception(f"import_treeaut_from_tmb(): Unknown items in TMB file")
    # end for loop

    if arity_done and statelist_done:
        if not consistency_check_tmb(transition_dict, all_states, arity_dict):
            raise Exception(f"import_treeaut_from_tmb(): Inconsistent transition data with info in preamble")

    if not roots_done:
        print("exception M")
        raise Exception(f"List of root states missing")
    input_stream.close()
    return TTreeAut(roots, transition_dict, name)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB EXPORT - FILE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def write_arities_tmb_file(arities: dict[str, int], tgt: TextIOWrapper) -> None:
    tgt.write("Ops")
    for symbol, arity in arities.items():
        tgt.write(f" {symbol}:{arity}")
    tgt.write("\n\n")


def write_name_tmb_file(name: str, tgt: TextIOWrapper) -> None:
    tgt.write("Automaton ")
    tgt.write(f"{name}") if name != "" else tgt.write("unnamed")
    tgt.write("\n\n")


def write_states_tmb_file(states: list[str], tgt: TextIOWrapper) -> None:
    tgt.write("States")
    for i in states:
        tgt.write(f" {i}:0")
    tgt.write("\n\n")


def write_roots_tmb_file(states: list[str], tgt: TextIOWrapper) -> None:
    tgt.write("Final States")
    for i in states:
        tgt.write(f" {i}")
    tgt.write("\n\n")


def write_transitions_tmb_file(ta: TTreeAut, tgt: TextIOWrapper) -> None:
    tgt.write("Transitions\n")
    # for edge_dict in ta.transitions.values():
    #     for edge in edge_dict.values():
    for edge in iterate_edges(ta):
        tgt.write(f"{edge.info.label}(")
        arity = len(edge.children)
        for i in range(arity):
            tgt.write(f"{edge.children[i]}")
            tgt.write("," if i < arity - 1 else "")
        tgt.write(f") -> {edge.src}\n")
    tgt.write("\n\n")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TMB EXPORT - STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# def write_arities_tmb_str(arities):
#     result = "Ops"
#     for i in arities:
#         result += f" {i}:{arities[i]}"
#     result += "\n\n"
#     return result


# def write_name_tmb_str(name):
#     return "Automaton " + (f"{name}" if name != "" else "unnamed") + "\n\n"


# def write_states_tmb_str(states):
#     result = "States"
#     for i in states:
#         result += f" {i}:0"
#     result += "\n\n"
#     return result


# def write_roots_tmb_str(states):
#     result = "Final States"
#     for i in states:
#         result += f" {i}"
#     result += "\n\n"
#     return result


# def write_transitions_tmb_str(ta):
#     result = "Transitions\n"
#     # for edge_dict in ta.transitions.values():
#     #     for edge in edge_dict.values():
#     for edge in iterate_edges(ta):
#         temp = f"{edge.info.label}("
#         for i in range(len(edge.children)):
#             temp += f"{edge.children[i]}"
#             temp += ", " if (i < len(edge.children) - 1) else ""
#         temp += f") -> {edge.src}\n"
#         result += temp
#     result += "\n\n"
#     return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# EXPORT TA TO TMB FILE/STRING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def export_treeaut_to_tmb(ta: TTreeAut, filepath: str):
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    result = open(filepath, "w")
    write_arities_tmb_file(ta.get_symbol_arity_dict(), result)
    write_name_tmb_file(ta.name, result)
    write_states_tmb_file(ta.get_states(), result)
    write_roots_tmb_file(ta.roots, result)
    write_transitions_tmb_file(ta, result)
    result.close()


# End of file format_tmb.py
