"""
[file] adhoc_tester.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] helping tester functions for debugging, optimization, etc.
[note] not essential/important for the final working version
"""

import os
import copy
from typing import Tuple

from tree_automata import TTreeAut, iterate_edges, remove_useless_states, reachable_top_down
from tree_automata.var_manipulation import create_var_order_dict, add_variables_bottom_up
from helpers.utils import box_orders, full_box_order as box_order
from bdd.bdd_to_treeaut import create_tree_aut_from_bdd, add_dont_care_boxes
from simulation import simulate_and_compare

import formats.format_abdd as abdd
import formats.render_dot as dot
from formats.format_vtf import export_treeaut_to_vtf, import_treeaut_from_vtf
from formats.format_dimacs import dimacs_read

from canonization.unfolding import ubda_unfolding
from canonization.normalization import ubda_normalize
from canonization.folding import ubda_folding


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# FOLDING testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TestOptions:
    def __init__(
        self,
        vars: int,
        output_path: str = "",
        cli=False,
        debug=False,
        vtf=False,
        png=False,
        log=False,
        sim=False,
        prog=False,
    ):
        self.vars: int = vars  # how many variables the benchmark consists of
        self.output_path: str = output_path  # where to store the exported images and TA files

        # debugging purposes (automatic, visual, etc.)
        self.cli: bool = cli  # print out semiresults to stdout,
        self.debug: bool = debug  # print out extra information during normalization, folding process, etc.
        self.export_vtf: bool = vtf  # exporting semiresults to vtf files
        self.export_png: bool = png  # exporting results as DOT graphs to png
        self.logging: bool = log  # log semi-results/debug info to files
        self.sim: bool = sim  # check equivalence (before/after folding)
        # simulates all variable assignments (time-consuming)
        self.progress: bool = prog  # show % progress of simulation
        self.box_order = box_orders["full"]  # if explicit box order is needed
        self.var_order = None  # if explicit variable order is needed


