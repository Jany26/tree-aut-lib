"""
[file] reachability.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Obtaining sets of reachable states of a tree automaton.
"""

from tree_automata import TTreeAut, iterate_edges
from tree_automata.functions.helpers import generate_possible_children


def get_all_state_reachability(ta: TTreeAut, reflexive=False) -> dict[str, set[str]]:
    """
    For each state q of tree automaton 'ta',
    get a set of states that are top-down reachable from q.

    If reflexive=True, the state 'q' itself is also counted towards reachability.
    """
    old_roots: list[str] = [i for i in ta.roots]
    result: dict[str, set[str]] = {}
    for i in ta.get_states():
        ta.roots = [i]
        result[i] = set(reachable_top_down(ta, count_itself=reflexive))
    ta.roots = [i for i in old_roots]
    return result


def reachable_top_down(ta: TTreeAut, count_itself=True) -> list[str]:
    """
    Generates a list of states reachable from the root states.
    """
    worklist: list[str] = [i for i in ta.roots]
    result: list[str] = [i for i in ta.roots] if count_itself is True else []

    while len(worklist) > 0:
        state: str = worklist.pop()

        if state not in ta.transitions:
            continue

        for edge in ta.transitions[state].values():
            for i in edge.children:
                if i not in result:
                    worklist.append(i)
                    result.append(i)
    return result


def create_state_arity_dict(ta: TTreeAut) -> dict[str, dict[str, list[int]]]:
    """
    TODO: Find out why is this extended arity dictionary needed?

    this is needed for some longer children arrays
    {'symbol1' : {'state1': 2, 'state2': 1}, 'symbol2': ...}
    """
    result: dict[str, dict[str, list[int]]] = {}
    arities: dict[str, int] = ta.get_symbol_arity_dict()
    for symbol, arity in arities.items():
        if arity == 0:
            continue
        if symbol not in result:
            result[symbol] = {}
        for state in ta.get_states():
            if state not in result[symbol]:
                result[symbol][state] = []

    for edge in iterate_edges(ta):
        child_set: set[str] = set(edge.children)
        symbol: str = edge.info.label
        if arities[symbol] == 0:
            continue
        length = len(edge.children)
        for state in child_set:
            if length not in result[symbol][state]:
                result[symbol][state].append(length)
    return result


def reachable_bottom_up(ta: TTreeAut) -> list[str]:
    """
    Get a list of states that are reachable from the leaf states.
    Parent state is only reachable if there is a transition to some child
    n-tuple and all n child states are bottom-up reachable.
    (i.e. for each state 'q' there exists some tree that the TA rooted in 'q' can generate).

    Here is an example of bottom-up unreachability.
    q0--a-->(q1, q2)  # q0 is bottom-up unreachable
    q1--b-->()        # because even though q2 has an output transition, thus is bottom-up reachable,
    q2--x-->(q2, q2)  # there is no output transition for q2 (only a "self-loop") - tree generation cannot terminate.
    """
    worklist: list[str] = list(ta.get_output_states())
    result: list[str] = list(ta.get_output_states())
    arity_dict: dict[str, int] = ta.get_symbol_arity_dict()
    extended_arity_dict: dict[str, dict[str, list[int]]] = create_state_arity_dict(ta)
    while len(worklist) > 0:
        state: str = worklist.pop()
        for symbol, arity in arity_dict.items():
            if arity <= 0:
                continue

            # TODO: this can probably be simplified to omit extended_arity_dict
            arities: list[int] = extended_arity_dict[symbol][state]
            child_tuple_array: list[list[str]] = []
            for a in arities:
                child_tuple_array.extend(generate_possible_children(state, result, a))

            for edge in iterate_edges(ta):
                if edge.info.label != symbol or edge.children not in child_tuple_array:
                    continue
                if edge.src not in result:
                    worklist.append(edge.src)
                    result.append(edge.src)  # similarly for dictionary
    return result


# End of file reachability.py
