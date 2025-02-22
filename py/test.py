from apply.abdd_node import ABDDNode
from apply.abdd import ABDD, init_abdd_from_ta
from apply.abdd_apply import check_if_abdd, abdd_apply
from apply.apply_edge import ApplyEdge
from apply.apply_node_materialization import materialize_node_on_edge
from apply.apply_testing import BooleanOperation
from formats.format_vtf import import_treeaut_from_vtf
from tree_automata import TTreeAut

# if __name__ == "__main__":
#     test_all_apply_intersectoids()
#     # applied = apply.apply_testing.apply_intersectoid_create(
#     #     apply.apply_testing.BooleanOperation.AND, box_catalogue["L1"], box_catalogue["HPort"])
#     # applied.name = f"test"
#     # print(applied)


if __name__ == "__main__":

    input_ta_1 = import_treeaut_from_vtf("../tests/apply/simple-input-1.vtf")
    input_ta_2 = import_treeaut_from_vtf("../tests/apply/simple-input-2.vtf")
    # print(input_ta_1)
    # print(input_ta_2)

    # result = abdd_apply(BooleanOperation.AND, init_abdd_from_ta(input_ta_1), init_abdd_from_ta(input_ta_2), 11)
    # print(result)
    # print(result)
    abdd_1 = init_abdd_from_ta(input_ta_1)
    abdd_2 = init_abdd_from_ta(input_ta_2)
    print(abdd_2)
    edge = ApplyEdge(abdd_2, None, abdd_2.root, None, None)
    node1 = materialize_node_on_edge(abdd_2, edge, 1, 50)
    print(abdd_2)

    node1 = abdd_2.root.low
    node2 = node1.high
    edge = ApplyEdge(abdd_2, node1, node2, node1.high_box, True)
    nodex = materialize_node_on_edge(abdd_2, edge, 7, 25)
    print(nodex)
    print(abdd_2)

    # print('norm4', check_if_abdd(norm4))
