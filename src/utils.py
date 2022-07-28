import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']

testVarOrder = [f"x{i+1}" for i in range(10)]
