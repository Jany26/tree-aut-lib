
"""
[file] format_abdd.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Import/export operations into .abdd format.
[note] see comments for a description of the format of files in
../tests/abdd-format/*.dd
"""

from ta_classes import *
from copy import deepcopy
from test_data import box_catalogue
import re
from pathlib import Path

# @ABDD     # Automata-based reduction BDDs
# %Name example-abdd
# %Vars 100
# %Root 1
def abdd_preamble(ta: TTreeAut, file, name: str):
    file.write("@ABDD\n")
    file.write(f"# imported from {ta.name}\n")
    final_name = ta.name if name == "" else name
    file.write(f"%Name {final_name}\n")
    max_var = ta.get_var_order()[-1]
    file.write(f"%Vars {max_var[ta.meta_data.var_prefix:]}\n")
    file.write(f"%Root {ta.roots[0][ta.meta_data.state_prefix:]}\n\n")


# 1[0] (2, 3)[HPort] 3[X] # this denotes node id 1 with variable x0 going
# over L to nodes id 2, id 3 with applying the reduction rule HPort (box with arity 2)
# and over H to node id 3 applying reduction rule X (arity 1)
# 1[0] 2 3     # this denotes node id 1 with variable x0 going
# over L (low) to node id 2 and over H (high) to node id 3
# 2[4] <0> 3   # in this case the node has variable x4, L goes to leaf *0*, and H goes to 3
# 3[6] <1> <0> # L goes to leaf *1* and H goes to leaf *0*
def abdd_transition(ta: TTreeAut, edge: TTransition) -> str:
    def write_child(ta, child) -> str:
        state_str = f"{child}"
        if child in ta.get_output_states():
            state_str = "<" + ta.get_output_edges(inverse=True)[child][0] + ">"
        return state_str

    edge_string = ""
    if edge.src in ta.get_output_states():
        return ""
    var = edge.info.variable[ta.meta_data.var_prefix:]
    edge_string += f"{edge.src}[{var}] "
    arity = 1
    child_index = 0
    box_str = ""
    for box in edge.info.box_array:
        if box is not None and box != "_":
            arity = box_catalogue[f"{box}"].get_port_arity()
            box_str = f"[{box[3:]}]" if box.startswith("box") else box
        if arity == 1:
            edge_string += write_child(ta, edge.children[child_index])
        if arity > 1:
            edge_string += f"("
            for idx in range(len(edge.children[child_index:arity-1])):
                edge_string += write_child(ta, edge.children[idx + child_index])
                if idx < child_index + arity:
                    edge_string += ', '
            edge_string += ')'
        child_index += arity
        edge_string += box_str
        edge_string += ' '
    edge_string = edge_string[:-1]
    return edge_string


def export_treeaut_to_abdd(ta: TTreeAut, filepath: str, name="", comments=False):
    # variables are expected to have the same prefix
    # DAG as the input is assumed (output states with no transitions)
    # box_array is expected to contain only strings (box names)
    treeaut_copy = deepcopy(ta)
    treeaut_copy.reformat_keys()
    treeaut_copy.reformat_states(prefix='', start_from=1)
    treeaut_copy.meta_data.recompute()
    file = open(filepath, 'w')
    abdd_preamble(treeaut_copy, file, name)
    edge_str_max_len = 0
    for edge in iterate_edges(treeaut_copy):
        edge_len = len(abdd_transition(treeaut_copy, edge))
        if edge_str_max_len < edge_len:
            edge_str_max_len = edge_len
    for state in iterate_states_bfs(treeaut_copy):
        for edge in treeaut_copy.transitions[state].values():
            edge_str = abdd_transition(treeaut_copy, edge)
            file.write(edge_str)
            if comments:
                file.write((edge_str_max_len - len(edge_str)) * ' ')
                file.write(f" # {edge}")
            if comments or edge_str != "":
                file.write('\n')

def import_treeaut_from_abdd(source) -> TTreeAut | list:
    file = open(source, "r")
    name = Path(source).stem
    results = []
    positions = []
    i = 0
    for l in file:
        if l.startswith("@BDD") or l.startswith("@ABDD"):
            positions.append(i)
        i += len(l)
    for pos in positions:
        file.seek(pos)
        results.append(create_treeaut_from_abdd(file, name))
    if len(results) == 1:
        return results[0]
    return results


def create_treeaut_from_abdd(file, name) -> TTreeAut:
    ta = TTreeAut([], {}, name)
    leaves = set()
    key_counter = 0
    preamble = False
    for l in file:
        line = l.split('#')[0]  # strip comments
        line = line.strip()  # strip leading and trailing whitespaces
        if line == "":
            continue
        data = line.split()
        if line.startswith('@'):
            if line != "@ABDD" and line != "@BDD":
                raise Exception(f"import_treeaut_from_abdd(): unexpected header: {line}")
            if preamble:
                break
            else:
                preamble = True
                continue
        if line.startswith('%'):
            if data[0] not in ["%Name", "%Vars", "%Root"]:
                raise Exception(f"import_treeaut_from_abdd(): unexpected metadata: {data[0]}")
            if data[0] == "%Name":
                ta.name = data[1]
            if data[0] == "%Vars":
                max_var = int(data[1])
            if data[0] == "%Root":
                ta.roots.append(data[1])
            continue
        if line == "":
            continue
        src_regex = "(\d+)"
        var_regex = "\[(\d+|)\]"
        child_regex = "(\(\d+(?:\s*,\s*\d+)*\)|<\d+>|\d+)"
        box_regex = "(\[\w+\]|)"
        # "(\d+)\[(\d+)\]\s*(\(\d+(?:\s*,\s*\d+)*\)|<\d+>|\d+)(\[\w+\]|)\s*(\(\d+(?:\s*,\s*\d+)*\)|<\d+>|\d+)(\[\w+\]|)"
        full_regex = f"{src_regex}{var_regex}\s*{child_regex}{box_regex}\s*{child_regex}{box_regex}"
        groups = re.match(full_regex, line)
        src = groups.group(1)
        var = groups.group(2)
        tgt1 = groups.group(3)
        box1 = groups.group(4)
        tgt2 = groups.group(5)
        box2 = groups.group(6)
        box1 = box1.lstrip('[').rstrip(']')
        box2 = box2.lstrip('[').rstrip(']')
        box1 = None if box1 == "" else box1
        box2 = None if box2 == "" else box2
        children = []
        for j in [i.strip() for i in tgt1.lstrip('(').rstrip(')').split(',')]:
            children.append(j)
        for j in [i.strip() for i in tgt2.lstrip('(').rstrip(')').split(',')]:
            children.append(j)
        edge = TTransition(src, TEdge('LH', [box1, box2], var), children)
        if src not in ta.transitions:
            ta.transitions[src] = {}
        ta.transitions[src][f"k{key_counter}"] = edge
        key_counter += 1
        if src.startswith('<') and src.endswith('>'):
            leaves.add(src)
        for state in children:
            if state.startswith('<') and state.endswith('>'):
                leaves.add(state)
    for leaf in leaves:
        symbol = leaf.lstrip("<").rstrip(">")
        edge = TTransition(leaf, TEdge(symbol, [], f"{int(max_var)-1}"), [])
        ta.transitions[leaf] = {}
        ta.transitions[leaf][f"k{key_counter}"] = edge
        key_counter += 1

    return ta


# End of file format_abdd.py
