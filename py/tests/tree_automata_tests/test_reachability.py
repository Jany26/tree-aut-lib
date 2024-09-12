import unittest

from formats.format_vtf import import_treeaut_from_vtf
from tree_automata.functions.reachability import reachable_bottom_up, reachable_top_down

import tests.tree_automata_examples as ta


class TestTreeAutomataReachability(unittest.TestCase):
    def test_reachability_top_down(self):
        test_1_result = reachable_top_down(import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf"))
        test_2_result = reachable_top_down(import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf"))
        test_3_result = reachable_top_down(import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf"))
        test_l0_result = reachable_top_down(ta.box_l0)

        self.assertSetEqual(set(test_1_result), set(["q0", "q1"]))
        self.assertSetEqual(set(test_2_result), set(["q0", "q1", "q2", "q3"]))
        self.assertSetEqual(set(test_3_result), set(["q0", "q1", "q2", "q3"]))
        self.assertSetEqual(set(test_l0_result), set(ta.box_l0.get_states()))

    def test_reachability_bottom_up(self):
        test_1_result = reachable_bottom_up(import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf"))
        test_2_result = reachable_bottom_up(import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf"))
        test_3_result = reachable_bottom_up(import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf"))
        test_l0_result = reachable_bottom_up(ta.box_l0)

        self.assertSetEqual(set(test_1_result), set(["q1"]))
        self.assertSetEqual(set(test_2_result), set(["q0", "q1", "q2", "q3"]))
        self.assertSetEqual(set(test_3_result), set(["q0", "q1", "q2", "q3"]))
        self.assertSetEqual(set(test_l0_result), set(ta.box_l0.get_states()))
