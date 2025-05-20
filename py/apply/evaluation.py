"""
[file] evaluation.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Testing for correctness of ABDD semantics by brute-force checking results of all var assignments.
"""

import itertools
from apply.abdd import ABDD
from apply.box_algebra.apply_tables import BooleanOperation
from tree_automata.automaton import TTreeAut, iterate_edges_from_state


def evaluate_for_treeaut_backtrack(ta: TTreeAut, assignment: list[int], debug=False) -> int:
    """
    Backtracking evaluator for TTreeAut (unfolded and normalizaed) using a Boolean assignment list.
    (more robust since it can potentially handle edges with multiple self loops)
    assignment: list of 0/1
    """

    prefix = ta.get_var_prefix()

    def dfs(state: str, idx: int) -> int | None:
        for t in ta.transitions[state].values():
            if t.info.label in ["0", "1"]:
                return int(t.info.label)

        if idx >= len(assignment):
            return None

        # assignment is indexed from 0
        # variables in the TAs are indexed from 1
        val = assignment[idx]
        var = f"{prefix}{idx + 1}"
        if debug:
            print(f"dfs(state={state}, idx={idx}, var={var}, val={val}), assign={assignment}")

        # first, we check if there is a transition with the current variable and pick it if equal
        for e1 in iterate_edges_from_state(ta, state):
            if not e1.is_self_loop() and e1.info.variable != "" and e1.info.variable == var:
                next_state = e1.children[val]
                if debug:
                    print(
                        f"A) using transition {e1} at idx={idx}, var={var}, val={assignment[idx]} to visit state {next_state}",
                        e1.info.variable,
                        type(e1.info.variable),
                        var,
                        type(var),
                    )
                res = dfs(next_state, idx + 1)
                if res is not None:
                    return res
        # if not, we pick some self-loop, if it fails to terminate, we pick another one
        for e2 in iterate_edges_from_state(ta, state):
            if not e2.is_self_loop():
                continue
            next_state = e2.children[val]
            if debug:
                print(
                    f"B) using transition {e2} at idx={idx}, var={var}, val={assignment[idx]} to visit state {next_state}",
                    e2.info.variable,
                    type(e2.info.variable),
                    var,
                    type(var),
                )
            try:
                res = dfs(next_state, idx + 1)
                if res is not None:
                    return res
            except:
                continue
        return None  # backtrack

    if debug:
        print(f"evaluating_treeaut_backtrack(): {assignment}")
    result = dfs(ta.roots[0], 0)
    if result is None:
        raise Exception("evaluate_for_treeaut_backtrack(): no accepting path found!")
    return result


def compare_abdds_tas(input1: ABDD | TTreeAut, input2: ABDD | TTreeAut, debug=False) -> bool:
    """
    Given two input ABDDs/UBDAs (without boxes), compare their semantics by checking results of all assignments.
    """
    varcount1 = input1.variable_count if isinstance(input1, ABDD) else (input1.get_var_max() - 1)
    varcount2 = input2.variable_count if isinstance(input2, ABDD) else (input2.get_var_max() - 1)
    if varcount1 != varcount2:
        raise ValueError("cannot compare abdds with unequal number of vars")

    equal = True
    for assign_tuple in itertools.product([0, 1], repeat=varcount1):
        assignment = list(assign_tuple)
        try:
            res1 = (
                evaluate_for_treeaut_backtrack(input1, assignment)
                if isinstance(input1, TTreeAut)
                else input1.evaluate_for(assignment)
            )
            res2 = (
                evaluate_for_treeaut_backtrack(input2, assignment)
                if isinstance(input2, TTreeAut)
                else input2.evaluate_for(assignment)
            )
        except:
            print(f"exception raised for {input1.name}: {assignment}")
            if isinstance(input1, TTreeAut):
                evaluate_for_treeaut_backtrack(input1, assignment, debug=debug)
            else:
                input1.evaluate_for(assignment, verbose=debug)
            print(f"exception raised for {input2.name}: {assignment}")
            if isinstance(input2, TTreeAut):
                evaluate_for_treeaut_backtrack(input2, assignment, debug=debug)
            else:
                input2.evaluate_for(assignment, verbose=debug)
            return False
        if res1 != res2:
            equal = False
            res1 = (
                evaluate_for_treeaut_backtrack(input1, assignment, debug=debug)
                if isinstance(input1, TTreeAut)
                else input1.evaluate_for(assignment, verbose=debug)
            )
            res2 = (
                evaluate_for_treeaut_backtrack(input2, assignment, debug=debug)
                if isinstance(input2, TTreeAut)
                else input2.evaluate_for(assignment, verbose=debug)
            )
            print(f"{input1.name} eval'd for {assignment} = {res1}")
            print(f"{input2.name} eval'd for {assignment} = {res2}")
            break
    return equal


