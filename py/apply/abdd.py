import copy
import itertools
import os
import re

from typing import Generator, Optional
from apply.abdd_node_cache import ABDDNodeCache, ABDDNodeCacheClass
from helpers.string_manipulation import create_string_from_name_set
from helpers.utils import eprint, box_catalogue, box_arities
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_key_edge_tuples
from tree_automata.transition import TEdge, TTransition
from apply.abdd_node import ABDDNode


class ABDD:
    name: str
    variable_count: int
    roots: list[ABDDNode]
    root_rule: Optional[str]

    # node_map is used during TA->ABDD conversion, probably could be kept outside the class
    # node_map: dict[str, ABDDNode]
    node_count: int
    terminal_0: Optional[ABDDNode]
    terminal_1: Optional[ABDDNode]

    def __init__(self, name: str, variable_count: int, roots: list[ABDDNode]):
        """
        Initializing ABDD structure will omit self-looping transitions in the TA/UBDA structure.
        Missing variables or box information will raise an exception.
        """
        self.name = name
        self.variable_count = variable_count
        self.roots = roots
        self.root_rule: Optional[str] = None
        self.node_map = {}
        self.node_count = 0
        self.terminal_0: Optional[ABDDNode] = None
        self.terminal_1: Optional[ABDDNode] = None
        for root in self.roots:
            zero = root.find_terminal(0)
            one = root.find_terminal(1)
            if zero is not None:
                self.terminal_0 = zero
            if one is not None:
                self.terminal_1 = one

    def __repr__(self):
        result = f"  [ABDD]: '{self.name}'\n"
        result += f"  > Root nodes indices  = {', '.join([str(r.node) for r in self.roots])}\n"
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
        for i in self.iterate_bfs_nodes(repeat=False):
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
                    self.roots == other.roots,
                ]
            )
        else:
            return self.check_brute_force_equivalence(other)

    def iterate_bfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        queue: list[ABDDNode] = [r for r in self.roots]
        visited = set()
        while queue != []:
            node = queue.pop(0)
            if not repeat and id(node) in visited:
                continue
            yield node
            visited.add(id(node))
            queue.extend(node.low)
            queue.extend(node.high)

    def iterate_dfs_nodes(self, repeat=False) -> Generator[ABDDNode, None, None]:
        stack: list[ABDDNode] = [r for r in reversed(self.roots)]
        visited = set()
        while stack != []:
            node = stack.pop()
            if not repeat and node in visited:
                continue
            yield node
            # we have to insert nodes in a reverse order
            visited.add(node)
            stack.extend(reversed(node.low))
            stack.extend(reversed(node.high))

    def count_nodes(self) -> int:
        result = 0
        for i in self.iterate_bfs_nodes():
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
                eprint(
                    f"check_brute_force_equivalence({self.name}, {other.name}): not equal for {assignment} -> results: ({res1}, {res2})"
                )
                # eprint(f"not equal for {{{','.join([f'{i}' for i, val in enumerate(assignment) if val])}}}")
                return False
        return True

    def evaluate_for(self, assignment: list[bool], verbose=False) -> int:
        def evaluate_box(box: TTreeAut, assignment: list[bool], node_map: dict[str, ABDDNode]) -> bool | ABDDNode:

            current = box.roots[0]
            outputs = box.get_output_edges(inverse=True)
            if verbose:
                print(f"  > box eval {box.name} start: current={current}, assignment={assignment}")
            for i, val in enumerate(subassign):
                for t in box.transitions[current].values():
                    if t.is_self_loop() == (i < len(subassign) - 1) and len(t.children) > int(val):
                        if verbose:
                            print(
                                f"  > current={current}, idx={i}, assignment={assignment}, current_val={val}, output=None, loop={t.is_self_loop()}"
                            )
                        current = t.children[int(val)]
                        break
            # if we managed to reach an output state,
            if current not in outputs:
                raise ValueError("evaluate_box(): didn't reach an output state")
            # then we either map a terminal result
            out_label = outputs[current][0]
            if out_label in ["0", "1"]:
                if verbose:
                    print(
                        f'  > current={current}, outputs={[f"{s}->{node_map[p[0]].node if p[0].startswith("Port") else p[0]}" for s, p in outputs.items()]}, result={out_label}'
                    )
                return out_label == "1"
            # or map the node corresponding to the port
            if verbose:
                print(
                    f'  > current={current}, outputs={[f"{s}->{node_map[p[0]].node if p[0].startswith("Port") else p[0]}" for s, p in outputs.items()]}, result={node_map[outputs[current][0]].node}'
                )
            return node_map[out_label]

        # end of evaluate_box()

        if verbose:
            print(f"evaluating {self.name} for {assignment}")
        current_node: Optional[ABDDNode] = None
        while True:
            using_root_rule = False
            if verbose:
                print(f" > node={current_node.node if current_node is not None else "None"}, ", end="")
            if current_node is not None and current_node.is_leaf:
                if verbose:
                    print(f"leaf={current_node.leaf_val}")
                return int(current_node.leaf_val)
            current_var = 0 if current_node is None else current_node.var - 1
            rule = (
                self.root_rule
                if current_node is None
                else (current_node.high_box if assignment[current_var] else current_node.low_box)
            )
            using_root_rule = current_node is None and self.root_rule is not None
            target = (
                [r for r in self.roots]
                if current_node is None
                else (current_node.high if assignment[current_var] else current_node.low)
            )
            if rule is None:
                if verbose:
                    print(f"var={current_var+1}, rule={rule}, target={','.join(f"{t.node}" for t in target)}")
                current_node = target[0]
            else:
                target_var = max([self.variable_count + 1 if t.is_leaf else t.var for t in target])
                port_map = {port: target[i] for i, (port, state) in enumerate(box_catalogue[rule].get_port_order())}
                subassign = (
                    assignment[current_var + 1 : target_var - 1]
                    if not using_root_rule
                    else assignment[current_var : target_var - 1]
                )
                if verbose:
                    print(
                        f"var={current_var+1}, rule={rule}, target={','.join(f"{t.node}" for t in target)}, target_var={target_var}, ports={[f"{i} -> {n.node}" for i, (p, n) in enumerate(port_map.items())]}, sub={subassign}"
                    )
                box_eval = evaluate_box(box_catalogue[rule], subassign, port_map)
                if type(box_eval) == bool:
                    return int(box_eval)
                current_node = box_eval

    def convert_to_treeaut_obj(self) -> TTreeAut:
        result = TTreeAut(
            [f"{r.node}" for r in self.roots], {f"{n.node}": {} for n in self.iterate_bfs_nodes()}, name=self.name
        )
        keycounter = 0
        result.rootbox = self.root_rule

        for n in self.iterate_bfs_nodes():
            sym = "LH" if not n.is_leaf else f"{n.leaf_val}"
            var = f"{n.var}" if not n.is_leaf else f"{self.variable_count + 1}"

            # NOTE: it is important to set the boxarray to [] in case of leaf nodes,
            # since during normalization, "symbol_arity_dict()" method is used, and it counts arities of symbols
            # using either the length of a box array (in case of leaf nodes it should be [] -> thus 0), or in case of
            # "LH", it counts the number of boxes in the boxarray (which is always 2 -> padded with None if needed)

            # this older way of counting boxes in the boxarray breaks when converting ABDD to a BDA,
            # unfolding and normalizing -> during conversion, terminal nodes still have low_box and high_box,
            # which are set to None and during the conversion, are changed as such

            boxarray = [] if n.is_leaf else [n.low_box, n.high_box]
            tr = TTransition(f"{n.node}", TEdge(sym, boxarray, var), [f"{n.node}" for n in n.low + n.high])
            result.transitions[f"{n.node}"][f"{keycounter}"] = tr
            keycounter += 1
        return result

    def export_to_abdd_file(self, path: str) -> None:
        """
        Format example:
        @ABDD
        %Name three_L1_to_zero
        %Vars 10
        %Rootrule LPort
        %Root 2 1

        1[3] <0>[L1] 2[H0]
        2[6] 3[H1] <0>[L1]
        3[8] <0>[L1] 4
        4[9] <0>[X] <1>[H0]
        """

        def target_str(tgt: list[ABDDNode]) -> str:
            mid_str = ", ".join(f"<{i.leaf_val}>" if i.is_leaf else f"{i.node}" for i in tgt)
            return mid_str

        basen = os.path.basename(path)
        dirn = os.path.dirname(path)
        if not os.path.exists(path):
            os.makedirs(dirn, exist_ok=True)

        with open(path, "w") as f:
            f.write(f"@ABDD\n")
            f.write(f"%Name {self.name}\n")
            f.write(f"%Vars {self.variable_count}\n")
            if self.root_rule is not None:
                f.write(f"%Rootrule {self.root_rule}\n")
            f.write(f"%Root {' '.join([f"<{i.leaf_val}>" if i.is_leaf else f"{i.node}" for i in self.roots])}\n")
            f.write(f"\n")

            for n in self.iterate_bfs_nodes():
                if n.is_leaf:
                    continue
                low_str = target_str(n.low)
                high_str = target_str(n.high)
                low_box_str = f"[{n.low_box}]" if n.low_box is not None else ""
                high_box_str = f"[{n.high_box}]" if n.high_box is not None else ""
                f.write(f"{n.node}[{n.var}] {low_str}{low_box_str} {high_str}{high_box_str}\n")
            f.write(f"\n")

    def reformat_node_names(self):
        name_map: dict[int, int] = {}
        counter = 2
        for i in self.iterate_bfs_nodes():
            if i.is_leaf:
                i.node = i.leaf_val
                continue
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


