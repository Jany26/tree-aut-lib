import unittest

from bdd.bdd_apply import apply_function
import tests.bdd_examples as bd


class TestBinaryDecisionDiagramApply(unittest.TestCase):
    # TODO: make some function to test certain variable assignments,
    # and then maybe test them in a loop or something
    # TODO: also create an expected result BDD and test for isomorphism
    def test_bdd_apply_small_example_or(self):
        bdd_new_or = apply_function("or", bd.bdd_3, bd.bdd_4, var_order=None)

    def test_bdd_apply_small_example_and(self):
        bdd_new_and = apply_function("and", bd.bdd_3, bd.bdd_4, var_order=None)
