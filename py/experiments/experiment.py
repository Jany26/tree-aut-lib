"""
[file] experiment.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Experiment analyzing the growth of benchmark during repetitive Apply usage.
"""

from io import TextIOWrapper
import os
import time

from typing import Optional
from apply.abdd import ABDD
from apply.abdd_apply_main import abdd_apply
from apply.abdd_node import ABDDNode
from apply.abdd_node_cache import ABDDNodeCacheClass
from apply.box_algebra.apply_tables import BooleanOperation
from canonization.folding import ubda_folding
from canonization.normalization import ubda_normalize
from canonization.unfolding import ubda_unfolding
from formats.format_abdd import export_treeaut_to_abdd, import_treeaut_from_abdd
from formats.render_dot import export_to_file
from helpers.string_manipulation import create_var_order_list
from tree_automata.automaton import iterate_states_bfs
from tree_automata.functions.trimming import shrink_to_top_down_reachable_2
from helpers.utils import box_orders


MAX_VAR = 20


def create_dimacs(
    path: str,
    outpath: str,
):
    def create_node(var: int, neg: bool, ncache: ABDDNodeCacheClass) -> ABDDNode:
        node = ABDDNode(ncache.counter)
        node.var = var
        node.is_leaf = False
        node.low_box = "X" if var != MAX_VAR else None
        node.high_box = "X" if var != MAX_VAR else None
        node.low = [ncache.terminal_1 if neg else ncache.terminal_0]
        node.high = [ncache.terminal_0 if neg else ncache.terminal_1]
        cache_hit = ncache.find_node(node)
        if cache_hit is not None:
            return cache_hit
        ncache.counter += 1
        ncache.insert_node(node)
        return node

    def analyze_literal(lit: str) -> tuple[int, bool]:
        var = int(lit)
        return abs(var), var < 0

    name = path.split("/")[-1].split(".")[0]
    f = open(path, "r")
    var_count: int
    clause_count: int
    processed_clauses: int = 0
    ncache = ABDDNodeCacheClass()
    result = ABDD(name, MAX_VAR, [ncache.terminal_1])
    result.root_rule = "X"
    for line in f:
        ncache.refresh_nodes()
        if line.startswith("c"):
            continue
        if line.startswith("p"):
            words = line.strip().split()
            var_count = int(words[2])
            clause_count = int(words[3])
            continue
        words = line.strip().split()
        if len(words) <= 1:
            continue
        var1, neg1 = analyze_literal(words[0])
        var2, neg2 = analyze_literal(words[1])
        var3, neg3 = analyze_literal(words[2])

        node1 = create_node(var1, neg1, ncache)
        abdd1 = ABDD(f"{processed_clauses + 1}-1", MAX_VAR, [node1])
        abdd1.root_rule = "X" if var1 != 1 else None

        node2 = create_node(var2, neg2, ncache)
        abdd2 = ABDD(f"{processed_clauses + 1}-2", MAX_VAR, [node2])
        abdd2.root_rule = "X" if var2 != 1 else None

        node3 = create_node(var3, neg3, ncache)
        abdd3 = ABDD(f"{processed_clauses + 1}-3", MAX_VAR, [node3])
        abdd3.root_rule = "X" if var3 != 1 else None

        or1 = abdd_apply(BooleanOperation.OR, abdd1, abdd2, cache=ncache, maxvar=MAX_VAR)
        ncache.refresh_nodes()
        or2 = abdd_apply(BooleanOperation.OR, or1, abdd3, cache=ncache, maxvar=MAX_VAR)
        ncache.refresh_nodes()
        result = abdd_apply(BooleanOperation.AND, result, or2, cache=ncache, maxvar=MAX_VAR)
        ncache.refresh_nodes()
        processed_clauses += 1
        result.name = name + f"-c{processed_clauses}"
        result.export_to_abdd_file(f"{outpath}/{result.name}.dd")
        if not check_node_uniq(result):
            break


