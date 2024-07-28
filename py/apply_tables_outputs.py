# from apply_op_merging import OutputTransition

AND_table = [
    ['-', '0', '-', '-'],
    ['0', '0', '0', '0'],
    ['-', '0', '1', 'P2'],
    ['-', '0', 'P1', 'OP']
]

# the top-right and bottom-left corners are ambigious in the following operations
# we are not sure whether a port transition is applicable in some cases,
# so we leave it empty for now

OR_table = [
    ['-', '-', '1', '-'],
    ['-', '0', '1', 'P2'],
    ['1', '1', '1', '1'],
    ['-', 'P1', '1', 'OP']
]

XOR_table = [
    ['-', '-', '-', '-'],
    ['-', '0', '1', 'P2'],
    ['-', '1', '0', '!P2'],
    ['-', 'P1', '!P1', 'OP']
]

IFF_table = [
    ['-', '-', '-', '-'],
    ['-', '1', '0', '!P2'],
    ['-', '0', '1', 'P2'],
    ['-', '!P1', 'P1', 'OP']
]

IMPLY_table = [
    ['-', '-', '1', '-'],
    ['1', '1', '1', '1'],
    ['-', '0', '1', 'P2'],
    ['-', '!P1', '1', 'OP']
]

NAND_table = [
    ['-', '1', '-', '-'],
    ['1', '1', '1', '1'],
    ['-', '1', '0', '!P2'],
    ['-', '1', '!P1', 'OP']
]

NOR_table = [
    ['-', '-', '0', '-'],
    ['-', '1', '0', '!P2'],
    ['0', '0', '0', '0'],
    ['-', '!P1', '0', 'OP']
]

# alternative ways of representing the apply operation cayley tables

# AND_table = {
#     OutputTransition.NO_TRANSITION: {
#         OutputTransition.NO_TRANSITION: OutputTransition.NO_TRANSITION,
#         OutputTransition.ZERO_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.ONE_TRANSITION: OutputTransition.NO_TRANSITION,
#         OutputTransition.PORT_TRANSITION_SECOND: OutputTransition.NO_TRANSITION,
#     },
#     OutputTransition.ZERO_TRANSITION: {
#         OutputTransition.NO_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.ZERO_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.ONE_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.PORT_TRANSITION_SECOND: OutputTransition.ZERO_TRANSITION,
#     },
#     OutputTransition.ONE_TRANSITION: {
#         OutputTransition.NO_TRANSITION: OutputTransition.NO_TRANSITION,
#         OutputTransition.ZERO_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.ONE_TRANSITION: OutputTransition.ONE_TRANSITION,
#         OutputTransition.PORT_TRANSITION_SECOND: OutputTransition.PORT_TRANSITION_SECOND,
#     },
#     OutputTransition.PORT_TRANSITION_FIRST: {
#         OutputTransition.NO_TRANSITION: OutputTransition.NO_TRANSITION,
#         OutputTransition.ZERO_TRANSITION: OutputTransition.ZERO_TRANSITION,
#         OutputTransition.ONE_TRANSITION: OutputTransition.PORT_TRANSITION_ONE,
#         OutputTransition.PORT_TRANSITION_SECOND: OutputTransition.OPERATION,
#     }
# }

# AND_table_strings = {
#     '-': {'-': '-', '0': '-', '1': '-', 'P2': '-',},
#     '0': {'-': '-', '0': '-', '1': '-', 'P2': '-',},
#     '1': {'-': '-', '0': '-', '1': '-', 'P2': '-',},
#     'P1': {'-': '-', '0': '-', '1': '-', 'P2': '-',}
# }
