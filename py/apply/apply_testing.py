from enum import Enum
from typing import Optional, Tuple

from apply.apply_tables_boxes import PortConnectionInfo
from apply.apply_tables_outputs import ApplyEffect, effects
from formats.format_vtf import export_treeaut_to_vtf
from formats.render_dot import export_to_file
from helpers.utils import box_catalogue
from tree_automata import (
    TEdge,
    TTransition,
    TTreeAut,
    remove_useless_states,
    tree_aut_intersection,
)

import apply.apply_tables_outputs as tables
from apply.box_trees import build_box_tree


class BooleanOperation(Enum):
    NOP = 0
    AND = 1
    OR = 2
    XOR = 3
    IFF = 4
    NAND = 5
    NOR = 6
    IMPLY = 7
    NOT = 8  # might make it a separate class since it has a different arity


op_lookup = {
    BooleanOperation.AND: tables.AND_table,
    BooleanOperation.OR: tables.OR_table,
    BooleanOperation.XOR: tables.XOR_table,
    BooleanOperation.IFF: tables.IFF_table,
    BooleanOperation.NAND: tables.NAND_table,
    BooleanOperation.NOR: tables.NOR_table,
    BooleanOperation.IMPLY: tables.IMPLY_table,
}


def get_transition_name(state: str, treeaut: TTreeAut) -> str:
    for tr in treeaut.transitions[state].values():
        tr: TTransition
        if len(tr.children) == 0:
            return tr.info.label
    return "-"


# TODO: somewhere add a map of port-states to ApplyEffect() instances or something similar,
# some data structure saying:
#   - what state is mapped where
#   - and how (negated, not-negated, recursive apply follow)


def apply_intersectoid_create(op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut):
    # create an intersection
    result = tree_aut_intersection(aut1, aut2)
    # result.reformat_keys()

    # remove any output transition created by the intersection operation
    result.remove_output_transitions()

    # add output transitions to the skeleton based on the operation tables
    apply_intersectoid_add_output_transitions(result, op, aut1, aut2)
    result.name = f"{aut1.name} {op.name} {aut2.name}"
    return remove_useless_states(result)


def map_states_to_output_transitions(aut: TTreeAut, idx: int) -> dict[str, str]:
    result = {}
    for state in aut.get_states():
        result[state] = "-"
        for tr in aut.transitions[state].values():
            if len(tr.children) != 0:
                continue
            result[state] = f"P{idx}" if tr.info.label.startswith("Port") else tr.info.label
    return result


def get_port(t: TTreeAut) -> str:
    for sym in t.get_output_symbols():
        if sym.startswith("Port"):
            return sym


def apply_intersectoid_add_output_transitions(
    result: TTreeAut, op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut
) -> None:
    # maps an output transition (-/0/1/Port) to each state for cayley table lookup
    # we assume each state has at most 1 output transition (based on the box correctness criteria)
    map1: dict[str, str] = map_states_to_output_transitions(aut1, 1)
    map2: dict[str, str] = map_states_to_output_transitions(aut2, 2)
    op_table = op_lookup[op]

    # cayley table to output edge label mapping
    # labels = {
    #     "0": "0",
    #     "1": "1",
    #     "P1": get_port(aut1),
    #     "P2": get_port(aut2),
    #     "OP": f"{get_port(aut1)}_{op.name}_{get_port(aut2)}",
    #     "!P1": f"{get_port(aut1)}_not",
    #     "!P2": f"{get_port(aut2)}_not",
    # }

    # output symbol to matrix/list index mapping (within the cayley table)
    translation = {"-": 0, "0": 1, "1": 2, "P1": 3, "P2": 3}

    key_idx = result.count_edges() + 1
    for state in result.get_states():
        [s1, s2] = state.lstrip("(").rstrip(")").split(",")
        output_symbol = op_table[translation[map1[s1]]][translation[map2[s2]]]
        if output_symbol == "-":
            continue
        # result.transitions[state][f"k{key_idx}"]
        portinfo, portname = decide_on_port_name(aut1, aut2, s1, s2, output_symbol)
        result.transitions[state][f"k{key_idx}"] = TTransition(state, TEdge(portname, [], ""), [])
        key_idx += 1


def decide_on_port_name(
    aut1: TTreeAut, aut2: TTreeAut, state1: str, state2: str, sym: str
) -> Tuple[Optional[PortConnectionInfo], str]:
    if sym in ["0", "1"]:
        return (None, sym)
    if sym in ["P1", "!P1"]:
        for edge in aut1.transitions[state1].values():
            if edge.info.label.startswith("Port"):
                return (PortConnectionInfo(state1, None, negation=(sym == "!P1")), edge.info.label)
    if sym in ["P2", "!P2"]:
        for edge in aut2.transitions[state2].values():
            if edge.info.label.startswith("Port"):
                return (PortConnectionInfo(None, state2, negation=(sym == "!P2")), edge.info.label)
    if sym == "OP":
        port1 = aut1.get_output_edges(inverse=True)[state1][0]
        port2 = aut2.get_output_edges(inverse=True)[state2][0]
        return (PortConnectionInfo(state1, state2, recursion=True), f"{port1}_OP_{port2}")
    raise KeyError("Unknown lookup symbol")


translate: dict[str, str] = {
    "X": "x_node",
    "L0": "l0_node",
    "L1": "l1_node",
    "H0": "h0_node",
    "H1": "h1_node",
    "LPort": "lport_node",
    "HPort": "hport_node",
    "n(HPort;LPort)": "iffport_node",
    "n(H0;L0)": "iff0_node",
    "n(H1;L1)": "iff1_node",
    "False": "0",
    "True": "1",
}


def test_all_apply_intersectoids():
    result_dict: dict[str, dict[str, str]] = {}
    for operation, _ in op_lookup.items():
        print(f"box_table_{operation.name} = [")
        print(f"    # X             L0            L1            H0            H1            LPort         HPort")
        for boxname1 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
            strtemp = f"ROW {boxname1}:"
            print(f"    [ ", end="")
            result_dict[boxname1] = {}
            for boxname2 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
                box1 = box_catalogue[boxname1]
                box2 = box_catalogue[boxname2]
                applied = apply_intersectoid_create(operation, box1, box2)
                print(f"{translate[str(build_box_tree(applied))] :<12}", end=", ")
                export_to_file(applied, f"../data/apply_boxes_tests/png/{operation.name.lower()}/{applied.name}")
                export_treeaut_to_vtf(
                    applied, f"../data/apply_boxes_tests/vtf/{operation.name.lower()}/{applied.name}.vtf"
                )
            print(f"], # {boxname1}")
        print(f"]")