def check_node_uniq(abdd: ABDD) -> bool:
    id_ptr_map: dict[int, int] = {}
    uniq = True
    for i in abdd.iterate_bfs_nodes():
        if i.node not in id_ptr_map:
            id_ptr_map[i.node] = id(i)
        else:
            uniq = False
    return uniq


def get_progressive_cnf_node_counts(benchmark_path, outdir, report_file: str):
    basename: str = os.path.basename(benchmark_path)
    base_no_ext = basename.split(".")[0]

    dirn = os.path.join(outdir, base_no_ext)
    create_dimacs(benchmark_path, dirn)
    # after create_dimacs, the directory for report_file should be ready
    report = open(report_file, "w")

    # the dimacs file has 91 clauses
    report.write(f"benchmark-name;init;norm;bdd;zbdd;tbdd;cbdd;czdd;esr;abdd;elapsed\n")
    print(f"benchmark-name;init;norm;bdd;zbdd;tbdd;cbdd;czdd;esr;abdd;elapsed")
    for i in range(1, 92):
        subbenchmark = f"{dirn}/{base_no_ext}-c{i}.dd"
        ta = import_treeaut_from_abdd(subbenchmark)
        ta.reformat_states()
        init_nc = len(ta.get_states())
        unf = ubda_unfolding(ta, 21)
        timestamp_start = time.time()
        norm = shrink_to_top_down_reachable_2(ubda_normalize(unf, create_var_order_list("", 21)))
        norm.reformat_keys()
        norm.reformat_states()
        norm_nc = len(norm.get_states())
        folded_bdd = ubda_folding(norm, box_orders["bdd"], 21)
        folded_zbdd = ubda_folding(norm, box_orders["zbdd"], 21)
        folded_tbdd = ubda_folding(norm, box_orders["tbdd"], 21)
        folded_cbdd = ubda_folding(norm, box_orders["cbdd"], 21)
        folded_czdd = ubda_folding(norm, box_orders["czdd"], 21)
        folded_esr = ubda_folding(norm, box_orders["esr"], 21)
        folded_abdd = ubda_folding(norm, box_orders["full"], 21)

        timestamp_stop = time.time()

        bdd_nc = len([i for i in iterate_states_bfs(folded_bdd)])
        zbdd_nc = len([i for i in iterate_states_bfs(folded_zbdd)])
        tbdd_nc = len([i for i in iterate_states_bfs(folded_tbdd)])
        cbdd_nc = len([i for i in iterate_states_bfs(folded_cbdd)])
        czdd_nc = len([i for i in iterate_states_bfs(folded_czdd)])
        esr_nc = len([i for i in iterate_states_bfs(folded_esr)])
        abdd_nc = len([i for i in iterate_states_bfs(folded_abdd)])

        elapsed = timestamp_stop - timestamp_start
        report.write(
            f"{subbenchmark};{init_nc};{norm_nc};{bdd_nc};{zbdd_nc};{tbdd_nc};{cbdd_nc};{czdd_nc};{esr_nc};{abdd_nc};{elapsed}\n"
        )
        report.flush()
        print(
            f"{subbenchmark};{init_nc};{norm_nc};{bdd_nc};{zbdd_nc};{tbdd_nc};{cbdd_nc};{czdd_nc};{esr_nc};{abdd_nc};{elapsed}"
        )

        if elapsed > 50.0:
            break
    report.close()


if __name__ == "__main__":
    done = 106
    for i in range(done, 1001):
        print(f"working uf20-0{i}.cnf")
        outpath = "../data/dimacs_analysis/"
        benchmark = f"../benchmark/dimacs/uf20/uf20-0{i}.cnf"
        report_file_path = f"../data/dimacs_analysis/uf20-0{i}/report.csv"
        get_progressive_cnf_node_counts(benchmark, outpath, report_file_path)


# End of file experiment.py
