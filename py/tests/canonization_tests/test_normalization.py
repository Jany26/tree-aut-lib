import unittest

from experiments.simulation import simulate_and_compare
from formats.format_vtf import import_treeaut_from_vtf
from canonization.normalization import ubda_normalize, is_normalized
from tree_automata.functions.trimming import remove_useless_states
from helpers.string_manipulation import create_var_order_list
from canonization.unfolding import ubda_unfolding
from tree_automata.var_manipulation import add_variables_bottom_up, add_variables_fixpoint, check_variable_overlap


# TODO: update detailed normalization tests
class TestUBDANormalization(unittest.TestCase):
    def test_normalization_after_unfolding(self):
        # failing for the same reason as the test_normalization_detailed_3
        test_bda_1 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        test_bda_2 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest2.vtf")
        test_bda_3 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest3.vtf")
        test_bda_4 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest4.vtf")
        test_bda_5 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest5.vtf")

        unfolded_bda_1 = ubda_unfolding(test_bda_1, 4)
        unfolded_bda_2 = ubda_unfolding(test_bda_2, 8)
        unfolded_bda_3 = ubda_unfolding(test_bda_3, 5)
        unfolded_bda_4 = ubda_unfolding(test_bda_4, 4)
        unfolded_bda_5 = ubda_unfolding(test_bda_5, 8)

        normalized_bda_1 = remove_useless_states(ubda_normalize(unfolded_bda_1, create_var_order_list("x", 4)))
        normalized_bda_2 = remove_useless_states(ubda_normalize(unfolded_bda_2, create_var_order_list("", 8)))
        normalized_bda_3 = remove_useless_states(ubda_normalize(unfolded_bda_3, create_var_order_list("", 5)))
        normalized_bda_4 = remove_useless_states(ubda_normalize(unfolded_bda_4, create_var_order_list("", 4)))
        normalized_bda_5 = remove_useless_states(ubda_normalize(unfolded_bda_5, create_var_order_list("x", 8)))

        self.assertTrue(simulate_and_compare(unfolded_bda_1, normalized_bda_1, 4))
        self.assertTrue(simulate_and_compare(unfolded_bda_2, normalized_bda_2, 8))
        self.assertTrue(simulate_and_compare(unfolded_bda_3, normalized_bda_3, 5))
        self.assertTrue(simulate_and_compare(unfolded_bda_4, normalized_bda_4, 4))
        self.assertTrue(simulate_and_compare(unfolded_bda_5, normalized_bda_5, 8))

        self.assertTrue(check_variable_overlap(normalized_bda_1, 5))
        self.assertTrue(check_variable_overlap(normalized_bda_2, 9))
        self.assertTrue(check_variable_overlap(normalized_bda_3, 6))
        self.assertTrue(check_variable_overlap(normalized_bda_4, 5))
        self.assertTrue(check_variable_overlap(normalized_bda_5, 9))

    def test_only_normalization(self):
        test_bda_1 = import_treeaut_from_vtf("../tests/normalization/normalizationTest1.vtf")
        test_bda_2 = import_treeaut_from_vtf("../tests/normalization/normalizationTest2.vtf")
        test_bda_3 = import_treeaut_from_vtf("../tests/normalization/normalizationTest3.vtf")
        test_bda_4 = import_treeaut_from_vtf("../tests/normalization/normalizationTest4.vtf")

        variables = create_var_order_list("x", 8)
        normalized_bda_1 = ubda_normalize(test_bda_1, variables)
        normalized_bda_2 = ubda_normalize(test_bda_2, variables)
        normalized_bda_3 = ubda_normalize(test_bda_3, variables)
        normalized_bda_4 = ubda_normalize(test_bda_4, variables)

        self.assertTrue(is_normalized(normalized_bda_1))
        self.assertTrue(is_normalized(normalized_bda_2))
        self.assertTrue(is_normalized(normalized_bda_3))
        self.assertTrue(is_normalized(normalized_bda_4))

    def test_normalization_detailed_1(self):
        initial = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        unfolded = ubda_unfolding(initial, 4)
        unfolded.reformat_keys()
        unfolded.reformat_states()

        normalized = ubda_normalize(unfolded, create_var_order_list("x", 4))
        self.assertTrue(simulate_and_compare(unfolded, normalized, 4))
        self.assertTrue(check_variable_overlap(normalized))

    def test_normalization_detailed_2(self):
        initial = import_treeaut_from_vtf("../tests/normalization/newNormTest5.vtf")
        add_variables_fixpoint(initial, 7)

        normalized = ubda_normalize(initial, create_var_order_list("x", 7))
        self.assertTrue(simulate_and_compare(initial, normalized, 6))
        self.assertTrue(check_variable_overlap(normalized))

    def test_normalization_detailed_3(self):
        initial = import_treeaut_from_vtf("../tests/normalization/newNormTest4-loops.vtf")
        unfolded = ubda_unfolding(initial, 9)
        unfolded.reformat_keys()
        unfolded.reformat_states()

        normalized = ubda_normalize(unfolded, create_var_order_list("x", 9))
        self.assertTrue(simulate_and_compare(unfolded, normalized, 8))
        self.assertTrue(check_variable_overlap(normalized))
