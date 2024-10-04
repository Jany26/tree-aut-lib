import copy
from typing import Dict, List, Optional, Set, Tuple

from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges
from bdd.bdd_class import BDD


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
    var_visibility: Dict[str, int] = {i: int(list(j)[0]) for i, j in ta.get_var_visibility().items()}
    leaves: Set[str] = set(ta.get_output_states())
    counter: int = 0
    skipped_var_edges: List[Tuple[str, str, TTransition]] = []
    var_prefix: str = ta.get_var_prefix()
    for edge in iterate_edges(result):
        if edge.is_self_loop():
            continue
        for idx, child in enumerate(edge.children):
            if (
                child in leaves
                and var_visibility[edge.src] != vars
                or child not in leaves
                and var_visibility[child] - var_visibility[edge.src] >= 2
            ):
                if len(edge.info.box_array) < idx + 1:
                    edge.info.box_array = [None] * len(edge.children)
                edge.info.box_array[idx] = "X"
    for new_state, new_key, new_edge in skipped_var_edges:
        if new_state not in result.transitions:
            result.transitions[new_state] = {}
        if new_key not in result.transitions[new_state]:
            result.transitions[new_state][new_key] = new_edge

    return result
