"""
[file] normalization.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] UBDA Normalization implementation.
Removes equivalent states (i.e. states with equivalent languages
if they were considered roots)
[note] Bottom-up determinization that takes variables into account (they
are considered a part of the edge-symbol).
"""

from io import TextIOWrapper
import itertools
import sys
import os
from typing import Any, Optional

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from tree_automata.automaton import state_name_sort
from helpers.string_manipulation import (
    create_string_from_name_set as macrostring,
    get_var_prefix_from_list,
    get_var_translate,
)


class NormalizationHelper:
    def __init__(self, treeaut: TTreeAut, variables: list[str], verbose: bool, output=None):
        self.treeaut: TTreeAut = treeaut  # copy of the initial TA (un-normalized)
        self.roots: set[str] = set()

        # these transitions after normalization are correct, and will be in the final TA/UBDA
        self.transitions: set[TTransition] = set()
        self.worklist: list[list[str]] = []  # currently considered (macro)states
        self.next_worklist: list[list[str]] = []  # which states are considered in next iteration
        self.var_worklist: dict[str, list] = {var: [] for var in variables}
        self.symbols: dict[str, int] = {s: a for s, a in treeaut.get_symbol_arity_dict().items() if a > 0}
        self.var_prefix = treeaut.get_var_prefix()

        # lookup is a map of stringified list of children to a list of key-edge pairs
        # such that the edge leads to this particular set of children
        # it helps with bottom-up traversal of the UBDA
        self.lookup: dict[str, list[tuple[str, TTransition]]] = {}
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
        if output is not None:
            dir_path = os.path.dirname(output)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
        self.output: TextIOWrapper = sys.stdout if output is None else open(output, "w")

        # child macrostate str -> variable
        # this is used for checking, if the currently considered transition is viable
        # if source state variable is greater than any child variable, the considered edge is not added to the result
        self.var_cache: dict[str, int] = {}
        self.var_translate: dict[str, int] = get_var_translate(self.variables)
        # outvar_cache is just an attempt to fix some erroneous transitions in the result
        self.outvar_cache: dict[str, int] = {}

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

    def debug_print(self, out: Any) -> None:
        if self.verbose:
            if self.output is None:
                print(out)
            else:
                self.output.write(out)
                self.output.write("\n")


