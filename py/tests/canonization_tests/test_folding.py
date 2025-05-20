import unittest

from apply.abdd_apply_main import abdd_apply
from apply.abdd import convert_ta_to_abdd, import_abdd_from_abdd_file
from apply.abdd_node_cache import ABDDNodeCacheClass
from apply.box_algebra.apply_tables import BooleanOperation
from formats.format_vtf import import_treeaut_from_vtf
from apply.evaluation import compare_abdds_tas, compare_op_abdd
from canonization.folding_new_attempt import new_fold, divide_multivar_states
from tree_automata import TTreeAut, remove_useless_states
from bdd.bdd_to_treeaut import add_dont_care_boxes
from canonization.unfolding import ubda_unfolding
from canonization.folding import get_mapping, ubda_folding
from canonization.folding_helpers import get_maximal_mapping_fixed, port_to_state_mapping
from canonization.normalization import is_normalized, ubda_normalize
from experiments.simulation import simulate_and_compare
from tree_automata.var_manipulation import add_variables_bottom_up, check_variable_overlap
from helpers.string_manipulation import create_var_order_list
from helpers.utils import box_catalogue, box_orders


# NOTE: These tests are deprecated and from an old version of folding, which didn't work correctly
@unittest.skip
class TestUBDAFolding(unittest.TestCase):
    @unittest.skip  # not sure if testing the mapping is necessary
    def test_mapping_compare(self):
        bda1: TTreeAut = import_treeaut_from_vtf("../tests/reachability/1_bda.vtf")
        bda2: TTreeAut = import_treeaut_from_vtf("../tests/reachability/2_bda.vtf")

        test1a: TTreeAut = import_treeaut_from_vtf("../tests/reachability/1_intersectoid_a.vtf")
        test1b: TTreeAut = import_treeaut_from_vtf("../tests/reachability/1_intersectoid_b.vtf")
        test1c: TTreeAut = import_treeaut_from_vtf("../tests/reachability/1_intersectoid_c.vtf")
        test2a: TTreeAut = import_treeaut_from_vtf("../tests/reachability/2_intersectoid_a.vtf")
        test2b: TTreeAut = import_treeaut_from_vtf("../tests/reachability/2_intersectoid_b.vtf")
        # NOTE: get_mapping() from canonization.folding is the final working version
        # These tests should be redone to specifically compare against particular mappings for given (U)BDAs.
        self.assertDictEqual(
            get_maximal_mapping_fixed(test1a, bda1, port_to_state_mapping(test1a)), get_mapping(test1a, bda1)
        )
        self.assertDictEqual(
            get_maximal_mapping_fixed(test1b, bda1, port_to_state_mapping(test1b)), get_mapping(test1b, bda1)
        )
        self.assertDictEqual(
            get_maximal_mapping_fixed(test1c, bda1, port_to_state_mapping(test1c)), get_mapping(test1c, bda1)
        )
        self.assertDictEqual(
            get_maximal_mapping_fixed(test2a, bda2, port_to_state_mapping(test2a)), get_mapping(test2a, bda2)
        )
        self.assertDictEqual(
            get_maximal_mapping_fixed(test2b, bda2, port_to_state_mapping(test2b)), get_mapping(test2b, bda2)
        )

    def test_folding_compare_1(self):
        boxorder = box_orders["full"]
        var_count = 4
        var_order = create_var_order_list("", var_count + 1)
        treeaut2 = import_treeaut_from_vtf("../tests/folding/foldingTest1.vtf")
        unfolded2 = ubda_unfolding(add_dont_care_boxes(treeaut2, var_count), 5)
        add_variables_bottom_up(unfolded2, var_count)
        normalized2 = remove_useless_states(ubda_normalize(unfolded2, var_order))
        add_variables_bottom_up(normalized2, var_count)
        normalized2.reformat_keys()
        normalized2.reformat_states()
        folded2 = remove_useless_states(ubda_folding(normalized2, boxorder, var_count + 1))
        new_unfolded2 = ubda_unfolding(folded2, 5)
        add_variables_bottom_up(new_unfolded2, var_count)
        self.assertTrue(simulate_and_compare(unfolded2, new_unfolded2, var_count))

    def test_folding_compare_2(self):  #  testcase from 2023-08-03 consultation
        ta = import_treeaut_from_vtf("../tests/folding/foldingTest2-ta.vtf")
        box = import_treeaut_from_vtf("../tests/folding/foldingTest2-box.vtf")
        box.name = "test"
        box_catalogue["test"] = box
        number_of_variables = 8

        folded = ubda_folding(ta, ["test"], number_of_variables, verbose=False)
        folded.reformat_keys()
        folded.reformat_states()
        self.assertEqual(folded.count_edges(), 4)
        self.assertEqual(folded.count_boxes(), 4)
        self.assertEqual(len(folded.get_states()), 3)

    def test_folding_compare_3(self):
        boxorder = box_orders["cesr"]
        var_count = 5  # < x1, x2, x3, x4, x5 >
        var_order = create_var_order_list("", var_count + 1)

        treeaut1 = import_treeaut_from_vtf("../tests/folding/folding-error-1.vtf")
        unfolded1 = ubda_unfolding(add_dont_care_boxes(treeaut1, var_count), 6)
        normalized1 = remove_useless_states(ubda_normalize(unfolded1, var_order))
        add_variables_bottom_up(normalized1, var_count)
        normalized1.reformat_keys()
        normalized1.reformat_states()
        self.assertTrue(simulate_and_compare(unfolded1, normalized1, var_count))  # pass
        self.assertTrue(check_variable_overlap(normalized1))  # pass
        folded1 = remove_useless_states(ubda_folding(normalized1, boxorder, var_count))
        new_unfolded1 = ubda_unfolding(folded1, 6)
        add_variables_bottom_up(new_unfolded1, var_count)

        x = simulate_and_compare(unfolded1, new_unfolded1, var_count, debug=True)
        self.assertTrue(x)

    def test_folding_compare_4(self):
        boxorder = box_orders["full"]
        var_count = 5  # < x1, x2, x3, x4, x5 >
        var_order = create_var_order_list("", var_count + 1)

        treeaut1 = import_treeaut_from_vtf("../tests/folding/folding-error-6.vtf")
        # NOTE: unfolding produces a different result when using the new definition of the "don't care" box X
        unfolded1 = ubda_unfolding(add_dont_care_boxes(treeaut1, var_count), 6)
        # TODO: make a better (fixpoint) algorithm for variable fill where applicable

        normalized1 = ubda_normalize(unfolded1, var_order)
        print(normalized1)
        normalized1 = remove_useless_states(normalized1)
        add_variables_bottom_up(normalized1, var_count)
        normalized1.reformat_keys()
        normalized1.reformat_states()
        self.assertTrue(simulate_and_compare(unfolded1, normalized1, var_count))  # pass
        self.assertTrue(is_normalized(normalized1))  # fail
        folded1 = ubda_folding(normalized1, boxorder, var_count + 1)
        folded1 = remove_useless_states(folded1)
        new_unfolded1 = ubda_unfolding(folded1, 6)
        add_variables_bottom_up(new_unfolded1, var_count)
        self.assertTrue(simulate_and_compare(unfolded1, new_unfolded1, var_count))
