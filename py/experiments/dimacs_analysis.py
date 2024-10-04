"""
[file] dimacs_analysis.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Folding tests on processed Boolean functions in
conjuntive normal form (CNF) - DIMACS format.
[note] Also gets box usage statistics for ABDD model.
"""

import os
import copy

from blif_analysis import test_folding_on_sub_benchmarks, boxname_simplified_translation, formatBoxCounts
from tree_automata import TTreeAut, reachable_top_down
from tree_automata.var_manipulation import create_var_order_list, add_variables_bottom_up
from helpers.utils import box_orders
from canonization.folding import ubda_folding
from canonization.normalization import ubda_normalize
from canonization.unfolding import ubda_unfolding
from formats.format_abdd import import_treeaut_from_abdd
from bdd.bdd_to_treeaut import add_dont_care_boxes


def get_folded_dimacs(initial: TTreeAut, order):
    vars = int(initial.get_var_order()[-1])
    initial_changed = add_dont_care_boxes(initial, vars)
    unfolded = ubda_unfolding(initial_changed)

    unfolded_extra = copy.deepcopy(unfolded)
    add_variables_bottom_up(unfolded_extra, vars)
    var_order = create_var_order_list("", vars + 2, start=0)
    normalized = ubda_normalize(unfolded_extra, var_order)
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformat_keys()
    normalized_clean.reformat_states()
    add_variables_bottom_up(normalized_clean, vars + 2)
    normalized.meta_data.recompute()
    normalized_clean.meta_data.recompute()
    folded = ubda_folding(normalized_clean, box_orders[order], normalized_clean.get_var_max())
    return folded


def create_dimacs_file_order(dir_path: str) -> list:
    dimacs_sorter: dict[int, str] = {}
    for subdir, dirs, files in os.walk(dir_path):
        for file in files:
            benchmark = int(file.split("-")[-1].split(".")[0])
            dimacs_sorter[benchmark] = f"{subdir}{file}"
    return dimacs_sorter


def print_dimacs_box_counts():
    order = "full"
    initial_string = f"{'path' :<30} = {'norm' :<5}, {order :<5}, "
    for val in boxname_simplified_translation.values():
        initial_string += f"{val :<5}, "
    print(initial_string)
    dimacs_sorter = create_dimacs_file_order(f"../data/uf20/")
    for benchmark in sorted(dimacs_sorter.keys()):
        path = dimacs_sorter[benchmark]
        name = path.split("/")[-1]
        initial = import_treeaut_from_abdd(path)
        folded = get_folded_dimacs(initial, order)
        print(
            f"{name :<30} = {len(initial.get_states()) :<5}, {len(reachable_top_down(folded)) :<5}, {formatBoxCounts(folded)}"
        )


def folding_test_dimacs():
    report_line = f"{'name of the benchmark' :<30}\t| init\t| unfo\t| norm"
    for order_name in box_orders.keys():
        report_line += f"\t| {order_name}"
    print(report_line)

    dimacs_sorter = create_dimacs_file_order("../data/uf20/")
    for benchmark in sorted(dimacs_sorter.keys()):
        filename = dimacs_sorter[benchmark]
        print(f"{filename}", end="\r")

        test_folding_on_sub_benchmarks(
            f"{filename}", f"../data/dimacs/uf20/{filename.split('.')[-1]}", orders=None, root_num=None
        )


if __name__ == "__main__":
    # print_dimacs_box_counts()
    folding_test_dimacs()
