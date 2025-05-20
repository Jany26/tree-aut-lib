"""
[file] algebra_generate.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Implementation of creating a box op-product.
Box op-product is a tree automata intersection with specific output transition adding).
"""

from typing import Optional, Tuple

from apply.box_algebra.port_connection import PortConnectionInfo
from apply.box_algebra.apply_tables import BooleanOperation, op_lookup
from tree_automata import (
    TTreeAut,
    TTransition,
    TEdge,
    remove_useless_states,
    tree_aut_intersection,
)


def apply_intersectoid_create(
    op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut
) -> tuple[TTreeAut, dict[str, PortConnectionInfo]]:
    """
    Create 'op'-product of boxes 'aut1' and 'aut2' (main function).
    """
    # create an intersection
    result = tree_aut_intersection(aut1, aut2)

    # remove any output transition created by the intersection operation
    result.remove_output_transitions()

    # add output transitions to the skeleton based on the operation tables
    port_connection_map = apply_intersectoid_add_output_transitions(result, op, aut1, aut2)
    result.name = f"{aut1.name} {op.name} {aut2.name}"
    trim_result = remove_useless_states(result)
    return trim_result, port_connection_map


def map_states_to_output_transitions(aut: TTreeAut, idx: int) -> dict[str, str]:
    result = {}
    for state in aut.get_states():
        result[state] = "-"
        for tr in aut.transitions[state].values():
            if len(tr.children) != 0:
                continue
            result[state] = f"P{idx}" if tr.info.label.startswith("Port") else tr.info.label
    return result


def apply_intersectoid_add_output_transitions(
    result: TTreeAut, op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut
) -> dict[str, PortConnectionInfo]:
    """
    Correctly add output transitions to 'result' ('op'-product of 'aut1' 'aut2')
    based on the operation tables (from 'apply_tables.py')
    """
    # maps an output transition (-/0/1/Port) to each state for cayley table lookup
    # we assume each state has at most 1 output transition (based on the box correctness criteria)
    map1: dict[str, str] = map_states_to_output_transitions(aut1, 1)
    map2: dict[str, str] = map_states_to_output_transitions(aut2, 2)
    op_table = op_lookup[op]

    # output symbol to matrix/list index mapping (within the cayley table)
    translation = {"-": 0, "0": 1, "1": 2, "P1": 3, "P2": 3}

    portmap = {}

    key_idx = result.count_edges() + 1
    for state in result.get_states():
        [s1, s2] = state.lstrip("(").rstrip(")").split(",")
        output_symbol = op_table[translation[map1[s1]]][translation[map2[s2]]]
        if output_symbol == "-":
            continue

        portinfo, portname = decide_on_port_name(aut1, aut2, s1, s2, output_symbol, op)
        portmap[state] = portinfo

        result.transitions[state][f"k{key_idx}"] = TTransition(state, TEdge(portname, [], ""), [])
        key_idx += 1
    return portmap


def decide_on_port_name(
    aut1: TTreeAut, aut2: TTreeAut, state1: str, state2: str, sym: str, op: BooleanOperation
) -> Tuple[Optional[PortConnectionInfo], str]:
    """
    Based on symbolic names from apply_tables, create correct labels for port transitions.

    [return]
    a tuple of PortConnectionInfo and the transition label (string)
    - PortConnectionInfo contains semantics needed in correct apply node-mapping and recursion guiding,
    absorption laws etc.
    """
    portmap1 = {i: idx for idx, (_, i) in enumerate(aut1.get_port_order())}
    portmap2 = {i: idx for idx, (_, i) in enumerate(aut2.get_port_order())}
    if sym in ["0", "1"]:
        return (None, sym)
    if sym in ["P1", "!P1"]:
        for edge in aut1.transitions[state1].values():
            if edge.info.label.startswith("Port"):
                return (PortConnectionInfo(portmap1[state1], None, negation=(sym == "!P1")), edge.info.label)
    if sym in ["P2", "!P2"]:
        for edge in aut2.transitions[state2].values():
            if edge.info.label.startswith("Port"):
                return (PortConnectionInfo(None, portmap2[state2], negation=(sym == "!P2")), edge.info.label)
    if sym == "OP":
        port1 = aut1.get_output_edges(inverse=True)[state1][0]
        port2 = aut2.get_output_edges(inverse=True)[state2][0]
        return (PortConnectionInfo(portmap1[state1], portmap2[state2], recursion=True), f"{port1}_{op.name}_{port2}")
    raise KeyError("Unknown lookup symbol")


# End of file apply_intersectoid.py
