import unittest
from bdd.bdd_class import compare_bdds
import tests.bdd_examples as bd


class TestBinaryDecisionDiagramBasic(unittest.TestCase):
    def test_bdd_compare_basic_equal(self):
        self.assertEqual(bd.bdd_1.count_nodes(), 6)
        self.assertEqual(bd.bdd_2.count_nodes(), 6)
        self.assertEqual(bd.bdd_1.count_branches_iter(0), bd.bdd_2.count_branches_iter(0))
        self.assertEqual(bd.bdd_1.count_branches_iter(0), 2)
        self.assertEqual(bd.bdd_1.count_branches_iter(1), bd.bdd_2.count_branches_iter(1))
        self.assertEqual(bd.bdd_1.count_branches_iter(1), 3)

        self.assertTrue(compare_bdds(bd.bdd_1, bd.bdd_2))
        self.assertTrue(bd.bdd_1.is_valid())
        self.assertTrue(bd.bdd_2.is_valid())
