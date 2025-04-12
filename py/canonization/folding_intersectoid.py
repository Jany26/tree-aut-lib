"""
[file] folding_intersectoid.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for manipulating intersectoid construction used in folding.
"""

import copy
import itertools
from typing import Dict, List, Optional, Set, Tuple, Generator

from tree_automata import (
    TTreeAut,
    TTransition,
    TEdge,
    iterate_edges,
    iterate_key_edge_tuples,
    remove_useless_states,
    reachable_bottom_up,
    non_empty_top_down,
)
from canonization.folding_helpers import FoldingHelper
from helpers.string_manipulation import tuple_name, get_first_name_from_tuple_str


def intersectoid_edge_key(e1: TTransition, e2: TTransition) -> str:
    """
    [description]
    Creates a "key" for transition dictionary modified for working with
    an "intersectoid" tree automaton.
    """
    state: str = f"({e1.src}, {e2.src})"
    symb: str = e2.info.label
    var: str = ""
    if e1.info.variable != "" and not symb.startswith("Port"):
        var = f",{e1.info.variable}"

    children: str = f""
    if not e2.info.label.startswith("Port"):
        for i in range(len(e1.children)):
            children += f"({e1.children[i]},{e2.children[i]}),"
        children = children[:-1]

    key: str = f"{state}-<{symb}{var}>-({children})"
    return key


def create_intersectoid(ta: TTreeAut, box: TTreeAut, root: str, helper: FoldingHelper) -> TTreeAut:
    """
    [description]
    Function produces an intersectoid from the 'ta' UBDA and 'box' TA.
    This intersectoid is used in box_finding() to determine the result mapping.
    Intersectoid is similar to a 'product' or an 'intersection' tree automaton.
    state set: Q' = Q_v x Q_b (v = normalized BDA, b = box)

    types of transitions and how they came to be:

    1) (q,s)-{LH}->[(q1,s1),(q2,s2)] | q-{LH}->(q1,q2) is in transition
        dictionary (trd.) of v and s-{LH}->(s1,s2) is in tr.dict. of b

    2) (q,s)-{LH,var}->[(q1,s1),(q2,s2)] | q-{LH,var}->(q1,q2) is in trd.
        of v and s-{LH}->(s1,s2) is in trd. of b

    3) (q,s)-{a}->() | q-{a}->() in trd. of v and s-{a}->() in trd. of b
        // a is a terminal symbol (e.g. '0' or '1') => output transition

    4) (q,s)-{Port_i}->() | s-{Port_i}->() in tr.d of b

    [parameters]
    'ta' - UBDA that is folded (first states of the tuples)
    'box' - TA representing reduction that is analysed (second states of the tuples)
    'root' - state from the UBDA ('ta') where the intersectoid is created from
    'helper' - FoldingHelper instance with additional information used during
    intersectoid creation

    [return]
    Tree automaton/UBDA representing the intersectoid (contains additional
    output symbols/output edges => port transitions), which is used later
    for finding the correct port-state mapping for applying folding reductions.
    """
    helper.key_counter = 0
    edges: dict[str, dict[str, TTransition]] = {}
    visited = set()
    worklist: list[tuple[str, str]] = [(root, b) for b in box.roots]
    helper.temp = []
    while worklist != []:
        current_tuple: tuple[str, str] = worklist.pop(0)
        state: str = tuple_name(current_tuple)
        if state not in edges:
            edges[state] = {}
        if state in visited:
            continue
        for key, ta_edge in ta.transitions[current_tuple[0]].items():  # ta edges
            # skipping edges with already applied reductions
            skip: bool = False
            for b in ta_edge.info.box_array:
                if b is not None:
                    # skipping when trying to reach through a reduced edge, BUT
                    # NOT when the source state can create a port transition
                    skip = True
            for box_edge in box.transitions[current_tuple[1]].values():  # box edges
                # skipping differently labeled (e.g. LH and 0) edges
                if ta_edge.info.label != box_edge.info.label and not box_edge.info.label.startswith("Port"):
                    continue
                if len(ta_edge.children) == 2 and len(box_edge.children) == 2:
                    if ta_edge.children[0] != ta_edge.children[1] and box_edge.children[0] == box_edge.children[1]:
                        continue
                # ports are exceptions to the different labeled exclusion
                # if one of the mismatched labels is a port label,
                # than that "overrules" any other label
                if box_edge.info.label.startswith("Port"):
                    edge_obj: TEdge = TEdge(box_edge.info.label, [], "")
                    edge: TTransition = TTransition(state, edge_obj, [])
                    edges[state][intersectoid_edge_key(ta_edge, box_edge)] = edge
                elif not skip:
                    children: list[str] = []
                    for i in range(len(ta_edge.children)):
                        child: tuple[str, str] = (ta_edge.children[i], box_edge.children[i])
                        children.append(tuple_name(child))
                        worklist.append(child)
                    edge_obj = TEdge(box_edge.info.label, [], f"{ta_edge.info.variable}")
                    if len(children) != 0:
                        helper.temp.append((get_first_name_from_tuple_str(state), key))
                    edge = TTransition(state, edge_obj, children)
                    edges[state][intersectoid_edge_key(ta_edge, box_edge)] = edge
            # for box edge
        # for tree automaton edge
        visited.add(state)
    # end while loop
    roots: list[str] = [f"({root},{b})" for b in box.roots]
    name: str = f"intersectoid({box.name}, {root})"
    result = TTreeAut(roots, edges, name, box.port_arity)
    return result


