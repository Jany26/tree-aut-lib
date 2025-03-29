from typing import Optional
from tree_automata.automaton import TTreeAut
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition

# During apply's recursive descent, what can happen, is that given two low-low
# or high-high edge part pairs with boxes B1, B2, the variable levels
# of target nodes of these boxes may have incompatible variables.
# Example: B1=LPort leading to nodes with variables 7, 4 and B2=HPort leading to nodes with variables 10, 13
# in order for apply to correctly work recurse, these variable levels have to be somehow synchronized
# this synchronization happens through creating intermediate nodes = node 'materialization'


# In this module is one attempt to materialize such nodes, which uses explicit box loop unfolding.
# Given the box which should have some intermediate states (differentiated with variable values) materialized,
# and given the variables on which the structure is unfolded,
# create the unfolded automaton's structure, which after folding will provide the 'materialized' structure with
# all needed intermediate box reductions and inner nodes specified.
def create_alpha_intersectoid_unfolded(
    node_src: ABDDNode,  # from here we find out the box, the target nodes and the variable levels needed
    direction: bool,  # False=low, True=high
    synchronization_vars: list[int],  # these variable levels are given by the 'other' ABDDnode and box
) -> tuple[ABDDNode, ABDDNode]:
    node_tgt: list[ABDDNode] = node_src.high if direction else node_src.low
    box: Optional[str] = node_src.high_box if direction else node_src.low_box
    if box is None:
        pass

    aut: TTreeAut = box_catalogue[box]

    info_map: dict[tuple[str, str], tuple[str, str]] = {
        (port, state): (n.var, n.node) for (port, state), n in zip(aut.get_port_order(), node_tgt)
    }

    target_vars = [i.var for i in node_tgt if i.var != 0]
    # NOTE: if there is >1 looping transition or >1 terminating transition for some state,
    # then we have a non-deterministic box, and we cannot work with those
    # the only "nondeterminism" allowed is choosing between 1 looping and 1 terminating transition
    # and the choice is clear when we add variable context
    terminating_tr: dict[str, TTransition] = {i.src: i for i in aut.get_terminable_transitions()}
    looping_tr: dict[str, TTransition] = {i.src: i for i in aut.get_loopable_transitions()}

    # port conditions = (state, var) tuples which have to have initial ports installed
    port_conditions: set[tuple[str, int]] = set([(state, var) for (_, state), (var, _) in info_map.items()])

    # sync conditions = (state, var) tuples which have to have arbitrary ports installed
    # (for finding intermediate boxes etc.)
    sync_conditions: set[tuple[str, int]] = set(
        (s, v) for s in aut.get_states() for v in synchronization_vars + target_vars
    )

    # term condition = (state, var) tuples in which terminating transition is chosen instead of a looping one
    term_conditions: set[tuple[str, int]] = set()

    for src, tr in terminating_tr.items():
        for child, var in port_conditions:
            if child in tr.children:
                # NOTE: this will not work properly in case of more complicated boxes,
                # where multiple var layers are visited before termination,
                # i.e. max root distance for some state is > 1
                term_conditions.add((src, var - 1))

    worklist: list[tuple[str, int]] = []
    for i in aut.roots:
        worklist.append((i, node_src.var))
    roots = [str(i) for i in worklist]
    counter = 0
    # src node -> (box root state, box root state)
    transitions: dict[str, dict[str, TTransition]] = {}
    for st, var in worklist:
        sname = str((st, var))
        term_tr = TTransition(sname, TEdge("LH", [], var), [str((st, var + 1)), str((st, var + 1))])
        if sname not in transitions:
            transitions[sname] = {}
        transitions[sname][f"k{counter}"] = term_tr
        counter += 1

    # alpha-intersectoid states are (state, variable) tuples - states from initial box, variables from ABDD
    while worklist != []:
        s, v = worklist.pop(0)
        sname = str((s, v))

        # transition before accessing states which will have final terminating ports
        if (s, v) in term_conditions:
            children = [(c, v + 1) for c in terminating_tr[s].children]
            term_tr = TTransition(sname, TEdge("LH", [], v), [str(c) for c in children])
            if sname not in transitions:
                transitions[sname] = {}
            transitions[sname][f"k{counter}"] = term_tr
            counter += 1
            for i in children:
                if i not in worklist:
                    worklist.append(i)
            continue

        # final terminating ports (present in the initial box)
        if (s, v) in port_conditions:
            port = ""
            for (p, state), (var, node) in info_map.items():
                if s == state and v == var:
                    port = p
            if port == "":
                ValueError("Inconsistent port condition with box automaton.")
            port_tr = TTransition(sname, TEdge(port, [], ""), [])
            if sname not in transitions:
                transitions[sname] = {}
            transitions[sname][f"k{counter}"] = port_tr
            counter += 1
            continue

        children = [(c, v + 1) for c in looping_tr[s].children]
        loop_tr = TTransition(sname, TEdge("LH", [], v), [str(c) for c in children])
        if sname not in transitions:
            transitions[sname] = {}
        transitions[sname][f"k{counter}"] = loop_tr
        counter += 1
        for i in children:
            if i not in worklist:
                worklist.append(i)

        # on top of normal looping transitions, if sync conditions are matched, arbitrary ports
        # for breaking "folding-like" process are added, so that materialized nodes are not "over-folded"
        if (s, v) in sync_conditions:
            sync_port_tr = TTransition(sname, TEdge("Port", [], ""), [])
            # print(f'adding syncing transition    : {sync_port_tr}')
            transitions[sname][f"k{counter}"] = sync_port_tr
            counter += 1

    return TTreeAut(roots, transitions, "", aut.port_arity)
