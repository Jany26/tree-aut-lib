import unittest
from tree_automata import TTreeAut
from tree_automata.functions import tree_aut_complement, match_tree_bottom_up
import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn


class TestTreeAutomatonComplement(unittest.TestCase):
    def test_complement_x(self):
        complement_x: TTreeAut = tree_aut_complement(ta.box_x, ta.full_alphabet)

        self.assertFalse(match_tree_bottom_up(complement_x, tn.x_test_tree_1))
        self.assertFalse(match_tree_bottom_up(complement_x, tn.x_test_tree_2))
        self.assertFalse(match_tree_bottom_up(complement_x, tn.x_test_tree_3))

        self.assertTrue(match_tree_bottom_up(complement_x, tn.l0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_x, tn.l1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.l1_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_x, tn.h0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_x, tn.h1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_x, tn.h1_test_tree_4))

    def test_complement_l0(self):
        complement_l0: TTreeAut = tree_aut_complement(ta.box_l0, ta.full_alphabet)

        self.assertTrue(match_tree_bottom_up(complement_l0, tn.x_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.x_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.x_test_tree_3))

        self.assertFalse(match_tree_bottom_up(complement_l0, tn.l0_test_tree_1))
        self.assertFalse(match_tree_bottom_up(complement_l0, tn.l0_test_tree_2))
        self.assertFalse(match_tree_bottom_up(complement_l0, tn.l0_test_tree_3))
        self.assertFalse(match_tree_bottom_up(complement_l0, tn.l0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_l0, tn.l1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.l1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.l1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.l1_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l0, tn.h1_test_tree_4))

    def test_complement_l1(self):
        complement_l1: TTreeAut = tree_aut_complement(ta.box_l1, ta.full_alphabet)

        self.assertTrue(match_tree_bottom_up(complement_l1, tn.x_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.x_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.x_test_tree_3))

        self.assertTrue(match_tree_bottom_up(complement_l1, tn.l0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.l0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.l0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.l0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(complement_l1, tn.l1_test_tree_1))
        self.assertFalse(match_tree_bottom_up(complement_l1, tn.l1_test_tree_2))
        self.assertFalse(match_tree_bottom_up(complement_l1, tn.l1_test_tree_3))
        self.assertFalse(match_tree_bottom_up(complement_l1, tn.l1_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_l1, tn.h1_test_tree_4))

    def test_complement_h0(self):
        complement_h0: TTreeAut = tree_aut_complement(ta.box_h0, ta.full_alphabet)

        self.assertTrue(match_tree_bottom_up(complement_h0, tn.x_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.x_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.x_test_tree_3))

        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.l1_test_tree_4))

        self.assertFalse(match_tree_bottom_up(complement_h0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_bottom_up(complement_h0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_bottom_up(complement_h0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_bottom_up(complement_h0, tn.h0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_h0, tn.h1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.h1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.h1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h0, tn.h1_test_tree_4))

    def test_complement_h1(self):
        complement_h1: TTreeAut = tree_aut_complement(ta.box_h1, ta.full_alphabet)

        self.assertTrue(match_tree_bottom_up(complement_h1, tn.x_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.x_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.x_test_tree_3))

        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l0_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.l1_test_tree_4))

        self.assertTrue(match_tree_bottom_up(complement_h1, tn.h0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.h0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.h0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(complement_h1, tn.h0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(complement_h1, tn.h1_test_tree_1))
        self.assertFalse(match_tree_bottom_up(complement_h1, tn.h1_test_tree_2))
        self.assertFalse(match_tree_bottom_up(complement_h1, tn.h1_test_tree_3))
        self.assertFalse(match_tree_bottom_up(complement_h1, tn.h1_test_tree_4))
