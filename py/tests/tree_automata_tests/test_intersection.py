import unittest

from tree_automata.automaton import TTreeAut
from tree_automata.functions.emptiness import non_empty_top_down, non_empty_bottom_up
from tree_automata.functions.intersection import tree_aut_intersection
import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn
from tree_automata.functions.match_tree import match_tree_bottom_up, match_tree_top_down


class TestTreeAutomatonIntersection(unittest.TestCase):
    def test_intersection_emptiness_different_boxes(self):
        intersection_l0_h0: TTreeAut = tree_aut_intersection(ta.box_l0, ta.box_h0)

        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.l0_test_tree_1))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.l0_test_tree_2))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.l0_test_tree_3))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.l0_test_tree_4))

        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_top_down(intersection_l0_h0, tn.h0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.l0_test_tree_1))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.l0_test_tree_2))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.l0_test_tree_3))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.l0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_bottom_up(intersection_l0_h0, tn.h0_test_tree_4))

    def test_intersection_emptiness_same_boxes_top_down(self):
        witness_tree_x, witness_str_x = non_empty_top_down(tree_aut_intersection(ta.box_x, ta.box_x))
        witness_tree_l0, witness_str_l0 = non_empty_top_down(tree_aut_intersection(ta.box_l0, ta.box_l0))
        witness_tree_l1, witness_str_l1 = non_empty_top_down(tree_aut_intersection(ta.box_l1, ta.box_l1))
        witness_tree_h0, witness_str_h0 = non_empty_top_down(tree_aut_intersection(ta.box_h0, ta.box_h0))
        witness_tree_h1, witness_str_h1 = non_empty_top_down(tree_aut_intersection(ta.box_h1, ta.box_h1))

        self.assertIsNotNone(witness_tree_x)
        self.assertIsNotNone(witness_tree_l0)
        self.assertIsNotNone(witness_tree_l1)
        self.assertIsNotNone(witness_tree_h0)
        self.assertIsNotNone(witness_tree_h1)

        self.assertNotEqual(witness_str_x, "")
        self.assertNotEqual(witness_str_l0, "")
        self.assertNotEqual(witness_str_l1, "")
        self.assertNotEqual(witness_str_h0, "")
        self.assertNotEqual(witness_str_h1, "")

    def test_intersection_emptiness_same_boxes_bottom_up(self):
        witness_tree_x, witness_str_x = non_empty_bottom_up(tree_aut_intersection(ta.box_x, ta.box_x))
        witness_tree_l0, witness_str_l0 = non_empty_bottom_up(tree_aut_intersection(ta.box_l0, ta.box_l0))
        witness_tree_l1, witness_str_l1 = non_empty_bottom_up(tree_aut_intersection(ta.box_l1, ta.box_l1))
        witness_tree_h0, witness_str_h0 = non_empty_bottom_up(tree_aut_intersection(ta.box_h0, ta.box_h0))
        witness_tree_h1, witness_str_h1 = non_empty_bottom_up(tree_aut_intersection(ta.box_h1, ta.box_h1))

        self.assertIsNotNone(witness_tree_x)
        self.assertIsNotNone(witness_tree_l0)
        self.assertIsNotNone(witness_tree_l1)
        self.assertIsNotNone(witness_tree_h0)
        self.assertIsNotNone(witness_tree_h1)

        self.assertNotEqual(witness_str_x, "")
        self.assertNotEqual(witness_str_l0, "")
        self.assertNotEqual(witness_str_l1, "")
        self.assertNotEqual(witness_str_h0, "")
        self.assertNotEqual(witness_str_h1, "")
