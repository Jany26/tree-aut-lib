"""
[file] folding.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] All top-level important folding procedures.
"""

import re
import copy
import os
from typing import Iterator, List, Dict, Optional, Set, Tuple

from formats.render_dot import export_to_file
from tree_automata import TTreeAut, TTransition, TEdge, iterate_edges, non_empty_bottom_up, iterate_edges_from_state
from tree_automata.functions.trimming import trim
from canonization.folding_helpers import (
    FoldingHelper,
    get_first_name_from_tuple_str,
    is_already_reduced,
    prepare_edge_info,
    get_state_index_from_box_index,
    fill_box_arrays,
)
from canonization.folding_intersectoid import (
    create_intersectoid,
    intersectoid_reachability,
    reduce_portable_states,
    add_variables_top_down,
)
from helpers.utils import box_catalogue, box_arities


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Main Folding algorithm functions:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_state_witness_relation(intersectoid: TTreeAut, port: str):
    """
    [description]
    Analyzes the intersectoid and gets states that are related to each other.
    That states are in relation if they in every tree of the intersectoid
    language there are all of or none of the related states.

    States s1 and s2 from the set of states Q of (TA) intersectoid I are
    related iff for every tree T in L(I) (s1 in T iff s2 in T).

    This relation is equivalence relation so the "neighbouring" or "related"
    states form partitions -> this function analyzes the properties of the
    transition function and returns the partitions of states.

    [parameters]
    'intersectoid' - TA/UBDA that is analyzed
    'port' - with regards to which port is the relation computed

    [return]
    Relation describing partitions of states that are always encountered together.
    """

    def is_edge_unified(children: List) -> bool:
        return len(set(children)) <= 1

    def get_relation_step(state: str, intersectoid: TTreeAut):
        res: List[Set[str]] = []

        for edge in intersectoid.transitions[state].values():
            if edge.src in edge.children:
                continue
            if len(edge.children) == 0:
                if edge.info.label == port:
                    return [set([edge.src])]
                continue

            if is_edge_unified(edge.children):
                res.extend(get_relation_step(edge.children[0], intersectoid))
                continue

            sub_result: Set[str] = set()
            for child in edge.children:
                for child_set in get_relation_step(child, intersectoid):
                    sub_result = sub_result.union(child_set)

            res.append(sub_result)
        return res

    result: List[Set[str]] = []
    for root in intersectoid.roots:
        result.extend(get_relation_step(root, intersectoid))
    return result


def get_mapping(intersectoid: TTreeAut, varvis: Dict[str, int], reach: Dict[str, Set[str]]) -> Dict[str, str]:
    """
    [description]
    This function finds all different port types in intersectoid and assigns
    one state from the original ta to be mapped to the port.
    It uses a reachability relation (similar to Floyd-Warshall algorithm) to
    determine the state that is "infimum" wrt. reachability, i.e. a state 'q',
    that can be reached from all 'suspect' states (1) of the particular port and no
    'suspect' state can reach the state 'q'. If no such state exists, mapping
    fails and thus no box folding should be applied.

    [parameters]
    'interesctoid' - contains states with output port transitions, for each
    different port type (2), one state will be chosen as the mapped state,
    according to the reachability relation, such that the chosen state will
    "cover" the biggest pattern of the folded TA, while not changing semantics

    'reach' - reachability dict - for each state a set of reachable states,
    reachability comparison is necessary for getting "maximum" mapping wrt. the
    semantics of the original unfolded tree automaton

    [return]
    port-state mapping dictionary, ports are keys, mapped states from the
    intersectoid (3) are values

    [notes]
    (1) 'suspect' states (a,b) from the intersectoid contain a Port output
    transition. (state 'a' from the original TA is compared wrt. the reachability)
    (2) amount of different port types is determined by the port arity
    of the box used in creation of the intersectoid
    (3) state names are in the format (s1,s2), where s1 comes from the treeaut
    and s2 comes from the box that was used during intersectoid creation)
    """
    ports: Set[str] = set(
        [edge.info.label for edge in iterate_edges(intersectoid) if edge.info.label.startswith("Port")]
    )
    # varvis = intersectoid.get_var_visibility_cache()
    mapping: Dict[str, str] = {}  # port_name -> state_name
    for port in ports:
        relation: list[tuple[int, set[str]]] = [
            (varvis[list(s)[0]], s) for s in get_state_witness_relation(intersectoid, port)
        ]
        relation.sort(reverse=True)  #
        for var, stateset in relation:
            skip: bool = False
            for state in stateset:
                s: str = get_first_name_from_tuple_str(state)
                infimum: bool = True
                for state2 in stateset:
                    if state == state2:
                        continue
                    s2: str = get_first_name_from_tuple_str(state2)
                    if s in reach[s2] and not s2 in reach[s]:
                        continue
                    else:
                        infimum = False
                if infimum:
                    mapping[port] = state
                    skip = True
                    break
            if skip:
                break
        if port not in mapping:
            return {}
    return mapping


