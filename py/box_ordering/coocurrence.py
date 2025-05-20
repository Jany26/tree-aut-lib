"""
[file] coocurrence.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Functions for computing coocurence relation between two tree automata.
[note] Part of a preliminary work on trying to find a total order over boxes
with regards to their language inclusion properties.
"""

from itertools import product
from typing import List, Set, Dict

from tree_automata import TTreeAut, remove_useless_states, tree_aut_intersection, non_empty_top_down
from box_ordering.product import tree_aut_product


def get_co_ocurent_states_top_down(ta: TTreeAut) -> List:
    """
    Docstring TBD
    """

    def merge(state, macro_list) -> Set[str]:
        """
        Docstring TBD
        """
        result: List[str] = [state]
        for item in macro_list:
            result.extend(item)
        return set(result)

    def process(state, ta, queue) -> List[str]:
        """
        Docstring TBD
        """
        queue.append(state)
        result: List[str] = []
        for edge in ta.transitions[state].values():
            process_results: List = []
            for child in edge.children:
                if child == state:
                    continue
                if child in queue:
                    continue
                process_results.append(process(child, ta, queue[:]))

            if edge.children == [] or process_results != []:
                result.extend([merge(state, macro_list) for macro_list in product(*process_results)])
        return result

    # -------------------------------------

    temp = []
    for i in ta.roots:
        temp.extend(process(i, ta, []))

    result = []
    for i in temp:
        x: List = list(i)
        x.sort()
        if x not in result:
            result.append(x)
    return result


def produce_output_tuples(ta1: TTreeAut, ta2: TTreeAut) -> dict:
    """
    Docstring TBD
    """
    out_edges_1 = ta1.get_output_edges(inverse=True)
    out_edges_2 = ta2.get_output_edges(inverse=True)
    result = {}
    for state1 in ta1.transitions:
        for state2 in ta2.transitions:
            key = f"({state1},{state2})"
            entry1 = out_edges_1[state1] if state1 in out_edges_1 else []
            entry2 = out_edges_2[state2] if state2 in out_edges_2 else []
            result[key] = (entry1, entry2)
    return result


def tree_aut_is_extension(ta1: TTreeAut, ta2: TTreeAut) -> bool:
    """
    Docstring TBD
    """
    debug: bool = False
    product: TTreeAut = remove_useless_states(tree_aut_product(ta1, ta2))
    co_occurent_list = get_co_ocurent_states_top_down(product)
    output_tuples = produce_output_tuples(ta1, ta2)
    out_edges = product.get_output_edges(inverse=True)

    if debug:
        print(ta1)
        print(ta2)
        print(product)
    full_list: List = []
    for i in co_occurent_list:
        temp_list = []
        for j in i:
            temp_list.append((j, output_tuples[j]))
        full_list.append(temp_list)

    if debug:
        for i in full_list:
            for j in i:
                print(j)
            print()

    # CHECKING LEAF-EDGE CONSISTENCY
    for coocurrence in full_list:
        check_dict = {}
        for state, edge_tuple in coocurrence:
            edges1, edges2 = edge_tuple

            # TODO: GENERALISATION NEEDED
            # e.g. going over all possible leaf-transitions in 1 state

            symbol1 = edges1[0] if edges1 != [] else ""
            symbol2 = edges2[0] if edges2 != [] else ""
            if symbol1 == "" or symbol2 == "":
                continue
            if symbol2 not in check_dict:
                check_dict[symbol2] = []
            if symbol1 not in check_dict[symbol2]:
                check_dict[symbol2].append(symbol1)
        for _, possible_leaf_edges in check_dict.items():
            if len(possible_leaf_edges) != 1:
                return False
    full_list = []
    for state_set in co_occurent_list:
        tuple_list = []
        for state in state_set:
            symbols = out_edges[state] if state in out_edges else []
            if (state, symbols) not in tuple_list:
                tuple_list.append((state, symbols))
        if tuple_list not in full_list:
            full_list.append(tuple_list)
    check_list = []
    for tuple_list in full_list:
        check = {}
        for item in tuple_list:
            for symbol in item[1]:
                if symbol.startswith("Port"):
                    if symbol not in check:
                        check[symbol] = []
                    check[symbol].append(item[0])
        check_list.append(check)
    for list_set in check_list:
        for state_list in list_set.values():
            intersection = None
            for state in state_list:
                product.roots = [state]
                intersection = tree_aut_intersection(product, intersection)
            witness_tree, _ = non_empty_top_down(intersection)
            if witness_tree is not None:
                return True
    return False


# End of file cooccurrence.py
