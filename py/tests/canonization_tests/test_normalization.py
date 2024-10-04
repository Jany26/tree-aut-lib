import unittest

from formats.format_vtf import import_treeaut_from_vtf
from canonization.normalization import ubda_normalize, is_normalized
from tree_automata.functions.trimming import remove_useless_states
from helpers.string_manipulation import create_var_order_list
from canonization.unfolding import ubda_unfolding


# TODO: update detailed normalization tests
class TestUBDANormalization(unittest.TestCase):
    def test_normalization_after_unfolding(self):
        # failing for the same reason as the test_normalization_detailed_3
        test_bda_1 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest1.vtf")
        test_bda_2 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest2.vtf")
        test_bda_3 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest3.vtf")
        test_bda_4 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest4.vtf")
        test_bda_5 = import_treeaut_from_vtf("../tests/unfolding/unfoldingTest5.vtf")

        variables = create_var_order_list("x", 8)

        unfolded_bda_1 = ubda_unfolding(test_bda_1)
        unfolded_bda_2 = ubda_unfolding(test_bda_2)
        unfolded_bda_3 = ubda_unfolding(test_bda_3)
        unfolded_bda_4 = ubda_unfolding(test_bda_4)
        unfolded_bda_5 = ubda_unfolding(test_bda_5)

        normalized_bda_1 = remove_useless_states(ubda_normalize(unfolded_bda_1, variables))
        normalized_bda_2 = remove_useless_states(ubda_normalize(unfolded_bda_2, variables))
        normalized_bda_3 = remove_useless_states(ubda_normalize(unfolded_bda_3, variables))
        normalized_bda_4 = remove_useless_states(ubda_normalize(unfolded_bda_4, variables))
        normalized_bda_5 = remove_useless_states(ubda_normalize(unfolded_bda_5, variables))

        self.assertTrue(is_normalized(normalized_bda_1))
        self.assertTrue(is_normalized(normalized_bda_2))
        self.assertTrue(is_normalized(normalized_bda_3))
        self.assertTrue(is_normalized(normalized_bda_4))
        self.assertTrue(is_normalized(normalized_bda_5))

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
        unfolded = ubda_unfolding(initial)
        unfolded.reformat_keys()
        unfolded.reformat_states()

        normalized = ubda_normalize(unfolded, create_var_order_list("x", 4))
        self.assertTrue(is_normalized(normalized))
        states = set(["{q0,q1,q2,q3}", "{q1,q2,q3}", "{q3,q4,q5}", "{q6}", "{q7}"])
        # self.assertSetEqual(set(normalized.get_states()), states)
        self.assertListEqual(normalized.get_var_occurence(), [1, 3, 4, 4])

    def test_normalization_detailed_2(self):
        initial = import_treeaut_from_vtf("../tests/normalization/newNormTest5.vtf")
        states = set(["{q1}", "{q3}", "{q2,q4}", "{q2}", "{q6}", "{q5}", "{q7}"])

        normalized = ubda_normalize(initial, create_var_order_list("x", 7))
        self.assertTrue(is_normalized(normalized))
        self.assertSetEqual(set(normalized.get_states()), states)
        self.assertListEqual(normalized.get_var_occurence(), [1, 7, 7])

    def test_normalization_detailed_3(self):
        # failing for the same reason as the test_normalization_after_unfolding
        # possible reasons:
        # - too many macrostate tuples are considered (probably not)
        # - variable saturation before normalization is not good enough (TODO)
        # - merging variable and non-variable transitions (or not differentiating between them) - see log
        #       - maybe 'force' a variable in case of non-self-looping transitions

        states = set(
            [
                "{q0}",
                "{q5,q12}",
                "{q13,q14,q16}",
                "{q9,q14}",
                "{q11,q12,q15}",
                "{q1,q3,q7}",
                "{q4,q8,q10}",
                "{q8}",
                "{q6}",
                "{q3,q6,q7}",
                "{q2,q4,q10}",
                "{q6,q8}",
            ]
        )
        initial = import_treeaut_from_vtf("../tests/normalization/newNormTest4-loops.vtf")
        unfolded = ubda_unfolding(initial)
        unfolded.reformat_keys()
        unfolded.reformat_states()

        normalized = ubda_normalize(unfolded, create_var_order_list("x", 9))
        self.assertTrue(is_normalized(normalized))
        self.assertSetEqual(set(normalized.get_states()), states)
        self.assertListEqual(normalized.get_var_occurence(), [1, 4, 6, 9, 9])
