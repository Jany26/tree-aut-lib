"""
[file] witness.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Isomorphism checks of two tree automata.
"""

# naive brute force isomorphism check of 2 tree automata
# also a variant that ignores the specificity of port transitions,
# only looks whether "some" outgoing port transition is present in a state

import itertools
from typing import Generator, Optional

from tree_automata import TTransition, TTreeAut


def generate_state_mappings(list1: list[str], list2: list[str]) -> Generator[dict[str, str], None, None]:
    """
    Generate mappings from states of the first tree automaton to states of the second automaton.
    Afterwards, these mappings will be checked to see if isomorphism holds.
    """
    for p in itertools.permutations(list2):
        yield dict(map(lambda i, j: (i, j), list1, list(p)))


def check_output_edges(
    state_map: dict[str, str],
    output_map_1: dict[str, list[str]],
    output_map_2: dict[str, list[str]],
    ignore_ports: bool,
) -> bool:
    """
    Before checking transitions with arity >= 1, check whether there is a way
    to map output transitions to each other (1:1 bijection).
    """
    if ignore_ports:
        rename_ports(output_map_1)
        rename_ports(output_map_2)
    for s1, s2 in state_map.items():
        if (s1 in output_map_1) != (s2 in output_map_2):
            return False
        if s1 not in output_map_1:
            continue
        for sym in output_map_1[s1]:
            if sym not in output_map_2[s2]:
                return False
        for sym in output_map_2[s2]:
            if sym not in output_map_1[s1]:
                return False
    return True


def rename_ports(output_map):
    """
    If the isomorphism check ignores ports, this function will rename all port transitions
    to the same label = "Port", thus ignoring semantics hidden within their indices etc.
    """
    for _, out_edges in output_map.items():
        for i in range(len(out_edges)):
            if out_edges[i].startswith("Port"):
                out_edges[i] = "Port"


def check_edge_counts(state_map: dict, edge_map_1: dict, edge_map_2: dict) -> bool:
    """
    Preliminary check of isomorphism comparing edge counts of states from the given mapping.
    Allows for early exit in many cases.
    """
    for s1, s2 in state_map.items():
        if edge_map_1[s1] != edge_map_2[s2]:
            return False
    return True


def compare_edges(state_map: dict, edge1: TTransition, edge2: TTransition) -> bool:
    """
    Return True if the edges are the same with regards to the given state mapping.
    """
    if edge2.src != state_map[edge1.src]:
        return False
    if edge1.info.label != edge2.info.label:
        return False
    if edge1.info.box_array != edge2.info.box_array:
        return False
    if edge1.info.variable != edge2.info.variable:
        return False
    for i in range(len(edge1.children)):
        if state_map[edge1.children[i]] != edge2.children[i]:
            return False
    return True


def tree_aut_isomorphic(aut1: TTreeAut, aut2: TTreeAut, ignore_ports=False) -> dict[str, str]:
    """
    Check the isomorphism of two tree automata/UBDAs.
    When not isomorphic, returns empty dictionary {}
    when isomorphic, returns a dictionary -> state to state bijection

    ignore_ports = when True, ports will not be checked literally,
    but only whether there is a port present or not (if "Port" prefix is present).

    Note:
    Check every possible bijection -> O(n!) complexity.
    Since we will use this mainly for checking "boxes" (small - max. 10 states),
    it is sufficient, since this is the simplest way to implement isomorphism checks.
    """

    # isomorphic automata have to have the same number of states
    outputs_1: dict[str, list[str]] = aut1.get_output_edges(inverse=True)
    outputs_2: dict[str, list[str]] = aut2.get_output_edges(inverse=True)

    edge_counts_1: dict[str, int] = aut1.get_edge_counts()
    edge_counts_2: dict[str, int] = aut2.get_edge_counts()

    # check total state and edge counts
    states_1: list[str] = aut1.get_states()
    states_2: list[str] = aut2.get_states()
    if len(states_1) != len(states_2):
        return {}
    if aut1.count_edges() != aut2.count_edges():
        return {}

    # early_exit = False
    for state_map in generate_state_mappings(states_1, states_2):
        if not check_output_edges(state_map, outputs_1, outputs_2, ignore_ports):
            continue
        if not check_edge_counts(state_map, edge_counts_1, edge_counts_2):
            continue
        early_exit: bool = False  # when a state has some edge not found in its equivalent, skip to another mapping
        for s1, s2 in state_map.items():  # check each state to state mapping
            # check non output edges (edgesets only contain edges with arity > 0)
            edgeset1: set[str] = set([k for k, e in aut1.transitions[s1].items() if len(e.children) != 0])
            edgeset2: set[str] = set([k for k, e in aut2.transitions[s2].items() if len(e.children) != 0])
            for k1 in edgeset1:
                pair: Optional[str] = None
                for k2 in edgeset2:
                    edges_are_equal = compare_edges(state_map, aut1.transitions[s1][k1], aut2.transitions[s2][k2])
                    if edges_are_equal:  # equivalent edges -> check others
                        pair = k2
                        break
                if pair is None:  # some edge from s1 has no equivalent edge -> wrong mapping
                    early_exit = True
                    break
                else:
                    edgeset2.remove(k2)
            if early_exit:
                break
        if early_exit:
            continue
        return state_map
    return {}


# End of file isomorphism.py
