"""
[file] dimacs.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Simple parser of DIMACS files (import/export).
[note] This parser tries using a Python implementation of BDDs which is slow.
Better and faster version using "buddy" library is in ../cpp/
"""

from io import TextIOWrapper
import os
from typing import Optional, Union

from bdd.bdd_class import BDD
from bdd.bdd_node import BDDnode
from bdd.bdd_apply import apply_function


def is_int(str) -> bool:
    try:
        int(str)
        return True
    except ValueError:
        return False


# TODO: use this class for dimacs parsing for cleaner code
class DimacsHelper:
    def __init__(self, source: str):
        self.dimacs_type: Optional[str] = None
        self.node_counter: int = 0
        self.variable_count: int = 0
        self.clausule_count: int = 0
        self.branch_count: int = 0
        self.processed_clausules: int = 1
        self.bdd_name: str = os.path.splitext(os.path.basename(source))[0]


def dimacs_read(source: str, override=None, verbose=False, horizontal_cut=None, max_clausules=None) -> BDD:
    """
    Reads a file in DIMACS format and stores it into a BDD instance.
    - source            ... path to the file in dimacs format (accepting .dnf and .cnf suffix)
    - override          ... "cnf"/"dnf" -> treat the file as the specified format
                            no override will imply the format from the dimacs preamble)
    - verbose           ... if True, the function will print debug info
    - horizontal_cut    ... None by default => treats the function 'as is'
                            if horizontal_cut is specified (integer value), every variable of
                            higher value will be skipped, useful for testing purposes
    'max_clausules'     ... None by default => only processes a certain amount of
                            clausules, the rest are skipped (for testing purposes)
    """

    # for now, we treat cnf as dnf, as they are more natural to parse as BDDs
    if not source.lower().endswith((".dnf", ".cnf")):
        Exception("unknown format for dimacs parsing")
    file = open(source, "r")
    info = DimacsHelper(source)

    result: BDD = BDD(None, None)
    terminal_0 = BDDnode(f"t0", 0)
    terminal_1 = BDDnode(f"t1", 1)

    for line_number, line in enumerate(file, start=1):
        words: list[str] = line.strip().split()
        if line.startswith("c"):  # comment
            continue

        if line.startswith("p"):  # p dnf variable_count clausule_count
            info.dimacs_type = words[1]  # so far all types are treated as dnf
            if override is not None and override in ["dnf", "cnf"]:
                info.dimacs_type = override
            info.variable_count = int(words[2])
            info.clausule_count = int(words[3])
            if max_clausules is not None:
                info.clausule_count = max_clausules
            if verbose:
                print(f"{info.dimacs_type}, clausules = {info.clausule_count}, variables = {info.variable_count}")
            continue

        if verbose:
            print(f"processing clausule {info.processed_clausules} = {words}")

        if info.processed_clausules > info.clausule_count:
            result.name = info.bdd_name
            result.reformat_nodes()
            return result

        if not is_int(words[0]):
            print("dimacs_read():", f"skipping unrecoginzed word at line {line_number}")
            continue

        variables: list[int] = []
        for word in words:
            if not is_int(word):
                raise Exception("dimacs_read():", f"Bad value {word} on line {line_number}!")
            variables.append(int(word))

        variables.pop()  # last 0
        if horizontal_cut is not None:
            variables = [i for i in variables if abs(i) <= horizontal_cut]
        if len(variables) < 2:
            info.processed_clausules += 1
            continue
        variables = sorted(variables, key=abs, reverse=True)
        # print(f" > {variables}")

        # bottom-up branch building approach
        info.branch_count += 1
        branch = BDD(f"branch_{info.branch_count}", None)
        branch.root = terminal_1 if info.dimacs_type == "dnf" else terminal_0

        for var in variables:
            current = BDDnode(f"n{info.node_counter}", str(abs(var)))
            info.node_counter += 1
            leaf: BDDnode = terminal_0 if info.dimacs_type == "dnf" else terminal_1
            if var > 0:
                if info.dimacs_type == "dnf":
                    current.attach(leaf, branch.root)
                else:
                    current.attach(branch.root, leaf)
            else:
                if info.dimacs_type == "dnf":
                    current.attach(branch.root, leaf)
                else:
                    current.attach(leaf, branch.root)
            branch.root = current
        # print(branch)
        func: str = "or" if info.dimacs_type == "dnf" else "and"
        if verbose:
            print(branch)
            print(f"applying {func}")
            print()
        result: BDD = apply_function(func, result, branch)
        info.processed_clausules += 1
        if verbose:
            if result.root != None:
                print(result)

    if info.clausule_count != info.branch_count:
        print("dimacs_read(): clausule_count != branch_count")
    result.name = info.bdd_name
    result.reformat_nodes()
    return result


def cache_dump_dnf(dst: TextIOWrapper, cache: list[tuple[Union[str, int], int]]) -> None:
    line: str = ""
    for value, direction in cache:
        if direction == 0:
            line += "-"
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


def dimacs_write_recursive_dnf(node: BDDnode, dst, cache: list[tuple[Union[int, str], int]]) -> None:
    """
    Traverses the BDD recursively, while storing the path in 'cache'.
    When a leaf node is reached, prints out the path to the node to 'dst'.
    For 'dnf', the values and directions taken are directly.
    - taking a 'low' branch towards 1 will yield a negation in the clausule.
    """
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


def dimacs_write_iterative_dnf(bdd: BDDnode, dst) -> None:
    pass


def cache_dump_cnf(dst: TextIOWrapper, cache: list[tuple[Union[str, int], int]]) -> None:
    line: str = ""
    for value, direction in cache:
        if direction == 1:
            line += "-"
        line += str(value) + " "
    line += "0\n"
    dst.write(line)


def dimacs_write_recursive_cnf(node: BDDnode, dst, cache: list[tuple[Union[str, int], int]]) -> None:
    """
    Traverses the BDD recursively, while storing the path in 'cache'.
    When a leaf node is reached, prints out the path to the node to 'dst'.
    For 'cnf' the values and directions taken are 'reversed' in the result.
      - taking a 'high' branch towards 0 will yield a negation in the clausule.
    """
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


def dimacs_write_iterative_cnf(bdd: BDDnode, dst) -> None:
    pass


def dimacs_write(bdd: BDD, dst: str, recursive=True, format="cnf"):
    """
    Exports the BDD into DIMACS format.
    'dst' - file name where the BDD will be exported to
    'recursive' - uses recursive traversal by default,
        if False, iterative traversal will be used (TODO)
    'format' - specifies which normal form will be used ('dnf'/'cnf')
    """
    file: TextIOWrapper = open(dst, "w")
    if recursive is True:
        cache: list[tuple[Union[str, int], int]] = []  # (node.value, ) tuples
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
