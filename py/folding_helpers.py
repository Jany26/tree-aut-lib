"""
[file] folding_helpers.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Helper functions and FoldingHelper class used during all
essential algorithms/operations regarding folding.

[note] mostly redundant or self-explanatory functions
"""

from ta_classes import *
from ta_functions import *
from test_data import *

import re
import copy

from render_dot import export_to_file

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Folding Helper class:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FoldingHelper:
    def __init__(self, ta: TTreeAut, verbose: bool, export_vtf: bool, export_png: bool, output, export_path, max_var):
        self.name = ""
        match = re.search(r"\(([^()]*)\)", ta.name)
        if match is None:
            self.name = f"{ta.name}"
        else:
            self.name = f"{match.group(1)}"

        # Helpful for storing (state, edge_key) tuples during intersectoid
        # construction. If the intersectoid has non-empty language, the items
        # from this list are moved to the final soft_flagged_edges dictionary
        self.soft_flagged_edges = {}
        self.flagged_edges = set()

        self.key_counter = 0

        # folding options
        self.max_var = max_var
        self.min_var = 0
        self.var_prefix = ta.get_var_prefix()
        self.state_map = {}
        self.counter = 0
        self.counter2 = 0
        self.reach: dict[str, set] = get_all_state_reachability(ta, reflexive=False)

        # export/debug options
        self.intersectoids = []
        self.verbose = verbose
        self.png = export_png
        self.vtf = export_vtf
        self.output = output
        self.path = export_path

    def __repr__(self):
        result = "[FoldingHelper]\n"
        src_len = 0
        key_len = 0
        child_len = 0
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
        result += f"statemap = {self.state_map}\n"
        # result += f"{}\n"
        # result += f"{}\n"
        return result

    def write(self, s):
        if self.verbose:
            if self.output is None:
                print(s)
            else:
                self.output.write(f"{s}\n")

    # def flag_edge(self, key: str, edge: TTransition):
    #     if edge.src not in self.soft_flagged_edges:
    #         self.soft_flagged_edges[edge.src] = {}
    #     child_str = ""
    #     for i in edge.children:
    #         child_str += i + " | "
    #     child_str = child_str[:-3]
    #     if child_str not in self.soft_flagged_edges[edge.src]:
    #         self.soft_flagged_edges[edge.src][child_str] = (key, edge)

    # def print_flagged_edges(self):
    #     for j in self.soft_flagged_edges.values():
    #         for (l, m) in j.values():
    #             print(l, m)

    # # ta -> intersectoid
    # def get_flagged_edges_from(self, ta: TTreeAut):
    #     for edge in transitions(ta):
    #         if len(edge.children) == 0:
    #             continue
    #         tree_aut_state = split_tuple_name(edge.src)
    #         children = [split_tuple_name(i) for i in edge.children]
    #         children_str = ','.join(children)
    #         key = f"{tree_aut_state}-{edge.info.variable}-{children_str}"
    #         self.flagged_edges.add(key)

    def export_ubda(self, result: TTreeAut, state: str, edge_part: list, box: TTreeAut):
        if self.png or self.vtf:
            temp = f"{state}-{edge_part[1]}:{box.name}-{edge_part[2]}"
            temp = f"{self.counter}-{temp}"
            if self.path is None:
                path = f"results/{self.name}/ubdas/{temp}"
            else:
                path = f"{self.path}/ubdas/{temp}"
            if self.vtf:
                export_treeaut_to_vtf(result, format="f", filepath=f"{path}.vtf")
            if self.png:
                export_to_file(result, path)
            self.counter += 1

    # helper.export_intersectoid(A, root, source, box.name)
    def export_intersectoid(self, treeaut: TTreeAut, source: str, root: str, box: str):
        self.intersectoids.append(treeaut)
        temp = f"{self.counter}-{source}-{box}-{root}"
        if self.path is None:
            path = f"results/{self.name}/intersectoids/{temp}"
        else:
            path = f"{self.path}/intersectoids/{temp}"
        if self.vtf:
            export_treeaut_to_vtf(treeaut, format="f", filepath=f"{path}.vtf")
        if self.png:
            export_to_file(treeaut, f"{path}")
        self.write(treeaut)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Helper functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Returns the first (important notice!) child state (index),
