"""
[file] box_materialization.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Algorithms that are used for creating a materialized box.
"""

from typing import Optional

from tree_automata.automaton import TTreeAut
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# current materialization attempt directly with given variable
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"""
Herein, we try to 'materialize' boxes on a given level using information about
possible visible variable ranges for each state -> minimum and maximum
Materializing box B at variable level i will work in the following fashion:
  - procedure will compute variable ranges for each state of B
  - if level i belongs to a variable range for some state s of box B, then
      a copy s' of state s will be created, such that variable range <j,k> of s
      will be split: <j,i-1> for s, <i,k> for s'
  - all loopable transitions of state s will be copied to s' with s->s' substitution
  - a copy of loopable transitions of s will be created, labeled with variable i
      such that children states have s->s' substitution
  - terminable transitions of s will be moved to s'

Boxes like L0, L1, H0, H1 have a state that inherently represents a terminal node.
Those states will have a range with infinite upper bound represented by varmax.
"""

ARBITRARY_PORT_SYMBOL: str = "Port_arb"


def compute_variable_ranges(
    aut: TTreeAut, invar: int, outvars: dict[str, int], leaf_level: int
) -> dict[str, tuple[int, int]]:
    """
    For a tree automaton 'aut', given the initial variable 'invar' with which the automaton's run is entered,
    and 'info_map', which has information about which variables should automaton's run be exited,
    return a dictionary of state to int-int tuple representing intervals of possible variables, that can be seen
    from within that state.

    Fix-point algorithm combining top-down and bottom-up exploration of the automaton, while checking certain
    conditions to ensure that variables are propagated properly.
    """
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
        print(f"compute_variable_ranges() warning: some variable range for box {aut.name} was not determined")

    # we could need to change the ranges during some manipulation, so instead of using immutable tuples,
    # we store the ranges in the two-element list
    result = {i: (mins[i], maxs[i]) for i in states}
    return result


