from tree_automata import (
    TTreeAut,
    tree_aut_intersection,
    tree_aut_complement,
    non_empty_bottom_up,
    non_empty_top_down,
)


def tree_aut_equal(aut: TTreeAut, box: TTreeAut, debug=False) -> bool:
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
