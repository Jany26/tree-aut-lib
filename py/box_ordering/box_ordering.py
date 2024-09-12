from tree_automata import TTreeAut, tree_aut_intersection, non_empty_bottom_up, tree_aut_complement


# these functions (commutativity and comparability checks) were supposed to
# help with finding the optimal "total" box ordering with regards to their
# reduction capabilities, however, this attempt lead nowhere,
# so it is left unused
def are_commutative(ta1: TTreeAut, ta2: TTreeAut) -> bool:
    suffix = ta1.create_suffix()
    prefix = ta2.create_prefix(ta1.get_output_symbols())
    intersection = tree_aut_intersection(suffix, prefix)
    witness_t, _ = non_empty_bottom_up(intersection)
    return witness_t is None


def are_comparable(ta1: TTreeAut, ta2: TTreeAut):
    infix = ta1.create_infix(ta2.get_output_edges(inverse=True))
    language = {**ta1.get_symbol_arity_dict(), **ta2.get_symbol_arity_dict()}
    complement = tree_aut_complement(infix, language)
    # print(complement)
    intersection = tree_aut_intersection(complement, ta2)
    witnessT, _ = non_empty_bottom_up(intersection)
    return witnessT is None