def create_materialized_box(
    aut: TTreeAut, invar: int, materialization_var: int, outvars: list[int], leaf_level: int, show_transitions=False
) -> TTreeAut:
    print(f"materializing {aut.name}: in={invar}, mat={materialization_var}, out={outvars}, leaf={leaf_level}")
    """
    Create a materialized box (with regards to input and output/leaf variables).
    The box has the same semantics as the original box, except the materialized variable
    is explicitly present in the transition relation of the box
    (plus some additional arbitrary ports are added for later steps).

    Imagine breaking some for-loop into two for-loops with one specific iteration
    explicitly performed in between the loops.

    The specific transitions and the motivation behind why they are present in the materialized box
    is then given below, when relevant to the source code.
    """
    outvar_map = {s: outvars[i] for i, (p, s) in enumerate(aut.get_port_order())}
    ranges = compute_variable_ranges(aut, invar, outvar_map, leaf_level)
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
        else:  # mat < minv or maxv <= mat
            orig_state_ranges[s] = (minv, maxv)
    mat_target_state_ranges = {
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
            newtr = TTransition(
                f"{s}<{minv},{maxv}>",
                TEdge(selfloop.info.label, [], selfloop.info.variable),
                [f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>" for i in selfloop.children],
            )
            transitions.add(newtr)
            if show_transitions:
                print(f"1 {newtr}")

        if s not in mat_target_state_ranges and s in term_tr:
            has_port = False
            for t in term_tr[s]:
                if t.info.label.startswith("Port"):
                    has_port = True
                children = []
                for i in t.children:
                    if (
                        i in mat_target_state_ranges
                        and mat_target_state_ranges[i][0] <= maxv + 1
                        and maxv + 1 <= mat_target_state_ranges[i][1]
                    ):
                        children.append(f"{i}<{mat_target_state_ranges[i][0]},{mat_target_state_ranges[i][1]}>")
                    else:
                        children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
                # 2 add a terminating transition, but make sure that the following variable of the terminating
                # transition (i.e. mat + 1) is in the range of the target states
                creating_tr = TTransition(
                    f"{s}<{minv},{maxv}>",
                    # TEdge(t.info.label, [], t.info.variable)
                    TEdge(t.info.label, [], f"{maxv}"),
                    children,
                )
                if show_transitions:
                    print(f"2 {creating_tr}")
                transitions.add(creating_tr)
            # X in case the port state transition would be used before the materialization variable level is reached,
            # we add an arbitrary port here as well (so that the first phase of pattern finding includes this state)
            if has_port and materialization_var >= maxv:
                newtr = TTransition(
                    f"{s}<{minv},{maxv}>", TEdge(ARBITRARY_PORT_SYMBOL, [], f"{materialization_var}"), []
                )
                transitions.add(newtr)
                if show_transitions:
                    print(f"X {newtr}")

        # 3 add a copy of looping transition to original/split states, such that
        # only the states that contain the FOLLOWING variable in their ranges are used (looping becomes terminating)
        if s in mat_target_state_ranges:

            # we have a state that is both in original and mat_targets...
            # and we are trying to create a copy of this selfloop, but such that it becomes the terminating transition
            # leading to the mat_targets
            selfloop = loop_tr[s]
            children = []
            # "maxv" in this context is "matvar", since we work with the orig states
            # that have a copy in targets, i.e. have been split.

            # if the child is a target of matvar and the follow-up variable after matvar
            # is in its var range, then we use that state.
            for i in selfloop.children:
                if i in mat_target_state_ranges:
                    children.append(f"{i}<{mat_target_state_ranges[i][0]},{mat_target_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            creating_tr = TTransition(f"{s}<{minv},{maxv}>", TEdge(selfloop.info.label, [], f"{maxv}"), children)
            if show_transitions:
                print(f"3 {creating_tr}")
            transitions.add(creating_tr)

        # 4 add an output transition if the non-mat target state has matvar in its range
        if materialization_var >= minv and materialization_var <= maxv:
            outedges = aut.get_output_edges(inverse=True)

            # if the original state has an 0/1 output transition, keep it
            # - this is an optimization, since normally we could place an arbitrary port here as well,
            # which would usually find some Lport or Hport box,
            # but the subpattern rooted in this state would just contain -X->0 or -X->1 edges,
            # so it is more efficient to perform a preemptive short-circuiting by utilizing the terminal output symbol
            if s in outedges and any([i in outedges[s] for i in ["0", "1"]]):
                newtr = TTransition(f"{s}<{minv},{maxv}>", TEdge(outedges[s][0], [], f"{maxv}"), [])
                transitions.add(newtr)
                if show_transitions:
                    print(f"4 {newtr}")
            # if it has a port, replace it with an arbitrary port
            else:
                newtr = TTransition(f"{s}<{minv},{maxv}>", TEdge(ARBITRARY_PORT_SYMBOL, [], f"{maxv}"), [])
                transitions.add(newtr)
                if show_transitions:
                    print(f"4 {newtr}")

    for s, (minv, maxv) in mat_target_state_ranges.items():

        # 5 add a self-loop if minv < maxv
        if minv != maxv and s in loop_tr:
            selfloop = loop_tr[s]
            children = []
            for i in selfloop.children:
                if i in mat_target_state_ranges:
                    children.append(f"{i}<{mat_target_state_ranges[i][0]},{mat_target_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            newtr = TTransition(f"{s}<{minv},{maxv}>", TEdge(selfloop.info.label, [], selfloop.info.variable), children)
            transitions.add(newtr)
            if show_transitions:
                print(f"5 {newtr}")

        # 6 add a terminating transition with substituted names (such that they contain the follow-up variable in their ranges)
        for t in term_tr[s]:
            children = []
            for i in t.children:
                # watch out here for the split state terminating conditions that choose which states are children
                if i in mat_target_state_ranges and mat_target_state_ranges[i][1] > maxv:
                    children.append(f"{i}<{mat_target_state_ranges[i][0]},{mat_target_state_ranges[i][1]}>")
                else:
                    children.append(f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>")
            newtr = TTransition(f"{s}<{minv},{maxv}>", TEdge(t.info.label, [], f"{maxv}"), children)
            transitions.add(newtr)
            if show_transitions:
                print(f"6 {newtr}")

    transition_dict = {}
    for i, t in enumerate(transitions):
        if t.src not in transition_dict:
            transition_dict[t.src] = {}
        transition_dict[t.src][f"k{i}"] = t

    root_list = [f"{i}<{orig_state_ranges[i][0]},{orig_state_ranges[i][1]}>" for i in aut.roots]
    name = f"materialized({aut.name}, in:{invar}, at:{materialization_var}, out:{outvars}, leaf:{leaf_level})"
    result = TTreeAut(root_list, transition_dict, name, aut.port_arity)
    return result


def create_materialized_box_wrapper(
    node_src: ABDDNode,  # from here we find out the box, the target nodes and the variable levels needed
    direction: bool,  # False=low, True=high
    materialization_var: int,  # for now we will only materialize one level at a time
    leaf_level: int,  # needed in case we work with boxes that contain inherent "leaf" transitions and
    # we need to compare variable ranges somehow
):
    """
    Wrapper function for materialized box creation, which just extracts variables etc.
    Used for testing and debugging.
    """
    node_tgt: list[ABDDNode] = node_src.high if direction else node_src.low
    box: Optional[str] = node_src.high_box if direction else node_src.low_box
    if box is None:
        pass
    aut: TTreeAut = box_catalogue[box]
    outvars = [n.var for n in node_tgt]
    invar = node_src.var
    if not (materialization_var > invar and any([materialization_var < var for var in outvars])):
        return aut
    return create_materialized_box(aut, invar, materialization_var, outvars, leaf_level)


# End of file box_materialization.py
