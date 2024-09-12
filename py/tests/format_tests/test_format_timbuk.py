import unittest
import os

from formats.format_tmb import export_treeaut_to_tmb, import_treeaut_from_tmb
from apply.apply_testing import tree_aut_equal
from tree_automata.functions.isomorphism import tree_aut_isomorphic
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_states_bfs
import tests.tree_automata_examples as ta


class TestTimbukFormatImport(unittest.TestCase):
    def test_import_box_x(self):
        imported_treeaut: TTreeAut = import_treeaut_from_tmb("../tests/boxes/boxX.tmb")
        edges = set([i for i in iterate_edges(imported_treeaut)])
        states = set([i for i in iterate_states_bfs(imported_treeaut)])

        self.assertEqual(len(edges), 3)
        self.assertSetEqual(set(["q0", "q1"]), states)
        self.assertSetEqual(set(imported_treeaut.roots), set(["q0"]))
        self.assertSetEqual(set(imported_treeaut.get_symbol_arity_dict().keys()), set(["LH", "Port_X"]))

    def test_import_box_lport(self):
        imported_treeaut: TTreeAut = import_treeaut_from_tmb("../tests/boxes/boxLPort.tmb")
        edges = set([i for i in iterate_edges(imported_treeaut)])
        states = set(imported_treeaut.get_states())

        self.assertEqual(len(edges), 5)
        self.assertSetEqual(set(["v0", "v1", "v2"]), states)
        self.assertSetEqual(set(imported_treeaut.roots), set(["v0"]))
        self.assertSetEqual(
            set(imported_treeaut.get_symbol_arity_dict().keys()), set(["LH", "Port_LPort0", "Port_LPort1"])
        )


class TestTimbukFormatExport(unittest.TestCase):
    @unittest.skip  # find the bug in isomorphism checker or language equality
    def test_isomorphism_after_export_import(self):
        temp_path = "./temp_TestTimbukFormatExport.tmb"

        export_treeaut_to_tmb(ta.box_l0, temp_path)
        imported_aut: TTreeAut = import_treeaut_from_tmb(temp_path)
        print(imported_aut)
        print(ta.box_l0)
        print(tree_aut_isomorphic(ta.box_l0, imported_aut))
        print(tree_aut_equal(ta.box_l0, imported_aut))

        self.assertFalse(tree_aut_isomorphic(ta.box_l0, imported_aut) == {})

        os.remove(temp_path)
