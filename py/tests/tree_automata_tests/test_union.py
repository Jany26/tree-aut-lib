import unittest

import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn
from tree_automata.automaton import TTreeAut
from tree_automata.functions.match_tree import match_tree_top_down
from tree_automata.functions.union import tree_aut_union


class TestTreeAutomatonUnion(unittest.TestCase):
    def test_union_boxes_l0_h0(self):
        union_l0_h0: TTreeAut = tree_aut_union(ta.box_l0, ta.box_h0)

        self.assertTrue(match_tree_top_down(union_l0_h0, tn.l0_test_tree_1))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.l0_test_tree_2))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.l0_test_tree_3))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.l0_test_tree_4))

        self.assertTrue(match_tree_top_down(union_l0_h0, tn.h0_test_tree_1))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.h0_test_tree_2))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.h0_test_tree_3))
        self.assertTrue(match_tree_top_down(union_l0_h0, tn.h0_test_tree_4))

        self.assertFalse(match_tree_top_down(union_l0_h0, tn.l1_test_tree_1))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.l1_test_tree_2))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.l1_test_tree_3))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.l1_test_tree_4))

        self.assertFalse(match_tree_top_down(union_l0_h0, tn.h1_test_tree_1))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.h1_test_tree_2))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.h1_test_tree_3))
        self.assertFalse(match_tree_top_down(union_l0_h0, tn.h1_test_tree_4))

    def test_union_boxes_l0_h1(self):
        union_l0_h1 = tree_aut_union(ta.box_l0, ta.box_h1)

        self.assertTrue(union_l0_h1, tn.l0_test_tree_1)
        self.assertTrue(union_l0_h1, tn.l0_test_tree_2)
        self.assertTrue(union_l0_h1, tn.l0_test_tree_3)
        self.assertTrue(union_l0_h1, tn.l0_test_tree_4)

        self.assertTrue(union_l0_h1, tn.h1_test_tree_1)
        self.assertTrue(union_l0_h1, tn.h1_test_tree_2)
        self.assertTrue(union_l0_h1, tn.h1_test_tree_3)
        self.assertTrue(union_l0_h1, tn.h1_test_tree_4)

    def test_union_boxes_x_l1(self):
        union_x_l1 = tree_aut_union(ta.box_x, ta.box_l1)

        self.assertTrue(union_x_l1, tn.x_test_tree_1)
        self.assertTrue(union_x_l1, tn.x_test_tree_2)
        self.assertTrue(union_x_l1, tn.x_test_tree_3)

        self.assertTrue(union_x_l1, tn.l1_test_tree_1)
        self.assertTrue(union_x_l1, tn.l1_test_tree_2)
        self.assertTrue(union_x_l1, tn.l1_test_tree_3)
        self.assertTrue(union_x_l1, tn.l1_test_tree_4)
