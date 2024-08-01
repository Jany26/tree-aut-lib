"""
[file] normalization.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] UBDA Normalization implementation.
Removes equivalent states (i.e. states with equivalent languages
if they were considered roots)
[note] Bottom-up determinization that takes variables into account (they
are considered a part of the edge-symbol).
"""

from ta_classes import *
from ta_functions import *
from test_data import *
from utils import *


class NormalizationHelper:
    def __init__(self, treeaut: TTreeAut, variables: list, verbose: bool, output):
        self.treeaut = treeaut  # copy of the initial TA (un-normalized)
        self.roots = {}
        self.transitions = []  # these will be in the final TA/UBDA
        self.worklist = []  # currently considered (macro)states
        self.next_worklist = []  # which states are considered in next iteration
        self.symbols = {}
        self.var_worklist: 'dict[str, list]' = {var: [] for var in variables}
        for symbol, arity in treeaut.get_symbol_arity_dict().items():
            if arity > 0:
                self.symbols[symbol] = arity
        self.lookup = {}
        self.edge_lookup = self.edges_to_process_cache_init()
        for edge_dict in treeaut.transitions.values():
            for key, edge in edge_dict.items():
                if str(edge.children) not in self.lookup:
                    self.lookup[str(edge.children)] = []
                self.lookup[str(edge.children)].append((key, edge))
        self.processed_edges = set()
        self.keys = set()
        for edge_dict in treeaut.transitions.values():
            for k in edge_dict.keys():
                self.keys.add(k)
        self.variables = variables[::-1]
        self.verbose = verbose
        self.output = output

    def __repr__(self):
        result = ""
        result += f"roots     = {self.roots}\n"
        result += f"symbols   = {self.symbols}\n"
        result += f"worklist  = {self.worklist}\n"
        result += f"variables = {self.variables}\n"
        result += f"transitions ----------------\n"
        for i in self.transitions:
            result += f" > {i[0]} -- {i[1]} "
            result += f"<{i[2]}> " if i[2] != "" else ""
            result += f"--> {i[3]}\n"
        return result

    def edges_to_process_cache_init(self) -> 'dict[str, set[str]]':
        result = {}
        for edge_dict in self.treeaut.transitions.values():
            for key, edge in edge_dict.items():
                for child in edge.children:
                    if child not in result:
                        result[child] = set()
                    result[child].add(key)
        return result

    def check_for_unprocessed_states(self):
        """
            Checking if some macrostate from current worklist has not yet been fully
            processed = i.e. some edge leading to some state from the macrostate
            has not yet been encountered.
        """
        temp = []
        for macrostate in self.worklist:
            # NOTE: check subset, (to not create redundant "single" states that can be represented by )
            is_fully_processed = True
            for state in macrostate:
                if len(self.edge_lookup[state]) != 0:
                    for k in self.edge_lookup[state]:
                        temp.append(k)
                    is_fully_processed = False
            if not is_fully_processed:
                if macrostate not in self.next_worklist:
                    self.next_worklist.append(macrostate)

    def optimize_redundant_states(self):
        delete_list = []
        for ms in self.next_worklist:
            keep = False
            for s in ms:
                if s not in self.edge_lookup:
                    continue
                if len(self.edge_lookup[s]) != 0:
                    keep = True
            if not keep:
                delete_list.append(ms)
        for ms in delete_list:
            self.next_worklist.remove(ms)

    def print_edge_lookup(self):
        # cleaning norm.edge_lookup
        to_pop = []
        for i,j in self.edge_lookup.items():
            if j == set():
                to_pop.append(i)
        for item in to_pop:
            self.edge_lookup.pop(item)

        result = ""
        for i,j in self.edge_lookup.items():
            result += f"{i} = ["
            for key in j:
                result += f"{key},"
            result = result[:-1]
            result += "] "

    def print_worklist(self, var):
        if self.variables != []:
            old_var = self.variables[0]
        worklist_str = f"var: {var}"
        for i in self.worklist:
            key_set = set()
            for j in i:
                if j not in self.edge_lookup:
                    continue
                for key in self.edge_lookup[j]:
                    key_set.add(key)
            key_list = list(key_set)
            worklist_str += f" | {det_create_name(i)}"
        print(worklist_str)


