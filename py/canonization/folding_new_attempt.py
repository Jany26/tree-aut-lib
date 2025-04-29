import re
from typing import Optional, Iterator
import copy

from canonization.folding_helpers import FoldingHelper, fill_box_arrays
from helpers.string_manipulation import tuple_name
from helpers.utils import box_catalogue, box_orders, box_arities
from canonization.folding import box_finding, mapping_is_correct
from tree_automata.automaton import TTreeAut, iterate_edges, iterate_edges_from_state, iterate_states_bfs
from tree_automata.functions.trimming import remove_useless_states, shrink_to_top_down_reachable_2
from tree_automata.transition import TEdge, TTransition


# NOTE: Perhaps this should be scrapped
# folding should explore all states with for specific box,
# going over all boxes for one state can affect the rest of the structure, denying
# proper folding for better suited boxes,
# especially for LPort/HPort boxes


def new_fold(ta: TTreeAut, initboxes: list[str], afterboxes: list[str], max_var: int) -> TTreeAut:
    fold = new_fold_terminal(ta, initboxes, max_var)
    new_fold_inner(fold, afterboxes, max_var)
    return shrink_to_top_down_reachable_2(fold)


def iterate_edge_parts(
    obj: TTreeAut, state: str, keep_loops=False, keep_folded=False, keep_nonvar=True, cut_reductions=False
) -> Iterator[tuple[TTransition, int]]:
    """
    Used in folding, this returns tuples of (TTransition, child-index),
    while skipping self-looping edges, edges unmarked with variables,
    or children that are targets of a box reduction, or
    """

    for edge in obj.transitions[state].values():
        if any(
            [edge.children == [], not keep_loops and edge.is_self_loop(), not keep_nonvar and edge.info.variable == ""]
        ):
            continue

        if keep_folded:
            for idx, child in enumerate(edge.children):
                yield edge, idx
        else:
            for idx, box in enumerate(edge.info.box_array):
                if box is None:
                    child_idx = sum([box_arities[edge.info.box_array[i]] for i in range(idx)])
                    if cut_reductions:
                        has_non_reduced_edge = False
                        for edge in iterate_edges_from_state(obj, edge.children[child_idx]):
                            if not edge.is_all_boxed():
                                has_non_reduced_edge = True
                        if not has_non_reduced_edge:
                            continue
                    yield edge, child_idx


# alternative version => loop1: iterate over states BFS ( loop2: iterate over boxes )
def ubda_folding_new(ta: TTreeAut, boxes: list[str], max_var: int):
    result: TTreeAut = copy.deepcopy(ta)
    fill_box_arrays(result)
    helper: FoldingHelper = FoldingHelper(ta, max_var)

    worklist: list[str] = [r for r in ta.roots]
    visited: set[str] = set()
    # states are explored in a BFS-like manner
    while worklist != []:
        state: str = worklist.pop(0)
        if state in visited:
            continue
        # not sure if we want to skip leaves, probably yes
        if state in result.get_output_states():
            continue
        # we find the best fit for reduction
        for e, cidx in iterate_edge_parts(result, state):
            for box in [box_catalogue[n] for n in boxes]:
                childstate = e.children[cidx]
                helper.min_var = int(e.info.variable[len(helper.var_prefix) :]) + 1
                mapping = box_finding(result, box, childstate, helper, state)
                if not mapping_is_correct(mapping, helper.state_var_map, helper.var_prefix):
                    helper.write("mapping_is_correct(): FALSE")
                    continue

                # phase 1: putting the box in the box array
                initial_box_list: list[Optional[str]] = e.info.box_array
                symbol = e.info.label
                box_list = [None] * ta.get_symbol_arity_dict()[symbol]
                for idx in range(len(initial_box_list)):
                    box_list[idx] = initial_box_list[idx]
                box_list[0 if cidx == 0 else 1] = box.name.replace("box", "")
                e.info.box_array = box_list

                # phase 2: fill the box-port children in the child array
                e.children.pop(cidx)
                for i, (map_state, var) in enumerate(mapping.values()):
                    e.children.insert(cidx + i, map_state)
                    # if var == helper.state_var_map[map_state]:
                    #     # NOTE: here, possibly remove self-loop(s) in map_state
                    #     # in case of identical variables (ta, intersectoid)
                    #     continue

        # update worklist and visited
        visited.add(state)
        for e in iterate_edges_from_state(result, state):
            for child in e.children:
                if child not in visited:
                    worklist.append(child)
    # end while

    # after folding, particularly after folding HPort and LPort boxes, the port-mapped states
    # can still contain self-looping transitions, which are unnecessary in the ABDD-context, so we can remove them

    result.remove_self_loops()

    match = re.search(r"\(([^()]*)\)", result.name)
    result.name = f"folded({ta.name if match is None else match.group(1)})"
    # return result
    return remove_useless_states(result)


def try_all_boxes(treeaut, state, var, boxes, helper) -> tuple[Optional[str], list[tuple[str, int]]]:
    map: dict[str, tuple[str, int]] = {}
    for b in boxes:
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


# OR: perhaps we apply the "terminal" boxes first,
# and then try reducing all patterns using the X, Lport, Hport boxes
def new_fold_terminal(treeaut: TTreeAut, boxes: list[str], varmax: int) -> TTreeAut:
    helper = FoldingHelper(treeaut, varmax)
    result = TTreeAut([], {}, f"fold({treeaut.name})", 0)
    prefix = treeaut.get_var_prefix()
    rootrule, roots = try_all_boxes(treeaut, treeaut.roots[0], 1, boxes, helper)
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
        # print(f"folding: state={s}, var={var}, edge={edge}")
        lowrule, lowtargets = try_all_boxes(treeaut, edge.children[0], var + 1, boxes, helper)
        # print('low =', lowrule, lowtargets)
        highrule, hightargets = try_all_boxes(treeaut, edge.children[1], var + 1, boxes, helper)
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
        visited.add((s, var))
    return shrink_to_top_down_reachable_2(result)


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


def box_finding_wrapper(treeaut: TTreeAut, state: str, var: int, box: TTreeAut, helper: FoldingHelper):
    map: dict[str, tuple[str, int]] = {}
    try:
        map = box_finding(treeaut, box, state, helper, "")
    except:
        map = {}
    if map != {}:
        targets = [map[p] for (p, _) in box.get_port_order()]
        print(f'box_finding({state}, {var}) = {box.name.replace("box", "")}, {targets}')
        return box.name.replace("box", ""), targets
    # print(f'box_finding({state}, {var}) = None, [({state}, {var})]')
    return None, [(state, var)]


def new_fold_inner(treeaut: TTreeAut, boxes: list[str], varmax: int) -> None:
    helper = FoldingHelper(treeaut, varmax)
    varvis = treeaut.get_var_visibility_deterministic()
    if treeaut.rootbox is None:
        rootrule, roots = try_all_boxes(treeaut, treeaut.roots[0], 1, boxes, helper)
        treeaut.rootbox = rootrule
        treeaut.roots = [r[0] for r in roots]
    for s in iterate_states_bfs(treeaut):
        for edge, idx in iterate_edge_parts(treeaut, s):
            rule, targets = try_all_boxes(treeaut, edge.children[idx], varvis[s], boxes, helper)
            if rule is None:
                continue
            edge.info.box_array[int(bool(idx))] = rule
            edge.children.pop(idx)
            if idx == 0:
                edge.children = [t[0] for t in targets] + edge.children
            else:
                edge.children = edge.children + [t[0] for t in targets]
