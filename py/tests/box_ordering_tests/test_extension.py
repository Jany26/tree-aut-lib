import unittest

from box_ordering.coocurrence import tree_aut_is_extension
import tests.tree_automata_examples as ta


class TestTreeAutomatonOrderingExtension(unittest.TestCase):
    def test_tree_aut_is_extension_true(self):
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_lport))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_hport))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_l0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_l1))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_h0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_h1))

        self.assertTrue(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_l0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_l1))

        self.assertTrue(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_h0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_h1))

    def test_tree_aut_is_extension_reflexive(self):
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_x, ta.tdd_box_x))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_l0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_l1))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_lport))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_h0))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_h1))
        self.assertTrue(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_hport))

    def test_tree_aut_is_extension_false(self):

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_l1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_lport))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_h0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_h1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l0, ta.tdd_box_hport))

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_l0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_lport))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_h0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_h1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_l1, ta.tdd_box_hport))

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_h0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_h1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_lport, ta.tdd_box_hport))

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_l0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_l1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_lport))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_h1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h0, ta.tdd_box_hport))

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_l0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_l1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_lport))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_h0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_h1, ta.tdd_box_hport))

        self.assertFalse(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_x))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_l0))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_l1))
        self.assertFalse(tree_aut_is_extension(ta.tdd_box_hport, ta.tdd_box_lport))
