import unittest

from formats.format_vtf import import_treeaut_from_vtf
from canonization.unfolding import ubda_unfolding, is_unfolded
from tree_automata.automaton import TTreeAut
from apply.abdd import ABDD, import_abdd_from_abdd_file
from apply.abdd_node_cache import ABDDNodeCacheClass


class TestUBDAUnfolding(unittest.TestCase):
    def test_unfolding_basic(self):

        test_1: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        test_2: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest2.vtf")
        test_3: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest3.vtf")
        test_4: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest4.vtf")

        unfolded_1 = ubda_unfolding(test_1, 4)
        unfolded_2 = ubda_unfolding(test_2, 8)
        unfolded_3 = ubda_unfolding(test_3, 5)
        unfolded_4 = ubda_unfolding(test_4, 4)

        self.assertTrue(is_unfolded(unfolded_1))
        self.assertTrue(is_unfolded(unfolded_2))
        self.assertTrue(is_unfolded(unfolded_3))
        self.assertTrue(is_unfolded(unfolded_4))


class TestUBDARootRuleUnfolding(unittest.TestCase):
    ncache = ABDDNodeCacheClass()

    def test_unfolding_root_rules_1(self):
        x_rule = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-2.vtf")
        unfolded_1 = ubda_unfolding(x_rule, 11)
        self.assertTrue(is_unfolded(unfolded_1))

    def test_unfolding_root_rules_2(self):
        lp_rule = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/multiroot-example.vtf")
        unfolded_2 = ubda_unfolding(lp_rule, 11)
        self.assertTrue(is_unfolded(unfolded_2))

    def test_unfolding_root_rules_3(self):
        multiport = import_treeaut_from_vtf("../tests/abdd-format/vtf-format-multiport-rootrule.vtf")
        unfolded_3 = ubda_unfolding(multiport, 7)
        self.assertTrue(is_unfolded(unfolded_3))

    def test_unfolding_root_rules_4(self):
        abdd_example = import_abdd_from_abdd_file("../tests/abdd-format/multiroot-example.dd", self.ncache)
        treeaut = abdd_example.convert_to_treeaut_obj()
        unfolded_4 = ubda_unfolding(treeaut, 11)
        self.assertTrue(is_unfolded(unfolded_4))
