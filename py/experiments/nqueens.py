"""
[file] nqueens.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Analyzing N-queens benchmarks.
"""

from canonization.folding import ubda_folding
from canonization.normalization import ubda_normalize
from canonization.unfolding import ubda_unfolding
from formats.render_dot import export_to_file
from helpers.string_manipulation import create_var_order_list
from helpers.utils import box_orders
from tree_automata.automaton import TTreeAut, iterate_states_bfs
from tree_automata.functions.trimming import remove_useless_states, shrink_to_top_down_reachable_2
from tree_automata.transition import TEdge, TTransition


def init_ta_from_buddy_output(filename: str) -> TTreeAut:
    """
    Format:
    node-count var-count
    ordered list of variables separated by spaces (first var labels the root)
    nodidx var low-target high-target

    No comments, no empty lines are assumed.
    """
    nodecount: int = 0
    varcount: int = 0
    varmap: dict[str, int] = {}
    statevarmap: dict[str, int] = {}
    transitions: set[TTransition] = set()
    lastvar: int = 0
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            stripped_line = line.strip()
            if idx == 0:
                nodes, vars = line.split()
                nodecount = int(nodes)
                varcount = int(vars)
                continue
            if idx == 1:
                varlist = line.split()
                for var_idx, var_str in enumerate(varlist, start=1):
                    varmap[var_str] = var_idx
                lastvar = varmap[varlist[-1]]
                continue

            node, var, low, high = line.split()
            statevarmap[node] = varmap[var]
            transitions.add(TTransition(node, TEdge("LH", [], f"{varmap[var]}"), [low, high]))
    statevarmap["0"] = lastvar + 1
    statevarmap["1"] = lastvar + 1

    roots = []
    for t in transitions:
        srcvar = statevarmap[t.src]
        lowvar = statevarmap[t.children[0]]
        highvar = statevarmap[t.children[1]]
        lowbox = "X" if lowvar > srcvar + 1 else None
        highbox = "X" if highvar > srcvar + 1 else None
        t.info.box_array = [lowbox, highbox]
        if statevarmap[t.src] == 1:
            roots.append(t.src)

    transitions.add(TTransition("0", TEdge("0", [], f"{lastvar+1}"), []))
    transitions.add(TTransition("1", TEdge("1", [], f"{lastvar+1}"), []))

    transition_dict = {t.src: {f"k{i}": t} for i, t in enumerate(transitions)}
    name = filename.split("/")[-1].split(".")[0]
    return TTreeAut(roots, transition_dict, name, 0)


def run_nqueens_benchmark(path: str):
    ta = init_ta_from_buddy_output(path)
    ta.reformat_keys()
    ta.reformat_states()
    unf = ubda_unfolding(ta, ta.get_var_max())
    unf.reformat_keys()
    unf.reformat_states()
    norm = ubda_normalize(unf, create_var_order_list("", unf.get_var_max()))
    norm = shrink_to_top_down_reachable_2(norm)
    norm.reformat_states()

    bdd = ubda_folding(norm, box_orders["bdd"], norm.get_var_max())
    print("bdd", len([i for i in iterate_states_bfs(bdd)]))
    zbdd = ubda_folding(norm, box_orders["zbdd"], norm.get_var_max())
    print("zbdd", len([i for i in iterate_states_bfs(zbdd)]))
    tbdd = ubda_folding(norm, box_orders["tbdd"], norm.get_var_max())
    print("tbdd", len([i for i in iterate_states_bfs(tbdd)]))
    cbdd = ubda_folding(norm, box_orders["cbdd"], norm.get_var_max())
    print("cbdd", len([i for i in iterate_states_bfs(cbdd)]))
    czdd = ubda_folding(norm, box_orders["czdd"], norm.get_var_max())
    print("czdd", len([i for i in iterate_states_bfs(czdd)]))
    esrbdd = ubda_folding(norm, box_orders["esr"], norm.get_var_max())
    print("esr", len([i for i in iterate_states_bfs(esrbdd)]))
    abdd = ubda_folding(norm, box_orders["full"], norm.get_var_max())
    print("full", len([i for i in iterate_states_bfs(abdd)]))


if __name__ == "__main__":
    START = 4
    CUTOFF = 10
    for i in range(START, CUTOFF):
        print(f"../benchmark/bdds/queens/queens-{i}-output.bdd")
        run_nqueens_benchmark(f"../benchmark/bdds/queens/queens-{i}-output.bdd")


# End of file nqueens.py
