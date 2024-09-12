from tree_automata.transition import TTransition, TEdge
from tree_automata.automaton import (
    TTreeAut,
    iterate_edges,
    iterate_edges_from_state,
    iterate_key_edge_tuples,
    iterate_keys,
    iterate_states_bfs,
    iterate_states_dfs,
)
from tree_automata.tree_node import TTreeNode

from tree_automata.functions.complement import tree_aut_complement
from tree_automata.functions.determinization import tree_aut_determinization
from tree_automata.functions.emptiness import non_empty_bottom_up, non_empty_top_down
from tree_automata.functions.intersection import tree_aut_intersection
from tree_automata.functions.isomorphism import tree_aut_isomorphic
from tree_automata.functions.union import tree_aut_union
from tree_automata.functions.match_tree import match_tree_bottom_up, match_tree_top_down
from tree_automata.functions.reachability import reachable_bottom_up, reachable_top_down
from tree_automata.functions.trimming import remove_useless_states, shrink_to_top_down_reachable
from tree_automata.functions.witness import generate_witness_tree, generate_witness_string
from tree_automata.functions.well_defined import is_well_defined
