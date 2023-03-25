import sys


# boxOrder = ['X', 'LPort', 'HPort', 'L0', 'L1', 'H0', 'H1']
# boxOrder = ['L0', 'L1', 'H0', 'H1', 'X']
boxOrder = ['L0', 'L1', 'H0', 'H1', 'LPort', 'HPort']

boxOrders = {
    "bdd": ['X'],
    "zdd": ['H0'],
    "esrbdd": ['L0', 'H0', 'X'],
    "esrbdd2": ['L1', 'H1', 'X'],
    "abdd-short": ['L0', 'H0', 'L1', 'H1', 'X'],
    # "abdd-full": ['L0', 'H0', 'L1', 'H1', 'LPort', 'HPort', 'X'],
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
