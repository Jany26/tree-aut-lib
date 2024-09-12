import copy
import unittest

from tree_automata.functions.helpers import generate_possible_children
from tree_automata.functions.match_tree import match_tree_top_down
from tree_automata import TTreeAut

import tests.tree_automata_examples as ta
import tests.tree_node_examples as tn


class TestTreeAutomatonGetOutputStates(unittest.TestCase):
    def test_get_output_states_x(self):
        x_output_states = set(["q1"])
        result = set(ta.box_x.get_output_states())
        self.assertSetEqual(result, x_output_states)

    def test_get_output_states_h1(self):
        h1_output_states = set(["u1", "u2"])
        result = set(ta.box_h1.get_output_states())
        self.assertSetEqual(result, h1_output_states)


class TestTreeAutomatonGetArityDict(unittest.TestCase):
    def test_arity_dict_x(self):
        x_arity_dict: dict[str, int] = {"LH": 2, "Port_X": 0}
        result = ta.box_x.get_symbol_arity_dict()
        self.assertDictEqual(result, x_arity_dict)

    def test_arity_dict_l0(self):
        l0_arity_dict: dict[str, int] = {"LH": 2, "0": 0, "Port_L0": 0}
        result = ta.box_l0.get_symbol_arity_dict()
        self.assertDictEqual(result, l0_arity_dict)

    def test_arity_dict_l1(self):
        l1_arity_dict: dict[str, int] = {"LH": 2, "1": 0, "Port_L1": 0}
        result = ta.box_l1.get_symbol_arity_dict()
        self.assertDictEqual(result, l1_arity_dict)

    def test_arity_dict_h0(self):
        h0_arity_dict: dict[str, int] = {"LH": 2, "Port_H0": 0, "0": 0}
        result = ta.box_h0.get_symbol_arity_dict()
        self.assertDictEqual(result, h0_arity_dict)

    def test_arity_dict_h1(self):
        h1_arity_dict: dict[str, int] = {"LH": 2, "Port_H1": 0, "1": 0}
        result = ta.box_h1.get_symbol_arity_dict()
        self.assertDictEqual(result, h1_arity_dict)

    def test_arity_dict_lport(self):
        lport_arity_dict: dict[str, int] = {"LH": 2, "Port_LPort0": 0, "Port_LPort1": 0}
        result = ta.box_lport.get_symbol_arity_dict()
        self.assertDictEqual(result, lport_arity_dict)

    def test_arity_dict_hport(self):
        hport_arity_dict: dict[str, int] = {"LH": 2, "Port_HPort0": 0, "Port_HPort1": 0}
        result = ta.box_hport.get_symbol_arity_dict()
        self.assertDictEqual(result, hport_arity_dict)


class TestTreeAutomatonRemoveState(unittest.TestCase):
    def test_remove_state_from_l0(self):
        test_automaton: TTreeAut = copy.deepcopy(ta.box_h0)
        test_automaton.remove_state("r2")

        result_1 = match_tree_top_down(test_automaton, tn.l0_test_tree_1)
        result_2 = match_tree_top_down(test_automaton, tn.l0_test_tree_2)
        result_3 = match_tree_top_down(test_automaton, tn.l0_test_tree_3)
        result_4 = match_tree_top_down(test_automaton, tn.l0_test_tree_4)

        self.assertFalse(result_1)
        self.assertFalse(result_2)
        self.assertFalse(result_3)
        self.assertFalse(result_4)

    def test_remove_state_from_l1(self):
        test_automaton: TTreeAut = copy.deepcopy(ta.box_l1)
        test_automaton.remove_state("s0")

        result_1 = match_tree_top_down(test_automaton, tn.l1_test_tree_1)
        result_2 = match_tree_top_down(test_automaton, tn.l1_test_tree_2)
        result_3 = match_tree_top_down(test_automaton, tn.l1_test_tree_3)
        result_4 = match_tree_top_down(test_automaton, tn.l1_test_tree_4)

        self.assertFalse(result_1)
        self.assertFalse(result_2)
        self.assertFalse(result_3)
        self.assertFalse(result_4)


class TestTreeAutomatonGenerateTuples(unittest.TestCase):
    def test_generate_possible_children(self):
        test_1 = generate_possible_children("q0", ["q0", "q1", "q2"], 3)
        test_2 = generate_possible_children("q0", ["q0", "q1"], 3)
        test_3 = generate_possible_children("q0", ["q0", "q1"], 2)
        test_4 = generate_possible_children("q0", ["q0", "q1", "q2", "q3", "q4"], 3)
        test_5 = generate_possible_children("q0", ["q0", "q1"], 4)

        self.assertEqual(len(test_1), 19)
        self.assertEqual(len(test_2), 7)
        self.assertEqual(len(test_3), 3)
        self.assertEqual(len(test_4), 61)
        self.assertEqual(len(test_5), 15)


if __name__ == "__main__":
    unittest.main()
