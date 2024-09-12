import unittest

from formats.format_vtf import import_treeaut_from_vtf
import tests.tree_automata_examples as ta
from tree_automata.automaton import TTreeAut
from tree_automata.functions.complement import tree_aut_complement
from tree_automata.functions.determinization import tree_aut_determinization
from tree_automata.functions.intersection import tree_aut_intersection
from tree_automata.functions.union import tree_aut_union
from tree_automata.functions.well_defined import is_well_defined


class TestTreeAutomataWellDefined(unittest.TestCase):
    def test_well_defined_boxes(self):
        self.assertTrue(is_well_defined(ta.box_x))
        self.assertTrue(is_well_defined(ta.box_l0))
        self.assertTrue(is_well_defined(ta.box_l1))
        self.assertTrue(is_well_defined(ta.box_lport))
        self.assertTrue(is_well_defined(ta.box_h0))
        self.assertTrue(is_well_defined(ta.box_h1))
        self.assertTrue(is_well_defined(ta.box_hport))

    def test_well_defined_unions(self):
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_x, ta.box_l0)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_x, ta.box_l1)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_x, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_x, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_l0, ta.box_l1)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_l0, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_l0, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_l1, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_l1, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_union(ta.box_h0, ta.box_h1)))

    def test_well_defined_intersections(self):
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_x, ta.box_l0)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_x, ta.box_l1)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_x, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_x, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_l0, ta.box_l1)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_l0, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_l0, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_l1, ta.box_h0)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_l1, ta.box_h1)))
        self.assertFalse(is_well_defined(tree_aut_intersection(ta.box_h0, ta.box_h1)))

    def test_well_defined_determinization(self):
        # box X is already top-down deterministic, so it is well defined
        self.assertTrue(is_well_defined(tree_aut_determinization(ta.box_x, ta.box_x.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_l0, ta.box_l0.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_l1, ta.box_l1.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_h0, ta.box_h0.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_h1, ta.box_h1.get_symbol_arity_dict())))

        # full alphabet introduces multiple extra output symbol, violating port-uniqueness property
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_x, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_l0, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_l1, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_h0, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_determinization(ta.box_h1, ta.full_alphabet)))

    def test_well_defined_complement(self):
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_x, ta.box_x.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_l0, ta.box_l0.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_l1, ta.box_l1.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_h0, ta.box_h0.get_symbol_arity_dict())))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_h1, ta.box_h1.get_symbol_arity_dict())))

        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_x, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_l0, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_l1, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_h0, ta.full_alphabet)))
        self.assertFalse(is_well_defined(tree_aut_complement(ta.box_h1, ta.full_alphabet)))

    def test_well_defined_random(self):
        test_unreachable_1: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf")
        test_unreachable_2: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf")
        test_unreachable_3: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf")
        self.assertFalse(is_well_defined(test_unreachable_1))
        self.assertFalse(is_well_defined(test_unreachable_2))
        self.assertFalse(is_well_defined(test_unreachable_3))
