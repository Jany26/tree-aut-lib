"""
[file] normalization.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] UBDA Normalization implementation.
Removes equivalent states (i.e. states with equivalent languages
if they were considered roots)
[note] Bottom-up determinization that takes variables into account (they
are considered a part of the edge-symbol).
"""

import itertools

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from tree_automata.automaton import state_name_sort
from helpers.string_manipulation import create_string_from_name_set


class NormalizationHelper:
    def __init__(self, treeaut: TTreeAut, variables: list[str], verbose: bool, output):
        self.treeaut: TTreeAut = treeaut  # copy of the initial TA (un-normalized)
        self.roots: dict[str, list[str]] = {}

        # transition => (src_macrostate, symbol, variable, list of child macrostates)
        # these transitions after normalization are correct, and will be in the final TA/UBDA
        self.transitions: list[tuple[list[str], str, str, list[list[str]]]] = []
        self.worklist: list[list[str]] = []  # currently considered (macro)states
        self.next_worklist: list[list[str]] = []  # which states are considered in next iteration
        self.symbols: dict[str, int] = {}
        self.var_worklist: "dict[str, list]" = {var: [] for var in variables}
        for symbol, arity in treeaut.get_symbol_arity_dict().items():
            if arity > 0:
                self.symbols[symbol] = arity
        self.lookup: dict[str, list[tuple[str, TTransition]]] = {}  #

        # NOTE: norm.edge_lookup is mostly redundant, no?
        # since it basically just mirrors self.treeaut.transitions
        # except the lowest level is not a dict key->transition, but a set of keys.
        self.edge_lookup: dict[str, set[str]] = self.edges_to_process_cache_init()
        for edge_dict in treeaut.transitions.values():
            for key, edge in edge_dict.items():
                if str(edge.children) not in self.lookup:
                    self.lookup[str(edge.children)] = []
                self.lookup[str(edge.children)].append((key, edge))
        self.processed_edges: set[str] = set()

        # norm.keys = all keys of the initial tree automaton, mostly debugging, now redundant
        self.keys: set[str] = set()
        for edge_dict in treeaut.transitions.values():
            for k in edge_dict.keys():
                self.keys.add(k)
        self.variables: list[str] = variables[::-1]
        self.verbose: bool = verbose
        self.output: str = output

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

    def edges_to_process_cache_init(self) -> dict[str, set[str]]:
        """
        Return a dictionary that assigns to each state a set of transition keys that start from that state.
        """
        result: dict[str, set[str]] = {}
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
        temp: list[str] = []
        for macrostate in self.worklist:
            # NOTE: check subset, (to not create redundant "single" states that can be represented by )
            is_fully_processed: bool = True
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
        for i, j in self.edge_lookup.items():
            if j == set():
                to_pop.append(i)
        for item in to_pop:
            self.edge_lookup.pop(item)

        result = ""
        for i, j in self.edge_lookup.items():
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
            worklist_str += f" | {create_string_from_name_set(i)}"
        print(worklist_str)


def process_possible_edges(
    children_macrostates: list[list[str]], norm: NormalizationHelper, current_var: str, symbol: str
):
    children_lists = [list(i) for i in itertools.product(*children_macrostates)]
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
        if new_macrostate in children_macrostates or not force_var:
            # if new_macrostate in tuple:
            added_var = ""
        else:
            added_var = current_var

        lookup_str = str([new_macrostate, symbol, added_var, children_macrostates])
        if lookup_str not in norm.processed_edges:
            norm.processed_edges.add(lookup_str)
            norm.transitions.append(tuple([new_macrostate, symbol, added_var, children_macrostates]))
            if norm.verbose:
                if norm.output is None:
                    print("[!] edge =", [new_macrostate, symbol, added_var, children_macrostates])
                else:
                    norm.output.write(f"[!] edge = {[new_macrostate, symbol, added_var, children_macrostates]}\n")
                # print("  [keys] =", keys_to_process)
            for root in norm.treeaut.roots:
                if root in new_macrostate:
                    norm.roots[str(new_macrostate)] = new_macrostate


