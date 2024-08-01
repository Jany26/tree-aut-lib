"""
[file] test_trees.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Some basic trees for testing (and helper functions)
"""

from ta_functions import *
import re

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS FOR TESTING PURPOSES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def convert_string_to_tree(string: str) -> TTreeNode:

    # Does not cover edge cases! (e.g. wrong string structure)
    def get_node_from_string(string: str):
        string = string.strip()
        node_name = re.match("^[\w]+", string).group()
        string = string.lstrip(str(node_name))
        node = TTreeNode(node_name)
        return node, string

    # Recursive function to generate a tree from a structured string
    # XYZ [...] = node with list of children following (can be nested)
    # [ node1 ; node2 [...] ; node3 ; ... ] = list of children of a previous node
    def build_tree_from_string(current_node: TTreeNode, string: str) -> TTreeNode:
        string = string.strip()  # skipping whitespaces

        # empty string - ending recursion
        if len(string) == 0:
            return current_node

        # starting children generation (down a level)
        if string.startswith("["):
            node, string = get_node_from_string(string[1:])
            current_node.connect_child(node)
            return build_tree_from_string(node, string)

        # continuing children generation (same level)
        elif string.startswith(";"):
            node, string = get_node_from_string(string[1:])
            current_node.parent.connect_child(node)
            return build_tree_from_string(node, string)

        # ending children generation - returning to a parent (up a level)
        elif string.startswith("]"):
            return build_tree_from_string(current_node.parent, string[1:])

        # start of a string - root creation (initial case - no special character at the beginning)
        else:
            root, string = get_node_from_string(string)
            return build_tree_from_string(root, string)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    return build_tree_from_string(None, string)


# Reverse of the buildTreeFromString function
# Creates a concise (string) representation of a tree from its structure
def convert_tree_to_string(node: TTreeNode) -> str:
    if len(node.children) == 0:
        return str(node.value)
    else:
        temp = node.value + "["
        for i in range(len(node.children)):
            temp += str(convert_tree_to_string(node.children[i]))
            if i < len(node.children) - 1:
                temp += ";"
        temp += "]"
        return temp


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTING DATA - TREES (represented by structured strings)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

X_tree_example1 = "LH[Port_X;Port_X]"
X_tree_example2 = "LH[LH[LH[Port_X;Port_X];Port_X];LH[Port_X;LH[Port_X;Port_X]]]"
X_tree_example3 = "LH[LH[Port_X;Port_X];LH[LH[LH[Port_X;Port_X];LH[Port_X;Port_X]];LH[Port_X;Port_X]]]"

L0_tree_example1 = "LH[0;LH[0;Port_L0]]"
L0_tree_example2 = "LH[0;LH[LH[LH[0;0];LH[0;0]];LH[0;Port_L0]]]"
L0_tree_example3 = "LH[LH[LH[0;0];LH[0;0]];LH[LH[0;0];LH[0;Port_L0]]]"
L0_tree_example4 = "LH[0;Port_L0]"

L1_tree_example1 = "LH[1;LH[1;Port_L1]]"
L1_tree_example2 = "LH[1;LH[LH[LH[1;1];LH[1;1]];LH[1;Port_L1]]]"
L1_tree_example3 = "LH[LH[LH[1;1];LH[1;1]];LH[LH[1;1];LH[1;Port_L1]]]"
L1_tree_example4 = "LH[1;Port_L1]"

H0_tree_example1 = "LH[LH[Port_H0;0];0]"
H0_tree_example2 = "LH[LH[LH[Port_H0;0];LH[LH[0;0];LH[0;0]]];0]"
H0_tree_example3 = "LH[LH[LH[Port_H0;0];LH[0;0]];LH[LH[0;0];LH[0;0]]]"
H0_tree_example4 = "LH[Port_H0;0]"

H1_tree_example1 = "LH[LH[Port_H1;1];1]"
H1_tree_example2 = "LH[LH[LH[Port_H1;1];LH[LH[1;1];LH[1;1]]];1]"
H1_tree_example3 = "LH[LH[LH[Port_H1;1];LH[1;1]];LH[LH[1;1];LH[1;1]]]"
H1_tree_example4 = "LH[Port_H1;1]"

test_tree_dict = {
    "treeXtest1": convert_string_to_tree(X_tree_example1),
    "treeXtest2": convert_string_to_tree(X_tree_example2),
    "treeXtest3": convert_string_to_tree(X_tree_example3),

    "treeL0test1": convert_string_to_tree(L0_tree_example1),
    "treeL0test2": convert_string_to_tree(L0_tree_example2),
    "treeL0test3": convert_string_to_tree(L0_tree_example3),
    "treeL0test4": convert_string_to_tree(L0_tree_example4),

    "treeL1test1": convert_string_to_tree(L1_tree_example1),
    "treeL1test2": convert_string_to_tree(L1_tree_example2),
    "treeL1test3": convert_string_to_tree(L1_tree_example3),
    "treeL1test4": convert_string_to_tree(L1_tree_example4),

    "treeH0test1": convert_string_to_tree(H0_tree_example1),
    "treeH0test2": convert_string_to_tree(H0_tree_example2),
    "treeH0test3": convert_string_to_tree(H0_tree_example3),
    "treeH0test4": convert_string_to_tree(H0_tree_example4),

    "treeH1test1": convert_string_to_tree(H1_tree_example1),
    "treeH1test2": convert_string_to_tree(H1_tree_example2),
    "treeH1test3": convert_string_to_tree(H1_tree_example3),
    "treeH1test4": convert_string_to_tree(H1_tree_example4)
}

# End of file test_trees.py
