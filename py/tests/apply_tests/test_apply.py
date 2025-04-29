import unittest

from apply.abdd import convert_ta_to_abdd
from apply.abdd_apply_main import abdd_apply
from apply.abdd_node_cache import ABDDNodeCacheClass
from apply.box_algebra.apply_tables import BooleanOperation
from apply.evaluation import compare_abdds_tas, compare_op_abdd
from canonization.folding_new_attempt import divide_multivar_states, new_fold
from canonization.normalization import ubda_normalize
from canonization.unfolding import ubda_unfolding
from experiments.simulation import simulate_and_compare
from formats.format_vtf import import_treeaut_from_vtf
from helpers.string_manipulation import create_var_order_list


class TestABDDApply(unittest.TestCase):
    def test_simple_test_1(self):
        varmax = 11
        ncache = ABDDNodeCacheClass()
        ta = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-1.vtf")
        abdd = convert_ta_to_abdd(ta, ncache, var_count=10)
        result = abdd.convert_to_treeaut_obj()
        unfolded = ubda_unfolding(result, varmax)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax), verbose=False)
        normalized.reformat_keys()
        normalized.reformat_states()

        self.assertTrue(compare_abdds_tas(abdd, unfolded))
        self.assertTrue(compare_abdds_tas(abdd, normalized))
        self.assertTrue(compare_abdds_tas(unfolded, normalized))

    def test_simple_test_2(self):
        varmax = 11
        ncache = ABDDNodeCacheClass()
        ta = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-2.vtf")
        abdd = convert_ta_to_abdd(ta, ncache, var_count=10)
        result = abdd.convert_to_treeaut_obj()
        unfolded = ubda_unfolding(result, varmax)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax))

        self.assertTrue(compare_abdds_tas(abdd, unfolded))
        self.assertTrue(compare_abdds_tas(abdd, normalized))
        self.assertTrue(compare_abdds_tas(unfolded, normalized))

    def test_simple_test_and(self):
        varmax = 10
        ncache = ABDDNodeCacheClass()
        ta1 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-1.vtf")
        ta2 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-2.vtf")
        abdd1 = convert_ta_to_abdd(ta1, ncache, var_count=varmax)
        abdd2 = convert_ta_to_abdd(ta2, ncache, var_count=varmax)
        result = abdd_apply(BooleanOperation.AND, abdd1, abdd2, ncache, maxvar=10)
        ncache.refresh_nodes()
        result_ta = result.convert_to_treeaut_obj()
        unfolded = ubda_unfolding(result_ta, varmax + 1)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax + 1), verbose=False)
        normalized.reformat_keys()
        normalized.reformat_states()

        self.assertTrue(compare_abdds_tas(result, unfolded))
        self.assertTrue(compare_abdds_tas(result, normalized))
        self.assertTrue(simulate_and_compare(unfolded, normalized, varmax + 1))
        self.assertTrue(compare_op_abdd(abdd1, abdd2, BooleanOperation.AND, result))

    def test_simple_test_or(self):
        varmax = 10
        ncache = ABDDNodeCacheClass()
        ta1 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-1.vtf")
        ta2 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-2.vtf")
        abdd1 = convert_ta_to_abdd(ta1, ncache, var_count=varmax)
        abdd2 = convert_ta_to_abdd(ta2, ncache, var_count=varmax)
        result = abdd_apply(BooleanOperation.OR, abdd1, abdd2, ncache, maxvar=10)
        ncache.refresh_nodes()
        self.assertTrue(compare_op_abdd(abdd1, abdd2, BooleanOperation.OR, result))
        result_ta = result.convert_to_treeaut_obj()
        unfolded = ubda_unfolding(result_ta, varmax + 1)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax + 1))
        normalized.reformat_keys()
        normalized.reformat_states()
        self.assertTrue(compare_abdds_tas(result, unfolded))
        self.assertTrue(compare_abdds_tas(result, normalized))
        self.assertTrue(simulate_and_compare(unfolded, normalized, varmax + 1))

    def test_simple_test_xor(self):
        varmax = 10
        ncache = ABDDNodeCacheClass()
        ta1 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-1.vtf")
        ta2 = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/simple-input-2.vtf")
        abdd1 = convert_ta_to_abdd(ta1, ncache, var_count=varmax)
        abdd2 = convert_ta_to_abdd(ta2, ncache, var_count=varmax)
        result = abdd_apply(BooleanOperation.XOR, abdd1, abdd2, ncache, maxvar=10)
        ncache.refresh_nodes()
        result_ta = result.convert_to_treeaut_obj()
        unfolded = ubda_unfolding(result_ta, varmax + 1)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax + 1), fix=True)
        normalized.reformat_keys()
        normalized.reformat_states()
        self.assertTrue(compare_abdds_tas(result, unfolded))
        self.assertTrue(compare_abdds_tas(result, normalized))
        self.assertTrue(simulate_and_compare(unfolded, normalized, varmax + 1))
        self.assertTrue(compare_op_abdd(abdd1, abdd2, BooleanOperation.XOR, result))

    def test_simple_multiroot(self):
        varmax = 10
        ncache = ABDDNodeCacheClass()
        multiroot_aut = import_treeaut_from_vtf("../tests/apply/ta-to-abdd-conversion/multiroot-example.vtf")
        multiroot_abdd = convert_ta_to_abdd(multiroot_aut, ncache, var_count=10)
        unfolded = ubda_unfolding(multiroot_aut, varmax + 1)
        normalized = ubda_normalize(unfolded, create_var_order_list("", varmax + 1))
        self.assertTrue(compare_abdds_tas(multiroot_abdd, unfolded))
        self.assertTrue(compare_abdds_tas(multiroot_abdd, normalized))
        self.assertTrue(simulate_and_compare(unfolded, normalized, varmax + 1))
