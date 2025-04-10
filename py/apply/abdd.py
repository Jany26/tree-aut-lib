import itertools
import re

from typing import Generator, Optional
from apply.abdd_node_cache import ABDDNodeCacheClass
from helpers.string_manipulation import create_string_from_name_set
from helpers.utils import eprint, box_catalogue
from tree_automata.automaton import TTreeAut, iterate_edges
from tree_automata.transition import TEdge, TTransition
from apply.abdd_node import ABDDNode


class ABDD:
    name: str
    variable_count: int
    root: ABDDNode

    # node_map is used during TA->ABDD conversion, probably could be kept outside the class
    # node_map: dict[str, ABDDNode]
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
        self.root_rule: Optional[str] = None
        self.node_map = {}
        self.node_count = 0
        self.terminal_0: Optional[ABDDNode] = root.find_terminal(0)
        self.terminal_1: Optional[ABDDNode] = root.find_terminal(1)

    def __repr__(self):
        result = f"  [ABDD]: '{self.name}'\n"
        result += f"  > Root node index     = {self.root.node}\n"
        result += f"  > Root rule           = {self.root_rule}\n"
        result += f"  > Number of variables = {self.variable_count}\n"
        result += "  > %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
            10,
            "node(var)",
            5,
            "LBox",
            20,
            "low(var)",
            5,
            "HBox",
            20,
            "high(var)",
            14,
            "hex(ID)",
        )
        result += f"  " + "-" * (74 + 7) + "\n"
        for i in self.root.explore_subtree_bfs(repeat=False):
            if i.is_leaf:
                continue
            lowStr = ", ".join([f"<{n.leaf_val}>" if n.is_leaf else f"{n.node}({n.var})" for n in i.low])
            highStr = ", ".join([f"<{n.leaf_val}>" if n.is_leaf else f"{n.node}({n.var})" for n in i.high])
            leaf = i.leaf_val if i.leaf_val is not None else "-"
            lowBox = i.low_box if i.low_box is not None else "-"
            highBox = i.high_box if i.high_box is not None else "-"
            result += "  > %-*s %-*s %-*s %-*s %-*s %-*s\n" % (
                10,
                f"{i.node}({i.var})",
                5,
                lowBox,
                20,
                lowStr,
                5,
                highBox,
                20,
                highStr,
                14,
                hex(id(i)),
            )
        return result

    def __eq__(self, other: "ABDD", brute_force: bool = False) -> bool:
        """
        'brute_force' = False -> Check structural equality of two ABDDs.
        This is essentially the top-down

        'brute_force' = True -> Check the result of evaluating all possible variable
        true/false assignments in a brute-force manner.
        """
        if not brute_force:
            return all(
                [
                    self.variable_count == other.variable_count,
                    self.root_rule == other.root_rule,
                    self.root == other.root,
                ]
            )
        else:
            return self.check_brute_force_equivalence(other)

    def iterate_bfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_bfs(repeat)

    def iterate_dfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        return self.root.explore_subtree_dfs(repeat)

    def count_nodes(self) -> int:
        result = 0
        for i in self.root.explore_subtree_bfs():
            result += 1
        return result

    def check_brute_force_equivalence(self, other: "ABDD") -> bool:
        if self.variable_count != other.variable_count:
            raise ValueError("unequal number of variables for equivalence checking")
        for assign_tuple in itertools.product([False, True], repeat=self.variable_count):
            assignment = list(assign_tuple)
            res1 = self.evaluate_for(assignment)
            res2 = other.evaluate_for(assignment)
            if res1 != res2:
                eprint(f"check_brute_force_equivalence({self.name}, {other.name}):")
                eprint(f"not equal for {{{','.join([f'{i}' for i, val in enumerate(assignment) if val])}}}")
                return False
        return True

    def evaluate_for(self, assignment: list[bool]) -> int:
        def evaluate_box(box: TTreeAut, assignment: list[bool], node_map: dict[str, ABDDNode]) -> bool | ABDDNode:
            current = box.roots[0]
            outputs = box.get_output_edges(inverse=True)
            while assignment != []:
                val = assignment.pop(0)
                if current in outputs:
                    break
                pick_loop = assignment != []
                for t in box.transitions[current].values():
                    if pick_loop == t.is_self_loop():
                        current = t.children[int(val)]
                    continue
            # either we map a terminal result
            if outputs[current][0] in ["0", "1"]:
                return True if outputs[current][0] == "1" else False
            # or map the node corresponding to the port
            return node_map[outputs[current][0]]

        current_node: Optional[ABDDNode] = None
        result = None
        while True:
            if current_node is not None and current_node.is_leaf:
                result = current_node.leaf_val
                break
            current_var = 0 if current_node is None else current_node.var - 1
            rule = (
                self.root_rule
                if current_node is None
                else (current_node.high_box if assignment[current_var - 1] else current_node.low_box)
            )
            target = (
                [self.root]
                if current_node is None
                else (current_node.high if assignment[current_var - 1] else current_node.low)
            )
            if rule is None:
                current_node = target[0]
            else:
                target_var = max([self.variable_count + 1 if t.is_leaf else t.var for t in target])
                port_map = {port: target[i] for i, (port, state) in enumerate(box_catalogue[rule].get_port_order())}
                subassign = assignment[current_var : target_var - 1]
                box_eval = evaluate_box(box_catalogue[rule], subassign, port_map)
                if type(box_eval) == bool:
                    result = int(box_eval)
                    break
                current_node = box_eval
        if result is None:
            raise ValueError(f"couldn't evaluate the truth value for {self.name}")
        return result

    def convert_to_treeaut_obj(self, cache) -> TTreeAut:
        result = TTreeAut([f"{self.root.node}"], {f"{n.node}": {} for n in self.iterate_bfs_nodes()}, name=self.name)
        keycounter = 0
        for n in self.iterate_bfs_nodes():
            sym = "LH" if not n.is_leaf else f"{n.leaf_val}"
            var = f"{n.var}" if not n.is_leaf else f"{self.variable_count + 1}"
            tr = TTransition(
                f"{n.node}", TEdge(sym, [n.low_box, n.high_box], var), [f"{n.node}" for n in n.low + n.high]
            )
            result.transitions[f"{n.node}"][f"{keycounter}"] = tr
            keycounter += 1
        return result

    def reformat_node_names(self):
        name_map: dict[int, int] = {}
        counter = 0
        for i in self.root.explore_subtree_bfs():
            i.node = counter
            counter += 1

    def change_leaf_level():
        """
        Leaf level can only be changed such that it is still larger than any inner node level.
        Before modifying the structure, a simple DFS traversal will obtain the maximum variable level
        of inner nodes.

        After that, all edges leading to terminal nodes will be analyzed and reduction rules
        will be modified so that if edge inner node -> terminal node will have short edge if the
        variable difference is one and 'X'-edge if it is greater than one.
        """
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


