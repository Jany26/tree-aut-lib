import copy
from typing import Optional

from tree_automata.automaton import TTreeAut, iterate_edges, iterate_key_edge_tuples
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

    # we could need to change the ranges during some manipulation, so instead of using immutable tuples,
    # we store the ranges in the two-element list
    result = {i: (mins[i], maxs[i]) for i in states}
    return result


def create_split_states(ranges: dict[str, list[int]], split_var: int) -> dict[str, tuple[int, int]]:
    result = {}
    for state, (minvar, maxvar) in ranges.items():
        if minvar <= split_var and split_var < maxvar:
            result[state] = [minvar, split_var]
            result[f"{state}_"] = (split_var, maxvar)
        else:
            result[state] = (minvar, maxvar)
    return result


def create_materialized_box(
    node_src: ABDDNode,  # from here we find out the box, the target nodes and the variable levels needed
    direction: bool,  # False=low, True=high
    materialization_var: int,  # for now we will only materialize one level at a time
    leaf_level: int,  # needed in case we work with boxes that contain inherent "leaf" transitions and
    # we need to compare variable ranges somehow
):
    """
    Description TODO ...
    """
    node_tgt: list[ABDDNode] = node_src.high if direction else node_src.low
    box: Optional[str] = node_src.high_box if direction else node_src.low_box
    if box is None:
        pass
    aut: TTreeAut = box_catalogue[box]
    info_map: dict[tuple[str, str], tuple[int, int]] = {
        (port, state): (n.var, n.node) for (port, state), n in zip(aut.get_port_order(), node_tgt)
    }
    outvars = {s: v for (p, s), (v, i) in info_map.items()}
    invar = node_src.var
    if not (materialization_var > invar and any([materialization_var < var for var in outvars.values()])):
        return aut
    ranges = compute_variable_ranges(aut, invar, info_map, leaf_level)
    loop_tr: dict[str, TTransition] = {i.src: i for i in aut.get_loopable_transitions()}
    term_tr: dict[str, set[TTransition]] = {
        s: set([t for t in aut.transitions[s].values() if t in aut.get_terminating_transitions()])
        for s in aut.get_states()
    }
    transitions: set[TTransition] = set()

    orig_state_ranges = {}
    for s, (minv, maxv) in ranges.items():
        if materialization_var >= minv and materialization_var < maxv:
            orig_state_ranges[s] = (minv, materialization_var)
        else:
            orig_state_ranges[s] = (minv, maxv)
    split_state_ranges = {
        s: (materialization_var + 1, maxv)
        for s, (minv, maxv) in ranges.items()
        if materialization_var >= minv and materialization_var < maxv
    }

    # now enhance the range lookup based on which states get split
    # state copies are labeled with an underscore at the end
    for s, (minv, maxv) in orig_state_ranges.items():
        # 1 add a self-loop if minv < maxv
        if minv != maxv and s in loop_tr:
            selfloop = loop_tr[s]
            transitions.add(
                TTransition(
                    f"{s}<{minv},{maxv}>",
                    TEdge(selfloop.info.label, [], selfloop.info.variable),
                    [f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>" for i in selfloop.children],
                )
            )

        # 2 if there is not a copy in the split_ranges(), keep the terminating transition, BUT
        # check if either the original state or a split state is added to the
        if s not in split_state_ranges and s in term_tr:
            for t in term_tr[s]:
                children = []
                for i in t.children:
                    if i in split_state_ranges:
                        children.append(f"{i}<{split_state_ranges[i][0]},{split_state_ranges[i][1]}>")
                    else:
                        children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
                creating_tr = TTransition(
                    f"{s}<{minv},{maxv}>",
                    # TEdge(t.info.label, [], t.info.variable)
                    TEdge(t.info.label, [], f"{maxv}"),
                    children,
                )
                transitions.add(creating_tr)

        # 3 add a copy of looping transition to original/split states, such that
        # only the states that contain the FOLLOWING variable in their ranges are used (looping becomes terminating)
        if s in split_state_ranges:
            selfloop = loop_tr[s]
            children = []
            for i in selfloop.children:
                if i in split_state_ranges:
                    children.append(f"{i}<{split_state_ranges[i][0]},{split_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            creating_tr = TTransition(f"{s}<{minv},{maxv}>", TEdge(selfloop.info.label, [], f"{maxv}"), children)
            # print(f'creating terminating transition {creating_tr}')
            transitions.add(creating_tr)

        # 4 add an arbitrary port transition if a copy is in the split_ranges()
        if s in split_state_ranges and materialization_var >= minv and materialization_var <= maxv:
            transitions.add(TTransition(f"{s}<{minv},{maxv}>", TEdge("Port_arbitrary", [], f"{maxv}"), []))

    for s, (minv, maxv) in split_state_ranges.items():
        # 1 add a self-loop if minv < maxv
        if minv != maxv and s in loop_tr:
            selfloop = loop_tr[s]
            children = []
            for i in selfloop.children:
                if i in split_state_ranges:
                    children.append(f"{i}<{split_state_ranges[i][0]},{split_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            transitions.add(
                TTransition(f"{s}<{minv},{maxv}>", TEdge(selfloop.info.label, [], selfloop.info.variable), children)
            )

        # 2 add a terminating transition with substituted names (such that they contain the follow-up variable in their ranges)
        for t in term_tr[s]:
            children = []
            for i in t.children:
                # watch out here for the split state terminating conditions that choose which states are children
                if i in split_state_ranges and split_state_ranges[i][1] > maxv:
                    children.append(f"{i}<{split_state_ranges[i][0]},{split_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            transitions.add(TTransition(f"{s}<{minv},{maxv}>", TEdge(t.info.label, [], f"{maxv}"), children))

    transition_dict = {}
    for i, t in enumerate(transitions):
        if t.src not in transition_dict:
            transition_dict[t.src] = {}
        transition_dict[t.src][f"k{i}"] = t

    root_list = [f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>" for i in aut.roots]
    name = f"materialized({aut.name}, in:{invar}, at:{materialization_var}, out:{[n.var for n in node_tgt]})"
    result = TTreeAut(root_list, transition_dict, name, aut.port_arity)
    return result