def box_finding(
    ta: TTreeAut, box: TTreeAut, root: str, helper: FoldingHelper, source: str
) -> Dict[str, Tuple[str, int]]:
    """
    [description]
    Main implementation of one step of the folding procedure.
    Function tries to apply tree automaton reduction starting from the specific
    state in the normalized (and well-specified) UBDA.

    [parameters]
    'ta' - UBDA on which we try to apply reduction
    'box' - specifies which tree automaton should be applied
    'root' - which state is the starting point of the procedure (child node)
    'helper' - FoldingHelper class with additional context information, debugging/exporting, etc.
    'source' - source node of the edge that will contain the reduction box

    [return]
      - dictionary which specifies mapping of the output ports of the 'box'
        TA to the states of the initial 'ta' (UBDA)
      - if no mapping is found, empty dictionary {} is returned
    """
    intersectoid: TTreeAut = create_intersectoid(ta, box, root, helper)
    intersectoid = trim(intersectoid)  # additional functionality maybe needed?
    tree, _ = non_empty_bottom_up(intersectoid)
    if tree is None:
        return {}

    add_variables_top_down(intersectoid, helper)
    helper.export_intersectoid(intersectoid, source, root, box.name)
    var_visibility: dict[str, int] = intersectoid.get_var_visibility_deterministic()
    reach: list[str] = intersectoid_reachability(intersectoid, var_visibility)
    intersectoid.shrink_tree_aut(reach)
    if intersectoid.get_port_arity() > 1:
        reduce_portable_states(intersectoid)
        intersectoid = trim(intersectoid)
    final_mapping: dict[str, str] = get_mapping(intersectoid, var_visibility, helper.reach)
    if final_mapping == {}:
        return {}
    # export_to_file(intersectoid, f"./debug-intersectoids/{root}-{box.name.replace("box", "")}-intersectoid")
    split_mapping: dict[str, str] = {
        p: (get_first_name_from_tuple_str(s), var_visibility[s]) for p, s in final_mapping.items()
    }
    # mapping in which root state is one of ports is invalid
    # for s, var in split_mapping.values():
    #     if root == s:
    #         return {}
    # print(f"box_finding({box.name.replace("box", "")}, {root}) = {split_mapping}")
    return split_mapping


def mapping_is_correct(mapping: dict[str, str], var_visibility: dict[str, int]) -> bool:
    """
    [description]
    Checks if the mapped states and variables they see are consistent.
    If not, the mapping is not correct and thus folding fails for that particular
    iteration.
    """
    if mapping == {}:
        return False
    bigger_var: bool = False
    none_var: bool = False
    for i, (map_state, var) in enumerate(mapping.values()):
        if var == "":
            none_var = True
        original_var: int = int(var_visibility[map_state])
        intersectoid_var: int = int(var)
        if intersectoid_var > original_var:
            bigger_var = True
    if bigger_var or none_var:
        return False
    return True


def get_box_index(edge_part: Tuple[str, int, str, str, TTransition]) -> int:
    """
    [description]
    Since children list of transitions is merged and does not have to be
    consistent with the arity of the symbol on transition (and is also related)
    to the box arities used on the transition parts,
    this function computes the starting child index of the states related
    to the edge_part child-index.
    """
    # edge_part contains 5 items: [key, child-index, child-state, source-state, edge]
    key, chidx, child, src, edge = edge_part
    current_idx: int = 0

    for idx, box in enumerate(edge.info.box_array):
        if current_idx == chidx:
            return idx
        if box == None:
            current_idx += 1
        else:
            current_idx += box_catalogue[box].port_arity
    return current_idx


