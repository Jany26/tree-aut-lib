from bdd import *
from apply import *
from format_vtf import *
import re

class BlifParser:
    def __init__(self):
        self.name = ""  # name of the benchmark = resulting BDD name
        self.tokens: list[str] = []
        self.token = None  # current token
        self.inputs = []  # contents of the .inputs list
        self.outputs = []  # contents of the .outputs list
        self.names = []  # contents of the current .names list

        # mapping strings from <.inputs> to indices => inferring variable order
        self.varMap: dict[str, int] = {}

        self.nodeCounter = 0  # for unique node names
        self.constructs = 0  # progress/debug (total constructs)
        self.constructCounter = 0  # progress/debug (done constructs)

        self.result = BDD(self.name, None)
        self.bdd = BDD(self.name, None)

        self.t0 = BDDnode('t0', 0)
        self.t1 = BDDnode('t1', 1)

    def __repr__(self):
        return "TODO"

    def parse(self, fileName) -> BDD:
        file = open(fileName, 'r')
        self.tokenize(file)
        file.close()
        self.createVariablesCache()
        self.syntaxAnalysis()
        self.result.name = self.name
        pass

    def tokenize(self, file):
        self.tokens = []
        for line in file:
            line.strip()
            if line == "\n" or line.startswith("#"):
                continue
            words = line.split()
            self.tokens.extend(words)
            self.tokens.append('\n')

    def createVariablesCache(self):
        vars = set()
        i = 0
        while i < len(self.tokens):
            if self.tokens[i] in ['.inputs', '.outputs', '.names']:
                if self.tokens[i] == '.names':
                    self.constructs += 1
                i += 1
                while self.tokens[i] != '\n':
                    if self.tokens[i] == "\\":  # redundant probably
                        i += 1
                    if self.tokens[i] not in vars:
                        vars.add(self.tokens[i])
                    i += 1
            else:
                i += 1
        vars = list(vars)
        self.varMap = {}
        for i in vars:
            match = re.search(r"\(([^()]*)\)", i)
            if match:
                result = match.group(0)[1:-1]
                self.varMap[i] = int(result)
            else:
                self.varMap[i] = int(i)

    def syntaxAnalysis(self):
        keywords = [".model", ".inputs", ".outputs", ".names", ".end"]
        def getToken() -> str:
            self.token = self.tokens.pop(0)
            return self.token

        def constructList():
            getToken()
            if self.token not in keywords:
                raise Exception(f"blif_parser: unsupported construct: {self.token}")
            if self.token == ".end":
                getToken()
                return
            construct()
            constructList()

        def construct():
            if self.token == ".model":
                modelName()
            if self.token == ".inputs":
                inputList()
            if self.token == ".outputs":
                outputList()
            if self.token == ".names":
                self.names = []
                namesList()
                namesContent()
                self.result = applyFunction('and', self.bdd, self.result)
                self.bdd = BDD(self.name, None)
                self.constructCounter += 1
                # print(f"{self.constructCounter}/{self.constructs}", end='\r')

        def modelName():
            self.name = getToken()
            getToken()  # '\n'

        def inputList():
            getToken()
            if self.token == "\n":
                return
            self.inputs.append(self.token)
            inputList()

        def outputList():
            getToken()
            if self.token == "\n":
                return
            self.outputs.append(self.token)
            outputList()

        def namesList():
            getToken()
            if self.token == "\n":
                return
            self.names.append(self.varMap[self.token])
            namesList()

        def namesContent():
            # print(self.token)
            inputPlane = getToken()
            output = int(getToken())
            getToken()  # '\n'
            assignment = [(self.names[i], int(inputPlane[i])) for i in range(len(self.names) - 1)]
            assignment.sort(reverse=True)

            straight = BDDnode(self.nodeCounter, f'{self.names[-1]}', self.t0, self.t1)  # 
            self.nodeCounter += 1
            complement = BDDnode(self.nodeCounter, f'{self.names[-1]}', self.t1, self.t0)  # complemented form
            self.nodeCounter += 1

            root, dump = (straight, complement) if output == 1 else (complement, straight)
            for var, bit in assignment:
                low = dump if bit == 1 else root
                high = root if bit == 1 else dump
                newRoot = BDDnode(self.nodeCounter, f'{var}', low, high)
                root = newRoot
                self.nodeCounter += 1
            bdd = BDD(self.names[-1], root)
            self.bdd = applyFunction('or', bdd, self.bdd)
            while self.tokens[0] == '\n':
                getToken()
            if self.tokens[0] in ['.names', '.end']:
                return
            namesContent()
        
        constructList()


    def checkNames(self, tokens: list):
        inputs = []
        outputs = []
        notFound = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '.inputs':
                i += 1
                while tokens[i] != '\n':
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in inputs:
                        inputs.append(tokens[i])
                    i += 1
            elif tokens[i] == '.outputs':
                i += 1
                while tokens[i] != '\n':
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in outputs:
                        outputs.append(tokens[i])
                    i += 1
            elif tokens[i] == '.names':
                i += 1
                while tokens[i] != '\n':
                    if tokens[i] == "\\":  # redundant probably
                        i += 1
                    if tokens[i] not in inputs and tokens[i] not in outputs:
                        if tokens[i] not in notFound:
                            notFound.append(tokens[i])
                    i += 1
            else:
                i += 1
                continue


if __name__ == '__main__':
    blif = BlifParser()
    blif.parse("./tests/blif/C17.blif")
    print(blif.result.countNodes())
    ta = createTAfromBDD(blif.result)
    ta.reformatStates()
    exportTAtoVTF(ta, "./tests/blif/C17.vtf")

# end of blif_parser.py