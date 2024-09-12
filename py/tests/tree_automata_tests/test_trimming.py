import unittest

from formats.format_vtf import import_treeaut_from_vtf
import tests.tree_automata_examples as ta
from tree_automata.automaton import TTreeAut
from tree_automata.functions.trimming import remove_useless_states


class TestTreeAutomatonTrimming(unittest.TestCase):
    def test_trimming_unreachable_states(self):
        tree_aut_1: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf")
        tree_aut_2: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf")
        tree_aut_3: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf")

        tree_aut_1_trimmed: TTreeAut = remove_useless_states(tree_aut_1)
        tree_aut_2_trimmed: TTreeAut = remove_useless_states(tree_aut_2)
        tree_aut_3_trimmed: TTreeAut = remove_useless_states(tree_aut_3)

        self.assertSetEqual(set(tree_aut_1_trimmed.get_states()), set())
        self.assertSetEqual(set(tree_aut_2_trimmed.get_states()), set(["q0", "q1", "q2", "q3"]))
        self.assertSetEqual(set(tree_aut_3_trimmed.get_states()), set(["q0", "q1", "q2", "q3"]))

    def test_trimming_boxes(self):
        box_x_trimmed: TTreeAut = remove_useless_states(ta.box_x)
        box_l0_trimmed: TTreeAut = remove_useless_states(ta.box_l0)
        box_l1_trimmed: TTreeAut = remove_useless_states(ta.box_l1)
        box_lport_trimmed: TTreeAut = remove_useless_states(ta.box_lport)
        box_h0_trimmed: TTreeAut = remove_useless_states(ta.box_h0)
        box_h1_trimmed: TTreeAut = remove_useless_states(ta.box_h1)
        box_hport_trimmed: TTreeAut = remove_useless_states(ta.box_hport)

        self.assertSetEqual(set(ta.box_x.get_states()), set(box_x_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_l0.get_states()), set(box_l0_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_l1.get_states()), set(box_l1_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_lport.get_states()), set(box_lport_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_h0.get_states()), set(box_h0_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_h1.get_states()), set(box_h1_trimmed.get_states()))
        self.assertSetEqual(set(ta.box_hport.get_states()), set(box_hport_trimmed.get_states()))
