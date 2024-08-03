"""
[file] test_data.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Test automata/structures used in all_tests.py
"""

from ta_functions import *
from test_trees import *
from format_vtf import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# first argument is a list of all "root" states
# "leaf" states are recognized by having at least one transition which
# has an empty tuple at the end (descendants) -> "output edge"

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

box_catalogue = {
    "False": import_treeaut_from_vtf("../tests/boxes/box0.vtf"),
    "True": import_treeaut_from_vtf("../tests/boxes/box1.vtf"),
    "X": import_treeaut_from_vtf("../tests/boxes/boxX.vtf"),
    "L0": import_treeaut_from_vtf("../tests/boxes/boxL0.vtf"),
    "L1": import_treeaut_from_vtf("../tests/boxes/boxL1.vtf"),
    "H0": import_treeaut_from_vtf("../tests/boxes/boxH0.vtf"),
    "H1": import_treeaut_from_vtf("../tests/boxes/boxH1.vtf"),
    "LPort": import_treeaut_from_vtf("../tests/boxes/boxLPort.vtf"),
    "HPort": import_treeaut_from_vtf("../tests/boxes/boxHPort.vtf"),
    # redundant probably -> can be built using Hx, Lx combinations
    "IFF0": import_treeaut_from_vtf("../tests/boxes/IFF0.vtf"),
    "IFF1": import_treeaut_from_vtf("../tests/boxes/IFF1.vtf"),
    "IFFPort": import_treeaut_from_vtf("../tests/boxes/IFFPort.vtf"),
    "boxX": import_treeaut_from_vtf("../tests/boxes/boxX.vtf"),
    "boxL0": import_treeaut_from_vtf("../tests/boxes/boxL0.vtf"),
    "boxL1": import_treeaut_from_vtf("../tests/boxes/boxL1.vtf"),
    "boxH0": import_treeaut_from_vtf("../tests/boxes/boxH0.vtf"),
    "boxH1": import_treeaut_from_vtf("../tests/boxes/boxH1.vtf"),
    "boxLPort": import_treeaut_from_vtf("../tests/boxes/boxLPort.vtf"),
    "boxHPort": import_treeaut_from_vtf("../tests/boxes/boxHPort.vtf"),
}

box_X = box_catalogue["X"]
box_L0 = box_catalogue["L0"]
box_L1 = box_catalogue["L1"]
box_H0 = box_catalogue["H0"]
box_H1 = box_catalogue["H1"]
box_LPort = box_catalogue["LPort"]
box_HPort = box_catalogue["HPort"]

# output edge array for createPrefix()

output_edges_X = box_X.get_output_symbols()
output_edges_L0 = box_L0.get_output_symbols()
output_edges_L1 = box_L1.get_output_symbols()
output_edges_H0 = box_H0.get_output_symbols()
output_edges_H1 = box_H1.get_output_symbols()
output_edges_LPort = box_LPort.get_output_symbols()
output_edges_HPort = box_HPort.get_output_symbols()

# reachability and useless state removal test data
test_unreachable_1 = import_treeaut_from_vtf("../tests/special_cases/testUnreachable1.vtf")
test_unreachable_2 = import_treeaut_from_vtf("../tests/special_cases/testUnreachable2.vtf")
test_unreachable_3 = import_treeaut_from_vtf("../tests/special_cases/testUnreachable3.vtf")

test_nonempty_1 = import_treeaut_from_vtf("../tests/special_cases/testNonEmpty1.vtf")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

