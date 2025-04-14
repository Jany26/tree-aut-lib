import itertools
from apply.abdd import ABDD
from apply.box_algebra.apply_tables import BooleanOperation
from tree_automata.automaton import TTreeAut


def evaluate_for_treeaut_backtrack(ta: TTreeAut, assignment: list[int]) -> int:
    """
    Backtracking evaluator for TTreeAut using a boolean assignment list.

    assignment: list of 0/1
    """

    prefix = ta.get_var_prefix()

    def dfs(state: str, idx: int) -> int | None:
        for t in ta.transitions[state].values():
            if t.info.label in ["0", "1"]:
                # print(f'return {t.info.label}')
                return int(t.info.label)

        if idx >= len(assignment):
            return None

        val = assignment[idx]
        var = f"{prefix}{idx + 1}"
        # print(f'dfs({state}, {idx}), val={val}, var={var}')

        for t in ta.transitions[state].values():
            if t.info.variable == var and not t.is_self_loop():
                next_state = t.children[val]
                res = dfs(next_state, idx + 1)
                if res is not None:
                    return res

        for t in ta.transitions[state].values():
            if t.is_self_loop():
                next_state = t.children[val]
                res = dfs(next_state, idx + 1)
                if res is not None:
                    return res

        return None  # backtrack

    result = dfs(ta.roots[0], 0)
    if result is None:
        raise Exception("evaluate_for_treeaut_backtrack(): no accepting path found!")
    return result


def compare_abdds_tas(input1: ABDD | TTreeAut, input2: ABDD | TTreeAut, debug=False) -> bool:
    varcount1 = input1.variable_count if isinstance(input1, ABDD) else (input1.get_var_max() - 1)
    varcount2 = input2.variable_count if isinstance(input2, ABDD) else (input2.get_var_max() - 1)
    if varcount1 != varcount2:
        raise ValueError("cannot compare abdds with unequal number of vars")

    equal = True
    for assign_tuple in itertools.product([0, 1], repeat=varcount1):
        assignment = list(assign_tuple)
        # print('evaluating', assignment)
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
        if res1 != res2:
            equal = False
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
            print(f"{input1.name} eval'd for {assignment} = {res1}")
            print(f"{input2.name} eval'd for {assignment} = {res2}")
            break
    return equal


def compare_op_abdd(input1: ABDD, input2: ABDD, op: BooleanOperation, output: ABDD) -> bool:
    equal = True
    for assign_tuple in itertools.product([0, 1], repeat=output.variable_count):
        assignment = list(assign_tuple)
        # print('evaluating', assignment)
        res1 = input1.evaluate_for(assignment)
        res2 = input2.evaluate_for(assignment)
        res = output.evaluate_for(assignment)

        if any(
            [
                op.name == "AND" and ((res1 and res2) != res),
                op.name == "OR" and ((res1 or res2) != res),
                op.name == "XOR" and ((res1 != res2) != res),
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
    Traverse a UBDA using assignment values. We assume that variables are in the form
    '1', '2', ... '10', etc. - directly convertible from str to int.
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
