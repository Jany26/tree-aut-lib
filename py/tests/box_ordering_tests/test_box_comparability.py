import unittest

from box_ordering.box_ordering import are_comparable
import tests.tree_automata_examples as ta


class TestTreeAutomatonOrderingComparability(unittest.TestCase):
    @unittest.skip  # TODO: check why these are not True + fix (if possible)
    def test_boxes_are_comparable_true(self):
        self.assertTrue(are_comparable(ta.box_l0, ta.box_x))
        self.assertTrue(are_comparable(ta.box_l1, ta.box_x))
        self.assertTrue(are_comparable(ta.box_h0, ta.box_x))
        self.assertTrue(are_comparable(ta.box_h1, ta.box_x))
        self.assertTrue(are_comparable(ta.box_lport, ta.box_x))
        self.assertTrue(are_comparable(ta.box_hport, ta.box_x))

        self.assertTrue(are_comparable(ta.box_lport, ta.box_l0))
        self.assertTrue(are_comparable(ta.box_lport, ta.box_l1))
        self.assertTrue(are_comparable(ta.box_hport, ta.box_h0))
        self.assertTrue(are_comparable(ta.box_hport, ta.box_h1))

    def test_boxes_are_comparable_reflexive(self):
        # TODO: check if these should really be true
        self.assertTrue(are_comparable(ta.box_x, ta.box_x))
        self.assertTrue(are_comparable(ta.box_l0, ta.box_l0))
        self.assertTrue(are_comparable(ta.box_l1, ta.box_l1))
        self.assertTrue(are_comparable(ta.box_lport, ta.box_lport))
        self.assertTrue(are_comparable(ta.box_h0, ta.box_h0))
        self.assertTrue(are_comparable(ta.box_h1, ta.box_h1))
        self.assertTrue(are_comparable(ta.box_hport, ta.box_hport))

    def test_boxes_are_comparable_false(self):
        self.assertFalse(are_comparable(ta.box_x, ta.box_l0))
        self.assertFalse(are_comparable(ta.box_x, ta.box_l1))
        self.assertFalse(are_comparable(ta.box_x, ta.box_lport))
        self.assertFalse(are_comparable(ta.box_x, ta.box_h0))
        self.assertFalse(are_comparable(ta.box_x, ta.box_h1))
        self.assertFalse(are_comparable(ta.box_x, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_l0, ta.box_l1))
        self.assertFalse(are_comparable(ta.box_l0, ta.box_lport))
        self.assertFalse(are_comparable(ta.box_l0, ta.box_h0))
        self.assertFalse(are_comparable(ta.box_l0, ta.box_h1))
        self.assertFalse(are_comparable(ta.box_l0, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_l1, ta.box_l0))
        self.assertFalse(are_comparable(ta.box_l1, ta.box_lport))
        self.assertFalse(are_comparable(ta.box_l1, ta.box_h0))
        self.assertFalse(are_comparable(ta.box_l1, ta.box_h1))
        self.assertFalse(are_comparable(ta.box_l1, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_lport, ta.box_h0))
        self.assertFalse(are_comparable(ta.box_lport, ta.box_h1))
        self.assertFalse(are_comparable(ta.box_lport, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_h0, ta.box_l0))
        self.assertFalse(are_comparable(ta.box_h0, ta.box_l1))
        self.assertFalse(are_comparable(ta.box_h0, ta.box_lport))
        self.assertFalse(are_comparable(ta.box_h0, ta.box_h1))
        self.assertFalse(are_comparable(ta.box_h0, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_h1, ta.box_l0))
        self.assertFalse(are_comparable(ta.box_h1, ta.box_l1))
        self.assertFalse(are_comparable(ta.box_h1, ta.box_lport))
        self.assertFalse(are_comparable(ta.box_h1, ta.box_h0))
        self.assertFalse(are_comparable(ta.box_h1, ta.box_hport))

        self.assertFalse(are_comparable(ta.box_hport, ta.box_l0))
        self.assertFalse(are_comparable(ta.box_hport, ta.box_l1))
        self.assertFalse(are_comparable(ta.box_hport, ta.box_lport))
