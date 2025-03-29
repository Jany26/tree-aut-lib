import re

from typing import Generator, Optional
from helpers.string_manipulation import create_string_from_name_set
from helpers.utils import eprint, box_catalogue
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_states_bfs
from tree_automata.transition import TTransition
from apply.abdd_node import ABDDNode


class ABDD:
    name: str
    variable_count: int
    root: ABDDNode
    node_map: dict[str, ABDDNode]
    node_count: int
    terminal_0: Optional[ABDDNode]
    terminal_1: Optional[ABDDNode]

    def __init__(self, name: str, variable_count: int, root: ABDDNode):
        """
        Initializing ABDD structure will omit self-looping transitions in the TA/UBDA structure.
        Missing variables or box information will raise an exception.
        """
        self.name = name
        self.variable_count = variable_count
        self.root = root
        self.node_map = {}
        self.node_count = 0
        self.terminal_0: Optional[ABDDNode] = root.find_terminal(0)
        self.terminal_1: Optional[ABDDNode] = root.find_terminal(1)

    def iterate_bfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_bfs(repeat)

    def iterate_dfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_dfs(repeat)

    def count_nodes(self) -> int:
        result = 0
        for i in self.root.explore_subtree_bfs():
            result += 1
        return result

    def evaluate_for(self, assignment: dict[int, bool]) -> int:
        pass

    def __repr__(self):
        result = f"  [ABDD]: '{self.name}'\n"
        result += f"  > Root = {self.root.node}\n"
        result += f"  > Vars = {self.variable_count}\n"
        result += "  > %-*s %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
            8,
            "nodeID",
            8,
            "varID",
            8,
            "leaf",
            8,
            "lowNode",
            8,
            "lowBox",
            8,
            "highNode",
            8,
            "highBox",
        )
        result += f"  " + "-" * 65 + "\n"
        for i in self.root.explore_subtree_bfs(repeat=False):
            if i.is_leaf:
                continue
            lowStr = ", ".join([f"<{n.leaf_val}>" if n.is_leaf else str(n.node) for n in i.low])
            highStr = ", ".join([f"<{n.leaf_val}>" if n.is_leaf else str(n.node) for n in i.high])
            leaf = i.leaf_val if i.leaf_val is not None else "-"
            lowBox = i.low_box if i.low_box is not None else "-"
            highBox = i.high_box if i.high_box is not None else "-"
            result += "  > %-*s %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
                8,
                i.node,
                8,
                i.var,
                8,
                leaf,
                8,
                lowStr,
                8,
                lowBox,
                8,
                highStr,
                8,
                highBox,
            )
        return result

    def convert_to_treeaut_obj(self) -> TTreeAut:
        pass

    def reformat_node_names(self):
        name_map: dict[int, int] = {}
        counter = 0
        for i in self.root.explore_subtree_bfs():
            if i.node is not None and i.node not in name_map:
                i.node = counter
                counter += 1

    def materialize_node_above(self):
        pass


def obtain_child_node_info(target_str: str, leafnode_count: int = 2) -> list[int]:
    if target_str.startswith("<"):
        leaf = int(target_str.lstrip("<").rstrip(">").strip())
        return [leaf]
    if target_str.startswith("("):
        nodes = target_str.lstrip("(").rstrip(")").split(",")
        result = []
        for n in nodes:
            result.append(int(n) + leafnode_count)
        return result if len(result) > 1 else result[0]
    return [int(target_str) + leafnode_count]


