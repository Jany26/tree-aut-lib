from typing import Optional

from tree_automata.automaton import TTreeAut
from helpers.utils import box_catalogue

from apply.abdd_node import ABDDNode
from tree_automata.transition import TEdge, TTransition

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# previous materialization attempt using intersectoid-like structures
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# similar to folding, we use product-like structure, or intersectoid to compute
# the intermediate structures spanning across the variable-levels of two ABDD edges,
# in order to synchronize these levels for further ABDD_Apply() calls

# to differentiate between folding intersectoids and apply intersectoids
# (which are used in different contexts and have differing semantics)
# herein we will refer to intersectoids used in Apply as a-intersectoids (or alpha)


# This is more of a structure instead of a class for a more explicit and clear manipulation
# during the a-intersectoid creation.
class AlphaIntersectoidStateInfo:
    def __init__(
        self,
        s1: Optional[str],
        s2: Optional[str],
        aut1: TTreeAut,
        aut2: TTreeAut,
        varmap1: dict[str, int],
        varmap2: dict[str, int],
    ):
        self.port_s1: Optional[str] = None
        for p, s in aut1.get_port_order():
            if s == s1:
                self.port_s1 = p
                break
        self.port_s2: Optional[str] = None
        for p, s in aut2.get_port_order():
            if s == s2:
                self.port_s2 = p
                break
        self.var_s1: Optional[int] = None if s1 not in varmap1 else varmap1[s1]
        self.var_s2: Optional[int] = None if s2 not in varmap2 else varmap2[s2]
        self.loopable_s1: bool = True if s1 is None else s1 in aut1.get_self_looping_states()
        self.loopable_s2: bool = True if s2 is None else s2 in aut2.get_self_looping_states()

    def __repr__(self):
        return "%-*s %-*s %-*s %-*s %-*s %-*s" % (
            8,
            self.port_s1.lstrip("Port_") if self.port_s1 is not None else "-",
            8,
            self.port_s2.lstrip("Port_") if self.port_s2 is not None else "-",
            8,
            self.var_s1 if self.var_s1 is not None else "-",
            8,
            self.var_s2 if self.var_s2 is not None else "-",
            8,
            "loop" if self.loopable_s1 else "-",
            8,
            "loop" if self.loopable_s2 else "-",
        )


def create_alpha_intersectoid(node_src_1: ABDDNode, node_src_2: ABDDNode, direction: bool):  # False='low', True='high'
    node_tgt_1: list[ABDDNode] = node_src_1.high if direction else node_src_1.low
    node_tgt_2: list[ABDDNode] = node_src_2.high if direction else node_src_2.low
    box_1: Optional[str] = node_src_1.high_box if direction else node_src_1.low_box
    box_2: Optional[str] = node_src_2.high_box if direction else node_src_2.low_box
    if box_1 is None or box_2 is None:
        return
    aut_1: TTreeAut = box_catalogue[box_1]
    aut_2: TTreeAut = box_catalogue[box_2]

    var_map_1: dict[str, int] = {s: n.var for (_, s), n in zip(aut_1.get_port_order(), node_tgt_1)}
    var_map_2: dict[str, int] = {s: n.var for (_, s), n in zip(aut_2.get_port_order(), node_tgt_2)}

    # lookup in the form of (s1, s2) -> Info, where s1/s2 can be None
    # (in case the run 'dies' in one of the automata due to exhausting variables)
    state_info_map: dict[tuple[Optional[str], Optional[str]], AlphaIntersectoidStateInfo] = {
        (s1, s2): AlphaIntersectoidStateInfo(s1, s2, aut_1, aut_2, var_map_1, var_map_2)
        for s1 in aut_1.get_states() + [None]
        for s2 in aut_2.get_states() + [None]
    }
    var_map_1.update({root: node_src_1.var for root in aut_1.roots})
    var_map_2.update({root: node_src_2.var for root in aut_2.roots})

    counter = 0

    tr_dict: dict[str, dict[str, TTransition]] = {}
    worklist = [(r1, r2) for r1 in aut_1.roots for r2 in aut_2.roots]
    for s1, s2 in worklist:
        sname = str((s1, s2))
        reachable_transitions = [
            (t1, t2) for t1 in aut_1.transitions[s1].values() for t2 in aut_2.transitions[s2].values()
        ]
        if sname not in tr_dict:
            tr_dict[sname] = {}
        for t1, t2 in reachable_transitions:
            tr_dict[sname][f"k{counter}"] = TTransition(f"{sname}", TEdge("LH"))
        counter += 1
    pass
