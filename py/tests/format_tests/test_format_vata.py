import unittest
import os

from formats.format_vtf import export_treeaut_to_vtf, import_treeaut_from_vtf
from apply.equality import tree_aut_equal
from tree_automata.functions.isomorphism import tree_aut_isomorphic
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_states_bfs
import tests.tree_automata_examples as ta


class TestVATAFormatImport(unittest.TestCase):
    def test_import_box_x(self):
        imported_treeaut: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxX.vtf")
        # print(imported_treeaut)
        edges = set([i for i in iterate_edges(imported_treeaut)])
        states = set([i for i in iterate_states_bfs(imported_treeaut)])
        self.assertEqual(len(edges), 3)
        self.assertSetEqual(set(["q0", "q1"]), states)
        self.assertSetEqual(set(imported_treeaut.roots), set(["q0"]))
        self.assertSetEqual(set(imported_treeaut.get_symbol_arity_dict().keys()), set(["LH", "Port_X"]))

    def test_random_box_import(self):
        test_unreachable_1: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf")
        test_unreachable_2: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf")
        test_unreachable_3: TTreeAut = import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf")

        edges_1 = set([i for i in iterate_edges(test_unreachable_1)])
        states_1 = set(test_unreachable_1.get_states())

        edges_2 = set([i for i in iterate_edges(test_unreachable_2)])
        states_2 = set(test_unreachable_2.get_states())

        edges_3 = set([i for i in iterate_edges(test_unreachable_3)])
        states_3 = set(test_unreachable_3.get_states())

        self.assertEqual(len(edges_1), 2)
        self.assertSetEqual(set(["q0", "q1"]), states_1)
        self.assertSetEqual(set(test_unreachable_1.roots), set(["q0"]))
        self.assertSetEqual(set(test_unreachable_1.get_symbol_arity_dict().keys()), set(["LH", "1"]))

        self.assertEqual(len(edges_2), 8)
        self.assertSetEqual(set(["q0", "q1", "q2", "q3", "q4"]), states_2)
        self.assertSetEqual(set(test_unreachable_2.roots), set(["q0"]))
        self.assertSetEqual(set(test_unreachable_2.get_symbol_arity_dict().keys()), set(["LH", "Port", "1"]))

        self.assertEqual(len(edges_3), 8)
        self.assertSetEqual(set(["q0", "q1", "q2", "q3", "q4"]), states_3)
        self.assertSetEqual(set(test_unreachable_3.roots), set(["q0"]))
        self.assertSetEqual(set(test_unreachable_3.get_symbol_arity_dict().keys()), set(["LH", "Port", "1"]))


class TestVATAFormatExport(unittest.TestCase):
    def test_isomorphism_after_vata_export_import(self):
        temp_path = "./temp_TestVATAFormatExport.vtf"

        export_treeaut_to_vtf(ta.box_l0, temp_path)
        imported_aut: TTreeAut = import_treeaut_from_vtf(temp_path)

        self.assertFalse(tree_aut_isomorphic(ta.box_l0, imported_aut) == {})
        self.assertTrue(tree_aut_equal(ta.box_l0, imported_aut))

        os.remove(temp_path)
