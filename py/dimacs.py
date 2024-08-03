"""
[file] dimacs.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Simple parser of DIMACS files (import/export).
[note] Better and faster version using "buddy" library is in ../cpp/
"""

import os
from bdd import *
from bdd_apply import *
from utils import *


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


# TODO: use this class for dimacs parsing
class DimacsHelper:
    def __init__(self):
        self.dimacs_type = None
        self.node_counter = 0
        self.variable_count = 0
        self.clausule_count = 0
        self.branch_count = 0


# Reads a file in DIMACS format and stores it into a BDD instance.
#   'source' = path to the file in dimacs format (accepting .dnf and .cnf suffix)
#   'override' = "cnf"/"dnf" -> treat the file as the specified format
#       no override will imply the format from the dimacs preamble)
#   'verbose' = if True, the function will print debug info
#   'horizontal_cut' = None by default => treats the function 'as is'
#       if horizontal_cut is specified (integer value), every variable of
#       higher value will be skipped, useful for testing purposes
#   'max_clausules' = None by default => only processes a certain amount of
#       clausules, the rest are skipped (for testing purposes)
def dimacs_read(source: str, override=None, verbose=False, horizontal_cut=None, max_clausules=None) -> BDD:
    # for now, we treat cnf as dnf, as they are more natural to parse as BDDs
    if not source.lower().endswith((".dnf", ".cnf")):
        Exception("unknown format for dimacs parsing")
    file = open(source, "r")
    base = os.path.basename(source)
    bdd_name = os.path.splitext(base)[0]
    dimacs_type = None
    node_counter = 0
    variable_count = 0
    clausule_count = 0
    branch_count = 0

    result: BDD = BDD(None, None)
    terminal_0 = BDDnode(f"t0", 0)
    terminal_1 = BDDnode(f"t1", 1)

    processed_clausules = 1
    for line_number, line in enumerate(file, start=1):
        words = line.strip().split()
        if line.startswith("c"):  # comment
            continue

        if line.startswith("p"):  # p dnf variable_count clausule_count
            dimacs_type = words[1]  # so far all types are treated as dnf
            if override is not None and override in ["dnf", "cnf"]:
                dimacs_type = override
            variable_count = int(words[2])
            clausule_count = int(words[3])
            if max_clausules is not None:
                clausule_count = max_clausules
            if verbose:
                print(f"{dimacs_type}, clausules = {clausule_count}, variables = {variable_count}")
            continue

        if verbose:
            print(f"processing clausule {processed_clausules} = {words}")

        if processed_clausules > clausule_count:
            result.name = bdd_name
            result.reformat_nodes()
            return result

        if not is_int(words[0]):
            eprint("dimacs_read():", f"skipping unrecoginzed word at line {line_number}")
            continue

        variables = []
        for word in words:
            if not is_int(word):
                raise Exception("dimacs_read():", f"Bad value {word} on line {line_number}!")
            variables.append(int(word))

        variables.pop()  # last 0
        if horizontal_cut is not None:
            variables = [i for i in variables if abs(i) <= horizontal_cut]
        if len(variables) < 2:
            processed_clausules += 1
            continue
        variables = sorted(variables, key=abs, reverse=True)
        # print(f" > {variables}")

        # bottom-up branch building approach
        branch_count += 1
        branch = BDD(f"branch_{branch_count}", None)
        branch.root = terminal_1 if dimacs_type == "dnf" else terminal_0

        for var in variables:
            current = BDDnode(f"n{node_counter}", str(abs(var)))
            node_counter += 1
            leaf = terminal_0 if dimacs_type == "dnf" else terminal_1
            if var > 0:
                if dimacs_type == "dnf":
                    current.attach(leaf, branch.root)
                else:
                    current.attach(branch.root, leaf)
            else:
                if dimacs_type == "dnf":
                    current.attach(branch.root, leaf)
                else:
                    current.attach(leaf, branch.root)
            branch.root = current
        # print(branch)
        func = "or" if dimacs_type == "dnf" else "and"
        if verbose:
            print(branch)
            print(f"applying {func}")
            print()
        result = apply_function(func, result, branch)
        processed_clausules += 1
        if verbose:
            if result.root != None:
                print(result)

    if clausule_count != branch_count:
        eprint("dimacs_read(): clausule_count != branch_count")
    result.name = bdd_name
    result.reformat_nodes()
    return result


def cache_dump_dnf(dst, cache):
    line = ""
    for value, direction in cache:
        if direction == 0:
            line += "-"
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


# Traverses the BDD recursively, while storing the path in 'cache'.
# When a leaf node is reached, prints out the path to the node to 'dst'.
# For 'dnf', the values and directions taken are directly.
#   - taking a 'low' branch towards 1 will yield a negation in the clausule.
def dimacs_write_recursive_dnf(node: BDDnode, dst, cache: list):
    if node.is_leaf():
        if node.value == 1:
            cache_dump_dnf(dst, cache)
        return

    cache.append((node.value, 0))
    dimacs_write_recursive_dnf(node.low, dst, cache)
    cache.pop()

    cache.append((node.value, 1))
    dimacs_write_recursive_dnf(node.high, dst, cache)
    cache.pop()
    return


def dimacs_write_iterative_dnf(bdd: BDDnode, dst):
    pass


def cache_dump_cnf(dst, cache):
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
def dimacs_write_recursive_cnf(node: BDDnode, dst, cache: list):
    if node.is_leaf():
        if node.value == 0:
            cache_dump_cnf(dst, cache)
        return
    cache.append((node.value, 0))
    dimacs_write_recursive_cnf(node.low, dst, cache)
    cache.pop()

    cache.append((node.value, 1))
    dimacs_write_recursive_cnf(node.high, dst, cache)
    cache.pop()
    return


def dimacs_write_iterative_cnf(bdd: BDDnode, dst):
    pass


# Exports the BDD into DIMACS format.
#   'dst' - file name where the BDD will be exported to
#   'recursive' - uses recursive traversal by default,
#       if False, iterative traversal will be used (TODO)
#   'format' - specifies which normal form will be used ('dnf'/'cnf')
def dimacs_write(bdd: BDD, dst, recursive=True, format="cnf"):
    file = open(dst, "w")
    if recursive is True:
        cache = []
        file.write(f"c {bdd.name}\n")
        var_count = len(bdd.get_variable_list())
        if format == "dnf":
            print("finding 1")
            file.write(f"p dnf {var_count} {bdd.count_branches_iter(1)}\n")
            dimacs_write_recursive_dnf(bdd.root, file, cache)
        elif format == "cnf":
            print("finding 0")
            file.write(f"p cnf {var_count} {bdd.count_branches_iter(0)}\n")
            dimacs_write_recursive_cnf(bdd.root, file, cache)
    else:
        file.write(f"c {bdd.name}\n")
        var_count = len(bdd.get_variable_list())
        if format == "dnf":
            file.write(f"p dnf {var_count} {bdd.count_branches_iter(1)}\n")
            dimacs_write_iterative_dnf(bdd.root, file)
        elif format == "cnf":
            file.write(f"p cnf {var_count} {bdd.count_branches_iter(0)}\n")
            dimacs_write_iterative_cnf(bdd.root, file)
    file.close()


# End of file dimacs.py
