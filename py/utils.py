"""
[file] utils.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] some helper utilities used throughout other modules
"""


import sys


# boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']
# boxOrder = ['L0', 'L1', 'H0', 'H1', 'X']
boxOrder = ['L0', 'L1', 'H0', 'H1', 'LPort', 'HPort']

boxOrders = {
    "bdd": ['X'],
    "zbdd": ['H0'],
    "tbdd": ['X', 'H0'],
    "cbdd": ['X', 'HPort'],
    "czdd": ['H0', 'X'],
    "esr": ['L0', 'H0', 'X'],
    "full": ['L0', 'H0', 'L1', 'H1', 'X', 'LPort', 'HPort'],
}

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# sorts the state names while ignoring the prefix
def stateNameSort(stateList: list) -> list:
    if stateList == []:
        return []

    prefixLen = 0
    for i in range(len(stateList[0])):
        if not stateList[0][i:].isnumeric():
            prefixLen += 1
    prefix = stateList[0][:prefixLen]
    try:
        myList = [int(i.lstrip(prefix)) for i in stateList]
        myList.sort()
        myList = [f"{prefix}{i}" for i in myList]
    except ValueError:
        myList = [i for i in stateList]
    return myList


def createVarOrder(prefix: str, count: int, start=1):
    return [f"{prefix}{i+start}" for i in range(count)]