def create_intersectoid_new(ta: TTreeAut, box: TTreeAut, root: str, helper: FoldingHelper):
    edges: set[TTransition] = set()
    visited: set[str] = set()
    worklist: list[tuple[str, str]] = [(root, b) for b in box.roots]
    while worklist != []:
        ta_state, box_state = worklist.pop(0)
        src: str = tuple_name((ta_state, box_state))
        if src in visited:
            continue
        for ta_edge in ta.transitions[ta_state].values():
            for box_edge in box.transitions[box_state].values():
                # print(f'processing {ta_edge} + {box_edge}')
                edge = process_intersectoid_edge(src, ta_edge, box_edge, helper)
                if edge is None:
                    continue
                # print(f'adding {edge}')
                edges.add(edge)
                new = [c for c in zip(ta_edge.children, box_edge.children) if tuple_name(c) not in visited]
                # print(f'worklist += {new}')
                worklist.extend(new)
        visited.add(src)
    roots = [tuple_name((root, b)) for b in box.roots]
    name = f"intersectoid({root}, {box.name.replace("box", "")})"
    transitions = {}
    for k, e in enumerate(edges, start=1):
        if e.src not in transitions:
            transitions[e.src] = {}
        transitions[e.src][f"k{k}"] = e
    result = TTreeAut(roots, transitions, name, box.port_arity)
    return result


def process_intersectoid_edge(
    src: str, ta_edge: TTransition, box_edge: TTransition, helper: FoldingHelper
) -> Optional[TTransition]:
    """
    UBDA = 'ta', BOX = 'box', Delta = set of transitions
    1) (q,s)-{LH}-->[ (q1,s1),(q2,s2) ] iff
            q-{LH}->(q1,q2) \in Delta(UBDA) and
            s-{LH}->(s1,s2) \in Delta(BOX) and
            s1 = s2 ==> q1 = q2

    2) (q,s)-{LH, var}-->[ (q1,s1),(q2,s2) ] iff
            q-{LH,var}->(q1,q2) \in Delta(UBDA) and
            s-{LH}->(s1,s2) \in Delta(BOX) and
            s1 = s2 ==> q1 = q2

    3) (q,s)-{a}->() where a \in {'0', '1'} iff
            q-{a}->() \in Delta(UBDA) and s-{a}->() \in Delta(BOX) trd. of b

    4) (q,s)-{Port_i}->() | s-{Port_i}->() in Delta(BOX)
    """
    edge_var = helper.state_var_map[ta_edge.src] if ta_edge.src in helper.state_var_map else ""

    # Case 4: If box label is a port, then that "overrules" any other label.
    if box_edge.info.label.startswith("Port"):
        return TTransition(src, TEdge(box_edge.info.label, [], edge_var), [])

    # Skip reduced edges, BUT NOT when the source state can create a port transition.
    # Since we work with a DAG and not a tree, I guess this can happen.
    if any([b is not None for b in ta_edge.info.box_array]):
        return None

    # Skip differently labeled edges (e.g. 'LH' vs. 0/1). Ports are exceptions.
    if ta_edge.info.label != box_edge.info.label:
        return None

    # A little optimization -> this means the box/UBDA paths diverge
    if len(ta_edge.children) == 2 and len(box_edge.children) == 2:
        if ta_edge.children[0] != ta_edge.children[1] and box_edge.children[0] == box_edge.children[1]:
            return None

    # The following merges cases 1, 2 and 3.
    children: list[str] = []
    for i in range(len(ta_edge.children)):
        children.append(tuple_name((ta_edge.children[i], box_edge.children[i])))
    return TTransition(src, TEdge(box_edge.info.label, [], ta_edge.info.variable), children)


