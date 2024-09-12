from itertools import product

from tree_automata import TTreeAut, iterate_edges
from tree_automata.functions.helpers import generate_possible_children
from tree_automata.functions.emptiness import non_empty_bottom_up
from tree_automata.functions.reachability import reachable_top_down, reachable_bottom_up


# One of the rule-checks for a well-defined tree automaton (box).
#  Implements bottom-up search and keeps information about all reachable port
#  combinations from a given state.
#
#  Each root state has to be able to reach a precise amount of ports, which is
#  given by TAs port-arity.
def port_consistency_check(ta: TTreeAut) -> bool:

    # Helper function, creates a list of sets,
    # which correspond to all possible reachable combinations of ports
    # (or output symbols) from a given list of states.
    # Also takes a current state of port dictionary for looking up data.
    #
    #   - port_dict = dictionary of reachable ports from each state
    #   - state_list = list of states, from which reachable ports are searched
    def create_port_set(port_dict: dict, state_list) -> set:
        all_set_lists = []
        for i in state_list:
            all_set_lists.append(port_dict[i])
        # create cartesian product of setlists
        # => list of tuples of lists of sets
        tuple_list = product(all_set_lists, repeat=len(all_set_lists))
        result = []
        for tuple in tuple_list:  # iterate over each tuple of lists of sets
            for set_list in tuple:  # iterate over each list of sets:
                union_set = set()  # create a union of each set from the setlist
                for unit_set in set_list:  # iterate over each set
                    union_set |= unit_set
                if union_set not in result:
                    result.append(union_set)
        return result

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # initialization phase
    worklist = ta.get_output_states()
    done = {}
    arity_dict = ta.get_symbol_arity_dict()
    for symbol, state_list in ta.get_output_edges().items():
        if not symbol.startswith("Port"):
            continue
        for state in state_list:
            if state not in done:
                done[state] = []
            if symbol not in done[state]:
                done[state].append(set([symbol]))

    # bottom-up parsing phase
    while len(worklist) > 0:
        state = worklist.pop()
        if state in ta.roots and state in done:
            if len(done[state]) != ta.port_arity:
                return False
        for symbol, arity in arity_dict.items():
            if arity_dict[symbol] == 0:
                continue
            # all possible combinations of children with 'state' in there
            tuples = generate_possible_children(state, list(done), arity)

            # for edge.src, edgeDict in ta.transitions.items():
            #     for edge in edgeDict.values():
            for edge in iterate_edges(ta):
                if edge.info.label != symbol or edge.children not in tuples:
                    continue
                if edge.src not in done:
                    done[edge.src] = []
                    worklist.append(edge.src)
                port_set = create_port_set(done, edge.children)
                for i in port_set:
                    if i not in done[edge.src]:
                        done[edge.src].append(i)
    return True


def is_well_defined(ta: TTreeAut, display_errors=False) -> bool:

    conditions = {
        "1-non-emptiness": True,
        "2-trimness": True,
        "3-port-consistency": True,
        "4-root-uniqueness": True,
        "5-non-vacuity": True,
        "6-port-uniqueness": True,
        "7-unambiguity": True,
    }

    # 1) Non-emptiness  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    witness_tree, witness_str = non_empty_bottom_up(ta)
    if witness_tree is None or witness_str == "":
        conditions["1-non-emptiness"] = False

    # 2) Trimness - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    all_states = ta.get_states()
    if set(reachable_bottom_up(ta)) != set(all_states) or set(reachable_top_down(ta)) != set(all_states):
        conditions["2-trimness"] = False

    # 3) Port consistency - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if not port_consistency_check(ta):
        conditions["3-port-consistency"] = False

    # 4) Root-uniqueness  - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if len(ta.roots) != 1:
        conditions["4-root-uniqueness"] = False

    # 5) Non-vacuity  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for i in ta.roots:
        edges_from_root = ta.transitions[i]
        for edge in edges_from_root.values():
            if len(edge.children) == 0 and edge.info.label.startswith("Port"):
                conditions["5-non-vacuity"] = False

    # 6) Port-uniqueness  - - - - - - - - - - - - - - - - - - - - - - - - - - -
    output_edges = ta.get_output_edges()
    port_counter = 0
    for symbol in output_edges:
        if symbol.startswith("Port"):
            port_counter += 1
            if len(output_edges[symbol]) != 1:
                conditions["6-port-uniqueness"] = False
    if port_counter != ta.get_port_arity():
        conditions["6-port-uniqueness"] = False

    # 7) Unambiguity TODO - - - - - - - - - - - - - - - - - - - - - - - - - - -
    sth = False
    if sth:
        conditions["7-unambiguity"] = True

    # Final processing  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    result = True
    error_msg = f"   > is_well_defined('{ta.name}'): failed conditions = "
    for condition, value in conditions.items():
        if value is False:
            error_msg += f"{condition} "
            result = False
    if not result and display_errors:
        print(error_msg)
    return result
