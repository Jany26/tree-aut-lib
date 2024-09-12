from typing import Tuple
import unittest

from formats.format_vtf import import_treeaut_from_vtf
from tree_automata.automaton import TTreeAut
from tree_automata.functions.complement import tree_aut_complement
from tree_automata.functions.emptiness import non_empty_top_down
from tree_automata.functions.intersection import tree_aut_intersection
from tree_automata.tree_node import TTreeNode
import tests.tree_automata_examples as ta


def sanity_emptiness_result(automaton: TTreeAut) -> Tuple[TTreeNode, str]:
    complement: TTreeAut = tree_aut_complement(automaton, automaton.get_symbol_arity_dict())
    intersection: TTreeAut = tree_aut_intersection(automaton, complement)
    witness_tree, witness_str = non_empty_top_down(intersection)
    return witness_tree, witness_str


class TestTreeAutomatonSanity(unittest.TestCase):
    """[description]
    check if `intersection(complement(L), L)` is empty

    essentially test multiple operations at once:
    - determinization (mainly), since complement needs determinization first
    - intersection
    - language emptiness
    """

    def test_sanity_boxes(self):
        witness_tree_x, witness_str_x = sanity_emptiness_result(ta.box_x)
        witness_tree_l0, witness_str_l0 = sanity_emptiness_result(ta.box_l0)
        witness_tree_l1, witness_str_l1 = sanity_emptiness_result(ta.box_l1)
        witness_tree_h0, witness_str_h0 = sanity_emptiness_result(ta.box_h0)
        witness_tree_h1, witness_str_h1 = sanity_emptiness_result(ta.box_h1)

        self.assertIsNone(witness_tree_x)
        self.assertIsNone(witness_tree_l0)
        self.assertIsNone(witness_tree_l1)
        self.assertIsNone(witness_tree_h0)
        self.assertIsNone(witness_tree_h1)

        self.assertEqual(witness_str_x, "")
        self.assertEqual(witness_str_l0, "")
        self.assertEqual(witness_str_l1, "")
        self.assertEqual(witness_str_h0, "")
        self.assertEqual(witness_str_h1, "")

    @unittest.skip("artmc determinization takes too long for usual regression testing")
    def test_sanity_artmc_benchmarks(self):
        """
        [notes]
        - benchmarks are from ARTMC [Abstract Regular Tree Model Checking]
        - see https://github.com/ondrik/automata-benchmarks
        """
        a0053_aut: TTreeAut = import_treeaut_from_vtf("../benchmark/nta/vtf/A0053.vtf")
        a0054_aut: TTreeAut = import_treeaut_from_vtf("../benchmark/nta/vtf/A0054.vtf")
        a0055_aut: TTreeAut = import_treeaut_from_vtf("../benchmark/nta/vtf/A0055.vtf")
        a0056_aut: TTreeAut = import_treeaut_from_vtf("../benchmark/nta/vtf/A0056.vtf")
        a0057_aut: TTreeAut = import_treeaut_from_vtf("../benchmark/nta/vtf/A0057.vtf")

        witness_tree_a0053, _ = non_empty_top_down(a0053_aut)
        witness_tree_a0054, _ = non_empty_top_down(a0054_aut)
        witness_tree_a0055, _ = non_empty_top_down(a0055_aut)
        witness_tree_a0056, _ = non_empty_top_down(a0056_aut)
        witness_tree_a0057, _ = non_empty_top_down(a0057_aut)

        self.assertIsNotNone(witness_tree_a0053)
        self.assertIsNotNone(witness_tree_a0054)
        self.assertIsNotNone(witness_tree_a0055)
        self.assertIsNotNone(witness_tree_a0056)
        self.assertIsNotNone(witness_tree_a0057)

        witness_tree_a0053, _ = sanity_emptiness_result(a0053_aut)
        witness_tree_a0054, _ = sanity_emptiness_result(a0054_aut)
        witness_tree_a0055, _ = sanity_emptiness_result(a0055_aut)
        witness_tree_a0056, _ = sanity_emptiness_result(a0056_aut)
        witness_tree_a0057, _ = sanity_emptiness_result(a0057_aut)

        self.assertIsNone(witness_tree_a0053)
        self.assertIsNone(witness_tree_a0054)
        self.assertIsNone(witness_tree_a0055)
        self.assertIsNone(witness_tree_a0056)
        self.assertIsNone(witness_tree_a0057)
