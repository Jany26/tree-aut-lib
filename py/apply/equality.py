from tree_automata import (
    TTreeAut,
    TTransition,
    TEdge,
    tree_aut_intersection,
    tree_aut_complement,
    non_empty_bottom_up,
    non_empty_top_down,
)


def create_trivial_aut(materialized_box: TTreeAut) -> TTreeAut:
    """
    During materialized box traversal, when we try to find patterns that are
    identical (semantically) to some of the boxes, we might encounter an automaton,
    that has a language almost the same as one of the boxes, except it can produce
    trivial trees (only one leaf node - either a port or a terminal symbol).

    For this reason, during "equality" check, we create an arbitrary automaton,
    that can accept ONLY these trivial trees (based on the compared box's output symbols),
    and complement it and then intersect it with the initial materialized box,
    resulting in an automaton that CANNOT produce these trivail trees,
    making the language comparison against boxes simpler and more straightforward.
    """
    symbols = materialized_box.get_output_symbols()

    rootstates = [i for i in materialized_box.roots]
    transitions = {
        i: {f"k{c}": TTransition(i, TEdge(s, [], ""), []) for c, s in enumerate(symbols)} for i in rootstates
    }
    name = f"trivial({materialized_box.name})"
    result = TTreeAut(rootstates, transitions, name, 0)
    return result


def tree_aut_equal(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    """
    Classic automaton language equality check.
    Works by two-way subset checking.

    L(A1) == L(A2) \iff L(A1) \subseteq L(A2) \and L(A2) \subseteq L(A1)

    L(A1) \subseteq L(A2) \iff L(A1) \intersect co-(L(A2)) == \emptylang
    L(A2) \subseteq L(A1) \iff L(A2) \intersect co-(L(A1)) == \emptylang
    """
    symbols = box.get_symbol_arity_dict()
    symbols.update(aut.get_symbol_arity_dict())

    # aut and co-box == empty => 'aut subseteq box'
    intersection1 = tree_aut_intersection(aut, tree_aut_complement(box, symbols))
    witness_BU_1, _ = non_empty_bottom_up(intersection1)
    witness_TD_1, _ = non_empty_top_down(intersection1)
    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None

    # box and co-aut == empty => 'box subseteq aut'
    intersection2 = tree_aut_intersection(box, tree_aut_complement(aut, symbols))
    witness_BU_2, _ = non_empty_bottom_up(intersection2)
    witness_TD_2, _ = non_empty_top_down(intersection2)
    box_subset_of_aut = witness_BU_2 is None or witness_TD_2 is None
    if debug:
        print(f"{aut.name} ==? {box.name}")
        print("witness 1")
        witness_BU_1.print_node() if witness_BU_1 is not None else "None"
        print("witness 2")
        witness_BU_2.print_node() if witness_BU_2 is not None else "None"
    return aut_subset_of_box and box_subset_of_aut


def matbox_equal_to_box(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    """
    If an automaton has a language equal to some box's language, return True.

    Since during materialization, arbitrary ports are added sometimes to root states, we need
    to be able to work-around the fact that aut's language can contain trivial trees.

    We don't consider trivial trees - i.e. only one node (either port or terminal symbol) -
    as a proof that languages are not subsets of each other.
    This is why we intersect with a complement of a tree automaton accepting only trivial trees.
    """
    symbols = box.get_symbol_arity_dict()
    symbols.update(aut.get_symbol_arity_dict())

    trivial = create_trivial_aut(aut)
    nontrivial = tree_aut_complement(trivial, symbols)
    nontrivial_aut = tree_aut_intersection(aut, nontrivial)

    # aut and co-box == empty => 'aut subseteq box'
    intersection1 = tree_aut_intersection(nontrivial_aut, tree_aut_complement(box, symbols))
    witness_BU_1, _ = non_empty_bottom_up(intersection1)
    witness_TD_1, _ = non_empty_top_down(intersection1)

    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None

    # box and co-aut == empty => 'box subseteq aut'
    intersection2 = tree_aut_intersection(box, tree_aut_complement(nontrivial_aut, symbols))
    witness_BU_2, _ = non_empty_bottom_up(intersection2)
    witness_TD_2, _ = non_empty_top_down(intersection2)
    box_subset_of_aut = witness_BU_2 is None or witness_TD_2 is None

    if debug:
        print(f"{aut.name} ==? {box.name}")
        print("witness 1")
        witness_BU_1.print_node() if witness_BU_1 is not None else "None"
        print("witness 2")
        witness_BU_2.print_node() if witness_BU_2 is not None else "None"
    return aut_subset_of_box and box_subset_of_aut


def matbox_sublang_of_box(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
    """
    If an automaton has nonempty language and this language is a subset of some box language,
    return True.

    Similar to 'matbox_equal_to_box', we don't consider trivial trees - i.e. only one node
    (either port or terminal symbol) - as a proof that languages are not subsets of each other.
    This is why we intersect with a complement of a tree automaton accepting only trivial trees.
    """
    symbols = box.get_symbol_arity_dict()
    symbols.update(aut.get_symbol_arity_dict())

    trivial = create_trivial_aut(aut)
    nontrivial = tree_aut_complement(trivial, symbols)
    nontrivial_aut = tree_aut_intersection(aut, nontrivial)
    witnessBU, _ = non_empty_bottom_up(nontrivial_aut)
    witnessTD, _ = non_empty_top_down(nontrivial_aut)
    aut_empty = witnessBU is None or witnessTD is None

    if aut_empty:
        return False

    # aut and co-box == empty => 'aut subseteq box'
    intersection1 = tree_aut_intersection(nontrivial_aut, tree_aut_complement(box, symbols))
    witness_BU_1, _ = non_empty_bottom_up(intersection1)
    witness_TD_1, _ = non_empty_top_down(intersection1)

    aut_subset_of_box = witness_BU_1 is None or witness_TD_1 is None
    return aut_subset_of_box
