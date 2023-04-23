import os
from bdd import *
from apply import *
from utils import *


def isInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


class DimacsHelper:
    def __init__(self):
        self.dimacsType = None
        self.nodeCounter = 0
        self.variableCount = 0
        self.clausuleCount = 0
        self.branchCount = 0


# Reads a file in DIMACS format and stores it into a BDD instance.
#   'source' = path to the file in dimacs format (accepting .dnf and .cnf suffix)
#   'override' = "cnf"/"dnf" -> treat the file as the specified format
#       no override will imply the format from the dimacs preamble)
#   'verbose' = if True, the function will print debug info
#   'horizontalCut' = None by default => treats the function 'as is'
#       if horizontalCut is specified (integer value), every variable of 
#       higher value will be skipped, useful for testing purposes
#   'maxClausules' = None by default => only processes a certain amount of
#       clausules, the rest are skipped (for testing purposes)
def dimacsRead(
    source: str,
    override=None,
    verbose=False,
    horizontalCut=None,
    maxClausules=None
) -> BDD:
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

    processedClausules = 1
    for lineNumber, line in enumerate(file, start=1):
        words = line.strip().split()
        if line.startswith("c"):  # comment
            continue

        if line.startswith("p"):  # p dnf variableCount clausuleCount
            dimacsType = words[1]  # so far all types are treated as dnf
            if override is not None and override in ['dnf', 'cnf']:
                dimacsType = override
            variableCount = int(words[2])
            clausuleCount = int(words[3])
            if maxClausules is not None:
                clausuleCount = maxClausules
            if verbose:
                print(f"{dimacsType}, clausules = {clausuleCount}, variables = {variableCount}")
            continue

        if verbose:
            print(f"processing clausule {processedClausules} = {words}")

        if processedClausules > clausuleCount:
            result.name = bddName
            result.reformatNodes()
            return result

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
        if horizontalCut is not None:
            variables = [i for i in variables if abs(i) <= horizontalCut]
        if len(variables) < 2:
            processedClausules += 1
            continue
        variables = sorted(variables, key=abs, reverse=True)
        # print(f" > {variables}")

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
        # print(branch)
        func = 'or' if dimacsType == 'dnf' else 'and'
        if verbose:
            print(branch)
            print(f"applying {func}")
            print()
        result = applyFunction(func, result, branch)
        processedClausules += 1
        if verbose:
            if result.root != None:
                print(result)

    if clausuleCount != branchCount:
        eprint("dimacsRead(): clausuleCount != branchCount")
    result.name = bddName
    result.reformatNodes()
    return result


def cacheDumpDNF(dst, cache):
    line = ""
    for value, direction in cache:
        if direction == 0:
            line += '-'
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


# Traverses the BDD recursively, while storing the path in 'cache'.
# When a leaf node is reached, prints out the path to the node to 'dst'.
# For 'dnf', the values and directions taken are directly.
#   - taking a 'low' branch towards 1 will yield a negation in the clausule.
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


# Traverses the BDD recursively, while storing the path in 'cache'.
# When a leaf node is reached, prints out the path to the node to 'dst'.
# For 'cnf' the values and directions taken are 'reversed' in the result.
#   - taking a 'high' branch towards 0 will yield a negation in the clausule.
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


# Exports the BDD into DIMACS format.
#   'dst' - file name where the BDD will be exported to
#   'recursive' - uses recursive traversal by default, 
#       if False, iterative traversal will be used (TODO)
#   'format' - specifies which normal form will be used ('dnf'/'cnf')
def dimacsWrite(bdd: BDD, dst, recursive=True, format='cnf'):
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