def compare_op_abdd(input1: ABDD, input2: ABDD, op: BooleanOperation, output: ABDD) -> bool:
    """
    Given two input ABDDs and a Boolean operator, check result consistency of all variable evaluations:
    'input1 op input2 == output' ?
    """
    equal = True
    for assign_tuple in itertools.product([0, 1], repeat=output.variable_count):
        assignment = list(assign_tuple)
        res1 = input1.evaluate_for(assignment)
        res2 = input2.evaluate_for(assignment)
        res = output.evaluate_for(assignment)

        if any(
            [
                op.name == "AND" and ((res1 and res2) != res),
                op.name == "OR" and ((res1 or res2) != res),
                op.name == "XOR" and (((res1 and not res2) or (not res1 and res2)) != res),
                op.name == "NOR" and ((not (res1 or res2)) != res),
                op.name == "NAND" and ((not (res1 and res2)) != res),
                op.name == "IFF" and ((res1 == res2) != res),
                op.name == "IMPLY" and ((not res1 or res2) != res),
            ]
        ):
            equal = False
            res1 = input1.evaluate_for(assignment, verbose=True)
            res2 = input2.evaluate_for(assignment, verbose=True)
            res = output.evaluate_for(assignment, verbose=True)
            print(f"{input1.name} eval'd for {assignment} = {res1}")
            print(f"{input2.name} eval'd for {assignment} = {res2}")
            print(f"{output.name} eval'd for {assignment} = {res}")
            break
    return equal


# NOTE: cannot work on edges with multiple self-loops, since it does not know how to backtrack
def evaluate_for_treeaut(ta: TTreeAut, assignment: list[int], outvars: dict[str, int]) -> int:
    """
    Traverse a UBDA using assignment values, no backtracking is used.
    We assume that variables are in the form '1', '2', ... '10', etc. - i.e. directly convertible from str to int.
    """
    state = ta.roots[0]
    for idx, val in enumerate(assignment):
        print(f"eval TA: a={assignment} var={idx+1} val={val} s={state}", end="")
        for t in ta.transitions[state].values():
            if t.info.label in ["0", "1"]:
                print(f" return={t.info.label}")
                return int(t.info.label)
        okay = False
        for t in ta.transitions[state].values():
            if not t.is_self_loop() and int(t.info.variable) == idx + 1:
                state = t.children[val]
                print(f" next={state}, using edge = {t}")
                okay = True
                break
            if f"{idx + 1}" not in outvars[t.src] and t.is_self_loop():
                state = t.children[val]
                print(f" next={state}, using edge = {t}")
                okay = True
                break
        if not okay:
            print("\n", idx + 1, t.src, outvars)
            raise Exception("evaluate_for_treeaut(): outvar overtaken!")
    for t in ta.transitions[state].values():
        if t.info.label in ["0", "1"]:
            print(f" return={t.info.label}")
            return int(t.info.label)
    raise Exception("evaluate_for_treeaut(): ran out of vars!")


# End of file evaluation.py