# to which does the transition lead through the box on index idx.
#
# E.g. q0 - [box1, box2] -> (q1, q2, q3, q4) ## consider box1 has port_arity = 3
# idx = 1 (box2)... box1 has port arity 3, so box2 is on the sub-edge leading
# to state q4, as subedge with box1 encapsulates children q1, q2, q3
#
# NOTE: might not work in some special cases of port arity combinations etc.
def get_state_index_from_box_index(edge: list, idx: int) -> int:
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


# Normalizes the box arrays within the ta,
# so that reducibility checks are consistent.
def fill_box_arrays(ta: TTreeAut):
    arities = ta.get_symbol_arity_dict()
    for edge in iterate_edges(ta):
        if edge.info.box_array == []:
            edge.info.box_array = [None] * len(edge.children)
        else:
            boxlen = len(edge.info.box_array)
            symlen = arities[edge.info.label]
            if boxlen != symlen:
                edge.info.box_array.extend([None] * (symlen - boxlen))


# This function checks whether or not a certain subedge has a box reduction.
# (subedge is based on 'state' and 'edge_info')
#
# NOTE: might be buggy if box arities and box_arrays on edges are inconsistent
# (consider different index in edge_info and boxes with different port arities)
def is_already_reduced(ta: TTreeAut, state: str, edge_info: list) -> bool:
    edge = ta.transitions[state][edge_info[0]]  # edge_info[0] = key
    if edge_info[2] not in edge.children:
        return True
    # idx = edge.children.index(edge_info[2])
    # print(edge_info[1])
    idx = edge_info[1]
    # if box is None => short edge => arity = 1 (1 target state)
    box_arities = []
    for box_str in edge.info.box_array:
        if box_str is None:
            box_arities.append((None, 1))
        else:
            box = box_catalogue[box_str]
            box_arities.append((box_str, box.port_arity))

    i = 0
    for tuple in box_arities:
        if idx < i + tuple[1]:
            if tuple[0] is not None:
                return True
            else:
                return False
        i += tuple[1]
    return False


def shrink_to_top_down_reachable(ta: TTreeAut) -> TTreeAut:
    work_treeaut = copy.deepcopy(ta)
    # reachable_states_bottomup = reachable_states_bottomup(work_treeaut)
    # work_treeaut.shrink_tree_aut(reachable_states_bottomup)
    reachable_states_top_down = reachable_top_down(work_treeaut)
    work_treeaut.shrink_tree_aut(reachable_states_top_down)
    return work_treeaut


def trim(ta: TTreeAut) -> TTreeAut:
    work_treeaut = shrink_to_top_down_reachable(ta)
    return remove_useless_states(work_treeaut)

    # remove transitions over variables which are clearly unnecessary
    # TODO: define/explain ^^
    # get all paths from roots to leaves ---> make a function

    return work_treeaut


class EdgePart:
    def __init__(self, key: str, edge: TTransition, index: int):
        assert edge.src not in edge.children
        assert edge.info.variable != ""
        self.key = key
        self.edge = edge
        self.index = index
        self.src = edge.src
        self.target = edge.children[index]


# Creates a list of all edge-parts across all transitions from 1 source state.
# e.g. transition q0 -> (q1, q2) has 2 edge-parts, q0->q1 and q0->q2
# Each edge-part item in the list contains 4 pieces of information:
# - 0: edge key for lookup,
# - 1: index of the child,
# - 2: child name,
# - 3: source state name
# - 4: the whole edge itself
def prepare_edge_info(ta: TTreeAut, state: str):
    result = []
    for key, edge in ta.transitions[state].items():
        # we do not fold edges that are self-loops
        if edge.src in edge.children:
            continue
        # ... or are not labeled with a variable
        if edge.info.variable == "":
            continue
        for i in range(len(edge.children)):
            result.append([key, i, edge.children[i], state, edge])
    return result


def tuple_name(tuple) -> str:
    return f"({tuple[0]},{tuple[1]})"


