# from apply_op_merging import OutputTransition

# TODO: use a structure/class to represent the resulting output transition:
# - attributes:
#
#       - output: bool
#               (if true, consider output_value, if false, consider port)
#
#       - output_value: bool
#               (true / false) => if output == True, output_value is relevant
#               true => '1' port transition, false => '0' port transition
#
#       - port: bool
#               (if true, consider port_placement)
#
#       - port_placement: enum
#               - enum: NONE (default, error), FIRST (ignore the second operand, use the ), Second, Combination (recursively apply boolean function on both)
#
#       - port_to_state map
#               - correctly map the output states to the port (maybe rethink port flag/port_placement enum/port_to_state map)
#
#       - negation flag: bool
#               - if true, the result is recursively propagated downwards (apply
#                   function used from here on out will flip transitions to zero-output
#                   nodes so that they lead to one-output nodes and vice-versa

AND_table = [
    ["-", "0", "-", "-"],
    ["0", "0", "0", "0"],
    ["-", "0", "1", "P2"],
    ["-", "0", "P1", "OP"],
]

# the top-right and bottom-left corners are ambiguous in the following operations
# we are not sure whether a port transition is applicable in some cases,
# so we leave it empty for now

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
