from multiprocessing.sharedctypes import Value
from typing import Union
from ta_classes import *
from unfolding import isUnfolded
from bdd import BDD


def assignVariables(num: int, size: int):
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return result


# Creates a lookup table for each variable in a simulated object.
# The object is expected to have a unified names of variables
#   - same prefix followed by a number, eg. ['x1', 'x2', 'x3', etc.]
def getVariableEvaluation(obj: Union[TTreeAut, BDD], assignment: list) -> dict:
    varList = []
    if type(obj) == BDD:
        varList = obj.getVariableList()
    if type(obj) == TTreeAut:
        varList = obj.getVariableOrder()
    assert(varList != [])

    prefixLen = 0
    for i in range(len(varList[0])):
        if not varList[0][i:].isnumeric():
            prefixLen += 1
    prefix = varList[0][:prefixLen]
    vars = {f"{prefix}{i}": val for i, val in enumerate(assignment, 1)}
    return vars



# Simulates boolean computation of all variable settings.
def simulateRunBDD(bdd: BDD, assignment: list, verbose=False) -> bool:
    vars = getVariableEvaluation(bdd, assignment)
    
    result = None
    node = bdd.root
    while result is None:
        if type(node.value) == int:
            result = node.value
        else:
            val = assignment[vars[node.value]]
            node = node.low if val == 0 else node.high
            if verbose:
                print(node.name, node.value)
    return result


class SimulationHelper:
    def __init__(self, ta: TTreeAut, assignment, verbose):
        # quick edge lookup (edge keys will be used in path as well)
        self.edgeLookup = {
            k: e for ed in ta.transitions.values() for k, e in ed.items()
        }
        # variables and their assigned values lookup
        self.varLookup = getVariableEvaluation(ta, assignment)
        # path = list of tuples (state, key), which were visited during parsing
        self.path: list(tuple(str, str)) = []
        self.leafStates = {
            i: j[0] for i, j in ta.getOutputEdges(inverse=True).items()
        }
        self.length = len(assignment)
        self.verbose = verbose

        self.vars = [(k, e) for k, e in self.varLookup.items()]

    def __repr__(self):
        result = "[Simulation Helper]:\n"
        result += f"> variables:\n"
        for var, val in self.varLookup.items():
            result += f"  > {var}: {val}\n"
        result += f"> path:\n"
        for s, e in self.path:
            result += f"  > {s} -> {e}\n"
        result += f"> leaf states: {self.leafStates}\n"
        return result


# Simulates a run through the automaton (branching / deciding process),
# given a variable evaluation. Returns a value on a leaf node
# ... with UBDAs => 1 = true, 0 = false
# NOTE: So far works with unfolded/normalized UBDA.
def simulateRunTA(ta: TTreeAut, assignment: list, verbose=False) -> bool:
    def createSortedEdgeList(edges: dict[str, TTransition]) -> list[str]:
        result = []
        for key, edge in edges.items():
            if not edge.checkSelfLoop():
                result.append(key)
        for key, edge in edges.items():
            if edge.checkSelfLoop():
                result.append(key)
        return result

    def backTrack(ta: TTreeAut, state, idx, sim: SimulationHelper):
        if idx >= sim.length:
            if state in sim.leafStates:
                return sim.leafStates[state]
            return None
        variable, value = sim.vars[idx]
        edgeKeys = createSortedEdgeList(ta.transitions[state])
        for key in edgeKeys:
            edge: TTransition = sim.edgeLookup[key]
            if len(edge.children) == 0:
                continue
            if edge.info.variable != "":
                if variable != edge.info.variable:
                    if sim.verbose:
                        print(f"{variable} does not correspond with {edge}")
                    return None
            newState = edge.children[value]
            if sim.verbose:
                print(f"{variable} = {value}:", newState, "through", edge)
            result = backTrack(ta, newState, idx + 1, sim)
            if result is not None:
                return result

    sim = SimulationHelper(ta, assignment, verbose)
    currentState = ta.rootStates[0]
    if verbose:
        print(currentState, "through root")
    result = backTrack(ta, currentState, 0, sim)
    if result is None:
        return False
    return bool(int(result))


def findFunction(obj: Union[TTreeAut, BDD]):
    if type(obj) == TTreeAut:
        return simulateRunTA
    if type(obj) == BDD:
        return simulateRunBDD
    return None

def simulateAndCompare(
    obj1: 'TTreeAut | BDD',
    obj2: 'TTreeAut | BDD',
    variables: int,
    debug=False
) -> bool:
    fun1 = findFunction(obj1)
    fun2 = findFunction(obj2)
    results1 = ""
    results2 = ""
    same = True
    for i in range(2 ** (variables)):
        currentAssignment = assignVariables(i, variables)
        res1 = fun1(obj1, currentAssignment)
        res2 = fun2(obj2, currentAssignment)
        if res1 != res2:
            same = False
            # if same is True:
            #     if debug:
            print("not same for", currentAssignment, f"1 = {res1}, 2 = {res2}")
        results1 += str(int(res1))
        results2 += str(int(res2))
    if debug:
        print("results1", results1)
        print("results2", results2)
    return same
            