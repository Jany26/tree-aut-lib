from cgi import print_environ
from enum import Enum

from format_vtf import exportTAtoVTF
from render_dot import exportToFile
from test_data import boxCatalogue
from ta_classes import TEdge, TTransition, TTreeAut

from ta_functions import (
    removeUselessStates,
    treeAutIntersection,
    treeAutComplement,
    treeAutDeterminization,
    nonEmptyBU,
    nonEmptyTD,
)

import apply_op_tables


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
    BooleanOperation.AND: apply_op_tables.AND_table,
    BooleanOperation.OR: apply_op_tables.OR_table,
    BooleanOperation.XOR: apply_op_tables.XOR_table,
    BooleanOperation.IFF: apply_op_tables.IFF_table,
    BooleanOperation.NAND: apply_op_tables.NAND_table,
    BooleanOperation.NOR: apply_op_tables.NOR_table,
    BooleanOperation.IMPLY: apply_op_tables.IMPLY_table,
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
    result.reformatKeys()

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
        "!P1": f"not {getPort(aut1)}",
        "!P2": f"not {getPort(aut2)}",
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


def treeAutEqual(aut: TTreeAut, box: TTreeAut) -> bool:
    symbols = box.getSymbolArityDict()
    symbols.update(aut.getSymbolArityDict())
    aut_complement = treeAutComplement(aut, symbols)
    box_complement = treeAutComplement(box, symbols)

    # aut and co-box == empty => aut subseteq box
    intersection1 = treeAutIntersection(aut, box_complement)
    witness_BU_1, _ = nonEmptyBU(intersection1)
    witness_TD_1, _ = nonEmptyTD(intersection1)
    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None

    # box and co-aut == empty => box subseteq aut
    intersection2 = treeAutIntersection(box, aut_complement)
    witness_BU_2, _ = nonEmptyBU(intersection2)
    witness_TD_2, _ = nonEmptyTD(intersection2)
    box_subset_of_aut = witness_BU_2 is None or witness_TD_2 is None

    return aut_subset_of_box and box_subset_of_aut


def apply_intersectoid_compare(aut: TTreeAut):
    for boxname in ["X", "L0", "L1", "H0", "H1", "0", "1"]:
        box = boxCatalogue[boxname]
        equal = treeAutEqual(aut, box)
        if equal:
            return boxname
    return "?"


if __name__ == "__main__":
    for operation, table in op_lookup.items():
        result_dict: dict[str, dict[str, str]] = {}
        for boxname1 in ["X", "L0", "L1", "H0", "H1"]:
            result_dict[boxname1] = {}
            for boxname2 in ["X", "L0", "L1", "H0", "H1"]:
                box1 = boxCatalogue[boxname1]
                box2 = boxCatalogue[boxname2]
                applied = apply_intersectoid_create(operation, box1, box2)
                removeUselessStates(applied)
                # print(box1.name, operation.name, box2.name)
                applied.name = f"{boxname1}_{operation.name}_{boxname2}"
                # exportToFile(applied, f'{operation.name}/{applied.name}')
                exportTAtoVTF(applied, f'../data/apply_tests/{operation.name}/{applied.name}.vtf')
                res = apply_intersectoid_compare(applied)
                result_dict[boxname1][boxname2] = res
                # print(box1.getOutputEdges(inverse=True))
                # exit()
