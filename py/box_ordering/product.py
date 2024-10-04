import itertools
from typing import Tuple, List, Dict

from tree_automata import TTreeAut, TEdge, TTransition
from helpers.string_manipulation import create_string_from_name_list


def create_roots(ta1: TTreeAut, ta2: TTreeAut) -> list:
    """
    Docstring TBD
    """
    root_merge: List = []
    root_merge.append(ta1.roots)
    root_merge.append(ta2.roots)
    roots: List[List[str]] = itertools.product(*root_merge)
    return [list(i) for i in roots]


def productify(
    state1: str,
    state2: str,
    ta1: TTreeAut,
    ta2: TTreeAut,
    edge_list: List[Tuple[str, str, Tuple[str, str]]],
    done: List[Tuple[str, str]],
) -> None:
    """
    Docstring TBD
    """
    if [state1, state2] in done:
        return
    done.append([state1, state2])
    for edge1 in ta1.transitions[state1].values():
        for edge2 in ta2.transitions[state2].values():
            src_state: List[str] = [edge1.src, edge2.src]
            sym1: str = edge1.info.label
            sym2: str = edge2.info.label
            if len(edge1.children) == 0 and len(edge2.children) == 0:
                # handle output symbols
                if sym1 == sym2 or sym1.startswith("Port"):
                    edge_list.append(tuple((src_state, sym1, [])))

            if sym1 == sym2 and len(edge1.children) > 0:
                children: List[Tuple[str, str]] = []

                # TODO: this works only with symbols of arity 2
                for i in range(len(edge1.children)):
                    children.append(tuple([edge1.children[i], edge2.children[i]]))

                edge_list.append(tuple((src_state, sym1, children)))
                for i in children:
                    if [i[0], i[1]] not in done:
                        productify(i[0], i[1], ta1, ta2, edge_list, done)


def create_product_relation(edge_list: list[Tuple[str, str, list[str]]], alphabet: dict) -> dict:
    """
    Docstring TBD
    """
    edge_dict: Dict[str, Dict[str, TTransition]] = {}
    for edge in edge_list:
        src_state: str = create_string_from_name_list(edge[0])
        if src_state not in edge_dict:
            edge_dict[src_state] = {}
        edge_obj = TEdge(edge[1], [None] * alphabet[edge[1]], "")
        children: List[str] = [create_string_from_name_list(edge[2][i]) for i in range(len(edge[2]))]
        key: str = f"{src_state}-{edge[1]}-{children}"
        edge_dict[src_state][key] = TTransition(src_state, edge_obj, children)
    return edge_dict


def tree_aut_product(ta1: TTreeAut, ta2: TTreeAut) -> TTreeAut:
    """
    Docstring TBD

    Note: needed for co-occurrence relation
    """
    alphabet: Dict[str, int] = {**ta1.get_symbol_arity_dict(), **ta2.get_symbol_arity_dict()}
    roots: List[List[str]] = create_roots(ta1, ta2)
    edge_list: List[Tuple[str, str, Tuple[str, str]]] = []
    done: List[Tuple[str, str]] = []
    for root in roots:
        productify(root[0], root[1], ta1, ta2, edge_list, done)

    new_roots: List[str] = [create_string_from_name_list(i) for i in roots]
    edge_dict: Dict[str, Dict[str, TTransition]] = create_product_relation(edge_list, alphabet)
    result = TTreeAut(new_roots, edge_dict, f"product({ta1.name},{ta2.name})", 0)
    result.port_arity = result.get_port_arity()

    return result
