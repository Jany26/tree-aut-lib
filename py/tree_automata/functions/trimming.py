import copy

from tree_automata import TTreeAut
from tree_automata.functions.reachability import reachable_bottom_up, reachable_top_down


# Searches the tree from bottom-up and from top-down,
#  removing unreachable states
def remove_useless_states(ta: TTreeAut) -> TTreeAut:
    work_ta = copy.deepcopy(ta)
    bottom_up_reachable_states = reachable_bottom_up(work_ta)
    work_ta.shrink_tree_aut(bottom_up_reachable_states)
    top_down_reachable_states = reachable_top_down(work_ta)
    work_ta.shrink_tree_aut(top_down_reachable_states)
    return work_ta


def shrink_to_top_down_reachable(ta: TTreeAut) -> TTreeAut:
    work_ta = copy.deepcopy(ta)
    top_down_reachable_states = set(reachable_top_down(work_ta))
    unreachable_states = set(i for i in work_ta.get_states() if i not in top_down_reachable_states)
    for i in unreachable_states:
        work_ta.transitions.pop(i)
    return work_ta


def shrink_to_top_down_reachable_2(ta: TTreeAut) -> TTreeAut:
    work_treeaut = copy.deepcopy(ta)
    # reachable_states_bottomup = reachable_states_bottomup(work_treeaut)
    # work_treeaut.shrink_tree_aut(reachable_states_bottomup)
    reachable_states_top_down = reachable_top_down(work_treeaut)
    work_treeaut.shrink_tree_aut(reachable_states_top_down)
    return work_treeaut


def trim(ta: TTreeAut) -> TTreeAut:
    work_treeaut = shrink_to_top_down_reachable_2(ta)
    return remove_useless_states(work_treeaut)

    # remove transitions over  variables which are clearly unnecessary
    # TODO: define/explain ^^
    # get all paths from roots to leaves ---> make a function

    return work_treeaut
