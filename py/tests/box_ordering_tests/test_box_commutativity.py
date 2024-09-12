import unittest

from box_ordering.box_ordering import are_commutative
import tests.tree_automata_examples as ta


# just to be sure, we test 'box commutativity' both ways (but it is redundant)
class TestTreeAutomatonOrderingCommutativity(unittest.TestCase):
    def test_boxes_are_commutative_true(self):
        self.assertTrue(are_commutative(ta.box_l0, ta.box_l1))
        self.assertTrue(are_commutative(ta.box_l1, ta.box_l0))
        self.assertTrue(are_commutative(ta.box_h0, ta.box_h1))
        self.assertTrue(are_commutative(ta.box_h1, ta.box_h0))

    @unittest.skip  # TODO: check: same 2 boxes should (probably) be commutative
    def test_boxes_are_commutative_reflexive(self):
        self.assertTrue(are_commutative(ta.box_x, ta.box_x))
        self.assertTrue(are_commutative(ta.box_l0, ta.box_l0))
        self.assertTrue(are_commutative(ta.box_l1, ta.box_l1))
        self.assertTrue(are_commutative(ta.box_lport, ta.box_lport))
        self.assertTrue(are_commutative(ta.box_h0, ta.box_h0))
        self.assertTrue(are_commutative(ta.box_h1, ta.box_h1))
        self.assertTrue(are_commutative(ta.box_hport, ta.box_hport))

    def test_boxes_are_commutative_false(self):
        self.assertFalse(are_commutative(ta.box_x, ta.box_l0))
        self.assertFalse(are_commutative(ta.box_x, ta.box_l1))
        self.assertFalse(are_commutative(ta.box_x, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_x, ta.box_h0))
        self.assertFalse(are_commutative(ta.box_x, ta.box_h1))
        self.assertFalse(are_commutative(ta.box_x, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_l0, ta.box_x))
        self.assertFalse(are_commutative(ta.box_l0, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_l0, ta.box_h0))
        self.assertFalse(are_commutative(ta.box_l0, ta.box_h1))
        self.assertFalse(are_commutative(ta.box_l0, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_l1, ta.box_x))
        self.assertFalse(are_commutative(ta.box_l1, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_l1, ta.box_h0))
        self.assertFalse(are_commutative(ta.box_l1, ta.box_h1))
        self.assertFalse(are_commutative(ta.box_l1, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_lport, ta.box_x))
        self.assertFalse(are_commutative(ta.box_lport, ta.box_l0))
        self.assertFalse(are_commutative(ta.box_lport, ta.box_l1))
        self.assertFalse(are_commutative(ta.box_lport, ta.box_h0))
        self.assertFalse(are_commutative(ta.box_lport, ta.box_h1))
        self.assertFalse(are_commutative(ta.box_lport, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_h0, ta.box_x))
        self.assertFalse(are_commutative(ta.box_h0, ta.box_l0))
        self.assertFalse(are_commutative(ta.box_h0, ta.box_l1))
        self.assertFalse(are_commutative(ta.box_h0, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_h0, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_h1, ta.box_x))
        self.assertFalse(are_commutative(ta.box_h1, ta.box_l0))
        self.assertFalse(are_commutative(ta.box_h1, ta.box_l1))
        self.assertFalse(are_commutative(ta.box_h1, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_h1, ta.box_hport))

        self.assertFalse(are_commutative(ta.box_hport, ta.box_x))
        self.assertFalse(are_commutative(ta.box_hport, ta.box_l0))
        self.assertFalse(are_commutative(ta.box_hport, ta.box_l1))
        self.assertFalse(are_commutative(ta.box_hport, ta.box_lport))
        self.assertFalse(are_commutative(ta.box_hport, ta.box_h0))
        self.assertFalse(are_commutative(ta.box_hport, ta.box_h1))
