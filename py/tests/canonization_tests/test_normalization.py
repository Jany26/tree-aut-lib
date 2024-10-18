import unittest

from bdd.bdd_to_treeaut import fill_dont_care_boxes
from experiments.simulation import simulate_and_compare
from formats.format_vtf import import_treeaut_from_vtf
from canonization.normalization import ubda_normalize, is_normalized
from formats.render_dot import export_to_file
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

        # export_to_file(unfolded_bda_1, "test-outputs/normalization-after-unfolding-input-1")
        # export_to_file(unfolded_bda_2, "test-outputs/normalization-after-unfolding-input-2")
        # export_to_file(unfolded_bda_3, "test-outputs/normalization-after-unfolding-input-3")
        # export_to_file(unfolded_bda_4, "test-outputs/normalization-after-unfolding-input-4")
        # export_to_file(unfolded_bda_5, "test-outputs/normalization-after-unfolding-input-5")

        # export_to_file(normalized_bda_1, "test-outputs/normalization-after-unfolding-output-1")
        # export_to_file(normalized_bda_2, "test-outputs/normalization-after-unfolding-output-2")
        # export_to_file(normalized_bda_3, "test-outputs/normalization-after-unfolding-output-3")
        # export_to_file(normalized_bda_4, "test-outputs/normalization-after-unfolding-output-4")
        # export_to_file(normalized_bda_5, "test-outputs/normalization-after-unfolding-output-5")

        self.assertTrue(simulate_and_compare(unfolded_bda_1, normalized_bda_1, 4))
        self.assertTrue(simulate_and_compare(unfolded_bda_2, normalized_bda_2, 8))
        self.assertTrue(simulate_and_compare(unfolded_bda_3, normalized_bda_3, 5))
        self.assertTrue(simulate_and_compare(unfolded_bda_4, normalized_bda_4, 4))
        self.assertTrue(simulate_and_compare(unfolded_bda_5, normalized_bda_5, 8))

        self.assertTrue(check_variable_overlap(normalized_bda_1, 4))
        self.assertTrue(check_variable_overlap(normalized_bda_2, 8))
        self.assertTrue(check_variable_overlap(normalized_bda_3, 5))
        self.assertTrue(check_variable_overlap(normalized_bda_4, 4))
        self.assertTrue(check_variable_overlap(normalized_bda_5, 8))

    def test_normalization_basic_1(self):
        vars: int = 8
        initial_bda_1 = import_treeaut_from_vtf("../tests/normalization/normalizationTest1.vtf")
        fill_dont_care_boxes(initial_bda_1, vars)
        test_bda_1 = ubda_unfolding(initial_bda_1, vars)
        normalized_bda_1 = ubda_normalize(test_bda_1, create_var_order_list("x", vars))
        # export_to_file(test_bda_1, "test_outputs/normalization-only-input-1")
        # export_to_file(normalized_bda_1, "test_outputs/normalization-only-output-1")
        self.assertTrue(check_variable_overlap(normalized_bda_1))
        self.assertTrue(simulate_and_compare(test_bda_1, normalized_bda_1, vars))

    def test_normalization_basic_2(self):
        vars: int = 8
        initial_bda_2 = import_treeaut_from_vtf("../tests/normalization/normalizationTest2.vtf")
        fill_dont_care_boxes(initial_bda_2, vars)
        test_bda_2 = ubda_unfolding(initial_bda_2, vars)
        normalized_bda_2 = ubda_normalize(test_bda_2, create_var_order_list("x", vars))
        # export_to_file(test_bda_2, "test_outputs/normalization-only-input-2")
        # export_to_file(normalized_bda_2, "test_outputs/normalization-only-output-2")
        self.assertTrue(check_variable_overlap(normalized_bda_2))
        self.assertTrue(simulate_and_compare(test_bda_2, normalized_bda_2, vars))

    def test_normalization_basic_3(self):
        vars: int = 8
        initial_bda_3 = import_treeaut_from_vtf("../tests/normalization/normalizationTest3.vtf")
        fill_dont_care_boxes(initial_bda_3, vars)
        test_bda_3 = ubda_unfolding(initial_bda_3, vars)
        normalized_bda_3 = ubda_normalize(test_bda_3, create_var_order_list("x", vars))
        # export_to_file(test_bda_3, "test_outputs/normalization-only-input-3")
        # export_to_file(normalized_bda_3, "test_outputs/normalization-only-output-3")
        self.assertTrue(check_variable_overlap(normalized_bda_3))
        self.assertTrue(simulate_and_compare(test_bda_3, normalized_bda_3, vars))

    def test_normalization_basic_4(self):
        vars: int = 8
        initial_bda_4 = import_treeaut_from_vtf("../tests/normalization/normalizationTest4.vtf")
        fill_dont_care_boxes(initial_bda_4, vars)
        test_bda_4 = ubda_unfolding(initial_bda_4, vars)
        normalized_bda_4 = ubda_normalize(test_bda_4, create_var_order_list("x", vars))
        # export_to_file(test_bda_4, "test_outputs/normalization-only-input-4")
        # export_to_file(normalized_bda_4, "test_outputs/normalization-only-output-4")
        self.assertTrue(check_variable_overlap(normalized_bda_4))
        self.assertTrue(simulate_and_compare(test_bda_4, normalized_bda_4, vars))

    def test_normalization_new_1(self):
        vars: int = 8
        initial_bda_1 = import_treeaut_from_vtf("../tests/normalization/newNormTest1.vtf")
        fill_dont_care_boxes(initial_bda_1, vars)
        test_bda_1 = ubda_unfolding(initial_bda_1, vars)
        normalized_bda_1 = ubda_normalize(test_bda_1, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_1))
        self.assertTrue(simulate_and_compare(test_bda_1, normalized_bda_1, vars))

    def test_normalization_new_2(self):
        vars: int = 8
        initial_bda_2 = import_treeaut_from_vtf("../tests/normalization/newNormTest2.vtf")
        fill_dont_care_boxes(initial_bda_2, vars)
        test_bda_2 = ubda_unfolding(initial_bda_2, vars)
        normalized_bda_2 = ubda_normalize(test_bda_2, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_2))
        self.assertTrue(simulate_and_compare(test_bda_2, normalized_bda_2, vars))

    def test_normalization_new_3(self):
        vars: int = 8
        initial_bda_3 = import_treeaut_from_vtf("../tests/normalization/newNormTest3.vtf")
        fill_dont_care_boxes(initial_bda_3, vars)
        test_bda_3 = ubda_unfolding(initial_bda_3, vars)
        normalized_bda_3 = ubda_normalize(test_bda_3, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_3))
        self.assertTrue(simulate_and_compare(test_bda_3, normalized_bda_3, vars))

    def test_normalization_new_4(self):
        vars: int = 8
        initial_bda_4 = import_treeaut_from_vtf("../tests/normalization/newNormTest4.vtf")
        fill_dont_care_boxes(initial_bda_4, vars)
        test_bda_4 = ubda_unfolding(initial_bda_4, vars)
        normalized_bda_4 = ubda_normalize(test_bda_4, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_4))
        self.assertTrue(simulate_and_compare(test_bda_4, normalized_bda_4, vars))

    def test_normalization_new_4_loops(self):
        vars: int = 8
        initial_bda_4_loops = import_treeaut_from_vtf("../tests/normalization/newNormTest4-loops.vtf")
        fill_dont_care_boxes(initial_bda_4_loops, vars)
        test_bda_4_loops = ubda_unfolding(initial_bda_4_loops, vars)
        normalized_bda_4_loops = ubda_normalize(test_bda_4_loops, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_4_loops))
        self.assertTrue(simulate_and_compare(test_bda_4_loops, normalized_bda_4_loops, vars))

    def test_normalization_new_4_boxes(self):
        vars: int = 8
        initial_bda_4_boxes = import_treeaut_from_vtf("../tests/normalization/newNormTest4-boxes.vtf")
        fill_dont_care_boxes(initial_bda_4_boxes, vars)
        test_bda_4_boxes = ubda_unfolding(initial_bda_4_boxes, vars)
        normalized_bda_4_boxes = ubda_normalize(test_bda_4_boxes, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_4_boxes))
        self.assertTrue(simulate_and_compare(test_bda_4_boxes, normalized_bda_4_boxes, vars))

    def test_normalization_new_5(self):
        vars: int = 8
        initial_bda_5 = import_treeaut_from_vtf("../tests/normalization/newNormTest5.vtf")
        add_variables_fixpoint(initial_bda_5, vars)
        fill_dont_care_boxes(initial_bda_5, vars)
        test_bda_5 = ubda_unfolding(initial_bda_5, vars)
        normalized_bda_5 = ubda_normalize(test_bda_5, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_5))
        self.assertTrue(simulate_and_compare(test_bda_5, normalized_bda_5, vars))

    def test_normalization_new_6(self):
        vars: int = 8
        initial_bda_6 = import_treeaut_from_vtf("../tests/normalization/newNormTest6.vtf")
        fill_dont_care_boxes(initial_bda_6, vars)
        test_bda_6 = ubda_unfolding(initial_bda_6, vars)
        normalized_bda_6 = ubda_normalize(test_bda_6, create_var_order_list("x", vars))
        self.assertTrue(check_variable_overlap(normalized_bda_6))
        self.assertTrue(simulate_and_compare(test_bda_6, normalized_bda_6, vars))
