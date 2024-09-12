from tree_automata import TTreeAut, iterate_edges
from tree_automata.functions.helpers import generate_possible_children


def get_all_state_reachability(ta: TTreeAut, reflexive=False) -> dict:
    old_roots = [i for i in ta.roots]
    result = {}
    for i in ta.get_states():
        ta.roots = [i]
        result[i] = set(reachable_top_down(ta, count_itself=reflexive))
    ta.roots = [i for i in old_roots]
    return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Generates a list of states reachable from the root states
def reachable_top_down(ta: TTreeAut, count_itself=True) -> list:
    worklist = [i for i in ta.roots]
    result = [i for i in ta.roots] if count_itself is True else []

    while len(worklist) > 0:
        state = worklist.pop()

        if state not in ta.transitions:
            continue

        for edge in ta.transitions[state].values():
            for i in edge.children:
                if i not in result:
                    worklist.append(i)
                    result.append(i)
    return result


# Generates a list of states reachable from the leaf states
def reachable_bottom_up(ta: TTreeAut) -> list:

    # this is needed for some longer children arrays
    # {'symbol1' : {'state1': 2, 'state2': 1}, 'symbol2': ...}
    def create_state_arity_dict(ta) -> dict:
        result = {}
        arities = ta.get_symbol_arity_dict()
        for symbol, arity in arities.items():
            if arity == 0:
                continue
            if symbol not in result:
                result[symbol] = {}
            for state in ta.get_states():
                if state not in result[symbol]:
                    result[symbol][state] = []

        for edge in iterate_edges(ta):
            child_set = set(edge.children)
            symbol = edge.info.label
            if arities[symbol] == 0:
                continue
            length = len(edge.children)
            for state in child_set:
                if length not in result[symbol][state]:
                    result[symbol][state].append(length)
        return result

    worklist = ta.get_output_states()
    result = ta.get_output_states()
    arity_dict = ta.get_symbol_arity_dict()
    extended_arity_dict = create_state_arity_dict(ta)
    while len(worklist) > 0:
        state = worklist.pop()
        for symbol, arity in arity_dict.items():
            if arity <= 0:
                continue

            arities = extended_arity_dict[symbol][state]
            tuples = []
            for a in arities:
                tuples.extend(generate_possible_children(state, result, a))

            # for state_name, edge_dict in ta.transitions.items():
            #     for edge in edge_dict.values():
            for edge in iterate_edges(ta):
                if edge.info.label != symbol or edge.children not in tuples:
                    continue
                if edge.src not in result:
                    worklist.append(edge.src)
                    result.append(edge.src)  # similarly for dictionary
    return result
