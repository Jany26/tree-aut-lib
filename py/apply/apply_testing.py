import os
from enum import Enum

from formats.format_vtf import export_treeaut_to_vtf
from formats.render_dot import export_to_file
from helpers.utils import box_catalogue
from tree_automata import (
    TEdge,
    TTransition,
    TTreeAut,
    remove_useless_states,
    tree_aut_intersection,
    tree_aut_complement,
    non_empty_bottom_up,
    non_empty_top_down,
)

from apply.equality import tree_aut_equal
import apply.apply_tables_outputs as tables
from apply.box_trees import build_box_tree, BoxTreeNode


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
    labels = {
        "0": "0",
        "1": "1",
        "P1": get_port(aut1),
        "P2": get_port(aut2),
        "OP": f"{get_port(aut1)}_{op.name}_{get_port(aut2)}",
        "!P1": f"{get_port(aut1)}_not",
        "!P2": f"{get_port(aut2)}_not",
    }

    # output symbol to matrix/list index mapping (within the cayley table)
    translation = {"-": 0, "0": 1, "1": 2, "P1": 3, "P2": 3}

    key_idx = result.count_edges() + 1
    for state in result.get_states():
        [s1, s2] = state.lstrip("(").rstrip(")").split(",")
        output_symbol = op_table[translation[map1[s1]]][translation[map2[s2]]]
        if output_symbol == "-":
            continue
        result.transitions[state][f"k{key_idx}"] = TTransition(state, TEdge(labels[output_symbol], [], ""), [])
        key_idx += 1


def test_all_apply_intersectoids():
    result_dict: dict[str, dict[str, str]] = {}
    for operation, _ in op_lookup.items():
        for boxname1 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
            result_dict[boxname1] = {}
            for boxname2 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
                box1 = box_catalogue[boxname1]
                box2 = box_catalogue[boxname2]
                applied = apply_intersectoid_create(operation, box1, box2)
                remove_useless_states(applied)
                applied.name = f"{boxname1}_{operation.name}_{boxname2}"
                applied.reformat_ports()
                print(box1.name, operation.name, box2.name, "=", build_box_tree(applied))
        print("----------------------------------------")
