import unittest

from tree_automata.automaton import TTreeAut
from tree_automata.functions.determinization import tree_aut_determinization
from tree_automata.functions.match_tree import match_tree_top_down
import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn


class TestTreeAutomatonDeterminization(unittest.TestCase):
    def test_determinization_x(self):
        det_x: TTreeAut = tree_aut_determinization(ta.box_x, ta.full_alphabet)
        self.assertTrue(match_tree_top_down(det_x, tn.x_test_tree_1))
        self.assertTrue(match_tree_top_down(det_x, tn.x_test_tree_2))
        self.assertTrue(match_tree_top_down(det_x, tn.x_test_tree_3))

    def test_determinization_l0(self):
        det_l0: TTreeAut = tree_aut_determinization(ta.box_l0, ta.full_alphabet)
        self.assertTrue(match_tree_top_down(det_l0, tn.l0_test_tree_1))
        self.assertTrue(match_tree_top_down(det_l0, tn.l0_test_tree_2))
        self.assertTrue(match_tree_top_down(det_l0, tn.l0_test_tree_3))
        self.assertTrue(match_tree_top_down(det_l0, tn.l0_test_tree_4))

        self.assertFalse(match_tree_top_down(det_l0, tn.x_test_tree_1))
        self.assertFalse(match_tree_top_down(det_l0, tn.x_test_tree_2))
        self.assertFalse(match_tree_top_down(det_l0, tn.x_test_tree_3))

        self.assertFalse(match_tree_top_down(det_l0, tn.l1_test_tree_1))
        self.assertFalse(match_tree_top_down(det_l0, tn.l1_test_tree_2))
        self.assertFalse(match_tree_top_down(det_l0, tn.l1_test_tree_3))
        self.assertFalse(match_tree_top_down(det_l0, tn.l1_test_tree_4))

        self.assertFalse(match_tree_top_down(det_l0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_top_down(det_l0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_top_down(det_l0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_top_down(det_l0, tn.h0_test_tree_4))

        self.assertFalse(match_tree_top_down(det_l0, tn.h1_test_tree_1))
        self.assertFalse(match_tree_top_down(det_l0, tn.h1_test_tree_2))
        self.assertFalse(match_tree_top_down(det_l0, tn.h1_test_tree_3))
        self.assertFalse(match_tree_top_down(det_l0, tn.h1_test_tree_4))

    def test_determinization_l1(self):
        det_l1: TTreeAut = tree_aut_determinization(ta.box_l1, ta.full_alphabet)
        self.assertTrue(match_tree_top_down(det_l1, tn.l1_test_tree_1))
        self.assertTrue(match_tree_top_down(det_l1, tn.l1_test_tree_2))
        self.assertTrue(match_tree_top_down(det_l1, tn.l1_test_tree_3))
        self.assertTrue(match_tree_top_down(det_l1, tn.l1_test_tree_4))

    def test_determinization_h0(self):
        det_h0: TTreeAut = tree_aut_determinization(ta.box_h0, ta.full_alphabet)
        self.assertTrue(match_tree_top_down(det_h0, tn.h0_test_tree_1))
        self.assertTrue(match_tree_top_down(det_h0, tn.h0_test_tree_2))
        self.assertTrue(match_tree_top_down(det_h0, tn.h0_test_tree_3))
        self.assertTrue(match_tree_top_down(det_h0, tn.h0_test_tree_4))

    def test_determinization_h1(self):
        det_h1: TTreeAut = tree_aut_determinization(ta.box_h1, ta.full_alphabet)
        self.assertTrue(match_tree_top_down(det_h1, tn.h1_test_tree_1))
        self.assertTrue(match_tree_top_down(det_h1, tn.h1_test_tree_2))
        self.assertTrue(match_tree_top_down(det_h1, tn.h1_test_tree_3))
        self.assertTrue(match_tree_top_down(det_h1, tn.h1_test_tree_4))