def split_tuple_name(string):
    match = re.search("^\(.*,", string)
    result = match.group(0)[1:-1]
    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# redundant edge removal - currently not included in implementation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def has_only_boxed_edges(ta: TTreeAut, state: str):
    arity_dict = ta.get_symbol_arity_dict()
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# probably useless
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# NOTE: this function is redundant, a newer version is used (prepare_edge_info)
# Helper function to create a list of states and some data about them,
# which will be helpful during main folding procedure.
# list of all sub-edges (parts of hyper-edge), with indexes to the child.
#
# e.g. key-transition pair "key": q0 -> (q1, q2) will be divided into:
# ["key", 0, q1] and ["key", 1, q2]
def prepare_edge_info_old(ta: TTreeAut, state: str) -> list:
    result = []
    for key, edge in ta.transitions[state].items():
        for i in range(len(edge.children)):
            result.append([key, i, edge.children[i]])
    return result


# NOTE: function add_variables_top_down is in use for folding
# temporarily copied from simulation.py
def add_variables_bottomup_folding(ta: TTreeAut, min_var: int):
    def convert_vars(var_list: list, prefix: str) -> dict:
        return {i: int(i[len(prefix) :]) for i in var_list}

    var_prefix = ta.get_var_prefix()
    var_lookup = convert_vars(ta.get_var_order(), var_prefix)
    # var_vis = {i: min_var for i in ta.roots}
    var_vis = {}
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


# In order to canonically and deterministically fold the unfolded and
# normalized UBDA, we need to determine an order in which the states will
# be checked for possible applicable reductions. Lexicographic order (ordered
# by the shortest path from root to the particular state),
# which is similar to DFS, provides such a way.
#
# e.g. path to q1 from root is: low(0), low(0), high(1) edges - 001
# path to q2 from root is: low(0), high(1), low(0) - 010
# thus, lexicographically, q1 comes before q2
#
# This function takes a
def lexicographical_order(ta: TTreeAut) -> list:
    def lexicographic_order_recursive(ta: TTreeAut, state: str, path: str, result, open):
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

    path_dict = {}  # state -> path string
    open = set()
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

    path_list = [path for path in reverse_path_dict.keys()]
    path_list.sort()
    result = []
    for path in path_list:
        result.extend(reverse_path_dict[path])
    return result


# changes box objects on edges to strings of their names ???
# initial try for compatibility with dot/vtf format modules
# NOTE: redundant
def stringify_boxes(ta: TTreeAut):
    for edge in iterate_edges(ta):
        new_box_array = []
        for box in edge.info.box_array:
            if type(box) == type(TTreeAut):
                new_box_array.append(box.name)
            else:
                new_box_array.append(box)
        edge.info.box_array = new_box_array


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# old port-state map creating functions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def get_mapping_old(intersectoid, treeaut):
    mapping = port_to_state_mapping(intersectoid)
    # old_mapping = get_maximal_mapping(intersectoid, treeaut, mapping)
    max_mapping = get_maximal_mapping_fixed(intersectoid, treeaut, mapping)
    # ^^ largest root_distance of "port" nodes (inside intersectoid)
    final_mapping = {i: split_tuple_name(j) for i, j in max_mapping.items()}
    return final_mapping


# This function parses an intersectoid and creates a dictionary with all
# port transitions and all states that begin with them.
# input:
# - an intersectoid "TA"
# output:
def port_to_state_mapping(intersectoid: TTreeAut) -> dict:
    result = {}
    for edge in iterate_edges(intersectoid):
        if edge.info.label.startswith("Port"):
            if edge.info.label not in result:
                result[edge.info.label] = []
            result[edge.info.label].append(edge.src)
    return result


