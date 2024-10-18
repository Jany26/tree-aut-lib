import copy
from typing import Dict, List, Optional, Set, Tuple

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from bdd.bdd_class import BDD
from tree_automata.automaton import iterate_output_edges
from helpers.utils import box_catalogue


def create_tree_aut_from_bdd(bdd: BDD) -> TTreeAut:
    """
    Convert a BDD structure to a tree automaton.
    """
    roots: List[str] = [bdd.root.name]
    transitions: Dict[str, Dict[str, TTransition]] = {}
    key: int = 0
    for node in bdd.iterate_bfs():
        transitions[node.name] = {}
        edge: Optional[TEdge] = None
        children: List[str] = []
        if node.is_leaf():
            edge = TEdge(str(node.value), [], "")
        else:
            edge = TEdge("LH", [], node.value)
            children = [node.low.name, node.high.name]
        new_transition = TTransition(node.name, edge, children)
        transitions[node.name][f"k{key}"] = new_transition

        key += 1

    # A BDA/UBDA created from a BDD has no ports, since it is not a 'box'.
    result = TTreeAut(roots, transitions, bdd.name, 0)
    result.port_arity = result.get_port_arity()
    return result


def add_dont_care_boxes(ta: TTreeAut, vars: int) -> TTreeAut:
    """
    Parses the tree automaton (freshly after dimacs parsing) and adds X boxes
    to the places which make sense.
      - case 1: when an edge skips some variables
          * e.g. node deciding by x1 leads to x4 (as opposed to x2)
      - case 2: when a node that does not contain last variable
          leads straight to a leaf node (basically a variation of case 1)
          * e.g deciding by var x5, but there are 10 variables)
    """
    result: TTreeAut = copy.deepcopy(ta)
    var_prefix: str = result.get_var_prefix()
    # var_visibility: Dict[str, int] = {i: int(list(j)[0]) for i, j in ta.get_var_visibility_deterministic().items()}
    for edge in iterate_output_edges(result):
        if edge.info.variable == "":
            edge.info.variable = f"{var_prefix}{vars}"
    var_visibility: dict[str, int] = result.get_var_visibility_deterministic()
    # print(var_visibility)
    leaves: Set[str] = set(ta.get_output_states())
    # print(leaves)
    # counter: int = 0
    skipped_var_edges: List[Tuple[str, str, TTransition]] = []
    for edge in iterate_edges(result):
        # print(f'analysing edge {edge}')
        if edge.is_self_loop():
            continue
        for idx, child in enumerate(edge.children):
            if (child in leaves and var_visibility[edge.src] != vars) or (
                child not in leaves and var_visibility[child] - var_visibility[edge.src] >= 2
            ):
                # print(f'  > condition satisfied')
                if len(edge.info.box_array) < idx + 1:
                    edge.info.box_array = [None] * len(edge.children)
                edge.info.box_array[idx] = "X"
    for new_state, new_key, new_edge in skipped_var_edges:
        if new_state not in result.transitions:
            result.transitions[new_state] = {}
        if new_key not in result.transitions[new_state]:
            result.transitions[new_state][new_key] = new_edge

    return result


def fill_dont_care_boxes(ta: TTreeAut, max_var: int) -> None:
    """
    Analyze the structure of a BDD-like (or automaton-like) construct,
    and put X / Don't care boxes on edges that seemingly skip some variables
    (e.g. going from a state which sees x4 to a state which sees x7).

    A necessary step for turning BDD-like structures loaded from BLIFs etc. into ABDD-compliant structures.
    A preprocessing step for unfolding, normalization, etc.
    """
    var_prefix = ta.get_var_prefix()
    # if a state 'q' seeing 'x1' has an edge 'e' leading to a state 'r' seeing x5, but 'r' can self-loop,
    # and thus, "catch up" with the missing variables, the edge 'e' does not need to contain a don't care box
    # NOTE: since this function is mostly used with ABDD-like structures, this factor is implemented just
    # for robustness and some potential edge cases
    selflooping_states = ta.get_self_looping_states()
    for edge in iterate_output_edges(ta):
        if edge.info.variable == "":
            edge.info.variable = f"{var_prefix}{max_var}"
        elif int(edge.info.variable[len(var_prefix) :]) != max_var:
            ValueError("fill_dont_care_boxes(): 'max_var' inconsistent with actual output edge variables")
    var_cache = ta.get_var_visibility_deterministic()

    for edge in iterate_edges(ta):
        if edge.info.box_array == []:
            edge.info.box_array = [None] * len(edge.children)
        if edge.is_self_loop() or edge.children == []:
            continue
        low_check = True if (len(edge.info.box_array) > 0 and edge.info.box_array[0] in [None, ""]) else False
        high_check = True if (len(edge.info.box_array) > 1 and edge.info.box_array[1] in [None, ""]) else False
        low_idx: int = 0
        high_idx: int = (
            1
            if (low_check or edge.info.box_array[0] in [None, ""])
            else box_catalogue[edge.info.box_array[0]].port_arity
        )

        for box_idx, (check, child_idx) in enumerate([(low_check, low_idx), (high_check, high_idx)]):
            child = edge.children[child_idx]
            src_var = var_cache[edge.src]
            child_var = var_cache[child]
            if check:
                if src_var < child_var and src_var != child_var - 1 and child not in selflooping_states:
                    edge.info.box_array[box_idx] = "X"
                elif src_var >= child_var:
                    ValueError(f"fill_dont_care_boxes(): variable is skipped on edge {edge}")
