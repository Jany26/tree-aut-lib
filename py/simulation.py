from typing import Union
from ta_classes import *
from bdd import BDD


def assignVariables(num: int, size: int) -> list:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return result


def assignVariablesDict(num: int, size: int) -> dict:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    resultDict = {i+1: result[i] for i in range(size)}
    return resultDict


def getVarPrefix(varList: list) -> str:
    if varList == []:
        return ""
    prefixLen = 0
    for i in range(len(varList[0])):
        if not varList[0][i:].isnumeric():
            prefixLen += 1
    prefix = varList[0][:prefixLen]
    return prefix


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
    prefix = getVarPrefix(varList)
    vars = {f"{prefix}{i}": val for i, val in enumerate(assignment, 1)}
    return vars



# Simulates boolean computation of all variable settings.
def simulateRunBDD(bdd: BDD, assignment: list | dict, verbose=False) -> bool:
    if type(assignment) == list:
        vars = getVariableEvaluation(bdd, assignment)
    else:
        vars = assignment
    
    result = None
    node = bdd.root
    if verbose:
        print(node.name, "through root")
    while result is None:
        if type(node.value) == int:
            result = node.value
            if verbose:
                print("result =", node.value, "in leaf node", node.name)
        else:
            previous = node.name
            val = assignment[vars[node.value]]
            node = node.low if val == 0 else node.high
            if verbose:
                transition = "low" if val == 0 else "high"
                # print(node.name, node.value, "through", transition "for")
                print(f"<{node.name} {node.value}> through {transition} for variable {previous}")
    return result


class SimulationHelper:
    def __init__(self, ta: TTreeAut, assignment, verbose):
        # quick edge lookup (edge keys will be used in path as well)
        self.edgeLookup = {
            k: e for ed in ta.transitions.values() for k, e in ed.items()
        }
        # variables and their assigned values lookup
        # self.varLookup = getVariableEvaluation(ta, assignment)
        self.varLookup = assignment
        # path = list of tuples (state, key), which were visited during parsing
        self.path: list(tuple(str, str)) = []
        self.leafStates = {
            i: j[0] for i, j in ta.getOutputEdges(inverse=True).items()
        }
        self.length = len(assignment)
        self.verbose = verbose
        self.varVisibility = ta.getVariableVisibility()
        self.prefix = ta.getVariablePrefix()
        self.vars = [(k, e) for k, e in assignment.items()]

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
        if idx >= sim.length or state in sim.leafStates:
            # if state in sim.leafStates and len(ta.transitions[state]) == 1:
            if sim.verbose:
                print(f"[value = {sim.leafStates[state]}]: {state} = leaf")
            return sim.leafStates[state]
            # return None
        variable, value = sim.vars[idx]
        edgeKeys = createSortedEdgeList(ta.transitions[state])
        for key in edgeKeys:
            edge: TTransition = sim.edgeLookup[key]
            if len(edge.children) == 0:
                continue
            if edge.info.variable != "":
                # when there is a chain of transitions with the same or decreasing variable
                if variable >= int(edge.info.variable[len(sim.prefix):]):
                    continue
                if f"{sim.prefix}{variable}" != edge.info.variable:
                    if len(ta.transitions[state]) == 1:
                        if sim.verbose:
                            print(f"[{variable :<2} -> {value}]: skipping")
                        result = backTrack(ta, state, idx + 1, sim)
                        if result is not None:
                            return result
                    if sim.verbose:
                        print(f"[{variable} -> {value}]: does not correspond with edge {edge}")
                    continue
            newState = edge.children[value]
            if sim.verbose:
                print(f"[{variable :<2} -> {value}]:", edge, "to", newState)
            result = backTrack(ta, newState, idx + 1, sim)
            if result is not None:
                return result

    sim = SimulationHelper(ta, assignment, verbose)
    currentState = ta.rootStates[0]
    result = backTrack(ta, currentState, 0, sim)
    if verbose:
        print(f"result = {result}")
    if result is None:
        return False
    return bool(int(result))


def findFunction(obj: Union[TTreeAut, BDD]):
    if type(obj) == TTreeAut:
        return simulateRunTAdict
    if type(obj) == BDD:
        return simulateRunBDD
    return None


def simulateAndCompare(
    obj1: 'TTreeAut | BDD',
    obj2: 'TTreeAut | BDD',
    variables: int,
    debug=False,
    output=None
) -> bool:
    fun1 = findFunction(obj1)
    fun2 = findFunction(obj2)
    # results1 = ""
    # results2 = ""
    same = True
    step = (2 ** variables) // 25
    progress = 0
    if debug:
        # print(f"Comparing equivalence of {obj1.name} and {obj2.name}")
        print(f"Equivalence check: {obj1.name} ...")
    if output is not None:
        output.write(f"Comparing equivalence of {obj1.name} and {obj2.name}\n\n")
    for i in range(2 ** (variables)):
        currentAssignment = assignVariablesDict(i, variables)
        res1 = fun1(obj1, currentAssignment)
        res2 = fun2(obj2, currentAssignment)
        # print(currentAssignment, f"1 = {res1}, 2 = {res2}")
        if res1 != res2:
            same = False
            if output is None:
                print(currentAssignment, f"1 = {res1}, 2 = {res2}")
            else:
                output.write(f"{currentAssignment}, 1 = {res1}, 2 = {res2}\n")
                output.flush()
        if i == progress + step:
            progress += step
            if debug:
                # progress = round(i / (2 ** variables) * 25)
                # print(f"[{'#' * progress}{' ' * (25 - progress)}]", end='\r')
                print(f"{round(i / (2 ** variables) * 100)} %", end='\r')
    # if debug: print('')
    if output is not None:
        output.write(f"\nEquivalent? = {same}.")
    return same