def import_abdd_from_abdd_file(path: str, ncache: Optional[ABDDNodeCacheClass] = None) -> ABDD:
    """
    TODO
    """
    if ncache is None:
        ncache = ABDDNodeCacheClass()
    if not path.endswith(".dd"):
        eprint("Warning: importing a Decision Diagram from not a .dd file")

    dd_name: Optional[str] = None
    var_count: Optional[int] = None
    root_idxs: Optional[list[int]] = None
    root_node: list[ABDDNode] = []
    node_cache: dict[int, tuple[ABDDNode, int | list[int], int | list[int]]] = {}
    root_rule: Optional[str] = None

    zero = ncache.terminal_0
    one = ncache.terminal_1
    node_cache[0] = (zero, [], [])
    node_cache[1] = (one, [], [])
    rootsmap: dict[int, ABDDNode] = {}
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
                parts = line.lstrip("%").split(maxsplit=1)
                attribute = parts[0]
                value = parts[1]
                if attribute == "Name":
                    dd_name = value
                elif attribute == "Vars":
                    var_count = int(value)
                elif attribute == "Root":
                    roots = value.split()
                    root_idxs = [int(r) for r in roots]
                elif attribute == "Rootrule":
                    if value in box_arities:
                        root_rule = value
                    else:
                        raise ValueError("Warning: Unknown root rule")
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

            if int(node) in root_idxs:
                # newnode.is_root = True
                rootsmap[int(node)] = newnode
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
    abddresult = ABDD(dd_name, var_count, [rootsmap[idx] for idx in root_idxs])
    abddresult.root_rule = root_rule
    return abddresult