# end of TestOptions class


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def test_dimacs_benchmark(path, options: TestOptions) -> Tuple[bool | None, str]:
    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)
    if path.endswith(".cnf") or path.endswith(".dnf"):
        dnf = dimacs_read(path)
        initial = create_tree_aut_from_bdd(dnf)
    elif path.endswith(".vtf"):
        initial = import_treeaut_from_vtf(path)
    else:
        print("unknown format")
        return None, None

    initial.reformat_states()
    initial.reformat_keys()

    tree_auts = canonize_benchmark(initial, options)
    eq, report = check_equivalence(tree_auts, options)
    names = [
        "init",
        "init-X",
        "unfold",
        "unfold-extra",
        "normal",
        "normal-clean",
        "fold",
        "fold-trim",
        "unfold-2",
        "unfold-2-extra",
    ]

    skip = []
    if not options.export_png and not options.export_vtf:
        return eq, report

    for i, ta in enumerate(tree_auts.values()):
        ta.meta_data.Frecompute()
        if options.export_vtf:
            export_treeaut_to_vtf(ta, f"{options.output_path}/{i:02d}-{names[i]}.vtf")
        if options.export_png:
            dot.export_to_file(ta, f"{options.output_path}/{i:02d}-{names[i]}")
        if not options.export_png and (i not in skip and eq is not True):
            dot.export_to_file(ta, f"{options.output_path}/{i:02d}-{names[i]}")
    return eq, report


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def check_equivalence(tree_auts: dict, options: TestOptions):
    result = None
    if options.sim:
        sim_log_file = open(f"{options.output_path}/log_simulation.txt", "w")
        result = simulate_and_compare(
            tree_auts["initial"],
            tree_auts["unfolded_2_extra"],
            options.vars,
            debug=options.progress,
            output=sim_log_file,
        )
        sim_log_file.close()

    if result is False:
        intersectoid_path = f"{options.output_path}/intersectoids/"
        ubda_path = f"{options.output_path}/ubdas/"
        for intersectoid in os.listdir(intersectoid_path):
            ta = import_treeaut_from_vtf(intersectoid)
            dot.export_to_file(ta, ta.name)
        for ubda in os.listdir(ubda_path):
            ta = import_treeaut_from_vtf(ubda)
            dot.export_to_file(ta, ta.name)

    unfold_count = len(tree_auts["initial"].get_states())
    fold_count = len(tree_auts["folded_trimmed"].get_states())
    report = f"{options.output_path :<50}: counts: {unfold_count :<5} | {fold_count :<5} equivalent: {result}"
    return result, report


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def canonize_benchmark(initial: TTreeAut, options: TestOptions):
    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)
    if options.progress:
        print(f"\rPreparing data for {options.output_path} (1/8)...", end="")
    path = options.output_path
    log_file = open(f"{path}/log.txt", "w")
    log_file.write(f"INITIAL\n\n{initial}\n\n")

    # var_order = initial.get_var_order()
    # boxes_order = box_order if "box_order" not in options else box_orders[options.box_order]

    if options.progress:
        print(f"\r{'Adding extra boxes (2/8)...': <80}", end="")
    initial_changed = add_dont_care_boxes(initial, options.vars)
    log_file.write(f"INITIAL (with X edge-correction)\n\n{initial_changed}\n\n")

    if options.progress:
        print(f"\r{'Unfolding (3/8)...': <80}", end="")
    unfolded = ubda_unfolding(initial_changed)
    log_file.write(f"UNFOLDED\n\n{unfolded}\n")

    if options.progress:
        print(f"\r{'Computing extra variables (4/8)...': <80}", end="")
    unfolded_extra = copy.deepcopy(unfolded)
    add_variables_bottom_up(unfolded_extra, options.vars)
    log_file.write(f"UNFOLDED (additional variables)\n\n{unfolded_extra}\n\n")

    if options.progress:
        print(f"\r{'Normalizing (5/8)...': <80}", end="")
    normalization_log = open(f"{path}/log_normalization.txt", "w")
    normalization_log.write(f"INPUT\n\n{unfolded_extra}\n\n")
    var_order = create_var_order_dict("", options.vars + 2, start=0)
    # print(var_order)
    normalized = ubda_normalize(unfolded_extra, var_order, verbose=options.debug, output=normalization_log)
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformat_keys()
    normalized_clean.reformat_states()
    add_variables_bottom_up(normalized_clean, options.vars + 2)
    normalized.meta_data.recompute()
    normalized_clean.meta_data.recompute()

    normalization_log.write(f"OUTPUT\n\n{normalized}\n\n")
    log_file.write(f"NORMALIZED\n\n{normalized}\n\n")
    log_file.write(f"NORMALIZED CLEAN\n\n{normalized_clean}\n\n")

    if options.progress:
        print(f"\r{'Folding (6/8)...': <80}", end="")
    folding_log = open(f"{path}/log_folding.txt", "w")
    folding_log.write(f"INPUT\n\n{normalized_clean}\n\n")
    if options.export_vtf:
        if not os.path.exists(f"{options.output_path}/vtf/"):
            os.makedirs(f"{options.output_path}/vtf/")
        names = [
            "00-init",
            "01-init-X",
            "02-unfold",
            "03-unfold-extra",
            "04-normal",
            "05-normal-clean",
            "06-fold",
            "07-fold-trim",
            "08-unfold-2",
            "09-unfold-2-extra",
        ]
        export_treeaut_to_vtf(initial, f"{options.output_path}/vtf/{names[0]}.vtf")
        export_treeaut_to_vtf(initial_changed, f"{options.output_path}/vtf/{names[1]}.vtf")
        export_treeaut_to_vtf(unfolded, f"{options.output_path}/vtf/{names[2]}.vtf")
        export_treeaut_to_vtf(unfolded_extra, f"{options.output_path}/vtf/{names[3]}.vtf")
        export_treeaut_to_vtf(normalized, f"{options.output_path}/vtf/{names[4]}.vtf")
        export_treeaut_to_vtf(normalized_clean, f"{options.output_path}/vtf/{names[5]}.vtf")

    folded = ubda_folding(
        normalized_clean,
        options.box_order,
        options.vars + 1,
        verbose=options.debug,
        export_vtf=options.export_vtf,
        export_png=options.export_png,
        output=folding_log,
        export_path=options.output_path,
    )
    folding_log.write(f"OUTPUT\n\n{folded}\n\n")
    log_file.write(f"FOLDED\n\n{folded}\n\n")

    folded_trimmed = remove_useless_states(folded)
    log_file.write(f"FOLDED TRIMMED\n\n{folded}\n\n")

    if options.progress:
        print(f"\r{'Unfolding again (7/8)...': <80}", end="")
    unfolded_after = ubda_unfolding(folded)
    log_file.write(f"UNFOLDED AFTER FOLDING\n\n{unfolded_after}\n\n")

    if options.progress:
        print(f"\r{'Computing extra variables again (8/8)...': <80}", end="")
    unfolded_after_extra = copy.deepcopy(unfolded_after)
    add_variables_bottom_up(unfolded_after_extra, options.vars)
    log_file.write(f"UNFOLDED AFTER FOLDING (additional variables)\n\n{unfolded_after_extra}\n\n")

    log_file.close()
    normalization_log.close()
    folding_log.close()

    result = {
        "initial": initial,
        "initial_extra": initial_changed,
        "unfolded": unfolded,
        "unfolded_extra": unfolded_extra,
        "normalized": normalized,
        "normalized_clean": normalized_clean,
        "folded": folded,
        "folded_trimmed": folded_trimmed,
        "unfolded_2": unfolded_after,
        "unfolded_2_extra": unfolded_after_extra,
    }

    names = [
        "init",
        "init-X",
        "unfold",
        "unfold-extra",
        "normal",
        "normal-clean",
        "fold",
        "fold-trim",
        "unfold-2",
        "unfold-2-extra",
    ]
    skip = []
    # skip = []
    if options.export_png:  # or options.export_vtf:
        for i, ta in enumerate(result.values()):
            ta.meta_data.recompute()
            # exportTAtoVTF(ta, f"{path}/{i:02d}-{names[i]}.vtf")
            if i not in skip:
                dot.export_to_file(ta, f"{path}/{i:02d}-{names[i]}")

    if options.cli:
        print(f"INITIAL\n\n{initial}\n")
        print(f"INITIAL (with X edge-correction)\n\n{initial_changed}\n")
        print(f"UNFOLDED\n\n{unfolded}\n")
        print(f"NORMALIZED\n\n{normalized}\n")
        print(f"FOLDED\n\n{folded}\n")
        print(f"UNFOLDED AFTER\n\n{unfolded_after}\n")

    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def simulate_benchmark(input_path: str, vars: int, output_path, simulate=False, images=False):
    results: dict[str, TTreeAut] = {}
    names = [
        "00-init",
        "01-init-X",
        "02-unfold",
        "03-unfold-extra",
        "04-normal",
        "05-normal-clean",
        "06-fold",
        "07-fold-trim",
        "08-unfold-2",
        "09-unfold-2-extra",
    ]
    if input_path.endswith(".vtf"):
        results["00-init"] = import_treeaut_from_vtf(input_path)
    elif input_path.endswith(".cnf") or input_path.endswith(".dnf"):
        bdd = dimacs_read(input_path)
        results["00-init"] = create_tree_aut_from_bdd(bdd)
    else:
        raise Exception(f"Unknown format: {input_path}")

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(f"{output_path}/vtf/"):
        os.makedirs(f"{output_path}/vtf/")

    log0 = open(f"{output_path}/log0.txt", "w")
    log1 = open(f"{output_path}/log1_normalization.txt", "w")
    log2 = open(f"{output_path}/log2_folding.txt", "w")
    log3 = open(f"{output_path}/log3_simulation.txt", "w")

    results["00-init"].reformat_keys()
    results["00-init"].reformat_states()
    results["01-init-X"] = add_dont_care_boxes(results["00-init"], vars)
    results["02-unfold"] = ubda_unfolding(results["01-init-X"])
    results["03-unfold-extra"] = copy.deepcopy(results["02-unfold"])
    add_variables_bottom_up(results["03-unfold-extra"], vars)
    results["04-normal"] = ubda_normalize(
        results["03-unfold-extra"], create_var_order_dict("", vars + 1), verbose=True, output=log1
    )
    results["05-normal-clean"] = copy.deepcopy(results["04-normal"])
    results["05-normal-clean"].reformat_keys()
    results["05-normal-clean"].reformat_states()
    results["06-fold"] = ubda_folding(
        results["05-normal-clean"],
        box_order,
        vars,
        verbose=True,
        export_vtf=True,
        export_png=False,
        output=log2,
        export_path=output_path,
    )
    results["07-fold-trim"] = remove_useless_states(results["06-fold"])
    results["08-unfold-2"] = ubda_unfolding(results["07-fold-trim"])
    results["09-unfold-2-extra"] = copy.deepcopy(results["08-unfold-2"])
    add_variables_bottom_up(results["09-unfold-2-extra"], vars)
    for name in names:
        export_treeaut_to_vtf(results[name], f"{output_path}/vtf/{name}.vtf")
        log0.write(f"{name}\n\n{results[name]}\n\n")

    equivalent = None
    if simulate:
        equivalent = simulate_and_compare(
            results["00-init"], results["09-unfold-2-extra"], vars, debug=True, output=log3
        )

    if equivalent is False or images is True:
        results["06-fold"] = ubda_folding(
            results["05-normal-clean"],
            box_order,
            vars,
            verbose=False,
            export_vtf=False,
            export_png=True,
            output=log2,
            export_path=output_path,
        )
        os.makedirs(f"{output_path}/png/")
        for name in names:
            dot.export_to_file(results[name], f"{output_path}/png/{name}")

    log0.close()
    log1.close()
    log2.close()
    log3.close()

    node_count_1 = len(results["00-init"].get_states())
    node_count_2 = len(results["07-fold-trim"].get_states())
    result = f"equivalent = {equivalent}, node counts: {node_count_1} | {node_count_2}"
    print(result)
    return equivalent, result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ABDD format testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def test_abdd_format():
    options = {
        "vars": 6,
        "image": f"results/uf20-01-error-1-minimized",
        "cli": False,
        "debug": False,
        "export_vtf": True,
        "sim": False,
    }
    raw = import_treeaut_from_vtf(f"./tests/folding/folding-error-1.vtf")
    tree_auts = canonize_benchmark(raw, options)
    test = tree_auts["folded_trimmed"]
    test.reformat_states()
    print(test)
    abdd.export_treeaut_to_abdd(test, "../tests/abdd-format/test-comments.dd", comments=True)
    abdd.export_treeaut_to_abdd(test, "../tests/abdd-format/test.dd", comments=False)
    result = abdd.import_treeaut_from_abdd("../tests/abdd-format/test-comments.dd")
    result.reformat_states()
    print(result)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# DIMACS Benchmark testing and debugging
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def run_all_dimacs_20_var_benchmark_tests(options: TestOptions, already_done: int):
    simulation_results = open("results/dimacs/simulationResults.txt", "a")
    for i in range(1000):
        simulation_results.flush()
        if i + 1 <= already_done:
            continue
        filename = f"../benchmark/dimacs/uf20/uf20-0{i+1}.cnf"
        if not filename.endswith(".cnf"):
            continue
        base = os.path.basename(filename).split(".")[0]
        options = TestOptions(20, f"../data/dimacs/{base}", vtf=True)
        # if not os.path.exists(f"results/{base}"):
        #     os.makedirs(f"results/{base}")
        if os.path.isfile(filename):
            try:
                eq, report = test_dimacs_benchmark(filename, options)
                print(report)
                simulation_results.write(f"{report}\n")
            except:
                simulation_results.write(f"{filename :<50}: error\n")
    simulation_results.close()