# For faster/more precise decision making, especially in unfolded UBDAs.
# TODO: Needs fixing (see results/folding-error-2/...)
def addVariablesBU(ta: TTreeAut, maxVar: int):
    def convertVars(varList: list, prefix: str) -> dict:
        return {i: int(i[len(prefix):]) for i in varList}
    varVis = ta.getVariableVisibility()
    trueLeafs = set()
    varPrefix = getVarPrefix(ta.getVariableOrder())
    for leaf in ta.getOutputStates():
        if len(ta.transitions[leaf]) == 1:
            trueLeafs.add(leaf)

    varLookup = convertVars(ta.getVariableOrder(), varPrefix)

    for edge in iterateEdges(ta):
        if edge.info.variable != "" or edge.src in edge.children:
            continue
        for child in edge.children:
            if child in varVis:
                var = varLookup[list(varVis[child])[0]]
                newVar = f"{varPrefix}{int(var)-1}"
                edge.info.variable = newVar
            if child in trueLeafs:
                edge.info.variable = f"{varPrefix}{maxVar}"
    # end for

def simulateRunTAdict(ta: TTreeAut, assignment: list | dict, verbose=False, startingVar=None):
    """Description ...
    """

    simHelper = {
        # 'path': [],
        'prefix': ta.getVariablePrefix(),
        'leaves': ta.getOutputEdges(inverse=True),
        'length': len(assignment),
        'vis': ta.getVariableVisibility(),
        'debug': verbose,
    }

    def sortKeys(ta: TTreeAut, state: str) -> list:
        result = []
        # NOTE: maybe there is a way to append (tail) and push (head) into the list ...
        for key, edge in ta.transitions[state].items():
            if edge.info.variable != "" or not edge.checkSelfLoop():  # and len(edge.children) != 0:
                result.append(key)
        for key, edge in ta.transitions[state].items():
            if edge.info.variable == "":  # and len(edge.children) != 0:
                if key not in result:
                    result.append(key)
        return result

    def backTrack(ta: TTreeAut, variable: int, state: str, assignment: dict):
        if state in simHelper['leaves']:  # or variable > sim['length']:
            if simHelper['debug']:
                print(f" END -> {simHelper['leaves'][state][0]} : {state} = leaf")
            return simHelper['leaves'][state][0]
        if variable not in assignment:
            return None
        try:
            value = assignment[variable]
        except:
            print(assignment)
        
        for key in simHelper['keys'][state]:
            edge: TTransition = ta.transitions[state][key]
            if edge.info.variable != "":
                if f"{simHelper['prefix']}{variable}" != edge.info.variable:
                    if len(ta.transitions[state]) == 1:
                        if simHelper['debug']:
                            print(f" {variable :<3} -> {value} : skipping")
                        # simHelper['path'].append(state)
                        result = backTrack(ta, variable + 1, state, assignment)
                        if result is not None:
                            return result
                    if simHelper['debug']: 
                        print(f" {variable :<3} -> {value} : ", end="")
                        print(f"{ta.getEdgeString(edge)} -> incompatible variable")
                    continue
            newState = edge.children[value]
            if simHelper['debug']:
                print(f"[{variable :<3} -> {value}]: {ta.getEdgeString(edge)} -> {newState}")
            # simHelper['path'].append(newState)
            result = backTrack(ta, variable + 1, newState, assignment)
            if result is not None:
                return result

    root = ta.rootStates[0]
    rootVar = list(simHelper['vis'][root])[0]
    start = int(rootVar) if startingVar is None else int(startingVar)
    simHelper['keys'] = {state: sortKeys(ta, state) for state in ta.getStates()}
    if simHelper['debug']:
        print(f"{ta.name} - simulating variable assignment")
    # simHelper['path'].append(root)
    result = backTrack(ta, start, root, assignment)
    return result


def leafify(ta: TTreeAut, state: str, value: str | int):
    keysToPop = [key for key in ta.transitions[state].keys()]
    vis = ta.getVariableVisibility()
    maxVar = max(vis[state])
    for key in keysToPop:
        ta.transitions[state].pop(key)
    newEdge = TTransition(state, TEdge(str(value), [], f"{maxVar}"), [])
    ta.transitions[state][keysToPop[0]] = newEdge
    # newEdge = TTransition(state, TEdge('LH', [], ""), [state, state])


# End of file simulation.py    