def process_possible_edges(children_macrostates: list[list[str]], norm: NormalizationHelper, current_var: int) -> None:
    children_lists = [list(i) for i in itertools.product(*children_macrostates)]
    new_macrostate = set()
    force_var = False
    keys_to_process = []
    varstr = f"{norm.var_prefix}{current_var}"
    for c in children_lists:
        if str(c) not in norm.lookup:
            continue
        possible_edges = norm.lookup[str(c)]
        for key, edge in possible_edges:
            norm.debug_print(f"      > EDGE = {edge}")
            if edge.info.variable not in ["", varstr]:
                continue
            new_macrostate.add(edge.src)
            for child in edge.children:
                if key not in norm.keys:
                    continue
                norm.keys.remove(key)
                keys_to_process.append(key)

    if len(new_macrostate) == 0:
        return
    new_macrostate = state_name_sort(list(new_macrostate))
    if new_macrostate not in norm.next_worklist:
        norm.next_worklist.append(new_macrostate)

    # if self-loop (even partial), then no variable on edge
    # variable appears only if that was the case in the original UBDA
    added_var = None if new_macrostate in children_macrostates else current_var

    # debug print info
    source: str = macrostring(new_macrostate)
    low: str = macrostring(children_macrostates[0])
    high: str = macrostring(children_macrostates[1])
    src_var: Optional[str] = norm.var_cache[source] if source in norm.var_cache else None
    low_var: int = norm.var_cache[low]
    high_var: int = norm.var_cache[high]
    self_loop = source == low or source == high

    # checking for edge relevancy => if failed, edge would disrupt semantics, so it won't be added
    if src_var is not None:
        # first check: source var cannot have a higher variable than a child variable
        # note that var_cache values change during the algorithm
        for child in [low, high]:
            if child not in norm.var_cache:
                raise ValueError(f"ubda_normalization(): cannot obtain cached variable of a child {child}")
            if src_var > norm.var_cache[child]:
                if norm.verbose:
                    norm.debug_print(f"[edge relevancy check failed]: {source} - {src_var} -> {children_macrostates}")
                return
    # however, var_cache is only updated at the end of the iteration

    # NOTE: for now we are not sure if this is correct or not, perhaps normalization has other issues
    # second check: in a self-loop, child variables havesource var cannot have a higher variable than a child variable
    # note that outvar_cache values DO NOT change during the algorithm ->
    # each state can have exactly one variable-marked outgoing edge (non self-loop) ->
    # thus when such an edge is added, the outvar is set

    # if self_loop and source in norm.outvar_cache:
    #     for child in [low, high]:
    #         if child not in norm.outvar_cache:
    #             raise ValueError(f"ubda_normalization(): cannot obtain outgoing variable of a child {child}")
    #         if norm.outvar_cache[source] > norm.outvar_cache[child]:
    #             if norm.verbose:
    #                 norm.debug_print(f"[self loop check failed]: {source} - {src_var} -> {children_macrostates}")
    #             return

    lookup_str = str([new_macrostate, added_var, children_macrostates])
    if lookup_str in norm.processed_edges:
        norm.debug_print(f"{lookup_str}: already in the result")
        return

    norm.debug_print(f"[var check OK]: -> {source} : {src_var} -> [ {low} : {low_var} , {high} : {high_var} ]")
    norm.processed_edges.add(lookup_str)
    norm.transitions.add(
        TTransition(
            source, TEdge("LH", [None] * 2, "" if added_var is None else f"{norm.var_prefix}{added_var}"), [low, high]
        )
    )

    # NOTE: part of the outvar cache fix attempt
    # if added_var is not None and not self_loop:
    #     norm.outvar_cache[source] = added_var

    norm.debug_print(f"[!] edge = {source, 'LH', added_var, [low, high]}")
    for root in norm.treeaut.roots:
        if root in new_macrostate:
            norm.roots.add(source)


def ubda_normalize(ta: TTreeAut, vars: list[str], verbose=False, output=None) -> TTreeAut:
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
    var: int = norm.var_translate[norm.variables.pop(0)]
    for symbol, state_list in ta.get_output_edges().items():
        norm.transitions.add(TTransition(macrostring(state_list), TEdge(symbol, [], f"{var}"), []))
        norm.worklist.append(state_list)
        norm.var_cache[macrostring(state_list)] = var
    norm.debug_print(f"var: {var} | {[macrostring(i) for i in norm.worklist]}")
    while norm.variables != []:
        var = norm.var_translate[norm.variables.pop(0)]
        norm.debug_print(f"var: {var} | {[macrostring(i) for i in norm.worklist]}")
        tuples: list[list[list[str]]] = []
        for i in itertools.product(norm.worklist, repeat=2):  # LH arity => 2
            tuples.append(list(i))
        for t in tuples:
            norm.debug_print(f"   > tuple = {t}")
            process_possible_edges(t, norm, var)
        norm.worklist = norm.next_worklist
        norm.next_worklist = []
        for macrostate in norm.worklist:
            norm.var_cache[macrostring(macrostate)] = var
        # if norm.variables == []:
        #     break
    ta = create_treeaut_from_helper(norm)
    # remove_bad_transitions(ta, vars)
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
    counter: int = 1
    transition_dict: dict[str, dict[str, TTransition]] = {}
    for tr in norm.transitions:
        if tr.src not in transition_dict:
            transition_dict[tr.src] = {}
        transition_dict[tr.src][f"k{counter}"] = tr
        counter += 1
    result = TTreeAut(list(norm.roots), transition_dict, name, norm.treeaut.port_arity)
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
                print("DUPLICATE", edge, f"[ sym={symbol} child={childStr} res={result[symbol][childStr]}]")
                duplicateEdges.append(edge)
            else:
                result[symbol][childStr].add(var)
        visited.add(parent)

    if verbose:
        for edge in duplicateEdges:
            print("is_normalized():", end="")
            print(f"edge {str(edge)} disrupts normalized property")

    return duplicateEdges == []


# End of normalization.py