# finds a state furthest from the root so that the mapping is "maximal"
# input:
# - an intersectoid "TA",
# - dictionary of ports and states with port output transitions
# output:
def get_maximal_mapping(intersectoid: TTreeAut, ta: TTreeAut, ports: dict) -> dict:
    mapping = {}
    for port, state_list in ports.items():
        mapping[port] = None
        current_distance = 0  # state, root_distance
        for state in state_list:
            dist = intersectoid.get_root_distance(state)
            if dist > current_distance:
                mapping[port] = state
                current_distance = dist
            elif dist == current_distance:
                current_state = split_tuple_name(mapping[port])
                possible_new_state = split_tuple_name(state)
                current_distance = ta.get_root_distance(current_state)
                new_distance = ta.get_root_distance(possible_new_state)
                if new_distance > current_distance:
                    mapping[port] = state
        if mapping[port] is None:
            raise Exception(f"get_maximal_mapping: {port} mapping not found")
    return mapping


def get_maximal_mapping_fixed(intersectoid: TTreeAut, ta: TTreeAut, ports: dict) -> dict:
    mapping = {}
    for port, state_list in ports.items():
        temp = {}
        mapping[port] = None
        for state in state_list:
            treeaut_state = split_tuple_name(state)
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
# different versions of manipulating the edge targets
# after finding out the mapping (used in tree_aut_folding function)
# ~~deprecated~~, kept for documenting/archiving purposes
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# for i, (map_state, var) in enumerate(mapping.values()):
#     edge.children.insert(idx + i, map_state)
#     if var != var_visibility[map_state]:
#         # create and assign state copy
#         if f"{map_state}{var}" in helper.state_map:
#             mapped_state = helper.state_map[f"{map_state}{var}"]
#             edge.children[idx + i] = mapped_state
#             # print(map_state, var, mapped_state)
#             continue
#         new_state = f"{map_state}_{helper.counter}"
#         helper.state_map[f"{map_state}{var}"] = new_state
#         # helper.state_map[f"{map_state}{var}"] = new_state
#         edge_dict_copy = {}
#         result.transitions[new_state] = edge_dict_copy
#         for k, e in result.transitions[map_state].items():
#             if e.is_full_self_loop():
#                 continue
#             edge_copy: TTransition = copy.deepcopy(e)
#             edge_copy.src += f'_{helper.counter}'
#             for index, child in enumerate(e.children):
#                 if child == e.src:
#                     edge_copy.children[index] += f'_{helper.counter}'
#             edge_dict_copy[f'{k}_{helper.counter}'] = edge_copy
#         # for k, e in edge_dict_copy.items():
#             # print("tr_copy_edge", e)
#         edge.children[idx + i] = new_state
#         # print(f"edge.children = {edge.children}, new_state = {new_state}")

#         new_edge = TTransition(new_state, TEdge('LH', [], var), [map_state, map_state])
#         # print("new_edge", new_edge)
#         helper.counter += 1
#         key = f"temp_{helper.counter2}"
#         helper.counter2 += 1
#         # if new_state not in result.transitions:
#         #     result.transitions[new_state] = {}
#         result.transitions[new_state][key] = new_edge


# for i, (map_state, var) in enumerate(mapping.values()):
#     print(mapping)
#     edge.children.insert(idx + i, map_state)
#     if var == var_visibility[map_state]:
#         continue
#     # if var == "":
#         # continue
#     print(f"mapstate = {map_state}, {type(map_state)}, var = {var}, {type(var)}, varvis = {var_visibility[map_state]}")
#     new_state = f"{map_state}-{var}"
#     print(edge, idx+i, edge.children[idx+i], new_state)
#     edge.children[idx+i] = new_state
#     if new_state not in result.transitions:
#         result.transitions[new_state] = {}
#     new_edge = TTransition(new_state, TEdge('LH', [], var), [map_state, map_state])
#     print(f"new_edge = {new_edge}")
#     result.transitions[new_state][f'{helper.counter2}'] = new_edge
#     helper.counter2 += 1
#     original_var = int(var_visibility[map_state][len(helper.var_prefix):])
#     intersectoid_var = int(var[len(helper.var_prefix):])
#     print(f'original = {original_var}, intersectoid = {intersectoid_var}')
#     if original_var > intersectoid_var + 1:
#         new_edge = TTransition(new_state, TEdge('LH', [], ""), [new_state, new_state])
#         print(f"new_edge = {new_edge}")
#         result.transitions[new_state][f'{helper.counter2}'] = new_edge
#         helper.counter2 += 1
