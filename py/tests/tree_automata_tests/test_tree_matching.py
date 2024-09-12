import unittest

import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn
from tree_automata.functions.match_tree import match_tree_top_down, match_tree_bottom_up


class TestTreeAutomatonMatchTopDown(unittest.TestCase):
    def test_match_tree_top_down_x(self):
        self.assertTrue(match_tree_top_down(ta.box_x, tn.x_test_tree_1))
        self.assertTrue(match_tree_top_down(ta.box_x, tn.x_test_tree_2))
        self.assertTrue(match_tree_top_down(ta.box_x, tn.x_test_tree_3))

    def test_match_tree_top_down_l0(self):
        self.assertTrue(match_tree_top_down(ta.box_l0, tn.l0_test_tree_1))
        self.assertTrue(match_tree_top_down(ta.box_l0, tn.l0_test_tree_2))
        self.assertTrue(match_tree_top_down(ta.box_l0, tn.l0_test_tree_3))
        self.assertTrue(match_tree_top_down(ta.box_l0, tn.l0_test_tree_4))

        self.assertFalse(match_tree_top_down(ta.box_l0, tn.x_test_tree_1))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.x_test_tree_2))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.x_test_tree_3))

        self.assertFalse(match_tree_top_down(ta.box_l0, tn.l1_test_tree_1))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.l1_test_tree_2))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.l1_test_tree_3))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.l1_test_tree_4))

        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h0_test_tree_4))

        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h1_test_tree_1))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h1_test_tree_2))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h1_test_tree_3))
        self.assertFalse(match_tree_top_down(ta.box_l0, tn.h1_test_tree_4))

    def test_match_tree_top_down_l1(self):
        self.assertTrue(match_tree_top_down(ta.box_l1, tn.l1_test_tree_1))
        self.assertTrue(match_tree_top_down(ta.box_l1, tn.l1_test_tree_2))
        self.assertTrue(match_tree_top_down(ta.box_l1, tn.l1_test_tree_3))
        self.assertTrue(match_tree_top_down(ta.box_l1, tn.l1_test_tree_4))

    def test_match_tree_top_down_h0(self):
        self.assertTrue(match_tree_top_down(ta.box_h0, tn.h0_test_tree_1))
        self.assertTrue(match_tree_top_down(ta.box_h0, tn.h0_test_tree_2))
        self.assertTrue(match_tree_top_down(ta.box_h0, tn.h0_test_tree_3))
        self.assertTrue(match_tree_top_down(ta.box_h0, tn.h0_test_tree_4))

    def test_match_tree_top_down_h1(self):
        self.assertTrue(match_tree_top_down(ta.box_h1, tn.h1_test_tree_1))
        self.assertTrue(match_tree_top_down(ta.box_h1, tn.h1_test_tree_2))
        self.assertTrue(match_tree_top_down(ta.box_h1, tn.h1_test_tree_3))
        self.assertTrue(match_tree_top_down(ta.box_h1, tn.h1_test_tree_4))


class TestTreeAutomatonMatchBottomUp(unittest.TestCase):
    def test_match_tree_bottom_up_x(self):
        self.assertTrue(match_tree_bottom_up(ta.box_x, tn.x_test_tree_1))
        self.assertTrue(match_tree_bottom_up(ta.box_x, tn.x_test_tree_2))
        self.assertTrue(match_tree_bottom_up(ta.box_x, tn.x_test_tree_3))

    def test_match_tree_bottom_up_l0(self):
        self.assertTrue(match_tree_bottom_up(ta.box_l0, tn.l0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(ta.box_l0, tn.l0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(ta.box_l0, tn.l0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(ta.box_l0, tn.l0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.x_test_tree_1))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.x_test_tree_2))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.x_test_tree_3))

        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.l1_test_tree_1))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.l1_test_tree_2))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.l1_test_tree_3))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.l1_test_tree_4))

        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h0_test_tree_1))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h0_test_tree_2))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h0_test_tree_3))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h0_test_tree_4))

        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h1_test_tree_1))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h1_test_tree_2))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h1_test_tree_3))
        self.assertFalse(match_tree_bottom_up(ta.box_l0, tn.h1_test_tree_4))

    def test_match_tree_bottom_up_l1(self):
        self.assertTrue(match_tree_bottom_up(ta.box_l1, tn.l1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(ta.box_l1, tn.l1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(ta.box_l1, tn.l1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(ta.box_l1, tn.l1_test_tree_4))

    def test_match_tree_bottom_up_h0(self):
        self.assertTrue(match_tree_bottom_up(ta.box_h0, tn.h0_test_tree_1))
        self.assertTrue(match_tree_bottom_up(ta.box_h0, tn.h0_test_tree_2))
        self.assertTrue(match_tree_bottom_up(ta.box_h0, tn.h0_test_tree_3))
        self.assertTrue(match_tree_bottom_up(ta.box_h0, tn.h0_test_tree_4))

    def test_match_tree_bottom_up_h1(self):
        self.assertTrue(match_tree_bottom_up(ta.box_h1, tn.h1_test_tree_1))
        self.assertTrue(match_tree_bottom_up(ta.box_h1, tn.h1_test_tree_2))
        self.assertTrue(match_tree_bottom_up(ta.box_h1, tn.h1_test_tree_3))
        self.assertTrue(match_tree_bottom_up(ta.box_h1, tn.h1_test_tree_4))
