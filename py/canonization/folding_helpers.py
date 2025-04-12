"""
[file] folding_helpers.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Helper functions and FoldingHelper class used during all
essential algorithms/operations regarding folding.

[note] mostly redundant or self-explanatory functions
"""

import os
import re
import copy
from typing import Tuple, Set, List, Dict, Optional

from tree_automata import TTreeAut, TTransition, iterate_edges, remove_useless_states, reachable_top_down
from tree_automata.functions.reachability import get_all_state_reachability
from formats.render_dot import export_to_file
from formats.format_vtf import export_treeaut_to_vtf
from helpers.utils import box_catalogue
from helpers.string_manipulation import get_first_name_from_tuple_str


class FoldingHelper:
    def __init__(
        self,
        ta: TTreeAut,
        max_var: int,
        verbose: bool = False,
        export_vtf: bool = False,
        export_png: bool = False,
        output: str = "",
        export_path: str = "",
    ):
        self.name: str = ""
        match = re.search(r"\(([^()]*)\)", ta.name)
        if match is None:
            self.name = f"{ta.name}"
        else:
            self.name = f"{match.group(1)}"

        # Helpful for storing (state, edge_key) tuples during intersectoid
        # construction. If the intersectoid has non-empty language, the items
        # from this list are moved to the final soft_flagged_edges dictionary
        self.soft_flagged_edges: Dict[Tuple[str, str]] = {}
        self.flagged_edges: Set[str] = set()  # set of edge-keys

        self.key_counter: int = 0

        # folding options
        self.max_var: int = max_var
        self.min_var: int = 0
        self.var_prefix: str = ta.get_var_prefix()
        self.state_var_map: Dict[str, str] = {}
        for e in iterate_edges(ta):
            if e.info.variable != "":
                if e.src in self.state_var_map:
                    raise ValueError(f"FoldingHelper(): multiple variable-marked edges from state {e.src}")
                self.state_var_map[e.src] = e.info.variable

        self.counter: int = 0
        self.counter2: int = 0  # obsolete currently
        self.reach: Dict[str, Set[str]] = get_all_state_reachability(ta, reflexive=False)

        # export/debug options
        self.intersectoids: List[TTreeAut] = []  # potentially memory intensive
        self.verbose: bool = verbose
        self.png: bool = export_png
        self.vtf: bool = export_vtf
        self.output: str = output
        self.path = export_path
        if self.vtf or self.png:
            if not os.path.exists(f"{self.path}/ubdas/"):
                os.makedirs(f"{self.path}/ubdas/")
            if not os.path.exists(f"{self.path}/intersectoids/"):
                os.makedirs(f"{self.path}/intersectoids/")

    def __repr__(self):
        result: str = "[FoldingHelper]\n"
        src_len: int = 0
        key_len: int = 0
        child_len: int = 0
        for state, edges in self.soft_flagged_edges.items():
            src_len = max(src_len, len(state))
            for child_str, (key, edge) in edges.items():
                child_len = max(child_len, len(child_str))
                key_len = max(key_len, len(key))
        for state, edges in self.soft_flagged_edges.items():
            for child_str, (key, edge) in edges.items():
                result += "%-*s -> %-*s : %-*s : %s\n" % (src_len, state, child_len, child_str, key_len, key, edge)
        result += f"minvar = {self.min_var}, maxvar = {self.max_var}\n"
        result += f"keycounter = {self.key_counter}, counter = {self.counter}, counter2 = {self.counter2}\n"
        result += f"statemap = {self.state_var_map}\n"
        return result

    def write(self, s):
        if self.verbose:
            if self.output is None:
                print(s)
            else:
                self.output.write(f"{s}\n")

    def flag_edge(self, key: str, edge: TTransition):
        """
        Note: edge flagging is unused
        """
        if edge.src not in self.soft_flagged_edges:
            self.soft_flagged_edges[edge.src] = {}
        child_str: str = ""
        for i in edge.children:
            child_str += i + " | "
        child_str = child_str[:-3]
        if child_str not in self.soft_flagged_edges[edge.src]:
            self.soft_flagged_edges[edge.src][child_str] = (key, edge)

    def print_flagged_edges(self):
        """
        Note: edge flagging is unused
        """
        for j in self.soft_flagged_edges.values():
            for l, m in j.values():
                print(l, m)

    # ta -> intersectoid
    def get_flagged_edges_from(self, ta: TTreeAut):
        """
        Note: edge flagging is unused
        """
        for edge in iterate_edges(ta):
            if len(edge.children) == 0:
                continue
            tree_aut_state: str = get_first_name_from_tuple_str(edge.src)
            children: List[str] = [get_first_name_from_tuple_str(i) for i in edge.children]
            children_str: str = ",".join(children)
            key = f"{tree_aut_state}-{edge.info.variable}-{children_str}"
            self.flagged_edges.add(key)

    def export_ubda(self, result: TTreeAut, state: str, edge_part: list, box: TTreeAut):
        """
        Exporting semi-results (during folding after each 'fold') to images for debugging.
        """
        if self.png or self.vtf:
            temp: str = f"{self.counter}-{state}-{edge_part[1]}:{box.name}-{edge_part[2]}"
            path: str = (f"results/{self.name}" if self.path is None else f"{self.path}") + f"/ubdas/{temp}"
            if self.vtf:
                export_treeaut_to_vtf(result, format="f", filepath=f"{path}.vtf")
            if self.png:
                export_to_file(result, path)
            self.counter += 1

    # helper.export_intersectoid(A, root, source, box.name)
    def export_intersectoid(self, treeaut: TTreeAut, source: str, root: str, box: str):
        """
        Helper function for exporting intersectoid images/files used in folding procedure.
        """
        if self.output == "":
            return
        self.intersectoids.append(treeaut)
        temp: str = f"{self.counter}-{source}-{box}-{root}"
        if self.path is None:
            path: str = f"results/{self.name}/intersectoids/{temp}"
        else:
            path: str = f"{self.path}/intersectoids/{temp}"
        if self.vtf:
            export_treeaut_to_vtf(treeaut, format="f", filepath=f"{path}.vtf")
        if self.png:
            export_to_file(treeaut, f"{path}")
        self.write(treeaut)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Helper functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_state_index_from_box_index(edge: TTransition, idx: int) -> int:
    """
    Returns the first (important notice!) child state (index),
    to which does the transition lead through the box on index idx.

    E.g. q0 - [box1, box2] -> (q1, q2, q3, q4) ## consider box1 has port_arity = 3
    idx = 1 (box2)... box1 has port arity 3, so box2 is on the sub-edge leading
    to state q4, as subedge with box1 encapsulates children q1, q2, q3

    NOTE: might not work in some special cases of port arity combinations etc.
    """
    if idx >= len(edge.info.box_array):
        raise Exception("get_state_index_from_box_index(): idx out of range")
    result = 0
    for i, box_str in enumerate(edge.info.box_array):
        if i == idx:
            return result
        if box_str is None:
            result += 1
        else:
            result += box_catalogue[box_str].port_arity
    raise Exception("get_state_index_from_box_index(): idx out of range")