def process_possible_edges(
    tuple: list,
    norm: NormalizationHelper,
    current_var: str,
    symbol: str
):
    children_lists = [list(i) for i in product(*tuple)]
    new_macrostate = set()
    force_var = False
    keys_to_process = []
    for c in children_lists:
        if str(c) not in norm.lookup:
            continue
        possible_edges = norm.lookup[str(c)]
        for key, edge in possible_edges:
            if norm.verbose:
                if norm.output is None:
                    print("      > EDGE =", edge)
                else:
                    norm.output.write(f"      > EDGE = {edge}\n")
            if edge.info.variable == "" or edge.info.variable == current_var:
                var_string = ""
                if edge.info.variable == current_var:
                    var_string = f" through {current_var}"
                    force_var = True
                new_macrostate.add(edge.src)
                for child in edge.children:
                    if key in norm.edge_lookup[child]:
                        # print(f"  [!] processed edge {key} leading to {child}{var_string}")
                        norm.edge_lookup[child].remove(key)
                        if key in norm.keys:
                            # print(f"  [!] removing key {key}")
                            norm.keys.remove(key)
                            keys_to_process.append(key)
    if len(new_macrostate) != 0:
        new_macrostate = list(new_macrostate)
        new_macrostate = state_name_sort(new_macrostate)
        if new_macrostate not in norm.next_worklist:
            # print(f"    > appending {new_macrostate}")
            norm.next_worklist.append(new_macrostate)

        # if new_macrostate not in norm.var_worklist[current_var]:
        #     norm.var_worklist[current_var].append(new_macrostate)

        # if self-loop (even partial), then no variable on edge
        # variable appears only if that was the case in the original UBDA
        if new_macrostate in tuple or not force_var:
        # if new_macrostate in tuple:
            added_var = ""
        else:
            added_var = current_var

        lookup_str = str([new_macrostate, symbol, added_var, tuple])
        if lookup_str not in norm.processed_edges:
            norm.processed_edges.add(lookup_str)
            norm.transitions.append([new_macrostate, symbol, added_var, tuple])
            if norm.verbose:
                if norm.output is None:
                    print("[!] edge =", [new_macrostate, symbol, added_var, tuple])
                else:
                    norm.output.write(f"[!] edge = {[new_macrostate, symbol, added_var, tuple]}\n")
                # print("  [keys] =", keys_to_process)
            for root in norm.treeaut.roots:
                if root in new_macrostate:
                    norm.roots[str(new_macrostate)] = new_macrostate


# Another approach to normalization. This approach also goes bottom-up,
# but remembers current variable, and always decreases the variable with each
# iteration until it reaches the root.
# This approach mostly does not create unnecessary transitions.
def tree_aut_normalize(ta: TTreeAut, vars: list, verbose=False, output=None) -> TTreeAut:
    norm = NormalizationHelper(ta, vars, verbose, output)
    var = norm.variables.pop(0)  # discrepancy about variables on output edges
    for symbol, state_list in ta.get_output_edges().items():
        norm.transitions.append([state_list, symbol, var, []])
        norm.worklist.append(state_list)
        # norm.var_worklist[var].append(state_list)
    if norm.verbose:
        if norm.output is None:
            print(f"var: {var} | {[det_create_name(i) for i in norm.worklist]}")
        else:
            norm.output.write(f"var: {var} | {[det_create_name(i) for i in norm.worklist]}\n")
    while norm.variables != []:
        old_var = var
        var = norm.variables.pop(0)
        if norm.verbose:
            if norm.output is None:
                print(f"var: {var} | {[det_create_name(i) for i in norm.worklist]}")
            else:
                norm.output.write(f"var: {var} | {[det_create_name(i) for i in norm.worklist]}\n")
        for sym in norm.symbols:
            tuples = []
            # for i in product(norm.var_worklist[old_var], repeat=norm.symbols[sym]):
            for i in product(norm.worklist, repeat=norm.symbols[sym]):
                tuples.append(list(i))
            for t in tuples:
                if norm.verbose:
                    if norm.output is None:
                        print(f"   > tuple = {t}\n")
                    else:
                        norm.output.write(f"   > tuple = {t}\n")
                process_possible_edges(t, norm, var, sym)
            # norm.optimize_redundant_states()
            # norm.check_for_unprocessed_states()
        norm.worklist = norm.next_worklist
        norm.next_worklist = []
        if norm.variables == []:
            break
    ta = create_treeaut_from_helper(norm)
    remove_bad_transitions(ta, vars, norm)
    return ta


