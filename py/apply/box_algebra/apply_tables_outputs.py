# from apply_op_merging import OutputTransition
from typing import Optional

AND_table = [
    ["-", "0", "-", "-"],
    ["0", "0", "0", "0"],
    ["-", "0", "1", "P2"],
    ["-", "0", "P1", "OP"],
]

# the top-right and bottom-left corners are ambiguous in the following operations
# we are not sure whether a port transition is applicable in some cases,
# so we leave it empty for now

# most probably, the whole first row and column should be '-', since we logically
# cannot perform a binary operation on a 'None' type operand

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
