"""
[file] utils.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] some helper utilities used throughout other modules
"""

import sys
from typing import Optional

from tree_automata.automaton import TTreeAut
from formats.format_vtf import import_treeaut_from_vtf


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


bdd_box_order: list[str] = ["X"]
zbdd_box_order: list[str] = ["H0"]
tbdd_box_order: list[str] = ["X", "H0"]
cbdd_box_order: list[str] = ["X", "HPort"]
czdd_box_order: list[str] = ["H0", "X"]
esr_box_order: list[str] = ["L0", "H0", "X"]
full_box_order: list[str] = ["L0", "H0", "L1", "H1", "X", "LPort", "HPort"]
cesr_box_order: list[str] = ["L0", "H0", "L1", "H1", "X"]

box_orders: dict[str, list[str]] = {
    "bdd": bdd_box_order,
    "zbdd": zbdd_box_order,
    "tbdd": tbdd_box_order,
    "cbdd": cbdd_box_order,
    "czdd": czdd_box_order,
    "esr": esr_box_order,
    "cesr": cesr_box_order,
    "full": full_box_order,
}

box_false: TTreeAut = import_treeaut_from_vtf("../tests/boxes/box0.vtf")
box_true: TTreeAut = import_treeaut_from_vtf("../tests/boxes/box1.vtf")
box_x: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxX.vtf")
box_l0: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxL0.vtf")
box_l1: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxL1.vtf")
box_lport: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxLPort.vtf")
box_h0: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxH0.vtf")
box_h1: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxH1.vtf")
box_hport: TTreeAut = import_treeaut_from_vtf("../tests/boxes/boxHPort.vtf")

box_arities: dict[Optional[str], int] = {
    None: 1,
    "X": 1,
    "L0": 1,
    "L1": 1,
    "H0": 1,
    "H1": 1,
    "LPort": 2,
    "HPort": 2,
}

box_catalogue: dict[str, TTreeAut] = {
    "0": box_false,
    "1": box_true,
    "False": box_false,
    "True": box_true,
    "X": box_x,
    "L0": box_l0,
    "L1": box_l1,
    "H0": box_h0,
    "H1": box_h1,
    "LPort": box_lport,
    "HPort": box_hport,
    "boxX": box_x,
    "boxL0": box_l0,
    "boxL1": box_l1,
    "boxH0": box_h0,
    "boxH1": box_h1,
    "boxLPort": box_lport,
    "boxHPort": box_hport,
}
