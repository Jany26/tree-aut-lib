import os
from enum import Enum

from format_vtf import exportTAtoVTF, importTAfromVTF
from render_dot import exportToFile, importTA
from test_data import boxCatalogue
from ta_classes import TEdge, TTransition, TTreeAut

from ta_functions import (
    removeUselessStates,
    treeAutIntersection,
    treeAutComplement,
    nonEmptyBU,
    nonEmptyTD,
)

import apply_tables_outputs


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
    BooleanOperation.AND: apply_tables_outputs.AND_table,
    BooleanOperation.OR: apply_tables_outputs.OR_table,
    BooleanOperation.XOR: apply_tables_outputs.XOR_table,
    BooleanOperation.IFF: apply_tables_outputs.IFF_table,
    BooleanOperation.NAND: apply_tables_outputs.NAND_table,
    BooleanOperation.NOR: apply_tables_outputs.NOR_table,
    BooleanOperation.IMPLY: apply_tables_outputs.IMPLY_table,
}


# more port transitions will later be needed probably
# class OutputTransition(Enum):
#     NO_TRANSITION = 0
#     ZERO_TRANSITION = 1
#     ONE_TRANSITION = 2
#     PORT_TRANSITION_FIRST = 3
#     PORT_TRANSITION_SECOND = 4
#     PORT_TRANSITION_FIRST_NEGATED = 5
#     PORT_TRANSITION_SECOND_NEGATED = 6
#     OPERATION = 7


def get_transition_name(state: str, treeaut: TTreeAut) -> str:
    for tr in treeaut.transitions[state].values():
        tr: TTransition
        if len(tr.children) == 0:
            return tr.info.label
    return "-"


def apply_intersectoid_create(op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut):
    # create an intersection
    result = treeAutIntersection(aut1, aut2)
    # result.reformatKeys()

    # remove any output transition created by the intersection operation
    result.removeOutputTransitions()

    # add output transitions to the skeleton based on the operation tables
    apply_intersectoid_add_output_transitions(result, op, aut1, aut2)
    result.name = f"{aut1.name} {op.name} {aut2.name}"
    return removeUselessStates(result)


def mapStatesToOutputTransitions(aut: TTreeAut, idx: int) -> dict[str, str]:
    result = {}
    for state in aut.getStates():
        result[state] = "-"
        for tr in aut.transitions[state].values():
            if len(tr.children) != 0:
                continue
            result[state] = (
                f"P{idx}" if tr.info.label.startswith("Port") else tr.info.label
            )
    return result


def getPort(t: TTreeAut) -> str:
    for sym in t.getOutputSymbols():
        if sym.startswith("Port"):
            return sym

# def renamePorts(aut: TTreeAut):
#    pass


def apply_intersectoid_add_output_transitions(
    result: TTreeAut, op: BooleanOperation, aut1: TTreeAut, aut2: TTreeAut
):
    # maps an output transition (-/0/1/Port) to each state for cayley table lookup
    # we assume each state has at most 1 output transition (based on the box correctness criteria)
    map1: dict[str, str] = mapStatesToOutputTransitions(aut1, 1)
    map2: dict[str, str] = mapStatesToOutputTransitions(aut2, 2)
    op_table = op_lookup[op]

    # cayley table to output edge label mapping
    labels = {
        "0": "0",
        "1": "1",
        "P1": getPort(aut1),
        "P2": getPort(aut2),
        "OP": f"{getPort(aut1)}_{op.name}_{getPort(aut2)}",
        "!P1": f"{getPort(aut1)}_not",
        "!P2": f"{getPort(aut2)}_not",
    }

    # output symbol to matrix/list index mapping (within the cayley table)
    translation = {"-": 0, "0": 1, "1": 2, "P1": 3, "P2": 3}

    keyIdx = result.countEdges() + 1
    for state in result.getStates():
        [s1, s2] = state.lstrip("(").rstrip(")").split(",")
        output_symbol = op_table[translation[map1[s1]]][translation[map2[s2]]]
        if output_symbol == "-":
            continue
        result.transitions[state][f"k{keyIdx}"] = TTransition(
            state, TEdge(labels[output_symbol], [], ""), []
        )
        keyIdx += 1


def treeAutEqual(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    symbols = box.getSymbolArityDict()
    symbols.update(aut.getSymbolArityDict())

    # aut and co-box == empty => aut subseteq box
    intersection1 = treeAutIntersection(aut, treeAutComplement(box, symbols))
    witness_BU_1, _ = nonEmptyBU(intersection1)
    witness_TD_1, _ = nonEmptyTD(intersection1)
    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None

    # box and co-aut == empty => box subseteq aut
    intersection2 = treeAutIntersection(box, treeAutComplement(aut, symbols))
    witness_BU_2, _ = nonEmptyBU(intersection2)
    witness_TD_2, _ = nonEmptyTD(intersection2)
    box_subset_of_aut = witness_BU_2 is None or witness_TD_2 is None
    if debug:
        print(f"{aut.name} ==? {box.name}")
        print("witness 1")
        witness_BU_1.printNode() if witness_BU_1 is not None else "None"
        print("witness 2")
        witness_BU_2.printNode() if witness_BU_2 is not None else "None"
    return aut_subset_of_box and box_subset_of_aut


def apply_intersectoid_compare(aut: TTreeAut, debug=False):
    for boxname in ["X", "L0", "L1", "H0", "H1", "0", "1", "LPort", "HPort", "IFF0", "IFF1", "IFFPort"]:
        box = boxCatalogue[boxname]
        box.reformatPorts()
        equal = treeAutEqual(aut, box, debug)
        if equal:
            return boxname
    return "?"


def test_all_apply_intersectoids():
    result_dict: dict[str, dict[str, str]] = {}
    for operation, _ in op_lookup.items():
        for boxname1 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort", "IFF0", "IFF1", "IFFPort"]:
            result_dict[boxname1] = {}
            for boxname2 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort", "IFF0", "IFF1", "IFFPort"]:
                box1 = boxCatalogue[boxname1]
                box2 = boxCatalogue[boxname2]
                applied = apply_intersectoid_create(operation, box1, box2)
                removeUselessStates(applied)
                applied.name = f"{boxname1}_{operation.name}_{boxname2}"
                applied.reformatPorts()
                res = apply_intersectoid_compare(applied)
                if res == "?":
                    print()
                    applied = apply_intersectoid_create(operation, box1, box2)
                    removeUselessStates(applied)
                    applied.name = f"{boxname1}_{operation.name}_{boxname2}"
                    applied.reformatPorts()
                    print(applied.get_shortest_state_paths_dict())
                    exportTAtoVTF(applied, f'../data/apply_tests/{operation.name}/{applied.name}.vtf')
                    exportToFile(applied, f'../data/apply_tests/{operation.name}/{applied.name}')
                    res = apply_intersectoid_compare(applied, debug=True)
                    print(applied)
                    if not os.path.exists(f'../data/apply_tests/{operation.name}'):
                        os.makedirs(f'../data/apply_tests/{operation.name}')
                    print()
                else:
                    print(box1.name, operation.name, box2.name, '=', res)
                # result_dict[boxname1][boxname2] = res
        print('----------------------------------------')


if __name__ == "__main__":
    test_all_apply_intersectoids()
    # aut = importTAfromVTF("../data/apply_tests/AND/L1_AND_HPort.vtf")
    # box = boxCatalogue["IFFPort"]
    # aut.reformatPorts()
    # box.reformatPorts()
    # print(treeAutEqual(aut, box))
