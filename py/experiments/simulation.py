"""
[file] simulation.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Equivalence testing via inputting all possible variable assignments.
[note] Used during developing/debugging the folding procedure.
"""

from typing import Callable, Union, Optional

from bdd.bdd_node import BDDnode
from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from helpers.string_manipulation import get_var_prefix_from_list
from bdd.bdd_class import BDD
from tree_automata.functions.emptiness import non_empty_bottom_up


def get_var_evaluation(obj: Union[TTreeAut, BDD], assignment: list) -> dict:
    """
    Creates a lookup table for each variable in a simulated object.
    The object is expected to have a unified names of variables
      - same prefix followed by a number, eg. ['x1', 'x2', 'x3', etc.]
    """
    var_list: list[str] = []
    if type(obj) == BDD:
        var_list = obj.get_variable_list()
    if type(obj) == TTreeAut:
        var_list = obj.get_var_order()
    assert var_list != []
    prefix: str = get_var_prefix_from_list(var_list)
    vars: dict[str, int] = {f"{prefix}{i}": val for i, val in enumerate(assignment, 1)}
    return vars


def simulate_run_bdd(bdd: BDD, assignment: dict[int, int], verbose=False) -> bool:
    """
    Simulates boolean computation of all variable settings.
    """
    # if type(assignment) == list:
    #     vars: dict = get_var_evaluation(bdd, assignment)
    # else:
    #     vars: dict = assignment

    result: Optional[int] = None
    node: BDDnode = bdd.root
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
        self.var_lookup: dict = assignment
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


def simulate_run_treeaut(ta: TTreeAut, assignment: list[int], verbose=False) -> bool:
    """
    # Simulates a run through the automaton (branching / deciding process),
    # given a variable evaluation. Returns a value on a leaf node
    # ... with UBDAs => 1 = true, 0 = false
    # NOTE: So far works with unfolded/normalized UBDA.
    """

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


def find_function(obj: Union[TTreeAut, BDD]) -> Callable:
    if type(obj) == TTreeAut:
        return simulate_run_treeaut_dict
    if type(obj) == BDD:
        return simulate_run_bdd
    return None


def assign_variables(num: int, size: int) -> list[int]:
    """
    Creates a list of variable truth-values indexed by their order
    (the order in which they are evaluated during BDD top-down traversal)
    if an ABDD has a variable range of size 10, this function would be used 2^10 times.

    Basically computes a bit vector of size `size` of the binary representing of a number `num`.
    """
    result: list[int] = []
    division: int = num
    for _ in range(size):
        remainder: int = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return result


def assign_variables_dict(num: int, size: int) -> dict[int, int]:
    """
    Create an int -> int (variable index -> 0/1 = true/false) dictionary from a number.
    Needed in semantic checking based on evaluating all variable assignments.
    (Iterating through all numbers in a range of 2 ^ (variable count)).
    if an ABDD has a variable range of size 10, this function is used 2^10 times
    """
    result: list[int] = []
    division: int = num
    for _ in range(size):
        remainder: int = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return {i + 1: result[i] for i in range(size)}


def is_empty(obj: Union[TTreeAut, BDD]) -> bool:
    if type(obj) == TTreeAut:
        obj: TTreeAut
        witness_tree, witness_str = non_empty_bottom_up(obj)
        return witness_tree is None
    if type(obj) == BDD:
        obj: BDD
        return obj.root is None


def simulate_and_compare(
    obj1: Union[TTreeAut, BDD], obj2: Union[TTreeAut, BDD], variables: int, debug=False, output=None
) -> bool:
    """
    [description]
    Compare the semantics of two BDDs (either defined as a TTreeAut class => BDA/ABDD or a BDD object itself)
    through iterating over all possible variable evaluations.

    Works in exponential time wrt. number of variables (BDD of 20 variables checks 2^20 assignments).

    [parameters]
    - obj1, obj2: BDDs/ABDDs/BDAs to be compared
    - variables: how many variables to be compared against (max var index if labelled from 1 for root nodes/states)
    - debug: print progress (%) and for which assignments the functions do not behave the same
    - output: file to which error prints are written.

    [return]
    - True if equivalent, otherwise False
    """
    function_for_obj_1: Callable = find_function(obj1)
    function_for_obj_2: Callable = find_function(obj2)
    # results1 = ""
    # results2 = ""
    same: bool = True
    step: int = (2**variables) // 25  # for progress bar printing
    progress: int = 0  # for progress bar printing
    # if compare_emptiness()
    if is_empty(obj1) != is_empty(obj2):
        return False
    if is_empty(obj1) and is_empty(obj2):
        return True
    if debug:
        # print(f"Comparing equivalence of {obj1.name} and {obj2.name}")
        print(f"Equivalence check: {obj1.name} ...")
    if output is not None:
        output.write(f"Comparing equivalence of {obj1.name} and {obj2.name}\n\n")
    for i in range(2 ** (variables)):
        current_assignment: dict[int, int] = assign_variables_dict(i, variables)
        res1 = function_for_obj_1(obj1, current_assignment)
        res2 = function_for_obj_2(obj2, current_assignment)
        # print(current_assignment, f"1 = {res1}, 2 = {res2}")
        same = same and (res1 == res2)  # once it becomes false, it never becomes true again
        if res1 != res2 and debug:
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


