"""
[file] blif_parser.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Simple parser of BLIF files (assumes bottom-up order of constructs)
[note] This parser tries using a Python implementation of BDDs which is slow.
Better and faster version using BuDDy library is in ../cpp/
"""

from io import TextIOWrapper
import re
from typing import Optional

from bdd.bdd_apply import apply_function
from bdd.bdd_class import BDD
from bdd.bdd_node import BDDnode


# Usage example:
# blif = BlifParser()
# blif.parse("../benchmark/blif/C17.blif")
# print(blif.result.count_nodes())
# temp = create_treeaut_from_bdd(blif.result)
# temp.reformat_states()
# export_treeaut_to_vtf(temp, "../benchmark/blif/C17.vtf")


class BlifParser:
    def __init__(self):
        self.name: str = ""  # name of the benchmark = resulting BDD name
        self.tokens: list[str] = []
        self.token: Optional[str] = None  # current token
        self.inputs: list[str] = []  # contents of the .inputs list
        self.outputs: list[str] = []  # contents of the .outputs list
        self.names: list[str] = []  # contents of the current .names list

        # mapping strings from <.inputs> to indices => inferring variable order
        self.var_map: dict[str, int] = {}

        self.node_counter: int = 0  # for unique node names
        self.constructs: int = 0  # progress/debug (total constructs)
        self.constructs_counter: int = 0  # progress/debug (done constructs)

        self.result: BDD = BDD(self.name, None)
        self.bdd: BDD = BDD(self.name, None)

        self.t0: BDDnode = BDDnode("t0", 0)
        self.t1: BDDnode = BDDnode("t1", 1)

    def __repr__(self):
        return "TODO"

    def parse(self, filepath: str) -> BDD:
        file: TextIOWrapper = open(filepath, "r")
        self.tokenize(file)
        file.close()
        self.create_vars_cache()
        self.syntax_analysis()
        self.result.name = self.name
        pass

    def tokenize(self, file: TextIOWrapper):
        self.tokens = []
        for line in file:
            line.strip()
            if line == "\n" or line.startswith("#"):
                continue
            words = line.split()
            self.tokens.extend(words)
            self.tokens.append("\n")

    def create_vars_cache(self):
        vars: set[str] = set()
        i: int = 0
        while i < len(self.tokens):
            if self.tokens[i] in [".inputs", ".outputs", ".names"]:
                if self.tokens[i] == ".names":
                    self.constructs += 1
                i += 1
                while self.tokens[i] != "\n":
                    if self.tokens[i] == "\\":  # redundant probably
                        i += 1
                    if self.tokens[i] not in vars:
                        vars.add(self.tokens[i])
                    i += 1
            else:
                i += 1
        vars: list = list(vars)
        self.var_map = {}
        for i in vars:
            match = re.search(r"\(([^()]*)\)", i)
            if match:
                result: str = match.group(0)[1:-1]
                self.var_map[i] = int(result)
            else:
                self.var_map[i] = int(i)

    def syntax_analysis(self):
        self.keywords = [".model", ".inputs", ".outputs", ".names", ".end"]

        def get_token() -> str:
            self.token = self.tokens.pop(0)
            return self.token

        def construct_list():
            get_token()
            if self.token not in self.keywords:
                raise Exception(f"blif_parser: unsupported construct: {self.token}")
            if self.token == ".end":
                get_token()
                return
            construct()
            construct_list()

        def construct():
            if self.token == ".model":
                model_name()
            if self.token == ".inputs":
                input_list()
            if self.token == ".outputs":
                output_list()
            if self.token == ".names":
                self.names = []
                names_list()
                names_content()
                self.result = apply_function("and", self.bdd, self.result)
                self.bdd = BDD(self.name, None)
                self.constructs_counter += 1
                # print(f"{self.constructs_counter}/{self.constructs}", end='\r')

        def model_name():
            self.name = get_token()
            get_token()  # '\n'

        def input_list():
            get_token()
            if self.token == "\n":
                return
            self.inputs.append(self.token)
            input_list()

        def output_list():
            get_token()
            if self.token == "\n":
                return
            self.outputs.append(self.token)
            output_list()

        def names_list():
            get_token()
            if self.token == "\n":
                return
            self.names.append(self.var_map[self.token])
            names_list()

        def names_content():
            input_plane: str = get_token()
            output: int = int(get_token())
            get_token()  # '\n'
            assignment: list[tuple[str, int]] = [
                (self.names[i], int(input_plane[i])) for i in range(len(self.names) - 1)
            ]
            assignment.sort(reverse=True)

            straight: BDDnode = BDDnode(self.node_counter, f"{self.names[-1]}", self.t0, self.t1)  #
            self.node_counter += 1
            complement: BDDnode = BDDnode(self.node_counter, f"{self.names[-1]}", self.t1, self.t0)  # complemented form
            self.node_counter += 1

            root, dump = (straight, complement) if output == 1 else (complement, straight)
            for var, bit in assignment:
                low = dump if bit == 1 else root
                high = root if bit == 1 else dump
                new_root = BDDnode(self.node_counter, f"{var}", low, high)
                root = new_root
                self.node_counter += 1
            bdd = BDD(self.names[-1], root)
            self.bdd = apply_function("or", bdd, self.bdd)
            while self.tokens[0] == "\n":
                get_token()
            if self.tokens[0] in [".names", ".end"]:
                return
            names_content()

        construct_list()

    def check_names(self, tokens: list):
        inputs: list[str] = []
        outputs: list[str] = []
        not_found: list[str] = []
        i: int = 0
        while i < len(tokens):
            if tokens[i] == ".inputs":
                i += 1
                while tokens[i] != "\n":
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in inputs:
                        inputs.append(tokens[i])
                    i += 1
            elif tokens[i] == ".outputs":
                i += 1
                while tokens[i] != "\n":
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in outputs:
                        outputs.append(tokens[i])
                    i += 1
            elif tokens[i] == ".names":
                i += 1
                while tokens[i] != "\n":
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in inputs and tokens[i] not in outputs:
                        if tokens[i] not in not_found:
                            not_found.append(tokens[i])
                    i += 1
            else:
                i += 1
                continue


# end of blif_parser.py