def ubda_folding(
    ta: TTreeAut,
    boxes: List[str],
    max_var: int,
    verbose: bool = False,
    export_vtf: bool = False,
    export_png: bool = False,
    output: Optional[str] = None,
    export_path: Optional[str] = None,
) -> TTreeAut:
    """
    [description]
    Main function implementing process of folding.
    Applying separate folding steps implemented in box_finding() function.
    Respects the chosen box order.

    [parameters]
    'ta' - UBDA that we want to apply folding on,
    'boxes' - ordered list of box names, which can be used to reduce the 'ta'

    [return]
    (folded) UBDA with applied reductions (same language as the input)
    """
    result: TTreeAut = copy.deepcopy(ta)
    fill_box_arrays(result)  # in case of [None, None] and [] discrepancies
    helper: FoldingHelper = FoldingHelper(ta, max_var, verbose, export_vtf, export_png, output, export_path)
    # print(helper)
    if helper.vtf or helper.png:
        if not os.path.exists(f"{helper.path}/ubdas/"):
            os.makedirs(f"{helper.path}/ubdas/")
        if not os.path.exists(f"{helper.path}/intersectoids/"):
            os.makedirs(f"{helper.path}/intersectoids/")
    var_visibility = helper.state_var_map
    # print(var_visibility)
    for box_name in boxes:
        box: TTreeAut = box_catalogue[box_name]
        worklist: List[str] = [root for root in ta.roots]
        visited: Set[str] = set()
        while worklist != []:
            state: str = worklist.pop(0)
            if state in visited:
                continue
            # TODO: simplify working with edge info -> just use the variable names listed below
            edges_to_children: List[Tuple[str, int, str, str, TTransition]] = prepare_edge_info(result, state)
            for edge_part in edges_to_children:
                # edge_part contains 5 items: [
                # key :
                # child-index :
                # child-state :
                # source-state :
                # edge :
                # ]

                # work_key
                # child_index
                # source_state
                # target_state
                key, chidx, chstate, srcstate, edgeref = edge_part

                part = "L" if chidx == 0 else "H"
                if is_already_reduced(result, state, edge_part):
                    continue
                helper.min_var = int(edgeref.info.variable[len(helper.var_prefix) :]) + 1

                # skipping self-loop
                if state in result.transitions[state][key].children:
                    continue
                if helper.verbose:
                    print("%s> box_finding(%s-[%s:%s]->%s)" % (f"{0 * ' '}", state, part, box.name, edge_part[2]))
                mapping = box_finding(result, box, chstate, helper, state)

                # phase 0: checking correctness of the mapping
                # checking if all mapped states have a visible variable
                # and have lower variables than states in the UBDA
                if not mapping_is_correct(mapping, var_visibility):
                    helper.write("mapping_is_correct(): FALSE")
                    continue
                helper.write(
                    "%s> box_finding(%s-[%s:%s]->%s => %s)\n"
                    % (f"{0 * ' '}", state, "L" if edge_part[1] == 0 else "H", box.name, chstate, mapping)
                )
                # print(f"box_finding({chstate} {box_name}) = {mapping})")

                # phase 1: putting the box in the box array
                edge = result.transitions[srcstate][key]
                # initial_box_list: List[str] = edge.info.box_array
                # symbol = edge.info.label
                # box_list = [None] * ta.get_symbol_arity_dict()[symbol]
                # for idx in range(len(initial_box_list)):
                #     box_list[idx] = initial_box_list[idx]
                # try:
                #     box_list[get_box_index(edge_part)] = box_name
                # except:
                #     continue
                # edge.info.box_array = box_list
                edge.info.box_array[1 if chidx > 0 else 0] = box_name

                # phase 2: fill the box-port children in the child array
                edge.children.pop(chidx)
                targets = [mapping[p] for (p, _) in box.get_port_order()]
                if chidx == 0:
                    edge.children = [t[0] for t in targets] + edge.children
                else:
                    edge.children = edge.children + [t[0] for t in targets]
                # idx = get_state_index_from_box_index(edge, get_box_index(edge_part))
                # edge.children.pop(idx)
                # for i, (map_state, var) in enumerate(mapping.values()):
                #     edge.children.insert(idx + i, map_state)
                #     if var == var_visibility[map_state]:
                #         # NOTE: here, possibly remove self-loop(s) in map_state
                #         # in case of identical variables (ta, intersectoid)
                #         continue
                #     new_state: str = f"{map_state}-{var}"
                #     if new_state in result.transitions:
                #         edge.children[idx + i] = new_state
                #     result.transitions[new_state] = {}
                #     edge.children[idx + i] = new_state
                #     new_edge = TTransition(new_state, TEdge("LH", [], f"{var+1}"), [map_state, map_state])
                #     var_visibility[new_state] = var
                #     helper.counter += 1
                #     key: str = f"temp_{helper.counter2}"
                #     helper.counter2 += 1
                #     result.transitions[new_state][key] = new_edge
                # for state in mapping
                helper.export_ubda(result, state, edge_part, box)
            # for edge_info
            visited.add(state)
            for edge in iterate_edges_from_state(result, state):
                for child in edge.children:
                    if child not in visited:
                        worklist.append(child)
            # worklist update
        # while worklist != []

    match = re.search(r"\(([^()]*)\)", result.name)
    result.name = f"folded({ta.name if match is None else match.group(1)})"
    return result


# End of folding.py
