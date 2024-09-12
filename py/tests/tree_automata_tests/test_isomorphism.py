import unittest

import tests.tree_automata_examples as ta
from tree_automata.functions.isomorphism import tree_aut_isomorphic


class TestTreeAutomatonIsomorphism(unittest.TestCase):
    def test_tree_aut_isomorphic_boxes_reflexive(self):
        self.assertNotEqual(tree_aut_isomorphic(ta.box_x, ta.box_x), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_l0, ta.box_l0), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_l1, ta.box_l1), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_lport, ta.box_lport), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_h0, ta.box_h0), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_h1, ta.box_h1), {})
        self.assertNotEqual(tree_aut_isomorphic(ta.box_hport, ta.box_hport), {})

    def test_tree_aut_isomorphic_boxes_false(self):
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_h1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_x, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_h1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l0, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_h1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_l1, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_h1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_lport, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_h1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h0, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_h1, ta.box_hport), {})

        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_x), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_l0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_l1), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_lport), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_h0), {})
        self.assertDictEqual(tree_aut_isomorphic(ta.box_hport, ta.box_h1), {})

    @unittest.skip  # TODO create some boxes for isomorphism testing, maybe use language inclusion testing too
    def test_tree_aut_isomorphic_custom_true(self):
        pass
