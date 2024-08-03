"""
[file] utils.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] some helper utilities used throughout other modules
"""

import sys


# boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']
# boxOrder = ['L0', 'L1', 'H0', 'H1', 'X']
box_order = ["L0", "L1", "H0", "H1", "LPort", "HPort"]

box_orders = {
    "bdd": ["X"],
    "zbdd": ["H0"],
    "tbdd": ["X", "H0"],
    "cbdd": ["X", "HPort"],
    "czdd": ["H0", "X"],
    "esr": ["L0", "H0", "X"],
    "full": ["L0", "H0", "L1", "H1", "X", "LPort", "HPort"],
}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# sorts the state names while ignoring the prefix
def state_name_sort(states: list) -> list:
    if states == []:
        return []

    prefix_len = 0
    for i in range(len(states[0])):
        if not states[0][i:].isnumeric():
            prefix_len += 1
    prefix = states[0][:prefix_len]
    try:
        result = [int(i.lstrip(prefix)) for i in states]
        result.sort()
        result = [f"{prefix}{i}" for i in result]
    except ValueError:
        result = [i for i in states]
    return result


def create_var_order(prefix: str, count: int, start=1):
    return [f"{prefix}{i+start}" for i in range(count)]
