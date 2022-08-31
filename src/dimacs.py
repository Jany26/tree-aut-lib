import os
from bdd import *
from apply import *
from utils import *


def isInt(str):
    try:
        int(str)
        return True
    except ValueError:
        raise Exception(f"{str} is not an integer!")


def dimacsRead(source: str, override=None) -> BDD:
    # for now, we treat cnf as dnf, as they are more natural to parse as BDDs
    if not source.lower().endswith(('.dnf', '.cnf')):
        Exception("unknown format for dimacs parsing")
    file = open(source, 'r')
    base = os.path.basename(source)
    bddName = os.path.splitext(base)[0]
    dimacsType = None
    nodeCounter = 0
    variableCount = 0
    clausuleCount = 0
    branchCount = 0

    result: BDD = BDD(None, None)
    leaf0 = BDDnode(f"t0", 0)
    leaf1 = BDDnode(f"t1", 1)

    for lineNumber, line in enumerate(file, start=1):
        words = line.split()
        if line.startswith("c"):  # comment
            continue

        if line.startswith("p"):  # p dnf varCount clausuleCount
            dimacsType = words[1]  # so far all types are treated as dnf
            if override is not None and override in ['dnf', 'cnf']:
                dimacsType = override
            variableCount = int(words[2])
            clausuleCount = int(words[3])
            continue

        if not isInt(words[0]):
            eprint(
                "dimacsRead():",
                f"skipping unrecoginzed word at line {lineNumber}"
            )
            continue

        variables = []
        for word in words:
            if not isInt(word):
                raise Exception(
                    "dimacsRead():",
                    f"Bad value {word} on line {lineNumber}!"
                )
            variables.append(int(word))

        variables.pop()  # last 0
        sorted(variables, key=abs)  # bottom-up building
        variables.reverse()

        # bottom-up branch building approach
        branchCount += 1
        branch = BDD(f"branch_{branchCount}", None)
        branch.root: BDDnode = leaf1 if dimacsType == 'dnf' else leaf0

        for var in variables:
            current = BDDnode(f"n{nodeCounter}", str(abs(var)))
            nodeCounter += 1
            leaf = leaf0 if dimacsType == 'dnf' else leaf1
            if var > 0:
                if dimacsType == 'dnf':
                    current.attach(leaf, branch.root)
                else:
                    current.attach(branch.root, leaf)
            else:
                if dimacsType == 'dnf':
                    current.attach(branch.root, leaf)
                else:
                    current.attach(leaf, branch.root)
            branch.root = current

        func = 'or' if dimacsType == 'dnf' else 'and'
        result = applyFunction(func, result, branch)

    if clausuleCount != branchCount:
        eprint("dimacsRead(): clausuleCount != branchCount")
    result.name = bddName
    return result


def cacheDumpDNF(dst, cache):
    line = ""
    for value, direction in cache:
        if direction == 0:
            line += '-'
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


def dimacsWriteRecursiveDNF(node: BDDnode, dst, cache: list):
    if node.isLeaf():
        if node.value == 1:
            cacheDumpDNF(dst, cache)
        return

    cache.append((node.value, 0))
    dimacsWriteRecursiveDNF(node.low, dst, cache)
    cache.pop()
    
    cache.append((node.value, 1))
    dimacsWriteRecursiveDNF(node.high, dst, cache)
    cache.pop()
    return


def dimacsWriteIterativeDNF(bdd: BDDnode, dst):
    pass


def cacheDumpCNF(dst, cache):
    line = ""
    for value, direction in cache:
        if direction == 1:
            line += "-"
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


def dimacsWriteRecursiveCNF(node: BDDnode, dst, cache: list):
    if node.isLeaf():
        if node.value == 0:
            cacheDumpCNF(dst, cache)
        return
    cache.append((node.value, 0))
    dimacsWriteRecursiveDNF(node.low, dst, cache)
    cache.pop()
    
    cache.append((node.value, 1))
    dimacsWriteRecursiveDNF(node.high, dst, cache)
    cache.pop()
    return


def dimacsWriteIterativeCNF(bdd: BDDnode, dst):
    pass


def dimacsWrite(bdd: BDD, dst, recursive=True, format='dnf'):
    file = open(dst, "w")
    if recursive is True:
        cache = []
        file.write(f"c {bdd.name}\n")
        varCount = len(bdd.getVariableList())
        if format == 'dnf':
            print("finding 1")
            file.write(f"p dnf {varCount} {bdd.countBranchesIter(1)}\n")
            dimacsWriteRecursiveDNF(bdd.root, file, cache)
        elif format == 'cnf':
            print("finding 0")
            file.write(f"p cnf {varCount} {bdd.countBranchesIter(0)}\n")
            dimacsWriteRecursiveCNF(bdd.root, file, cache)
    else:
        file.write(f"c {bdd.name}\n")
        varCount = len(bdd.getVariableList())
        if format == 'dnf':
            file.write(f"p dnf {varCount} {bdd.countBranchesIter(1)}\n")
            dimacsWriteIterativeDNF(bdd.root, file)
        elif format == 'cnf':
            file.write(f"p cnf {varCount} {bdd.countBranchesIter(0)}\n")
            dimacsWriteIterativeCNF(bdd.root, file)
    file.close()

# End of file dimacs.py