def convert_ta_to_abdd(
    ta: TTreeAut, ncache: ABDDNodeCacheClass, var_count: Optional[int] = None, node_start: int = 0
) -> ABDD:
    """
    Given a folded TreeAut-like structure (UBDA/BDA), convert this TreeAut
    to ABDD instance.

    Assumes no loop-edges are present.

    TODO: root rule unfold
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

    # if len(ta.roots) != 1:
    #     raise ValueError("convert_ta_to_abdd(): ABDD-compatible BDA can have only one root")
    if len(ta.roots) != box_arities[ta.rootbox]:
        raise ValueError("convert_ta_to_abdd(): roots incompatible with root box")

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

    # node_map[ta.roots[0]].is_root = True
    result = ABDD(
        f"{ta.name}", var_count if var_count is not None else ta.get_var_max() - 1, [node_map[r] for r in ta.roots]
    )
    result.terminal_0 = ncache.terminal_0
    result.terminal_1 = ncache.terminal_1
    result.node_count = result.count_nodes()
    # result.root_rule = "X" if result.root.var > 1 else None
    result.root_rule = ta.rootbox
    for i in result.iterate_bfs_nodes():
        hit = ncache.find_node(i)
        if hit is None:
            ncache.insert_node(i)

    ncache.refresh_nodes()

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
        if edge.info.box_array == []:
            arity_sum = len(edge.children)
        if len(edge.children) != arity_sum:
            eprint(f"inconsistent arity on edge {edge}, {edge.info.box_array}")
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
    if "" in output_vars:
        output_vars.remove("")
    if len(output_vars) > 1:
        eprint(f"inconsistent output variables: {create_string_from_name_set(output_vars)}")
        result = False
    return result