def folding_debug(idx):
    options = TestOptions(20, f"../benchmark/dimacs/uf20-0{idx}")

    path = f"./tests/dimacs/uf20/uf20-0{idx}.cnf"
    options.path = path
    initial = create_tree_aut_from_bdd(dimacs_read(path))
    initial.reformat_keys()
    initial.reformat_states()
    initial.name = f"uf20-0{idx}"
    initial = remove_useless_states(initial)

    tree_auts = canonize_benchmark(initial, options)
    print(tree_auts["initial"])
    print(tree_auts["folded_trimmed"])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BLIF Benchmark testing and debugging
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def blif_test_c17():
    options = {
        "vars": 11,
        "image": f"../data/blif/c17",
        "cli": False,
        "debug": False,
        "sim": False,
        "progress": False,
        "export_vtf": False,
        "export_png": False,
    }
    init = import_treeaut_from_vtf("./tests/blif/C17.vtf")
    print("initial =", len(init.get_states()))
    print(init)
    var_mapping = {f"{i}": f"{i+1}" for i in range(11)}
    for edge in iterate_edges(init):
        if edge.info.variable in var_mapping:
            edge.info.variable = var_mapping[edge.info.variable]
    results = canonize_benchmark(init, options)
    print("folded =", len(results["folded_trimmed"].get_states()))
    print(results["folded_trimmed"])