class SimHelperTreeAutDict:
    def __init__(self, ta: TTreeAut, assignment: Union[list[int], dict[int, int]], verbose: bool = False):
        self.prefix: str = ta.get_var_prefix()
        self.leaves: dict[str, list[str]] = ta.get_output_edges(inverse=True)
        self.length: int = len(assignment)
        self.vis: dict[str, set[str]] = ta.get_var_visibility()
        self.debug: bool = verbose
        self.keys: dict[str, list[str]] = {state: sort_keys(ta, state) for state in ta.get_states()}
        # self.path: list[str] = []


def sort_keys(ta: TTreeAut, state: str) -> list:
    """
    Given a state of a UBDA/BDA, return a list of transition keys, such that
    transitions with variables and non-self loops are first,
    and transitions without variables or (partial) self-loops are last.

    This gives the order in which the transitions should be explored
    during the backtracking simulation algorithm.
    """
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


def simulate_run_treeaut_dict(ta: TTreeAut, assignment: dict[int, int], verbose=False, starting_var=None):
    """
    Given an assignment
    """
    sim_helper = SimHelperTreeAutDict(ta, assignment, verbose)

    def backtrack(
        ta: TTreeAut, variable: int, state: str, assignment: Union[dict[int, int], list[int]]
    ) -> Optional[str]:
        if state in sim_helper.leaves:
            if sim_helper.debug:
                print(f" END -> {sim_helper.leaves[state][0]} : {state} = leaf")
            return sim_helper.leaves[state][0]
        if variable not in assignment:
            return None
        try:
            value = assignment[variable]
        except:
            print(assignment)

        for key in sim_helper.keys[state]:
            edge: TTransition = ta.transitions[state][key]
            if edge.info.variable != "":
                if f"{sim_helper.prefix}{variable}" != edge.info.variable:
                    if len(ta.transitions[state]) == 1:
                        if sim_helper.debug:
                            print(f" {variable :<3} -> {value} : skipping")
                        # sim_helper.path.append(state)
                        result = backtrack(ta, variable + 1, state, assignment)
                        if result is not None:
                            return result
                    if sim_helper.debug:
                        print(f" {variable :<3} -> {value} : ", end="")
                        print(f"{ta.get_edge_string(edge)} -> incompatible variable")
                    continue
            new_state = edge.children[value]
            if sim_helper.debug:
                print(f"[{variable :<3} -> {value}]: {ta.get_edge_string(edge)} -> {new_state}")
            # sim_nelper.path.append(new_state)
            result = backtrack(ta, variable + 1, new_state, assignment)
            if result is not None:
                return result

    root: str = ta.roots[0]
    root_var: str = list(sim_helper.vis[root])[0]
    start: int = int(root_var) if starting_var is None else int(starting_var)
    if sim_helper.debug:
        print(f"{ta.name} - simulating variable assignment")
    # sim_helper.path.append(root)
    result: Optional[str] = backtrack(ta, start, root, assignment)
    return result


# below are unused functions:


def leafify(ta: TTreeAut, state: str, value: str | int):
    """
    Turns a state into a leaf - output transition will be labeled with the max variable visible.
    """
    keys_to_pop: list[str] = [key for key in ta.transitions[state].keys()]
    # note to fix: get_var_visibility assumes strings
    vars_visible_from_state: dict[str, set[int]] = ta.get_var_visibility()
    max_var: int = max(vars_visible_from_state[state])
    for key in keys_to_pop:
        ta.transitions[state].pop(key)
    new_edge = TTransition(state, TEdge(str(value), [], f"{max_var}"), [])
    ta.transitions[state][keys_to_pop[0]] = new_edge
    # new_edge = TTransition(state, TEdge('LH', [], ""), [state, state])


# End of file simulation.py