def check_box_arrays(ta: TTreeAut) -> None:
    for edge in iterate_edges(ta):
        if edge.info.label == "LH" and len(edge.info.box_array) != 2:
            raise ValueError(f"check_box_arrays(): {edge} has unfilled box array = {edge.info.box_array}")


def fill_box_arrays(ta: TTreeAut) -> None:
    """
    Normalizes the box arrays within the tree automaton, so that reducibility checks are consistent.
    In essence, each box array on a non-output edge will look like this:
    [ #1, #2 ], where #1, #2 are of type: None | str
    """
    arities: Dict[str, int] = ta.get_symbol_arity_dict()
    for edge in iterate_edges(ta):
        if edge.info.label != "LH":
            continue
        if edge.info.box_array == []:
            edge.info.box_array = [None] * len(edge.children)
        else:
            boxlen = len(edge.info.box_array)
            symlen = arities[edge.info.label]
            if boxlen != symlen:
                edge.info.box_array.extend([None] * (symlen - boxlen))


def is_already_reduced(ta: TTreeAut, state: str, edge_info: list) -> bool:
    """
    This function checks whether or not a certain subedge has a box reduction.
    (subedge is based on 'state' and 'edge_info')

    NOTE: might be buggy if box arities and box_arrays on edges are inconsistent
    (consider different index in edge_info and boxes with different port arities)
    """
    edge: TTransition = ta.transitions[state][edge_info[0]]  # edge_info[0] = key
    if edge_info[2] not in edge.children:
        return True
    idx: int = edge_info[1]
    # if box is None => short edge => arity = 1 (1 target state)
    box_arities: List[Tuple[Optional[str], int]] = []
    for box_str in edge.info.box_array:
        if box_str is None:
            box_arities.append((None, 1))
        else:
            box = box_catalogue[box_str]
            box_arities.append((box_str, box.port_arity))

    i = 0
    for box_str, arity in box_arities:
        if idx < i + arity:
            if box_str is not None:
                return True
            else:
                return False
        i += arity
    return False


