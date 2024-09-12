import unittest

from tree_automata.functions.emptiness import non_empty_top_down, non_empty_bottom_up
from tree_automata.functions.intersection import tree_aut_intersection
import tests.tree_automata_examples as ta
from tree_automata.functions.match_tree import match_tree_top_down, match_tree_bottom_up


class TestTreeAutomatonNonEmptiness(unittest.TestCase):
    def test_non_emptiness_top_down_boxes(self):
        witness_tree_x, witness_str_x = non_empty_top_down(ta.box_x)
        witness_tree_l0, witness_str_l0 = non_empty_top_down(ta.box_l0)
        witness_tree_l1, witness_str_l1 = non_empty_top_down(ta.box_l1)
        witness_tree_h0, witness_str_h0 = non_empty_top_down(ta.box_h0)
        witness_tree_h1, witness_str_h1 = non_empty_top_down(ta.box_h1)

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

        self.assertTrue(match_tree_top_down(ta.box_x, witness_tree_x))
        self.assertTrue(match_tree_top_down(ta.box_l0, witness_tree_l0))
        self.assertTrue(match_tree_top_down(ta.box_l1, witness_tree_l1))
        self.assertTrue(match_tree_top_down(ta.box_h0, witness_tree_h0))
        self.assertTrue(match_tree_top_down(ta.box_h1, witness_tree_h1))

    def test_non_emptiness_top_down_intersections(self):
        int_x_l0_tree, int_x_l0_str = non_empty_top_down(tree_aut_intersection(ta.box_x, ta.box_l0))
        int_x_l1_tree, int_x_l1_str = non_empty_top_down(tree_aut_intersection(ta.box_x, ta.box_l1))
        int_x_h0_tree, int_x_h0_str = non_empty_top_down(tree_aut_intersection(ta.box_x, ta.box_h0))
        int_x_h1_tree, int_x_h1_str = non_empty_top_down(tree_aut_intersection(ta.box_x, ta.box_h1))
        int_l0_l1_tree, int_l0_l1_str = non_empty_top_down(tree_aut_intersection(ta.box_l0, ta.box_l1))
        int_l0_h0_tree, int_l0_h0_str = non_empty_top_down(tree_aut_intersection(ta.box_l0, ta.box_h0))
        int_l0_h1_tree, int_l0_h1_str = non_empty_top_down(tree_aut_intersection(ta.box_l0, ta.box_h1))
        int_l1_h0_tree, int_l1_h0_str = non_empty_top_down(tree_aut_intersection(ta.box_l1, ta.box_h0))
        int_l1_h1_tree, int_l1_h1_str = non_empty_top_down(tree_aut_intersection(ta.box_l1, ta.box_h1))
        int_h0_h1_tree, int_h0_h1_str = non_empty_top_down(tree_aut_intersection(ta.box_h0, ta.box_h1))

        self.assertIsNone(int_x_l0_tree)
        self.assertIsNone(int_x_l1_tree)
        self.assertIsNone(int_x_h0_tree)
        self.assertIsNone(int_x_h1_tree)
        self.assertIsNone(int_l0_l1_tree)
        self.assertIsNone(int_l0_h0_tree)
        self.assertIsNone(int_l0_h1_tree)
        self.assertIsNone(int_l1_h0_tree)
        self.assertIsNone(int_l1_h1_tree)
        self.assertIsNone(int_h0_h1_tree)

        self.assertEqual(int_x_l0_str, "")
        self.assertEqual(int_x_l1_str, "")
        self.assertEqual(int_x_h0_str, "")
        self.assertEqual(int_x_h1_str, "")
        self.assertEqual(int_l0_l1_str, "")
        self.assertEqual(int_l0_h0_str, "")
        self.assertEqual(int_l0_h1_str, "")
        self.assertEqual(int_l1_h0_str, "")
        self.assertEqual(int_l1_h1_str, "")
        self.assertEqual(int_h0_h1_str, "")

    @unittest.skip  # TODO remove a state or an edge and test language emptiness before/after
    def test_non_emptiness_top_down_state_removal(self):
        pass

    def test_non_emptiness_bottom_up_boxes(self):
        witness_tree_x, witness_str_x = non_empty_bottom_up(ta.box_x)
        witness_tree_l0, witness_str_l0 = non_empty_bottom_up(ta.box_l0)
        witness_tree_l1, witness_str_l1 = non_empty_bottom_up(ta.box_l1)
        witness_tree_h0, witness_str_h0 = non_empty_bottom_up(ta.box_h0)
        witness_tree_h1, witness_str_h1 = non_empty_bottom_up(ta.box_h1)

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

        self.assertTrue(match_tree_bottom_up(ta.box_x, witness_tree_x))
        self.assertTrue(match_tree_bottom_up(ta.box_l0, witness_tree_l0))
        self.assertTrue(match_tree_bottom_up(ta.box_l1, witness_tree_l1))
        self.assertTrue(match_tree_bottom_up(ta.box_h0, witness_tree_h0))
        self.assertTrue(match_tree_bottom_up(ta.box_h1, witness_tree_h1))

    def test_non_emptiness_bottom_up_intersections(self):
        int_x_l0_tree, int_x_l0_str = non_empty_bottom_up(tree_aut_intersection(ta.box_x, ta.box_l0))
        int_x_l1_tree, int_x_l1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_x, ta.box_l1))
        int_x_h0_tree, int_x_h0_str = non_empty_bottom_up(tree_aut_intersection(ta.box_x, ta.box_h0))
        int_x_h1_tree, int_x_h1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_x, ta.box_h1))
        int_l0_l1_tree, int_l0_l1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_l0, ta.box_l1))
        int_l0_h0_tree, int_l0_h0_str = non_empty_bottom_up(tree_aut_intersection(ta.box_l0, ta.box_h0))
        int_l0_h1_tree, int_l0_h1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_l0, ta.box_h1))
        int_l1_h0_tree, int_l1_h0_str = non_empty_bottom_up(tree_aut_intersection(ta.box_l1, ta.box_h0))
        int_l1_h1_tree, int_l1_h1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_l1, ta.box_h1))
        int_h0_h1_tree, int_h0_h1_str = non_empty_bottom_up(tree_aut_intersection(ta.box_h0, ta.box_h1))

        self.assertIsNone(int_x_l0_tree)
        self.assertIsNone(int_x_l1_tree)
        self.assertIsNone(int_x_h0_tree)
        self.assertIsNone(int_x_h1_tree)
        self.assertIsNone(int_l0_l1_tree)
        self.assertIsNone(int_l0_h0_tree)
        self.assertIsNone(int_l0_h1_tree)
        self.assertIsNone(int_l1_h0_tree)
        self.assertIsNone(int_l1_h1_tree)
        self.assertIsNone(int_h0_h1_tree)

        self.assertEqual(int_x_l0_str, "")
        self.assertEqual(int_x_l1_str, "")
        self.assertEqual(int_x_h0_str, "")
        self.assertEqual(int_x_h1_str, "")
        self.assertEqual(int_l0_l1_str, "")
        self.assertEqual(int_l0_h0_str, "")
        self.assertEqual(int_l0_h1_str, "")
        self.assertEqual(int_l1_h0_str, "")
        self.assertEqual(int_l1_h1_str, "")
        self.assertEqual(int_h0_h1_str, "")

    @unittest.skip  # TODO remove a state or an edge and test language emptiness before/after
    def test_non_emptiness_bottom_up_state_removal(self):
        pass
