from tree_automata.automaton import TTreeAut, iterate_edges
from helpers.string_manipulation import create_string_from_name_set
from helpers.utils import box_catalogue


def check_if_abdd(ta: TTreeAut) -> bool:
    """
    Perform checks if the BDA structkure is convertible to automaton:
    - there should be no self-loops, or any other loops
    - each state should have just one outgoing edge (determinism)
    - every edge should be labeled with a variable
    """
    visited: set[str] = set()
    output_vars: set[str] = set()
    result: bool = True
    for edge in iterate_edges(ta):
        if edge.src in visited:
            print(f"multiple edges from {edge.src}")
            result = False
        visited.add(edge.src)
        if edge.children == []:
            output_vars.add(edge.info.variable)
            continue
        arity_sum = sum(1 if b in [None, ""] else box_catalogue[b].port_arity for b in edge.info.box_array)
        if len(edge.children) != arity_sum:
            print(f"inconsistent arity on edge {edge}")
            result = False

        for i in edge.info.box_array:
            # boxes are either non-empty string or None
            if type(i) == str and i == "":
                print(f"{edge} boxes are either None or a non-empty string")
                result = False
        if edge.src in edge.children:
            print(f"self loop {edge}")
            result = False
            continue
        if edge.info.variable == "":
            print(f"no variable on edge {edge}")
            result = False
    output_vars.remove("")
    if len(output_vars) > 1:
        print(f"inconsistent output variables: {create_string_from_name_set(output_vars)}")
        result = False
    return result
