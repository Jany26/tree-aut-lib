import unittest

from formats.format_vtf import import_treeaut_from_vtf

# from apply.abdd_apply import check_if_abdd
from apply.abdd_check import check_if_abdd
from tree_automata.automaton import TTreeAut


class TestApplyCheckIfABDD(unittest.TestCase):
    def test_normalization_inputs(self):
        norm1: TTreeAut = import_treeaut_from_vtf("../tests/normalization/normalizationTest1.vtf")
        self.assertTrue(check_if_abdd(norm1))

        norm2: TTreeAut = import_treeaut_from_vtf("../tests/normalization/normalizationTest2.vtf")
        self.assertTrue(check_if_abdd(norm2))

        norm3: TTreeAut = import_treeaut_from_vtf("../tests/normalization/normalizationTest3.vtf")
        self.assertTrue(check_if_abdd(norm3))

        norm4: TTreeAut = import_treeaut_from_vtf("../tests/normalization/normalizationTest4.vtf")
        self.assertFalse(check_if_abdd(norm4))

        newnorm1: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest1.vtf")
        self.assertTrue(check_if_abdd(newnorm1))

        newnorm2: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest2.vtf")
        self.assertTrue(check_if_abdd(newnorm2))

        newnorm3: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest3.vtf")
        self.assertTrue(check_if_abdd(newnorm3))

        newnorm4: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest4.vtf")
        self.assertTrue(check_if_abdd(newnorm4))

        newnorm4_loops: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest4-loops.vtf")
        self.assertFalse(check_if_abdd(newnorm4_loops))

        newnorm4_boxes: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest4-boxes.vtf")
        self.assertTrue(check_if_abdd(newnorm4_boxes))

        newnorm5: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest5.vtf")
        self.assertFalse(check_if_abdd(newnorm5))

        newnorm6: TTreeAut = import_treeaut_from_vtf("../tests/normalization/newNormTest6.vtf")
        self.assertTrue(check_if_abdd(newnorm6))

    def test_unfolding_inputs(self):
        unf1: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        self.assertTrue(check_if_abdd(unf1))

        unf2: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest2.vtf")
        self.assertTrue(check_if_abdd(unf2))

        unf3: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest3.vtf")
        self.assertFalse(check_if_abdd(unf3))

        unf4: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest4.vtf")
        self.assertTrue(check_if_abdd(unf4))

        unf5: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest5.vtf")
        self.assertTrue(check_if_abdd(unf5))

        unf6: TTreeAut = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest6.vtf")
        self.assertTrue(check_if_abdd(unf6))
