import unittest

from tree_automata import non_empty_top_down
from box_ordering.product import tree_aut_product
import tests.tree_automata_examples as ta


# non_empty_top_down() returns two results => witness TTreeNode and witness string
# we assert that the witness tree node is (not) empty / None
class TestTreeAutomatonOrderingProduct(unittest.TestCase):
    @unittest.skip
    def test_tree_aut_product_reflexive(self):
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_x))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_l0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_l1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_lport))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_h0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_h1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_hport))[0])

    def test_tree_aut_product_not_none(self):
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_l0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_l1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_lport))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_h0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_h1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_x, ta.tdd_box_hport))[0])

        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_l0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_l1))[0])

        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_h0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_h1))[0])

        # NOTE: Since we can map two different ports of LPort and HPort box to the same output (X port),
        # the product is non-empty, as any tree produced by X box can be mapped to LPort/HPort.
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_x))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_x))[0])

        # NOTE: It makes sense why these also produce non empty witness.
        # The only possible witnesses of product(LPort, Hx) and product(HPort, Lx) will have a max depth of 1.
        # For such small trees (binary tree with 2 leaves), the output transitions will be used only once
        # and thus can be mapped to 2 different ports. If such small witnesses were disallowed,
        # then LPort and HPort could not map ports properly and no other witness 'should' be possible (not tested).
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_h0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_h1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_lport, ta.tdd_box_hport))[0])

        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_l0))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_l1))[0])
        self.assertIsNotNone(non_empty_top_down(tree_aut_product(ta.tdd_box_hport, ta.tdd_box_lport))[0])

    def test_tree_aut_product_none(self):
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_x))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_l1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_lport))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_h0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_h1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l0, ta.tdd_box_hport))[0])

        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_x))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_l0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_lport))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_h0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_h1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_l1, ta.tdd_box_hport))[0])

        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_x))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_l0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_l1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_lport))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_h1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h0, ta.tdd_box_hport))[0])

        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_x))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_l0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_l1))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_lport))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_h0))[0])
        self.assertIsNone(non_empty_top_down(tree_aut_product(ta.tdd_box_h1, ta.tdd_box_hport))[0])
