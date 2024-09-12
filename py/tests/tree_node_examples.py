from tree_automata.tree_node import TTreeNode, convert_string_to_tree


x_test_tree_1: TTreeNode = convert_string_to_tree("LH[Port_X;Port_X]")
x_test_tree_2: TTreeNode = convert_string_to_tree("LH[LH[LH[Port_X;Port_X];Port_X];LH[Port_X;LH[Port_X;Port_X]]]")
x_test_tree_3: TTreeNode = convert_string_to_tree(
    "LH[LH[Port_X;Port_X];LH[LH[LH[Port_X;Port_X];LH[Port_X;Port_X]];LH[Port_X;Port_X]]]"
)

l0_test_tree_1: TTreeNode = convert_string_to_tree("LH[0;LH[0;Port_L0]]")
l0_test_tree_2: TTreeNode = convert_string_to_tree("LH[0;LH[LH[LH[0;0];LH[0;0]];LH[0;Port_L0]]]")
l0_test_tree_3: TTreeNode = convert_string_to_tree("LH[LH[LH[0;0];LH[0;0]];LH[LH[0;0];LH[0;Port_L0]]]")
l0_test_tree_4: TTreeNode = convert_string_to_tree("LH[0;Port_L0]")

l1_test_tree_1: TTreeNode = convert_string_to_tree("LH[1;LH[1;Port_L1]]")
l1_test_tree_2: TTreeNode = convert_string_to_tree("LH[1;LH[LH[LH[1;1];LH[1;1]];LH[1;Port_L1]]]")
l1_test_tree_3: TTreeNode = convert_string_to_tree("LH[LH[LH[1;1];LH[1;1]];LH[LH[1;1];LH[1;Port_L1]]]")
l1_test_tree_4: TTreeNode = convert_string_to_tree("LH[1;Port_L1]")

h0_test_tree_1: TTreeNode = convert_string_to_tree("LH[LH[Port_H0;0];0]")
h0_test_tree_2: TTreeNode = convert_string_to_tree("LH[LH[LH[Port_H0;0];LH[LH[0;0];LH[0;0]]];0]")
h0_test_tree_3: TTreeNode = convert_string_to_tree("LH[LH[LH[Port_H0;0];LH[0;0]];LH[LH[0;0];LH[0;0]]]")
h0_test_tree_4: TTreeNode = convert_string_to_tree("LH[Port_H0;0]")

h1_test_tree_1: TTreeNode = convert_string_to_tree("LH[LH[Port_H1;1];1]")
h1_test_tree_2: TTreeNode = convert_string_to_tree("LH[LH[LH[Port_H1;1];LH[LH[1;1];LH[1;1]]];1]")
h1_test_tree_3: TTreeNode = convert_string_to_tree("LH[LH[LH[Port_H1;1];LH[1;1]];LH[LH[1;1];LH[1;1]]]")
h1_test_tree_4: TTreeNode = convert_string_to_tree("LH[Port_H1;1]")
