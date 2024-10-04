import copy

from tree_automata import TTreeAut
from tree_automata.functions.reachability import reachable_bottom_up, reachable_top_down


def remove_useless_states(ta: TTreeAut) -> TTreeAut:
    """
    Searches the tree from bottom-up and from top-down,
    removing unreachable states.
    """
    # TODO: Perhaps remove_useless_states could work as a fixpoint algorithm.
    # Since it is not clear, whether one bottom-up trim followed by one top-down
    # trim is enough.
    work_ta: TTreeAut = copy.deepcopy(ta)
    bottom_up_reachable_states: list[str] = reachable_bottom_up(work_ta)
    work_ta.shrink_tree_aut(bottom_up_reachable_states)
    top_down_reachable_states: list[str] = reachable_top_down(work_ta)
    work_ta.shrink_tree_aut(top_down_reachable_states)
    return work_ta


def shrink_to_top_down_reachable(ta: TTreeAut) -> TTreeAut:
    """
    Removes the states from the automaton that are top-down unreachable.
    """
    work_ta = copy.deepcopy(ta)
    top_down_reachable_states: set[str] = set(reachable_top_down(work_ta))
    unreachable_states = set(i for i in work_ta.get_states() if i not in top_down_reachable_states)
    for i in unreachable_states:
        work_ta.transitions.pop(i)
    return work_ta


def shrink_to_top_down_reachable_2(ta: TTreeAut) -> TTreeAut:
    """
    Probably more efficient version of shrink_to_top_down_reachable().
    """
    work_treeaut: TTreeAut = copy.deepcopy(ta)
    # reachable_states_bottomup = reachable_states_bottomup(work_treeaut)
    # work_treeaut.shrink_tree_aut(reachable_states_bottomup)
    reachable_states_top_down: list[str] = reachable_top_down(work_treeaut)
    work_treeaut.shrink_tree_aut(reachable_states_top_down)
    return work_treeaut


def trim(ta: TTreeAut) -> TTreeAut:
    """
    During folding, intersectoid trimming took too long,
    because the bottom-up reachability is more complicated,
    so this version is used there, which firstly removes top-down unreachable states,
    since created intersectoids contain many such states, increasing the complexity.
    """
    work_treeaut: TTreeAut = shrink_to_top_down_reachable_2(ta)
    return remove_useless_states(work_treeaut)

    # TODO: further definition/explanation needed possibly
    # remove transitions over variables which are clearly unnecessary

    # after normalization, there are clearly some transitions left over
    # that do not make any sense (either they provide a some loop through already used variables),
    # or they somehow break the "determinism wrt. variables"

    # solution is to:
    #   - either tweak the normalization algorithm (which could prove to be complicated)
    #   - or to remove the "bad" transitions after-the-fact
    #       - traversing every possible rootstate-leafstate path in the UBDA,
    #       while checking visited variables (in order), and flagging the transitions that break the order

    return work_treeaut
