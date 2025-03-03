from typing import Optional

from tree_automata.automaton import TTreeAut
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# current materialization attempt directly with given variable
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Herein, we try to 'materialize' boxes on a given level using information about
# possible visible variable ranges for each state -> minimum and maximum
# Materializing box B at variable level i will work in the following fashion:
#   - procedure will compute variable ranges for each state of B
#   - if level i belongs to a variable range for some state s of box B, then
#       a copy s' of state s will be created, such that variable range <j,k> of s
#       will be split: <j,i-1> for s, <i,k> for s'
#   - all loopable transitions of state s will be copied to s' with s->s' substitution
#   - a copy of loopable transitions of s will be created, labeled with variable i
#       such that children states have s->s' substitution
#   - terminable transitions of s will be moved to s'

# this process is similar to the explicit materialiation, except instead of explicit
# state copies for each variable level, loops and breakpoint transitions are utilized

# Boxes like L0, L1, H0, H1 have a state that inherently represents a terminal node.
# Those states will have a range with infinite upper bound represented by varmax.


def compute_variable_ranges(
    aut: TTreeAut, invar: int, info_map: dict[tuple[str, str], tuple[int, int]], leaf_level: int
) -> dict[str, tuple[int, int]]:
    """
    For a tree automaton 'aut', given the initial variable 'invar' with which the automaton's run is entered,
    and 'info_map', which has information about which variables should automaton's run be exited,
    return a dictionary of state to int-int tuple representing intervals of possible variables, that can be seen
    from within that state.
    """
    outvars = {s: v for (p, s), (v, i) in info_map.items()}
    states = aut.get_states()
    terminating_tr: dict[str, TTransition] = {i.src: i for i in aut.get_terminable_transitions()}
    looping_tr: dict[str, TTransition] = {i.src: i for i in aut.get_loopable_transitions()}

    mins: dict[str, Optional[int]] = {s: invar + 1 if s in aut.roots else None for s in states}
    maxs: dict[str, Optional[int]] = {s: outvars[s] if s in outvars else None for s in states}

    out_states = aut.get_output_edges()
    for sym, statelist in out_states.items():
        if sym in ["0", "1"]:
            for i in statelist:
                maxs[i] = leaf_level

    some_bound_is_unset = True
    change = True
    while change:
        change = False
        # unloopable termination state setting
        for i in states:
            if i not in looping_tr and maxs[i] is not None and mins[i] is None:
                mins[i] = maxs[i]
                change = True
            if i not in looping_tr and mins[i] is not None and maxs[i] is None:
                maxs[i] = mins[i]
                change = True
        # if a terminable transition of a 's' leads to a child with a minimum M (i.e. not None),
        # maximum of 's' will be set to M-1
        for state, transition in terminating_tr.items():
            for child in transition.children:
                # we also just make sure that 's' can actually loop
                if maxs[state] is None and mins[child] is not None and state in looping_tr:
                    maxs[state] = mins[child] - 1
                    change = True

        # children of looping transition of a state with a minimum M will have their minimum set to M+1
        for state, transition in looping_tr.items():
            if mins[state] is None:
                continue
            for child in transition.children:
                if child == state:
                    continue
                if mins[child] is None:
                    mins[child] = mins[state] + 1
                    change = True

        # if any interval bound is zero, keep iterating:
        some_bound_is_unset = False
        some_bound_is_unset = any([i is None for i in mins.values()]) or any([i is None for i in maxs.values()])
        if some_bound_is_unset:
            print(f"copmute_variable_ragnes() warning: some variable range for box {aut.name} was not determined")

    result = {i: (mins[i], maxs[i]) for i in states}
    return result


def create_materialized_box(
    node_src: ABDDNode,  # from here we find out the box, the target nodes and the variable levels needed
    direction: bool,  # False=low, True=high
    materialization_var: int,  # for now we will only materialize one level at a time
    leaf_level: int,
):
    node_tgt: list[ABDDNode] = node_src.high if direction else node_src.low
    box: Optional[str] = node_src.high_box if direction else node_src.low_box
    if box is None:
        pass
    aut: TTreeAut = box_catalogue[box]
    info_map: dict[tuple[str, str], tuple[int, int]] = {
        (port, state): (n.var, n.node) for (port, state), n in zip(aut.get_port_order(), node_tgt)
    }
    invar = node_src.var
    # outvars = [i.var for i in node_tgt]
    terminating_tr: dict[str, TTransition] = {i.src: i for i in aut.get_terminable_transitions()}
    looping_tr: dict[str, TTransition] = {i.src: i for i in aut.get_loopable_transitions()}

    compute_variable_ranges(aut, invar, info_map, leaf_level)
