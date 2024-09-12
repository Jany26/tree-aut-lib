import unittest

from formats.format_vtf import import_treeaut_from_vtf
from canonization.unfolding import ubda_unfolding, is_unfolded
from tree_automata.automaton import TTreeAut


class TestUBDAUnfolding(unittest.TestCase):
    def test_unfolding_basic(self):

        test_1: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        test_2: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest2.vtf")
        test_3: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest3.vtf")
        test_4: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest4.vtf")

        unfolded_1 = ubda_unfolding(test_1)
        unfolded_2 = ubda_unfolding(test_2)
        unfolded_3 = ubda_unfolding(test_3)
        unfolded_4 = ubda_unfolding(test_4)

        self.assertTrue(is_unfolded(unfolded_1))
        self.assertTrue(is_unfolded(unfolded_2))
        self.assertTrue(is_unfolded(unfolded_3))
        self.assertTrue(is_unfolded(unfolded_4))