def blif_test_node_counts(path):
    tas = abdd.import_treeaut_from_abdd(path)
    if type(tas) != list:
        tas = [tas]
    initial_total = 0
    folded_total = 0
    for i in range(len(tas)):
        ta = tas[i]

        options = {
            "vars": int(ta.get_var_order()[-1]),
            "image": f"../benchmark/blif/{ta.name}",
            "cli": False,
            "debug": False,
            "sim": True,
            "progress": True,
            "export_vtf": True,
            "export_png": False,
        }
        print("var =", int(ta.get_var_order()[-1]))
        print(f"testing... {ta.name}")
        results = canonize_benchmark(ta, options)
        initial = len(ta.get_states())
        folded = len(results["folded_trimmed"].get_states())
        print(f"{ta.name}, init = {initial}, fold = {folded}")
        initial_total += initial
        folded_total += folded
    print("total before folding =", initial_total)
    print("total after folding  =", folded_total)


# similar to top down determinism, except not only do we restrict
# the number of possible transitions from a state upon reading a specific symbol to 1,
# we restrict number of any possible transitions from a state to 1
# (so across all possible encountered symbols)
def is_bdd_convertible(treeaut: TTreeAut) -> bool:
    for state in treeaut.get_states():
        if len(treeaut.transitions[state].values()) > 1:
            return False
    return True


