from typing import Optional
from canonization.folding_helpers import FoldingHelper
from helpers.string_manipulation import tuple_name
from helpers.utils import box_catalogue, box_orders
from canonization.folding import box_finding
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_edges_from_state
from tree_automata.transition import TEdge, TTransition


def try_all_boxes(treeaut, state, var, helper) -> tuple[Optional[str], list[tuple[str, int]]]:
    map: dict[str, tuple[str, int]] = {}
    for b in box_orders["cesr"]:
        box = box_catalogue[b]
        try:
            map = box_finding(treeaut, box, state, helper, "")
        except:
            map = {}
        if map != {}:
            targets = [map[p] for (p, _) in box.get_port_order()]
            # print(f'box_finding({state}, {var}) = {b}, {targets}')
            return b, targets
    # print(f'box_finding({state}, {var}) = None, [({state}, {var})]')
    return None, [(state, var)]


def new_fold(treeaut: TTreeAut, varmax: int) -> TTreeAut:
    helper = FoldingHelper(treeaut, varmax)
    result = TTreeAut([], {}, f"fold({treeaut.name})", 0)
    prefix = treeaut.get_var_prefix()
    rootrule, roots = try_all_boxes(treeaut, treeaut.roots[0], 1, helper)
    result.rootbox = rootrule
    result.roots = [tuple_name(r) for r in roots]
    worklist = [r for r in roots]
    edgecount = 0
    visited: set[tuple[str, int]] = set()
    for state, symbols in treeaut.get_output_edges(inverse=True).items():
        result.transitions[tuple_name((state, varmax))] = {}
        for s in symbols:
            result.transitions[tuple_name((state, varmax))][f"k{edgecount}"] = TTransition(
                tuple_name((state, varmax)), TEdge(s, [], f"{prefix}{varmax}"), []
            )
            edgecount += 1
        visited.add((state, varmax))
    while worklist != []:
        s, var = worklist.pop(0)
        # print('worklist popped', s, var)
        if (s, var) in visited:
            continue
        edge = None
        # pick the edge to fold
        for e in iterate_edges_from_state(treeaut, s):
            # if proper outedge found, pick that
            if e.info.variable == f"{prefix}{var}":
                edge = e
        # otherwise choose self-loop -> NOTE: in case multiple self-loops are possible, not sure what to do
        if edge is None:
            for e in iterate_edges_from_state(treeaut, s):
                if e.is_self_loop():
                    edge = e
        # print(f'folding on edge {edge}')
        lowrule, lowtargets = try_all_boxes(treeaut, edge.children[0], var + 1, helper)
        # print('low =', lowrule, lowtargets)
        highrule, hightargets = try_all_boxes(treeaut, edge.children[1], var + 1, helper)
        # print('high =', highrule, hightargets)
        if s not in result.transitions:
            result.transitions[tuple_name((s, var))] = {}
        result.transitions[tuple_name((s, var))][f"k{edgecount}"] = TTransition(
            tuple_name((s, var)),
            TEdge("LH", [lowrule, highrule], f"{prefix}{var}"),
            [tuple_name(t) for t in lowtargets + hightargets],
        )
        edgecount += 1
        worklist.extend(lowtargets)
        worklist.extend(hightargets)
        visited.add(s)
    return result


def divide_multivar_states(treeaut: TTreeAut):
    varvis = treeaut.get_var_visibility()
    lookup = treeaut.get_var_lookup()
    # we first find all bad states (along with the list of outvars)
    badstates = {}
    for s, vars in varvis.items():
        if len(vars) > 1:
            badstates[s] = vars

    for s, vars in badstates.items():
        # we create multiple copies of bad states -> one for each variable
        for v in vars:
            newstate = f"{s}({lookup[v]})"
            treeaut.transitions[newstate] = {}
            for key, edge in treeaut.transitions[s].items():
                if edge.info.variable != "" and edge.info.variable != v:
                    continue
                treeaut.transitions[newstate][key] = TTransition(
                    newstate,
                    TEdge(edge.info.label, [], edge.info.variable),
                    [c if c != s else newstate for c in edge.children],
                )

        # then we find all edges leading to the bad state -> along with the edge source outvar

        edges_to_fix = []
        for edge in iterate_edges(treeaut):
            if edge.src != s and s in edge.children:
                # edges_to_fix.append(edge)
                target_var = max(lookup[v] for v in varvis[edge.src])
                out_var = sorted([lookup[v] for v in vars])
                for i in out_var:
                    if target_var < i:
                        new = [f"{s}({i})" if c == s else c for c in edge.children]
                        edge.children = new

        # remove the original bad state
        treeaut.remove_state(s)
