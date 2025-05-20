"""
[file] apply_tables.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Operation tables (similar to Cayley) tables on output symbols of tree automata.
Needed for obtaining box op-products, they follow the common semantics of Boolean operators.
"""

from enum import Enum


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


# the top-right and bottom-left corners are ambiguous in the following operations
# we are not sure whether a port transition is applicable in some cases,
# so we leave it empty for now

# most probably, the whole first row and column should be '-', since we logically
# cannot perform a binary operation on a 'None' type operand


AND_table = [
    ["-", "0", "-", "-"],
    ["0", "0", "0", "0"],
    ["-", "0", "1", "P2"],
    ["-", "0", "P1", "OP"],
]

OR_table = [
    ["-", "-", "1", "-"],
    ["-", "0", "1", "P2"],
    ["1", "1", "1", "1"],
    ["-", "P1", "1", "OP"],
]

XOR_table = [
    ["-", "-", "-", "-"],
    ["-", "0", "1", "P2"],
    ["-", "1", "0", "!P2"],
    ["-", "P1", "!P1", "OP"],
]

IFF_table = [
    ["-", "-", "-", "-"],
    ["-", "1", "0", "!P2"],
    ["-", "0", "1", "P2"],
    ["-", "!P1", "P1", "OP"],
]

IMPLY_table = [
    ["-", "-", "1", "-"],
    ["1", "1", "1", "1"],
    ["-", "0", "1", "P2"],
    ["-", "!P1", "1", "OP"],
]

NAND_table = [
    ["-", "1", "-", "-"],
    ["1", "1", "1", "1"],
    ["-", "1", "0", "!P2"],
    ["-", "1", "!P1", "OP"],
]

NOR_table = [
    ["-", "-", "0", "-"],
    ["-", "1", "0", "!P2"],
    ["0", "0", "0", "0"],
    ["-", "!P1", "0", "OP"],
]

op_lookup = {
    BooleanOperation.AND: AND_table,
    BooleanOperation.OR: OR_table,
    BooleanOperation.XOR: XOR_table,
    BooleanOperation.IFF: IFF_table,
    BooleanOperation.NAND: NAND_table,
    BooleanOperation.NOR: NOR_table,
    BooleanOperation.IMPLY: IMPLY_table,
}

# End of file apply_tables.py
