# from apply_op_merging import OutputTransition
from typing import Optional


class ApplyEffect:
    def __init__(self, out: Optional[int], port: Optional[int], negation: bool = False, operate: bool = False):
        self.output = out  # If None, assume neither 0 nor 1
        self.port = port  # If None, assume none of { P1, P2, !P1, !P2 }
        self.negation = negation  # If True, negate the result (redirect transitions from 0 to 1 and vice-versa)
        self.operate = operate  # If True, assume OP => recursively continue with the operation


effects: dict[str, ApplyEffect] = {
    "-": ApplyEffect(None, None),
    "0": ApplyEffect(0, None),
    "1": ApplyEffect(1, None),
    "P1": ApplyEffect(None, 0),
    "P2": ApplyEffect(None, 1),
    "!P1": ApplyEffect(None, 0, negation=True),
    "!P2": ApplyEffect(None, 1, negation=True),
    "OP": ApplyEffect(None, None, operate=True),
}


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