class EdgePart:
    def __init__(self, key: str, edge: TTransition, index: int):
        assert edge.src not in edge.children
        assert edge.info.variable != ""
        self.key = key
        self.edge = edge
        self.index = index
        self.src = edge.src
        self.target = edge.children[index]


def prepare_edge_info(ta: TTreeAut, state: str) -> List[Tuple[str, int, str, str, TTransition]]:
    """
    Creates a list of all edge-parts across all transitions from 1 source state.
    e.g. transition q0 -> (q1, q2) has 2 edge-parts, q0->q1 and q0->q2
    Each edge-part item in the list contains 4 pieces of information:
    - 0: edge key for lookup,
    - 1: index of the child,
    - 2: child name,
    - 3: source state name
    - 4: the whole edge itself
    """
    result = []
    for key, edge in ta.transitions[state].items():
        # we do not fold edges that are self-loops
        if edge.src in edge.children:
            continue
        # ... or are not labeled with a variable
        if edge.info.variable == "":
            continue
        for i in range(len(edge.children)):
            result.append(tuple([key, i, edge.children[i], state, edge]))
    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# All the functions below are obsolete, or a better version is used.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def add_variables_bottomup_folding(ta: TTreeAut, min_var: int) -> None:
    """
    NOTE: function add_variables_top_down is in use for folding
    temporarily copied from simulation.py
    NOTE: Unused
    """

    def create_var_lookup(var_list: list, prefix: str) -> dict[str, int]:
        return {i: int(i[len(prefix) :]) for i in var_list}

    var_prefix: str = ta.get_var_prefix()
    var_lookup: dict[str, int] = create_var_lookup(ta.get_var_order(), var_prefix)
    # var_vis = {i: min_var for i in ta.roots}
    var_vis: dict[str, str] = {}
    for edge in iterate_edges(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src not in var_vis:
            var_vis[edge.src] = f"{var_prefix}{var_lookup[edge.info.variable]}"
    for edge in iterate_edges(ta):
        if edge.info.variable == "":
            continue
        if edge.src in edge.children:
            continue
        for child in edge.children:
            if child in var_vis:
                continue
            var_vis[child] = f"{var_prefix}{var_lookup[var_vis[edge.src]] + 1}"

    for edge in iterate_edges(ta):
        if edge.info.variable != "":
            continue
        if edge.src in edge.children:
            continue
        if edge.src in var_vis:
            edge.info.variable = f"{var_vis[edge.src]}"
        pass  # do_sth()


def lexicographical_order(ta: TTreeAut) -> list[str]:
    """
    In order to canonically and deterministically fold the unfolded and
    normalized UBDA, we need to determine an order in which the states will
    be checked for possible applicable reductions. Lexicographic order (ordered
    by the shortest path from root to the particular state),
    which is similar to DFS, provides such a way.

    e.g. path to q1 from root is: low(0), low(0), high(1) edges - 001
    path to q2 from root is: low(0), high(1), low(0) - 010
    thus, lexicographically, q1 comes before q2.
    Shorter paths always come first (e.g.: 0, 00, 000, 001, 010, 01, 1).

    This function takes a tree automaton and returns a list of states in the lexicographical order.

    NOTE: Not used. Instead, a BFS-like traversal is used.
    """

    def lexicographic_order_recursive(ta: TTreeAut, state: str, path: str, result, open) -> None:
        if state not in result:
            result[state] = path
        else:  # probably redundant, as we go depth first from the lowest path
            if path < result[state]:
                result[state] = path

        for edge in ta.transitions[state].values():
            for idx, child in enumerate(edge.children):
                if child in open:
                    continue
                open.add(child)
                lexicographic_order_recursive(ta, child, path + str(idx), result, open)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    path_dict: dict[str, str] = {}  # state -> path string
    open: set[str] = set()
    for i in ta.roots:
        open.add(i)
        lexicographic_order_recursive(ta, i, "", path_dict, open)

    # because some states can be accessed through identical paths,
    # we need to have lists in the reverse path dict.
    reverse_path_dict: dict[str, list[str]] = {}  # path -> list of states
    for state, path in path_dict.items():
        if path not in reverse_path_dict:
            reverse_path_dict[path] = []
        reverse_path_dict[path].append(state)

    path_list: list[str] = [path for path in reverse_path_dict.keys()]
    path_list.sort()
    result = []
    for path in path_list:
        result.extend(reverse_path_dict[path])
    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Redundant: old port-state map creating functions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_mapping_old(intersectoid, treeaut):
    mapping: dict[str, list[str]] = port_to_state_mapping(intersectoid)
    # old_mapping = get_maximal_mapping(intersectoid, treeaut, mapping)
    max_mapping = get_maximal_mapping_fixed(intersectoid, treeaut, mapping)
    # ^^ largest root_distance of "port" nodes (inside intersectoid)
    final_mapping: dict[str, str] = {i: get_first_name_from_tuple_str(j) for i, j in max_mapping.items()}
    return final_mapping


def port_to_state_mapping(intersectoid: TTreeAut) -> Dict[str, List[str]]:
    """
    This function parses an intersectoid and creates a dictionary with all
    port transitions and all states that begin with them.
    input:
    - an intersectoid "TA"
    output:
    - mapping of port_names (str) to list of states with the output port transitions
    """
    result: Dict[str, List[str]] = {}
    for edge in iterate_edges(intersectoid):
        if edge.info.label.startswith("Port"):
            if edge.info.label not in result:
                result[edge.info.label] = []
            result[edge.info.label].append(edge.src)
    return result


def get_maximal_mapping(intersectoid: TTreeAut, ta: TTreeAut, ports: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Find a state furthest from the root so that the mapping is "maximal"
    input:
    - an intersectoid "TA" (really a binary decision automaton),
    - the currently reduced BDA (which will result in an ABDD)
    - port to state list mapping [list contains states with the specific port output transitions]
    output:
    - map: port name -> state name

    NOTE: Not used
    """
    mapping: Dict[str, Optional[str]] = {}
    for port, state_list in ports.items():
        mapping[port] = None
        current_distance: int = 0  # state, root_distance
        for state in state_list:
            dist: int = intersectoid.get_root_distance(state)
            if dist > current_distance:
                mapping[port] = state
                current_distance = dist
            elif dist == current_distance:
                current_state: str = get_first_name_from_tuple_str(mapping[port])
                possible_new_state: str = get_first_name_from_tuple_str(state)
                current_distance = ta.get_root_distance(current_state)
                new_distance = ta.get_root_distance(possible_new_state)
                if new_distance > current_distance:
                    mapping[port] = state
        if mapping[port] is None:
            raise Exception(f"get_maximal_mapping: {port} mapping not found")
    return mapping


def get_maximal_mapping_fixed(intersectoid: TTreeAut, ta: TTreeAut, ports: Dict) -> Dict:
    """
    NOTE: Not used
    """
    mapping: Dict[str, Optional[str]] = {}
    for port, state_list in ports.items():
        temp = {}
        mapping[port] = None
        for state in state_list:
            treeaut_state = get_first_name_from_tuple_str(state)
            dist = ta.get_root_distance(treeaut_state)
            if dist not in temp:
                temp[dist] = set()
            temp[dist].add(state)
        max_distance = 0
        for dist in temp.keys():
            max_distance = max(max_distance, dist)
        if len(temp[max_distance]) > 1:
            return {}
        mapping[port] = list(temp[max_distance])[0]
    return mapping


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Redundant: edge removal - currently not included in implementation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def has_only_boxed_edges(ta: TTreeAut, state: str) -> bool:
    arity_dict: Dict[str, int] = ta.get_symbol_arity_dict()
    for edge in ta.transitions[state].values():
        arity = arity_dict[edge.info.label]
        if arity == 0:
            return False
        box_count = 0
        for box in edge.info.box_array:
            if box is not None and box != "":
                box_count += 1
        if arity != box_count:
            return False
    return True


def remove_flagged_edges_fix(ta: TTreeAut, helper: FoldingHelper):
    key_dict = {}
    for state, edges in ta.transitions.items():
        key_dict[state] = set()
        for key, edge in edges.items():
            if len(edge.children) == 0:
                continue
            child_str = ",".join(edge.children)
            if f"{edge.src}-{edge.info.variable}-{child_str}" in helper.flagged_edges:
                key_dict[state].add(key)
    for state, key_set in key_dict.items():
        for key in key_set:
            ta.transitions[state].pop(key)


def remove_flagged_edges(ta: TTreeAut, helper: FoldingHelper):
    key_list = []
    for state, edges in helper.soft_flagged_edges.items():
        for child_str, (key, edge) in edges.items():
            original_children = child_str.split(" | ")
            only_boxed = True
            children_stayed = True
            for i in range(len(edge.children)):
                if original_children[i] != edge.children[i]:
                    children_stayed = False
                if not has_only_boxed_edges(ta, edge.children[i]):
                    only_boxed = False
            if children_stayed and not only_boxed:
                key_list.append(key)
                ta.transitions[state].pop(key)
