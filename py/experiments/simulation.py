"""
[file] simulation.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Equivalence testing via inputting all possible variable assignments.
[note] Used during developing/debugging the folding procedure.
"""

from typing import Union, List, Dict

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from tree_automata.var_manipulation import get_var_prefix, assign_variables_dict
from bdd.bdd_class import BDD


# Creates a lookup table for each variable in a simulated object.
# The object is expected to have a unified names of variables
#   - same prefix followed by a number, eg. ['x1', 'x2', 'x3', etc.]
def get_var_evaluation(obj: Union[TTreeAut, BDD], assignment: list) -> dict:
    var_list = []
    if type(obj) == BDD:
        var_list = obj.get_variable_list()
    if type(obj) == TTreeAut:
        var_list = obj.get_var_order()
    assert var_list != []
    prefix = get_var_prefix(var_list)
    vars = {f"{prefix}{i}": val for i, val in enumerate(assignment, 1)}
    return vars


# Simulates boolean computation of all variable settings.
def simulate_run_bdd(bdd: BDD, assignment: list | dict, verbose=False) -> bool:
    if type(assignment) == list:
        vars = get_var_evaluation(bdd, assignment)
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
        self.edge_lookup = {k: e for ed in ta.transitions.values() for k, e in ed.items()}
        # variables and their assigned values lookup
        # self.var_lookup = get_var_evaluation(ta, assignment)
        self.var_lookup = assignment
        # path = list of tuples (state, key), which were visited during parsing
        self.path: list[(str, str)] = []
        self.leaves = {i: j[0] for i, j in ta.get_output_edges(inverse=True).items()}
        self.length = len(assignment)
        self.verbose = verbose
        self.var_visibility = ta.get_var_visibility()
        self.prefix = ta.get_var_prefix()
        self.vars = [(k, e) for k, e in assignment.items()]

    def __repr__(self):
        result = "[Simulation Helper]:\n"
        result += f"> variables:\n"
        for var, val in self.var_lookup.items():
            result += f"  > {var}: {val}\n"
        result += f"> path:\n"
        for s, e in self.path:
            result += f"  > {s} -> {e}\n"
        result += f"> leaf states: {self.leaves}\n"
        return result


# Simulates a run through the automaton (branching / deciding process),
# given a variable evaluation. Returns a value on a leaf node
# ... with UBDAs => 1 = true, 0 = false
# NOTE: So far works with unfolded/normalized UBDA.
def simulate_run_treeaut(ta: TTreeAut, assignment: list, verbose=False) -> bool:
    def create_sorted_edge_list(edges: dict[str, TTransition]) -> list[str]:
        result = []
        for key, edge in edges.items():
            if not edge.is_self_loop():
                result.append(key)
        for key, edge in edges.items():
            if edge.is_self_loop():
                result.append(key)
        return result

    def backtrack(ta: TTreeAut, state, idx, sim: SimulationHelper):
        if idx >= sim.length or state in sim.leaves:
            # if state in sim.leaves and len(ta.transitions[state]) == 1:
            if sim.verbose:
                print(f"[value = {sim.leaves[state]}]: {state} = leaf")
            return sim.leaves[state]
            # return None
        variable, value = sim.vars[idx]
        edge_keys = create_sorted_edge_list(ta.transitions[state])
        for key in edge_keys:
            edge: TTransition = sim.edge_lookup[key]
            if len(edge.children) == 0:
                continue
            if edge.info.variable != "":
                # when there is a chain of transitions with the same or decreasing variable
                if variable >= int(edge.info.variable[len(sim.prefix) :]):
                    continue
                if f"{sim.prefix}{variable}" != edge.info.variable:
                    if len(ta.transitions[state]) == 1:
                        if sim.verbose:
                            print(f"[{variable :<2} -> {value}]: skipping")
                        result = backtrack(ta, state, idx + 1, sim)
                        if result is not None:
                            return result
                    if sim.verbose:
                        print(f"[{variable} -> {value}]: does not correspond with edge {edge}")
                    continue
            new_state = edge.children[value]
            if sim.verbose:
                print(f"[{variable :<2} -> {value}]:", edge, "to", new_state)
            result = backtrack(ta, new_state, idx + 1, sim)
            if result is not None:
                return result

    sim = SimulationHelper(ta, assignment, verbose)
    current_state = ta.roots[0]
    result = backtrack(ta, current_state, 0, sim)
    if verbose:
        print(f"result = {result}")
    if result is None:
        return False
    return bool(int(result))


def find_function(obj: Union[TTreeAut, BDD]):
    if type(obj) == TTreeAut:
        return simulate_run_treeaut_dict
    if type(obj) == BDD:
        return simulate_run_bdd
    return None


