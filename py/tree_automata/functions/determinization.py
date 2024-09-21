import copy
from itertools import product

from helpers.string_manipulation import create_string_from_name_set
from tree_automata import TTreeAut, TEdge, TTransition


# Create a "reverse" transition dictionary, in which parents of specified edges
#  can be found -- important for bottom-up algorithms (determinization).
#  Lookup goes like this:
#    symbol -> children -> then the parent/source state is found
#  Note: list of children is "stringified"
# {symbol : {"children" : [parents]}}
def det_create_lookup(ta: TTreeAut, alphabet) -> dict:
    result = {symbol: {} for symbol in alphabet}
    for edges in ta.transitions.values():
        for edge in edges.values():
            symbol = edge.info.label

            if str(edge.children) not in result[symbol]:
                result[symbol][str(edge.children)] = []

            if edge.src not in result[symbol][str(edge.children)]:
                result[symbol][str(edge.children)].append(edge.src)
    return result


# Creates all needed permutations for determinization consideration,
#  which contain the specified 'state' and other states are filled with states
#  from the 'states' (to get the specific permutation 'size').
def det_generate_tuples(states: list, state: list, size: int) -> list:
    prod = product(states, repeat=size)
    return [list(i) for i in prod if state in i]


# Creates a list of output states based on the symbols.
def det_out_edges(out_edges: list, done_edges, alphabet):
    result = []
    for symbol in out_edges:
        done_edges.append([out_edges[symbol], symbol, []])
        result.append(out_edges[symbol])

    for symbol in alphabet:
        if symbol not in out_edges and alphabet[symbol] == 0:
            done_edges.append([[], symbol, []])
            if [] not in result:
                result.append([])
    return result


# Finds all possible source states (parents) for a set of given
#  macrostates (lists of states) - parameter 'tuple'.
#  For this, a lookup dictionary is created at the start of determinization.
#  Function tries to perform a bottom-up step:
#  trying to find a feasible transition from a given children tuple
def det_child_handle(tuple: list, lookup: dict) -> list:
    children = [list(i) for i in product(*tuple)]
    result = []
    for i in children:
        if str(i) not in lookup:
            continue
        for j in lookup[str(i)]:
            if j in result:
                continue
            result.append(j)
    result.sort()
    return result


# This function creates a transition dict for the resulting tree automaton,
#  based on the ad-hoc data notes created during determinization.
#  The result is in the right format needed for TTreeAut class.
def det_create_relation(edge_list: list, alphabet: dict) -> dict:
    edge_dict = {}
    # print(f"> ALPHABET\n{alphabet}")
    for edge in edge_list:
        # print(f"  > EDGE = {edge}")
        source = create_string_from_name_set(edge[0])
        symbol = TEdge(edge[1], [None] * alphabet[str(edge[1])], "")
        # print(f"    > SRC = {source}")
        # print(f"    > SYM = {edge[1]}")
        # print(f"    > CHI = {edge[2]}")
        children = [create_string_from_name_set(i) for i in edge[2]]
        key = f"{source}-{edge[1]}->({children})"
        if source not in edge_dict:
            edge_dict[source] = {}
        edge_dict[source][key] = TTransition(source, symbol, children)
    return edge_dict


def det_create_roots(done_states: list, roots: list) -> list:
    result = set()
    for done_set in done_states:
        for root in roots:
            if root in done_set:
                result.add(create_string_from_name_set(done_set))
    return list(result)


# Creates a deterministic and complete version of the "ta"
#  tree automaton with regards to the "alphabet"
#  alphabet is a dictionary -> key = "symbol", value = arity (integer)
#  done_states = list of macrostates (macrostate = list of states/strings)
#  done_transitions = dictionary of transitions,
#  key is just some string created from done_states by a function
#       - each key references a list/dict of all possible transitions
#  the transitions themselves look like this:
#       [ parent_macro_state, symbol, child_macro_state_list ]
#       - parent_macro_state = list of states
#       - symbol =
#       - child_macro_state_list = list of lists of states
#           - from which the states in parent_macro_state can be reached
#             through an edge labeled with the symbol
#
#  * IMPORTANT NOTE
#     = done_states and done_transitions are just placeholder structures
#       - in the final automaton the macro_states
#         (list/set of states) will be represented by a string
#       - this string is created using make_name_from_set() function
def tree_aut_determinization(ta: TTreeAut, alphabet: dict, verbose=False) -> TTreeAut:

    parent_lookup = det_create_lookup(ta, alphabet)
    done_tuples = {symbol: {} for symbol in alphabet}
    done_edges = []
    done_set = det_out_edges(ta.get_output_edges(), done_edges, alphabet)
    work_set = copy.deepcopy(done_set)
    if verbose:
        print("{:<60} {:<20} {:<60} {:<5} {:<5}".format("current_state", "symbol", "children", "work", "done"))
        print("-" * 160)
        counter = 0
    while work_set != []:
        state = work_set[0]
        work_set.remove(state)
        done_set.append(state)
        for symbol, arity in alphabet.items():
            lookup = parent_lookup[symbol]
            if lookup == {}:
                # TODO: HANDLE UNUSED SYMBOL
                pass
            combinations = det_generate_tuples(done_set, state, arity)
            for tuple in combinations:
                # print(combinations)
                if str(tuple) in done_tuples[symbol]:
                    continue
                if verbose:
                    counter += 1
                    print(
                        "{:<60} {:<20} {:<60} {:<5} {:<5}".format(
                            f"{counter}) {state}"[:60], symbol[:20], str(tuple)[:60], len(work_set), len(done_set)
                        )
                    )
                parents = det_child_handle(tuple, lookup)
                done_tuples[symbol][str(tuple)] = parents
                if parents not in work_set:
                    work_set.append(parents)
                done_edges.append([parents, symbol, tuple])

    new_roots = det_create_roots(done_set, ta.roots)
    new_edges = det_create_relation(done_edges, alphabet)
    result = TTreeAut(new_roots, new_edges, f"determinized({ta.name})")
    result.port_arity = result.get_port_arity()

    if verbose:
        print(f"determinization of {ta.name} done")

    return result
