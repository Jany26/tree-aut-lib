from optparse import Option
from typing import Generator, Optional
import re


class TTreeNode:
    """
    [class description]
    Implementation of an n-ary tree node class.
    Language of a tree automaton is made up of trees.
    Each tree consists of nodes.
    Since we mainly focus on binary decision diagrams and languages of binary nodes,
    the nodes will be mostly binary (or in case of leaf nodes, "null-ary").
    Root node can be recognized with parent node set to 'None',
    Leaf nodes have no child nodes (node.children == []).
    Inner and leaf nodes have a parent, when connected using add_child() and connect_child() methods.

    [attributes]
    'value' = what is in the node
    'parent' = if None, then the node is a root
    'children' = since trees can be n-arylist
    """

    def __init__(self, value):
        self.value: str = value
        self.parent: Optional[TTreeNode] = None
        self.children: list[TTreeNode] = []
        self.depth: int = 0

    # TODO pretty print of a tree
    def __repr__(self):
        # vertical space # of lines => # of leaves + 3 * (# of leaves - 1)
        # if 4 leaves -> 3 in-between spaces
        # 1 in between space => 3 lines if untight
        #                    => 1 line if untight

        # length of 1 line => depth of the tree + spaces in between
        # one tree node will be long max_length characters

        # so we need to precompute:
        # max_depth, number_of_leaves, longest_nodename
        # high nodes (true branch) will be up
        # low nodes (false branch) will be down

        # we use postorder DFS traversal in reverse order of child nodes (from 1 down to 0)
        pass

    def print_node(self, offset: int = 0) -> None:
        """
        Recursively prints the whole node in somehow structured manner.
        If called on root node, prints the whole tree
        """
        space: str = " " * offset
        temp: str = space + 2 * self.depth * " " + str(self.value)
        print(temp + "   --> lv " + str(self.depth))
        for i in self.children:
            i.print_node(offset)

    def update_depth(self, new_root_depth: int) -> None:
        """
        Recursively recompute the depth of all nodes of a Tree, starting with root node at `new_root_depth`.
        """
        self.depth = new_root_depth
        for i in self.children:
            i.update_depth(new_root_depth + 1)

    def add_child(self, value) -> None:
        """
        Creates a child node with a specific value.
        Connects the created node to the current node/parent.
        """
        new_child = TTreeNode(value)
        new_child.parent = self
        new_child.update_depth(self.depth + 1)
        self.children.append(new_child)

    def connect_child(self, node: "TTreeNode") -> None:
        """
        Connects a specific node to current node.
        """
        self.children.append(node)
        node.parent = self
        node.update_depth(self.depth + 1)

    def remove_child(self, value: str) -> None:
        """
        Removes the first child from the 'left' that matches the specified value.
        If no child is matched, nothing happens.
        """
        for i in range(len(self.children)):
            if self.children[i].value == value:
                self.children.pop(i)
                return

    def get_depth(self) -> int:
        """
        Compute the depth of the tree (using recursion).
        """
        result: int = self.depth + 1
        for i in self.children:
            temp = i.get_depth()
            if temp > result:
                result = temp
        return result

    # Maybe redundant functions #

    def find_from_left(self, value_to_find: str) -> Optional["TTreeNode"]:
        """
        Recursive search for a node with a specified value.
        Finds the first left-most occurrence.
        If not found, None is returned.
        """
        for i in self.children:
            x = i.find_from_left(value_to_find)
            if x is not None:
                return x
        return self if (self.value == value_to_find) else None

    def find_from_right(self, value_to_find: str) -> Optional["TTreeNode"]:
        """
        Recursive search for a node with a specified value.
        Finds the first right-most occurrence.
        If not found, None is returned.
        """
        temp_list = self.children[::-1]
        for i in temp_list:
            x = i.find_from_right(value_to_find)
            if x is not None:
                return x
        return self if (self.value == value_to_find) else None

    def treenode_iterate_bfs(self) -> Generator["TTreeNode", None, None]:
        pass

    def treenode_iterate_dfs(self) -> Generator["TTreeNode", None, None]:
        pass


def convert_string_to_tree(string: str) -> TTreeNode:
    """
    Convert a structured string into the tree structure.
    Special characters are `[ ] ;` -- brackets enclose children nodes, semicolons separate children node values.

    Note: Node names are expected to only contain
    alphanumeric characters (no whitespaces or special characters) for guaranteed functionality.

    E.g. x[y;z] will create a tree rooted at node x with children y, z.
    """

    def get_node_from_string(string: str) -> tuple[TTreeNode, str]:
        """
        Carve out a part of the structured string enough to define a new tree node.
        Return the created node and the rest of the structured string covering the rest of the tree structure.

        Node: Does not cover edge cases! (e.g. wrong string structure)
        """
        string = string.strip()
        node_name = re.match("^[\w]+", string).group()
        string = string.lstrip(str(node_name))
        node = TTreeNode(node_name)
        return node, string

    def build_tree_from_string(current_node: TTreeNode, string: str) -> TTreeNode:
        """
        Recursive function to generate a tree from a structured string
        XYZ [...] = node with list of children following (can be nested)
        [ node1 ; node2 [...] ; node3 ; ... ] = list of children of a previous node
        """
        string: str = string.strip()  # skipping whitespaces

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


def convert_tree_to_string(node: TTreeNode) -> str:
    """
    Reverse of the convert_string_to_tree() function.
    Creates a concise (string) representation of a tree from its structure
    """
    if len(node.children) == 0:
        return str(node.value)
    else:
        temp: str = node.value + "["
        for i in range(len(node.children)):
            temp += str(convert_tree_to_string(node.children[i]))
            if i < len(node.children) - 1:
                temp += ";"
        temp += "]"
        return temp