# remove edges that do not comply with the "variable order"
#   - either edges that create a chain of same variable edges (x1, x1)
#   - or edges that create a chain of unordered variable edges (x2, x1)
def remove_bad_transitions(ta: TTreeAut, vars: list, norm):
    var_index = {j: i for i, j in enumerate(vars, start=1)}
    max_var_cache = {}
    for edge in iterate_edges(ta):
        if edge.info.variable == "":
            continue
        if (
            edge.src not in max_var_cache or
            max_var_cache[edge.src] < var_index[edge.info.variable]
        ):
            max_var_cache[edge.src] = var_index[edge.info.variable]

    flagged_edges = set()

    for edge_dict in ta.transitions.values():
        for key, edge in edge_dict.items():
            if edge.info.variable == "" or edge.src not in max_var_cache:
                continue
            for child in edge.children:
                if child not in max_var_cache:
                    continue
                if max_var_cache[child] <= max_var_cache[edge.src]:
                    flagged_edges.add((edge.src, key))

    for src, key in flagged_edges:
        ta.transitions[src].pop(key)


def create_treeaut_from_helper(norm: NormalizationHelper) -> TTreeAut:
    name = f"normalized({norm.treeaut.name})"
    roots = [det_create_name(i) for i in norm.roots.values()]
    roots.sort()
    counter = 1
    transition_dict = {}
    for edge in norm.transitions:
        src_state = det_create_name(edge[0])
        edge_info = TEdge(edge[1], [], edge[2])
        children = [det_create_name(i) for i in edge[3]]
        transition = TTransition(src_state, edge_info, children)
        if src_state not in transition_dict:
            transition_dict[src_state] = {}
        transition_dict[src_state][f"k{counter}"] = transition
        counter += 1
    result = TTreeAut(roots, transition_dict, name, norm.treeaut.port_arity)
    return result

# This function performs a bottom-up check of normalization.
# Each combination of children is supposed to meet parents through
# a few transitions. In normalized UBDA the transitions do not repeat the same
# variable. Either the edges to the specific children list have all
# the variables once or have one "variable-less" edge. (empty string as var)
def is_normalized(ta: TTreeAut, verbose=False) -> bool:
    # lookup = edge symbol -> children array key ->
    # set of variables over all transitions from parent to child
    result: 'dict[str, dict[str, set]]' = {}

    duplicateEdges: 'list[TTransition]' = []

    for symbol, arity in ta.get_symbol_arity_dict().items():
        if arity != 0:
            result[symbol] = {}
    queue = [i for i in ta.roots]
    visited = set()
    while queue != []:
        parent = queue.pop(0)
        if parent in visited:
            continue
        for edge in ta.transitions[parent].values():
            if edge.children == []:
                continue
            for child in edge.children:
                if child not in visited:
                    queue.append(child)
            symbol = edge.info.label
            childStr = str(edge.children)
            if childStr not in result[symbol]:
                result[symbol][childStr] = set()
            var = edge.info.variable
            if (
                var in result[symbol][childStr]
                or (var == "" and len(result[symbol][childStr]) != 0)
                or (var != "" and "" in result[symbol][childStr])
            ):
                duplicateEdges.append(edge)
            else:
                result[symbol][childStr].add(var)
        visited.add(parent)

    if verbose:
        for edge in duplicateEdges:
            eprint("is_normalized():", end="")
            eprint(f"edge {str(edge)[4:]} disrupts normalized property")

    return duplicateEdges == []

# End of normalization.py
