from tree_automata import TTreeAut
from tree_automata.tree_node import TTreeNode, convert_string_to_tree
from formats.format_vtf import import_treeaut_from_vtf

PATH_TO_BOXES = "../tests/boxes"
PATH_TO_TDD_BOXES = "../tests/boxes-topdowndet"  # tdd = top-down deterministic

full_alphabet = {
    "LH": 2,
    "0": 0,
    "1": 0,
    "Port_X": 0,
    "Port_L0": 0,
    "Port_L1": 0,
    "Port_H0": 0,
    "Port_H1": 0,
    "Port_LPort0": 0,
    "Port_LPort1": 0,
    "Port_HPort0": 0,
    "Port_HPort1": 0,
}

box_x: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxX.vtf")
box_l0: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxL0.vtf")
box_l1: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxL1.vtf")
box_h0: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxH0.vtf")
box_h1: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxH1.vtf")
box_lport: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxLPort.vtf")
box_hport: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_BOXES}/boxHPort.vtf")

tdd_box_x: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetX.vtf")
tdd_box_l0: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetL0.vtf")
tdd_box_l1: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetL1.vtf")
tdd_box_h0: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetH0.vtf")
tdd_box_h1: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetH1.vtf")
tdd_box_lport: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetLPort.vtf")
tdd_box_hport: TTreeAut = import_treeaut_from_vtf(f"{PATH_TO_TDD_BOXES}/tddetHPort.vtf")
