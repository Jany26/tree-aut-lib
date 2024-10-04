from typing import Optional

from tree_automata import TTreeNode, TTransition

# Non emptiness check (+ witness generation) helper functions


def generate_witness_tree(edge_dict: dict[str, TTransition], root: str) -> Optional[TTreeNode]:
    """
    Helper function for generating tree starting from a specified node
    uses a dictionary of transitions (only 1 needed for each state).
    """

    # bugfix = False: will create node names in the format: '(symbol;state)'
    # which is better for visual debugging sbut these trees will not work with
    # match_tree functions used with the original tree automata that produced
    # these witness trees. For it to match with original tree automaton,
    # the format should be: 'symbol' (bugfix = True)
    bugfix: bool = True

    if type(edge_dict) is None or type(root) is None:
        return None
    if len(edge_dict[root].children) == 0:
        if bugfix:
            return TTreeNode(f"{edge_dict[root].info.label}")
        else:
            return TTreeNode(f"({edge_dict[root].info.label};{root})")
    else:
        if bugfix:
            temp_node = TTreeNode(f"{edge_dict[root].info.label}")
        else:
            temp_node = TTreeNode(f"({edge_dict[root].info.label};{root})")

        for i in edge_dict[root].children:
            temp_child: TTreeNode = generate_witness_tree(edge_dict, i)
            temp_node.connect_child(temp_child)
        return temp_node


def generate_witness_string(edge_dict: dict[str, TTransition], root: str) -> str:
    """
    Helper function for generating a string that represents a tree, top-down,
    uses dictionary of transitions (only 1 needed for each state).
    """
    if len(edge_dict[root].children) == 0:
        return str(edge_dict[root].info.label)
    else:
        parent_string: str = str(edge_dict[root].info.label) + "["
        for i in range(len(edge_dict[root].children)):
            child_string: str = generate_witness_string(edge_dict, edge_dict[root].children[i])
            parent_string += child_string
            if i < len(edge_dict[root].children) - 1:
                parent_string += ";"
        return parent_string + "]"