def import_abdd_from_abdd_file(path: str) -> ABDD:
    """
    TODO
    """
    if not path.endswith(".dd"):
        eprint("Warning: importing a Decision Diagram from not a .dd file")

    dd_name: Optional[str] = None
    var_count: Optional[int] = None
    root_idx: Optional[int] = None
    root_node: Optional[ABDDNode] = None
    node_cache: dict[int, tuple[ABDDNode, int | list[int], int | list[int]]] = {}

    zero = ABDDNode(0)
    zero.set_as_leaf(0)
    one = ABDDNode(1)
    one.set_as_leaf(1)
    node_cache[0] = (zero, [], [])
    node_cache[1] = (one, [], [])

    leafnode_count = 2

    with open(path, "r") as file:
        for linenum, line in enumerate(file, start=1):
            # remove comments, leading, trailing whitespaces
            line = line.split("#")[0].strip()
            if line == "":
                continue
            if line.startswith("@"):
                if line not in ["@ABDD"]:
                    eprint("Warning: Not @ABDD in the preamble")
                continue
            if line.startswith("%"):
                attribute, value = line.lstrip("%").split()
                if attribute == "Name":
                    dd_name = value
                elif attribute == "Vars":
                    var_count = int(value)
                elif attribute == "Root":
                    root_idx = int(value)
                else:
                    eprint(f"Warning: Unknown metadata attribute '{attribute}'")
                continue

            idxr = "([0-9]+)"
            varr = "\[([0-9]*)\]"
            tgtr = "(\([0-9\s\,]+\)|\<[0-9]+\>|[0-9]+)"
            redr = "(?:\[(\w+)\])?"
            node_record_regex = idxr + "\s*" + varr + "\s*" + tgtr + "\s*" + redr + "\s*" + tgtr + "\s*" + redr
            node_record_match = re.search(node_record_regex, line)
            node, var, low, lowr, high, highr = node_record_match.group(1, 2, 3, 4, 5, 6)

            if any([s is None or s == "" for s in [node, var, low, high]]):
                raise ValueError(f"Missing important node information at line {linenum}")

            node_idx = int(node) + leafnode_count
            if node_idx in node_cache:
                raise ValueError(f"Duplicate entry for node {node}")
            var = int(var)

            if lowr is not None and lowr not in box_catalogue:
                raise ValueError(f"Unknown low reduction rule '{lowr}' from node '{node}'")
            if highr is not None and highr not in box_catalogue:
                raise Exception(f"Unknown high reduction rule '{highr}' from node '{node}'")

            try:
                low_tgt: list[int] = obtain_child_node_info(low)
            except:
                raise ValueError(f"Invalid low child information for node '{node}'")
            try:
                high_tgt: list[int] = obtain_child_node_info(high)
            except:
                raise ValueError(f"Invalid high child information for node '{node}'")

            newnode = ABDDNode(node_idx)
            if int(node) == root_idx:
                newnode.is_root = True
                root_node = newnode
            newnode.var = var
            newnode.is_leaf = False
            newnode.low_box = lowr
            newnode.high_box = highr
            # only internal nodes are in the cache
            node_cache[node_idx] = (newnode, low_tgt, high_tgt)

    for node_idx, (node, low, high) in node_cache.items():
        for i in low:
            lownode, _, _ = node_cache[i]
            node.connect_to_low_child(lownode)
        for i in high:
            highnode, _, _ = node_cache[i]
            node.connect_to_high_child(highnode)
    return ABDD(dd_name, var_count, root_node)


def init_abdd_from_ta(ta: TTreeAut, var_count: Optional[int] = None) -> ABDD:
    """
    Given a folded TreeAut-like structure (UBDA/BDA), convert this TreeAut
    to ABDD instance.

    Assumes no loop-edges are present.
    """
    if not check_if_abdd(ta):
        ValueError(f"cannot turn {ta.name} to an ABDD")

    try:
        slen: int = len(ta.get_statename_prefix())
    except ValueError:
        ta.reformat_states()
        slen: int = len(ta.get_statename_prefix())
    vlen = len(ta.get_var_prefix())

    if len(ta.roots) != 1:
        raise ValueError("ABDD can have only one root")

    root = ta.roots[0]
    root_node = ABDDNode(ta.roots[0], state_prefix_len=slen)
    result = ABDD(f"{ta.name}", var_count if var_count is not None else ta.get_var_max(), root_node)
    result.node_map[root] = root_node

    for state in iterate_states_bfs(ta):
        if state in ta.roots:
            continue
        result.node_map[state] = ABDDNode(state, state_prefix_len=slen)

    for state in ta.roots:
        result.node_map[state].is_root = True
        result.root = result.node_map[state]

    for edge in iterate_edges(ta):
        node: ABDDNode = result.node_map[edge.src]
        if edge.children == []:
            node.set_leaf_info_from_ta_transition(edge, var_prefix_len=vlen)
            if edge.info.label == "0":
                result.terminal_0 = node
            if edge.info.label == "1":
                result.terminal_1 = node
            continue
        if edge.info.box_array == []:
            edge.info.box_array = [None, None]
        node.set_node_info_from_ta_transition(edge, result.node_map, var_prefix_len=vlen)
    result.node_count = result.count_nodes()
    return result


def check_abdd_isomorphism(abdd1: ABDD, abdd2: ABDD) -> bool:
    pass


def check_if_abdd(ta: TTreeAut) -> bool:
    """
    Perform checks if the BDA structkure is convertible to automaton:
    - there should be no self-loops, or any other loops
    - each state should have just one outgoing edge (determinism)
    - every edge should be labeled with a variable
    """
    visited: set[str] = set()
    output_vars: set[str] = set()
    result: bool = True
    for edge in iterate_edges(ta):
        if edge.src in visited:
            print(f"multiple edges from {edge.src}")
            result = False
        visited.add(edge.src)
        if edge.children == []:
            output_vars.add(edge.info.variable)
            continue
        arity_sum = sum(1 if b in [None, ""] else box_catalogue[b].port_arity for b in edge.info.box_array)
        if len(edge.children) != arity_sum:
            print(f"inconsistent arity on edge {edge}")
            result = False

        for i in edge.info.box_array:
            # boxes are either non-empty string or None
            if type(i) == str and i == "":
                print(f"{edge} boxes are either None or a non-empty string")
                result = False
        if edge.src in edge.children:
            print(f"self loop {edge}")
            result = False
            continue
        if edge.info.variable == "":
            print(f"no variable on edge {edge}")
            result = False
    output_vars.remove("")
    if len(output_vars) > 1:
        print(f"inconsistent output variables: {create_string_from_name_set(output_vars)}")
        result = False
    return result