def import_abdd_from_abdd_file(path: str, ncache: ABDDNodeCacheClass) -> ABDD:
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

    zero = ncache.terminal_0
    one = ncache.terminal_1
    node_cache[-1] = (zero, [], [])
    node_cache[-2] = (one, [], [])

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

            node_idx = int(node)  # + leafnode_count
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


def convert_ta_to_abdd(
    ta: TTreeAut, ncache: ABDDNodeCacheClass, var_count: Optional[int] = None, node_start: int = 0
) -> ABDD:
    """
    Given a folded TreeAut-like structure (UBDA/BDA), convert this TreeAut
    to ABDD instance.

    Assumes no loop-edges are present.
    """
    if not check_if_abdd(ta):
        ValueError(f"cannot turn {ta.name} to an ABDD")

    # statename -> corresponding node
    node_map: dict[str, ABDDNode] = {}
    # visited_states: dict[str, ABDDNode] = {}
    # state_idx_map: dict[str, int] = {}
    ncounter = node_start + 2  # idx 0 and idx 1 are reserved for terminal nodes

    vlen = len(ta.get_var_prefix())

    # when this function is called, the following is assumed (for an ABDD-compatible binary decision automaton):
    # - one TA rootstate
    # - one state with "0"-labeled output edge
    # - one state with "1"-labeled output edge
    # - no two states represent roots of isomorphic ABDDs (i.e. the BDA is normalized)

    if len(ta.roots) != 1:
        raise ValueError("convert_ta_to_abdd(): ABDD-compatible BDA can have only one root")

    for sym, states in ta.get_output_edges().items():
        if sym not in ["0", "1"]:
            raise ValueError(
                "convert_ta_to_abdd(): ABDD-compatible BDA can only have output transitions labeled with '0' and '1'"
            )
        # if len(states) > 1:
        #     raise ValueError("convert_ta_to_abdd(): ABDD-compatible BDA can only have one state with specifically labeled output transition")
        if sym == "0":
            for s in states:
                node_map[s] = ncache.terminal_0
        if sym == "1":
            for s in states:
                node_map[s] = ncache.terminal_1

    # since we now assume that every state is representing a unique Boolean function,
    # inner node cache hits should not happen
    for edge in iterate_edges(ta):
        if edge.children == []:
            continue
        if edge.src not in node_map:
            node_map[edge.src] = ABDDNode(ncounter)
            ncounter += 1
        for c in edge.children:
            if c not in node_map:
                node_map[c] = ABDDNode(ncounter)
                ncounter += 1
        if edge.info.box_array == []:
            edge.info.box_array = [None, None]
        node_map[edge.src].set_node_info_from_ta_transition(edge, node_map, var_prefix_len=vlen)

    node_map[ta.roots[0]].is_root = True
    result = ABDD(f"{ta.name}", var_count if var_count is not None else ta.get_var_max(), node_map[ta.roots[0]])
    result.terminal_0 = ncache.terminal_0
    result.terminal_1 = ncache.terminal_1
    result.node_count = result.count_nodes()
    result.root_rule = "X" if result.root.var > 1 else None

    return result


def check_if_abdd(ta: TTreeAut) -> bool:
    """
    Perform checks if the BDA structure is convertible to automaton:
    - there should be no self-loops, or any other loops
    - each state should have just one outgoing edge (determinism)
    - every edge should be labeled with a variable
    """
    visited: set[str] = set()
    output_vars: set[str] = set()
    result: bool = True
    for edge in iterate_edges(ta):
        if edge.src in visited:
            eprint(f"multiple edges from {edge.src}")
            result = False
        visited.add(edge.src)
        if edge.children == []:
            output_vars.add(edge.info.variable)
            continue
        arity_sum = sum(1 if b in [None, ""] else box_catalogue[b].port_arity for b in edge.info.box_array)
        if len(edge.children) != arity_sum:
            eprint(f"inconsistent arity on edge {edge}")
            result = False

        for i in edge.info.box_array:
            # boxes are either non-empty string or None
            if type(i) == str and i == "":
                eprint(f"{edge} boxes are either None or a non-empty string")
                result = False
        if edge.src in edge.children:
            eprint(f"self loop {edge}")
            result = False
            continue
        if edge.info.variable == "":
            eprint(f"no variable on edge {edge}")
            result = False
    output_vars.remove("")
    if len(output_vars) > 1:
        eprint(f"inconsistent output variables: {create_string_from_name_set(output_vars)}")
        result = False
    return result