def ubda_normalize(ta: TTreeAut, vars: list, verbose=False, output=None) -> TTreeAut:
    """
    Another approach to normalization. This approach also goes bottom-up,
    but remembers current variable, and always decreases the variable with each
    iteration until it reaches the root.
    This approach mostly does not create unnecessary transitions.

    Normalization is similar to determinization, thus works with sets of states
    (represented as lists ordered using state_name_sort()).
    """
    norm = NormalizationHelper(ta, vars, verbose, output)

    # NOTE: discrepancy about variables on output edges
    # if the BDA is defined over variables x(1) to x(n),
    # then output edges will have variable x(n+1)
    var: str = norm.variables.pop(0)
    for symbol, state_list in ta.get_output_edges().items():
        norm.transitions.append(tuple([state_list, symbol, var, []]))
        norm.worklist.append(state_list)
        # norm.var_worklist[var].append(state_list)
    if norm.verbose:
        if norm.output is None:
            print(f"var: {var} | {[create_string_from_name_set(i) for i in norm.worklist]}")
        else:
            norm.output.write(f"var: {var} | {[create_string_from_name_set(i) for i in norm.worklist]}\n")
    while norm.variables != []:
        old_var: str = var
        var: str = norm.variables.pop(0)
        if norm.verbose:
            if norm.output is None:
                print(f"var: {var} | {[create_string_from_name_set(i) for i in norm.worklist]}")
            else:
                norm.output.write(f"var: {var} | {[create_string_from_name_set(i) for i in norm.worklist]}\n")
        for sym in norm.symbols:
            tuples: list[list[list[str]]] = []
            # for i in product(norm.var_worklist[old_var], repeat=norm.symbols[sym]):
            for i in itertools.product(norm.worklist, repeat=norm.symbols[sym]):
                tuples.append(list(i))
            for t in tuples:
                if norm.verbose:
                    if norm.output is None:
                        print(f"   > tuple = {t}")
                    else:
                        norm.output.write(f"   > tuple = {t}\n")
                process_possible_edges(t, norm, var, sym)
                # NOTE: some sort of optimization is needed for redundant edges
                # e.g. cycles through variables, or edges from higher variable states "back" to lower variable states
                # that semantically mean deciding over the same variables more than once
            # norm.optimize_redundant_states()
            # norm.check_for_unprocessed_states()
        norm.worklist = norm.next_worklist
        norm.next_worklist = []
        if norm.variables == []:
            break
    ta = create_treeaut_from_helper(norm)
    remove_bad_transitions(ta, vars)
    return ta


def remove_bad_transitions(ta: TTreeAut, vars: list[str]) -> None:
    """
    Remove edges that do not comply with the "variable order":
    - either edges that create a chain of same variable edges (x1, x1)
    - or edges that create a chain of disordered variable edges (x2, x1) if the order is x1 -> x2 -> ...
    """
    var_index: dict[int, str] = {j: i for i, j in enumerate(vars, start=1)}
    max_var_cache: dict[str, str] = {}  # state -> (max) variable found, which will be kept in the final UBDA
    for edge in iterate_edges(ta):
        if edge.info.variable == "":
            continue
        if edge.src not in max_var_cache or max_var_cache[edge.src] < var_index[edge.info.variable]:
            max_var_cache[edge.src] = var_index[edge.info.variable]

    flagged_edges: set[tuple[str, str]] = set()  # state, key tuple for edge lookup

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
    """
    Build the result using the stored data in the normalization helper.
    Mainly turn the macrostates (lists of states) into state "strings".
    """
    name: str = f"normalized({norm.treeaut.name})"
    roots: list[str] = [create_string_from_name_set(i) for i in norm.roots.values()]
    roots.sort()
    counter: int = 1
    transition_dict: dict[str, dict[str, TTransition]] = {}
    for edge in norm.transitions:
        src_state: str = create_string_from_name_set(edge[0])
        edge_info = TEdge(edge[1], [], edge[2])
        children: list[str] = [create_string_from_name_set(i) for i in edge[3]]
        transition = TTransition(src_state, edge_info, children)
        if src_state not in transition_dict:
            transition_dict[src_state] = {}
        transition_dict[src_state][f"k{counter}"] = transition
        counter += 1
    result = TTreeAut(roots, transition_dict, name, norm.treeaut.port_arity)
    return result


def is_normalized(ta: TTreeAut, verbose=False) -> bool:
    """
    This function performs a bottom-up check of normalization.
    Each combination of children is supposed to meet parents through
    a few transitions. In normalized UBDA the transitions do not repeat the same
    variable. Either the edges to the specific children tuple have all
    the variables once or have one "variable-less" edge. (empty string as var)
    """
    # lookup = edge symbol -> children array key -> set of variables
    # over all transitions from parent to child (empty string "" for unlabeled transitions)
    result: dict[str, dict[str, set[str]]] = {}

    duplicateEdges: list[TTransition] = []

    for symbol, arity in ta.get_symbol_arity_dict().items():
        if arity != 0:
            result[symbol] = {}
    queue: list[str] = [i for i in ta.roots]
    visited: set[str] = set()
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
            symbol: str = edge.info.label
            childStr: str = str(edge.children)
            if childStr not in result[symbol]:
                result[symbol][childStr] = set()
            var: str = edge.info.variable
            if (
                var in result[symbol][childStr]
                or (var == "" and len(result[symbol][childStr]) != 0)
                or (var != "" and "" in result[symbol][childStr])
            ):
                print("DUPLICATE", edge)
                duplicateEdges.append(edge)
            else:
                result[symbol][childStr].add(var)
        visited.add(parent)

    if verbose:
        for edge in duplicateEdges:
            print("is_normalized():", end="")
            print(f"edge {str(edge)[4:]} disrupts normalized property")

    return duplicateEdges == []


# End of normalization.py