def bdd_isomorphic_check(ta1: TTreeAut, ta2: TTreeAut) -> bool:
    outputs1 = ta1.get_output_edges(inverse=True)
    outputs2 = ta2.get_output_edges(inverse=True)
    var_visibility_1 = ta1.get_var_visibility_cache()
    var_visibility_2 = ta2.get_var_visibility_cache()

    def compare_node(ta1: TTreeAut, ta2: TTreeAut, state1: str, state2: str):
        found1 = state1 in outputs1
        found2 = state2 in outputs2
        if found1 or found2:
            if found1 == found2:
                return True
            else:
                print(f"outputs not agreeing => {state1}, {state2}")
                return False
            # return found1 == found2
        if found1 and found2:
            if outputs1[state1] != outputs2[state2]:
                print(f"outputs => {state1}, {state2}")
                return False
        if var_visibility_1[state1] != var_visibility_2[state2]:
            print(f"varvis => {state1}, {state2}")
            return False

        for edge1 in ta1.transitions[state1].values():
            for edge2 in ta2.transitions[state2].values():
                if len(edge1.children) != len(edge2.children):
                    print(f"children length => {edge1}, {edge2}")
                    return False
                for idx in range(len(edge1.children)):
                    child1 = edge1.children[idx]
                    child2 = edge2.children[idx]
                    if not compare_node(ta1, ta2, child1, child2):
                        return False
        return True

    if len(ta1.roots) != len(ta2.roots) or len(ta1.roots) != 1:
        raise AssertionError("tree_aut_isomorphic(): Nondeterminism - rootstates > 1.")

    if not is_bdd_convertible(ta1):
        raise AssertionError(f"tree_aut_isomorphic(): {ta1.name} is not bdd_convertible")
    if not is_bdd_convertible(ta2):
        raise AssertionError(f"tree_aut_isomorphic(): {ta2.name} is not bdd_convertible")

    return compare_node(ta1, ta2, ta1.roots[0], ta2.roots[0])


def isomorphic_check_blif():
    for subdir, dirs, files in os.walk("../data/blif/"):
        init: TTreeAut = None
        bdd: TTreeAut = None
        for file in files:
            if file.endswith("1-init.vtf"):
                init = import_treeaut_from_vtf(f"{subdir}/{file}")
            if file.endswith("4-bdd-fold.vtf"):
                bdd = import_treeaut_from_vtf(f"{subdir}/{file}")
        if init is None or bdd is None:
            continue
        isomorphic = bdd_isomorphic_check(init, bdd)
        if not isomorphic:
            return False
    return True


def pop_unreachable(treeaut: TTreeAut) -> TTreeAut:
    result = copy.deepcopy(treeaut)
    pop_states = []
    reachable = set(reachable_top_down(result))
    for state in result.get_states():
        if state not in reachable:
            pop_states.append(state)
    for state in pop_states:
        result.transitions.pop(state)
    return result


def print_boxed_edges(ta: TTreeAut):
    for edge in iterate_edges(ta):
        foundbox = False
        for box in edge.info.box_array:
            if box is not None:
                foundbox = True
        if foundbox:
            print(edge)


def set_var_max(ta: TTreeAut, var: int):
    prefix = ta.get_var_prefix()
    for edge in iterate_edges(ta):
        if len(edge.children) == 0:
            edge.info.variable = f"{prefix}{var}"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    opt = TestOptions(19, "../data/testout", vtf=True, png=True)
    ta = abdd.import_treeaut_from_abdd("../data/uf20/uf20-01.abdd")
    set_var_max(ta, 20)
    ta.reformat_states()
    canonize_benchmark(ta, opt)
    pass

# End of file adhoc_tester.py