def intersectoid_reachability(ta: TTreeAut, var_visibility: dict[str, int]) -> list[str]:
    """
    [description]
    Computes bottom-up reachability within the intersectoid with regards to
    properly labeled port transitions with variables.
    Port transitions without variables are considered invalid.

    [parameters]
    'ta' - intersectoid to analyze

    [return]
    list of states that are reachable without invalid port transitions.

    [note]
    This function is used after creating the intersectoid and saturating the
    transitions with variables where possible.
    """

    def intersectoid_tuple_gen(state: str, parents: list, var_visibility: dict) -> list[list[str]]:
        possibilities = itertools.product(parents, repeat=2)
        result: list[list[str]] = []
        for k in possibilities:
            if state not in k:
                continue
            if k[0] in var_visibility and k[1] in var_visibility:
                if var_visibility[k[0]] != var_visibility[k[1]]:
                    continue
            result.append(list(k))
        return result

    copyta: TTreeAut = copy.deepcopy(ta)
    copyta.reformat_keys()

    edges_to_pop: list[tuple[str, str]] = []
    for edge_dict in copyta.transitions.values():
        for key, edge in edge_dict.items():
            # port edge should be labeled with a variable
            if len(edge.children) == 0:
                if edge.info.label.startswith("Port") and edge.info.variable == "":
                    edges_to_pop.append((edge.src, key))
                continue
            bad: bool = False
            # low = edge.children[0]
            # high = edge.children[1]
            if bad:
                edges_to_pop.append((edge.src, key))

    for src, key in edges_to_pop:
        copyta.transitions[src].pop(key)

    copyta: TTreeAut = remove_useless_states(copyta)
    result: list[str] = reachable_bottom_up(copyta)
    return result


def add_variables_top_down(treeaut: TTreeAut, helper: FoldingHelper) -> None:
    """
    [description]
    Top-down variable saturation. Can compute variables to edges where child
    states do not contain self looping transitions (so it is clear which variables
    can go there) and recursively propagates following variables down from
    each edge that was var-labeled beforehand.

    [parameters]
    'treeaut' - usually an intersectoid to saturate
    'helper' - contains additional information like min_var, max_var, etc.,
    that are useful in this procedure

    [note]
    nothing is returned -> the variables are saturated in situ into 'treeaut'

    TODO: side effect: transitions who disrupt the variable path, i.e. introduce
    a path that can backtrack or repeat a variable, are deleted
    """

    def add_variables(ta: TTreeAut, var: int, state: str, helper: FoldingHelper) -> None:
        if var > helper.max_var + 1:
            return
        for edge in ta.transitions[state].values():
            if edge.src in edge.children:
                return
        for edge in ta.transitions[state].values():
            if edge.info.variable != "":
                edge_var = int(edge.info.variable[len(helper.var_prefix) :])
                if edge_var != var:
                    if helper.verbose:
                        print(f"WARNING: add_variables(): edge {edge} does not agree with var {var}")
                return
            if helper.verbose:
                print(f"add_variables(): adding {helper.var_prefix}{var} to {edge}")
            edge.info.variable = f"{helper.var_prefix}{var}"

    # edge-case 1:
    # if root has no var-labeled edges and has no self-loops,
    # min_var is used to label edges starting from root
    for root in treeaut.roots:
        self_looping = False
        no_vars = True
        for edge in treeaut.transitions[root].values():
            if edge.src in edge.children:
                self_looping = True
            if edge.info.variable != "":
                no_vars = False
        # if not self_looping and no_vars:
        if self_looping or not no_vars:
            continue
        for edge in treeaut.transitions[root].values():
            if helper.verbose:
                print(f"add_variables(): adding {helper.var_prefix}{helper.min_var} to {edge}")
            edge.info.variable = f"{helper.var_prefix}{helper.min_var}"

    # edge-case 2:
    # when using LPort, HPort, possibly even X port, sometimes the port-mapped state
    # can be reached through multiple vars
    var_visibility: dict[str, int] = treeaut.get_var_visibility_deterministic()
    for edge in iterate_edges(treeaut):
        if edge.info.label.startswith("Port") and edge.info.variable == "":
            if edge.src in var_visibility:
                edge.info.variable = f"{helper.var_prefix}{var_visibility[edge.src]}"

    # propagating variable values to lower edges where possible
    for edge in iterate_edges(treeaut):
        if edge.src in edge.children:  # or edge.info.variable == "":
            continue
        if edge.info.variable == "":
            continue
        var = int(edge.info.variable[len(helper.var_prefix) :])
        for child in edge.children:
            add_variables(treeaut, var + 1, child, helper)