def simulate_and_compare(
    obj1: "TTreeAut | BDD", obj2: "TTreeAut | BDD", variables: int, debug=False, output=None
) -> bool:
    fun1 = find_function(obj1)
    fun2 = find_function(obj2)
    # results1 = ""
    # results2 = ""
    same = True
    step = (2**variables) // 25
    progress = 0
    if debug:
        # print(f"Comparing equivalence of {obj1.name} and {obj2.name}")
        print(f"Equivalence check: {obj1.name} ...")
    if output is not None:
        output.write(f"Comparing equivalence of {obj1.name} and {obj2.name}\n\n")
    for i in range(2 ** (variables)):
        current_assignment = assign_variables_dict(i, variables)
        res1 = fun1(obj1, current_assignment)
        res2 = fun2(obj2, current_assignment)
        # print(current_assignment, f"1 = {res1}, 2 = {res2}")
        if res1 != res2:
            same = False
            if debug:
                if output is None:
                    print(current_assignment, f"1 = {res1}, 2 = {res2}")
                else:
                    output.write(f"{current_assignment}, 1 = {res1}, 2 = {res2}\n")
                    output.flush()
        if i == progress + step:
            progress += step
            if debug:
                # progress = round(i / (2 ** variables) * 25)
                # print(f"[{'#' * progress}{' ' * (25 - progress)}]", end='\r')
                print(f"{round(i / (2 ** variables) * 100)} %", end="\r")
    # if debug: print('')
    if output is not None:
        output.write(f"\nequivalent? = {same}.")
    return same


def simulate_run_treeaut_dict(ta: TTreeAut, assignment: list | dict, verbose=False, starting_var=None):
    """Description ..."""

    sim_helper = {
        # 'path': [],
        "prefix": ta.get_var_prefix(),
        "leaves": ta.get_output_edges(inverse=True),
        "length": len(assignment),
        "vis": ta.get_var_visibility(),
        "debug": verbose,
    }

    def sort_keys(ta: TTreeAut, state: str) -> list:
        result = []
        # NOTE: maybe there is a way to append (tail) and push (head) into the list ...
        for key, edge in ta.transitions[state].items():
            if edge.info.variable != "" or not edge.is_self_loop():  # and len(edge.children) != 0:
                result.append(key)
        for key, edge in ta.transitions[state].items():
            if edge.info.variable == "":  # and len(edge.children) != 0:
                if key not in result:
                    result.append(key)
        return result

    def backtrack(ta: TTreeAut, variable: int, state: str, assignment: dict):
        if state in sim_helper["leaves"]:  # or variable > sim['length']:
            if sim_helper["debug"]:
                print(f" END -> {sim_helper['leaves'][state][0]} : {state} = leaf")
            return sim_helper["leaves"][state][0]
        if variable not in assignment:
            return None
        try:
            value = assignment[variable]
        except:
            print(assignment)

        for key in sim_helper["keys"][state]:
            edge: TTransition = ta.transitions[state][key]
            if edge.info.variable != "":
                if f"{sim_helper['prefix']}{variable}" != edge.info.variable:
                    if len(ta.transitions[state]) == 1:
                        if sim_helper["debug"]:
                            print(f" {variable :<3} -> {value} : skipping")
                        # sim_helper['path'].append(state)
                        result = backtrack(ta, variable + 1, state, assignment)
                        if result is not None:
                            return result
                    if sim_helper["debug"]:
                        print(f" {variable :<3} -> {value} : ", end="")
                        print(f"{ta.get_edge_string(edge)} -> incompatible variable")
                    continue
            new_state = edge.children[value]
            if sim_helper["debug"]:
                print(f"[{variable :<3} -> {value}]: {ta.get_edge_string(edge)} -> {new_state}")
            # sim_nelper['path'].append(new_state)
            result = backtrack(ta, variable + 1, new_state, assignment)
            if result is not None:
                return result

    root = ta.roots[0]
    root_var = list(sim_helper["vis"][root])[0]
    start = int(root_var) if starting_var is None else int(starting_var)
    sim_helper["keys"] = {state: sort_keys(ta, state) for state in ta.get_states()}
    if sim_helper["debug"]:
        print(f"{ta.name} - simulating variable assignment")
    # sim_helper['path'].append(root)
    result = backtrack(ta, start, root, assignment)
    return result


def leafify(ta: TTreeAut, state: str, value: str | int):
    keys_to_pop = [key for key in ta.transitions[state].keys()]
    vis = ta.get_var_visibility()
    max_var = max(vis[state])
    for key in keys_to_pop:
        ta.transitions[state].pop(key)
    new_edge = TTransition(state, TEdge(str(value), [], f"{max_var}"), [])
    ta.transitions[state][keys_to_pop[0]] = new_edge
    # new_edge = TTransition(state, TEdge('LH', [], ""), [state, state])


# End of file simulation.py