boxes_dict = {
    "boxX": box_X,
    "boxL0": box_L0,
    "boxL1": box_L1,
    "boxH0": box_H0,
    "boxH1": box_H1,
    "boxLPort": box_LPort,
    "boxHPort": box_HPort,
    "unionXL0": tree_aut_union(box_X, box_L0),
    "unionXL1": tree_aut_union(box_X, box_L1),
    "unionXH0": tree_aut_union(box_X, box_H0),
    "unionXH1": tree_aut_union(box_X, box_H1),
    "unionL0H0": tree_aut_union(box_L0, box_H0),
    "unionL0H1": tree_aut_union(box_L0, box_H1),
    "unionL0L1": tree_aut_union(box_L0, box_L1),
    "unionL1H0": tree_aut_union(box_L1, box_H0),
    "unionL1H1": tree_aut_union(box_L1, box_H1),
    "unionH0H1": tree_aut_union(box_H0, box_H1),
    "intersectionXL0": tree_aut_intersection(box_X, box_L0),
    "intersectionXL1": tree_aut_intersection(box_X, box_L1),
    "intersectionXH0": tree_aut_intersection(box_X, box_H0),
    "intersectionXH1": tree_aut_intersection(box_X, box_H1),
    "intersectionL0H0": tree_aut_intersection(box_L0, box_H0),
    "intersectionL0H1": tree_aut_intersection(box_L0, box_H1),
    "intersectionL0L1": tree_aut_intersection(box_L0, box_L1),
    "intersectionL1H0": tree_aut_intersection(box_L1, box_H0),
    "intersectionL1H1": tree_aut_intersection(box_L1, box_H1),
    "intersectionH0H1": tree_aut_intersection(box_H0, box_H1),
    "complementX": tree_aut_complement(box_X, full_alphabet),
    "complementL0": tree_aut_complement(box_L0, full_alphabet),
    "complementL1": tree_aut_complement(box_L1, full_alphabet),
    "complementH0": tree_aut_complement(box_H0, full_alphabet),
    "complementH1": tree_aut_complement(box_H1, full_alphabet),
    "complementLPort": tree_aut_complement(box_LPort, full_alphabet),
    "complementHPort": tree_aut_complement(box_HPort, full_alphabet),
    "determinizedX": tree_aut_determinization(box_X, full_alphabet),
    "determinizedL0": tree_aut_determinization(box_L0, full_alphabet),
    "determinizedL1": tree_aut_determinization(box_L1, full_alphabet),
    "determinizedH0": tree_aut_determinization(box_H0, full_alphabet),
    "determinizedH1": tree_aut_determinization(box_H1, full_alphabet),
    "determinizedLPort": tree_aut_determinization(box_LPort, full_alphabet),
    "determinizedHPort": tree_aut_determinization(box_HPort, full_alphabet),
    "Xsuffix": box_X.create_suffix(),
    "L0suffix": box_L0.create_suffix(),
    "L1suffix": box_L1.create_suffix(),
    "H0suffix": box_H0.create_suffix(),
    "H1suffix": box_H1.create_suffix(),
    "LPortsuffix": box_LPort.create_suffix(),
    "XprefixForL0": box_X.create_prefix(output_edges_L0),
    "XprefixForL1": box_X.create_prefix(output_edges_L1),
    "XprefixForH0": box_X.create_prefix(output_edges_H0),
    "XprefixForH1": box_X.create_prefix(output_edges_H0),
    "XprefixForLPort": box_X.create_prefix(output_edges_LPort),
    "XprefixForHPort": box_X.create_prefix(output_edges_HPort),
    "L0prefixForX": box_L0.create_prefix(output_edges_X),
    "L0prefixForL1": box_L0.create_prefix(output_edges_L1),
    "L0prefixForH0": box_L0.create_prefix(output_edges_H0),
    "L0prefixForH1": box_L0.create_prefix(output_edges_H0),
    "L0prefixForLPort": box_L0.create_prefix(output_edges_LPort),
    "L1prefixForX": box_L1.create_prefix(output_edges_X),
    "L1prefixForL0": box_L1.create_prefix(output_edges_L0),
    "L1prefixForH0": box_L1.create_prefix(output_edges_H0),
    "L1prefixForH1": box_L1.create_prefix(output_edges_H0),
    "L1prefixForLPort": box_L1.create_prefix(output_edges_LPort),
    "H0prefixForX": box_H0.create_prefix(output_edges_X),
    "H0prefixForL0": box_H0.create_prefix(output_edges_L0),
    "H0prefixForL1": box_H0.create_prefix(output_edges_L1),
    "H0prefixForH1": box_H0.create_prefix(output_edges_H0),
    "H0prefixForLPort": box_H0.create_prefix(output_edges_LPort),
    "H1prefixForX": box_H1.create_prefix(output_edges_X),
    "H1prefixForL0": box_H1.create_prefix(output_edges_L0),
    "H1prefixForL1": box_H1.create_prefix(output_edges_L1),
    "H1prefixForH0": box_H1.create_prefix(output_edges_H0),
    "H1prefixForLPort": box_H1.create_prefix(output_edges_LPort),
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

function_ptrs = {
    "match_tree_bottom_up": match_tree_bottom_up,
    "match_tree_top_down": match_tree_top_down,
    "tree_aut_union": tree_aut_union,
    "tree_aut_intersection": tree_aut_intersection,
    "tree_aut_determinization": tree_aut_determinization,
    "tree_aut_complement": tree_aut_complement,
    "non_empty_top_down": non_empty_top_down,
    "non_empty_bottom_up": non_empty_bottom_up,
    "reachable_top_down": reachable_top_down,
    "reachable_bottom_up": reachable_bottom_up,
    "removeUselessStates": remove_useless_states,
}

# End of file test_data.py