def get_port_edge_lookup(intersectoid: TTreeAut) -> Tuple[Dict[str, List[Tuple[str, str]]], Dict[str, Set[str]]]:
    """
    Get list of lookup info tuples (statename, key) for transitions corresponding to ports.
    Also return state -> set of keys dictionary (for the same transitions).
    """
    # each port is mapped to a list of edge lookups - (state, key) tuples
    result: dict[str, list[(str, str)]] = {}

    # which edges can be removed -> map: state -> set of keys in edge_dictionary to remove
    edges: dict[str, set[str]] = {}

    for key, edge in iterate_key_edge_tuples(intersectoid):
        if not edge.info.label.startswith("Port"):
            continue
        if edge.info.label not in result:
            result[edge.info.label] = []
        if edge.src not in edges:
            edges[edge.src] = set()
        edges[edge.src].add(key)
        result[edge.info.label].append((edge.src, key))

    return result, edges


def iterate_port_edge_paths(
    inp: Dict[str, List[Tuple[str, str]]]
):  # -> Generator[None, None, dict[str, tuple[str, str]]]:
    return (dict(zip(inp.keys(), values)) for values in itertools.product(*inp.values()))
    # return dict(zip(inp.keys(), itertools.product(*inp.values())))


def reduce_intersectoid_edges(
    intersectoid: TTreeAut,
    port_mapping: dict[str, tuple[str, str]],
    port_edges: dict[str, list[tuple[str, str]]],
    edge_storage: dict[str, dict[str, TTransition]],
):
    """
    port_mapping - paths to port edges that stay in the intersectoid
    port_edges - for each port there is a list of tuples,
                 which contain edge lookup info (state, edge-key)
    edge_storage - for storing/saving removed edges from the intersectoid,
                   identical structure as TTreeAut transition dictionary
    """
    for port, path_list in port_edges.items():
        (state_to_stay, key_to_stay) = port_mapping[port]
        for state, key in path_list:
            if state == state_to_stay and key == key_to_stay:
                continue
            if state not in edge_storage:
                edge_storage[state] = {}
            if key not in edge_storage[state]:
                edge_storage[state][key] = intersectoid.transitions[state].pop(key)
    # for port1, state, key in port_mapping.items():


def return_reduced_edges(intersectoid: TTreeAut, edge_storage: dict):
    for state, edges in edge_storage.items():
        for key, edge in edges.items():
            intersectoid.transitions[state][key] = edge


def reduce_portable_states(intersectoid: TTreeAut):
    """
    [description]
    This function is used to find out which tuples of port states
    (in multiport boxes => port arity > 1) can be used as a mapping.

    This is computed by trying out all different combinations of port transitions
    (the other port transitions of the same type are temporarily left out)
    and checking if the language of the intersectoid is non-empty.

    If the language of the intersectoid is empty for the particular combination
    of port transitions => the mapping would not be possible and thus these
    are then not considered.

    """

    port_edges, edge_popper = get_port_edge_lookup(intersectoid)
    edge_storage: dict[str, dict[str, TTransition]] = {}
    # candidates: list[dict[str, tuple[str, str]]]] = [i for i in iterate_port_edge_paths(port_edges)]
    for i in iterate_port_edge_paths(port_edges):
        reduce_intersectoid_edges(intersectoid, i, port_edges, edge_storage)
        node, _ = non_empty_top_down(intersectoid)
        if node is not None:
            for port, (state, key) in i.items():
                if key in edge_popper[state]:
                    edge_popper[state].remove(key)

        return_reduced_edges(intersectoid, edge_storage)
        edge_storage = {}
    for state, key_set in edge_popper.items():
        for key in key_set:
            intersectoid.transitions[state].pop(key)


# end folding_intersectoid.py
