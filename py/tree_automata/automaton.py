import copy
from typing import Generator, Tuple

from tree_automata.transition import TEdge, TTransition


# Tree automaton class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - has two attributes = dictionary of states and root state array
#     transitions = dict (A) of dicts (B) referenced by state name
#     inner dicts (B) are then referenced by transition names (arbitrary)
#     the transition itself is then just a tuple of:
#         - input state,
#         - edge object (edge label, edge boxes, edge variable label)
#         - array of output states (size of array = arity of the node)
#     * all state and label names are considered as strings
#
#     In documentation, the naming convention will be:
#     - TTreeAut consists of: array of root states and "state" dictionary
#     - state dictionaries are referenced by names of the states
#     - each state in the state dictionary references another dictionary
#         - this will be called "transition" dictionary (for the current state)
#         - the transition dictionary is referenced by arbitrary keys (for now)
class TTreeAut:
    def __init__(
        self, roots: list[str], transitions: dict[str, dict[str, TTransition]], name: str, port_arity: int = 0
    ):
        self.roots: list[str] = roots
        self.transitions: dict[str, dict[str, TTransition]] = transitions
        self.name: str = name
        self.port_arity: int = port_arity
        if self.port_arity == 0:
            self.port_arity = self.get_port_arity()
        # this parameter is only for formatted printing with edge-keys
        self.print_keys: bool = True
        self.meta_data: TTreeAutMetaData = TTreeAutMetaData(self)

    def __repr__(self):
        # printing tree automaton header
        result = ""
        # result = "-" * 78 + '\n'
        result += f"  [TreeAut]: '{self.name}'\n"
        result += f"  > Root States = {self.roots}\n"

        src_str = "source"
        edge_str = "edge"
        child_str = "child #"
        key_str = "key"

        # computing lengths
        self.meta_data.recompute()
        src_len = max(len(src_str), self.meta_data.state)
        edge_len = max(len(edge_str), self.meta_data.edge)
        child_len = max(len(child_str), self.meta_data.child)
        key_len = max(len(key_str), self.meta_data.key)

        # printing edge table header
        result += "  > %-*s -- %-*s --> " % (src_len, src_str, edge_len, edge_str)
        for i in range(self.meta_data.arity):
            result += "%-*s  " % (child_len, f"{child_str[:-2]} {i + 1}")
        if self.print_keys:
            result += "  %-*s" % (key_len, key_str) + "\n"
            result += "  " + "-" * sum([src_len, edge_len, key_len, child_len * self.meta_data.arity, 17]) + "\n"
        else:
            result = result[:-2] + "\n"
            result += "  " + "-" * sum([src_len, edge_len, child_len * self.meta_data.arity, 13]) + "\n"

        # printing edges
        for state in iterate_states_bfs(self):
            for k, e in self.transitions[state].items():
                # note = " <<< LEAF TRANSITION >>>" if e.children == [] else ""
                # result += f"  > {e.src} -- {e.info} --> {e.children}{note}\n"
                result += "  > %-*s -- %-*s" % (src_len, e.src, edge_len, e.info)
                if len(e.children) != 0:
                    result += " --> "
                    for i in e.children:
                        result += "%-*s  " % (child_len, i)
                    result = result[:-2]
                else:
                    result += " " * (self.meta_data.arity * child_len + 7)
                if self.print_keys:
                    result += "  : %-*s" % (key_len, k)
                result += "\n"
        # result = "-" * 78 + '\n'
        return result[:-1]  # trim the last '\n'

    # Check if two TAs are equivalent... NOTE: wip
    # An attempt to create an on-the-fly isomorphism check.
    def __eq__(self, ta):
        # unique counter value will be used to compare states
        # states will be stored in two separate hash-maps, values will be counters
        # need to compare child counts,
        # different, 'redundant' edges are stored in two separate places (maybe no)
        if len(self.roots) != len(ta.roots):
            return False
        state_mapper: dict[str, (str, str)] = {}
        pass

    def get_edge_string(self, edge: TTransition) -> str:
        result = ""
        result += "%-*s -- %-*s" % (self.meta_data.state, edge.src, self.meta_data.edge, edge.info)
        if len(edge.children) != 0:
            result += " --> "
            for i in edge.children:
                result += "%-*s  " % (self.meta_data.child, i)
        if self.print_keys is True:
            for k, e in self.transitions[edge.src].items():
                if str(edge) == str(e):
                    result += "  : %-*s" % (self.meta_data.key, k)
        return result

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Informative functions # - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def get_states(self) -> list:
        result = set()
        for state_name in self.roots:
            result.add(state_name)
        for state_name, edges in self.transitions.items():
            result.add(state_name)
            for data in edges.values():
                for i in data.children:
                    result.add(i)
        result = list(result)
        # result.sort()
        return state_name_sort(result)

    # needed for feeding make_prefix() function
    # generates all edge symbols labeling the output edges from the TA
    def get_output_symbols(self) -> list[str]:
        result = []
        for edge in iterate_edges(self):
            if len(edge.children) == 0:
                result.append(edge.info.label)
        return result

    # needed for feeding tree_aut_determinize() function
    # generates a dictionary of all output edge symbols
    # which correspond to a list of states,
    # from which the transitions with the specific symbol originate
    def get_output_edges(self, inverse=False) -> dict[str, list[str]]:
        result = {}
        for edge in iterate_edges(self):
            if len(edge.children) != 0:
                continue
            if inverse:
                if edge.src not in result:
                    result[edge.src] = []
                result[edge.src].append(edge.info.label)
            else:
                if edge.info.label not in result:
                    result[edge.info.label] = []
                result[edge.info.label].append(edge.src)
        for item in result.values():
            item.sort()
        return result

    # needed for bottom-up reachability -> used in useless state removal
    def get_output_states(self) -> list[str]:
        result = []
        for state_name, edges in self.transitions.items():
            for data in edges.values():
                if len(data.children) == 0:
                    result.append(state_name)
                    break
        return result

    def get_symbol_arity_dict(self) -> dict[str, int]:
        result = {}
        for edges in self.transitions.values():
            for edge in edges.values():
                if edge.info.label not in result:
                    if edge.info.box_array == []:
                        result[edge.info.label] = len(edge.children)
                    else:
                        result[edge.info.label] = len(edge.info.box_array)
        return result

    def get_port_arity(self) -> int:
        port_set = set()
        for edge in iterate_edges(self):
            sym = edge.info.label
            if sym.startswith("Port"):
                port_set.add(sym)
        return len(port_set)

    def is_top_down_deterministic(self) -> bool:
        for edges in self.transitions.values():
            used_symbols = set()
            for e in edges.values():
                if e.info.label in used_symbols:
                    return False
                used_symbols.add(e.info.label)
        return True

    def get_var_order(self) -> list:
        vars = set()
        for edge in iterate_edges(self):
            vars.add(edge.info.variable)
        if "" in vars:
            vars.remove("")
        vars = list(vars)
        vars = state_name_sort(vars)
        return vars

    def get_var_prefix(self) -> str:
        """Returns largest prefix of a variable in a TA,
        that does not contain only numeric symbols.

        Examples:
            'x1' - returns 'x'
            'var5ta01 - returns 'var5ta'
        """
        for edge in iterate_edges(self):
            if edge.info.variable != "":
                prefix_len = 0
                for i in range(len(edge.info.variable)):
                    if not edge.info.variable[i:].isnumeric():
                        prefix_len += 1
                return edge.info.variable[:prefix_len]
        return ""

    def count_edges(self) -> int:
        counter = 0
        for _ in iterate_edges(self):
            counter += 1
        return counter

    def count_boxes(self) -> int:
        boxes = 0
        for edge in iterate_edges(self):
            for box in edge.info.box_array:
                if box is not None and box != "_":
                    boxes += 1
        return boxes

    # Returns a map of states to number of edges starting in that state.
    def get_edge_counts(self) -> dict[str, int]:
        return {s: len(e) for s, e in self.transitions.items()}

    # Returns a dictionary of states, each of which has a set of variables,
    # that the state can "see" = i.e. the state has a transition with
    # this variable. e.g. {'q0': {'x1', 'x2'}, 'q1': {'x5'}}
    # if reverse==True: the dictionary is referenced by variables, and values
    # are lists of states. e.g. {'x1': {'q0'}, 'x2': {'q0'}, 'x5': {'q1'}}
    def get_var_visibility(self, reverse=False) -> dict:
        result: dict[str, set] = {}
        for edge in iterate_edges(self):
            if edge.info.variable == "":
                continue
            lookup = edge.info.variable if reverse else edge.src
            value = edge.src if reverse else edge.info.variable
            if lookup not in result:
                result[lookup] = set()
            result[lookup].add(value)
        return result

    # Works similarly to get_var_visibility(), but instead assigns only one
    # variable to each state (assumes 'determinism' wrt. variable visibility)
    def get_var_visibility_cache(self) -> dict:
        result: dict[str, int] = {}
        prefix = len(self.get_var_prefix())
        for state in self.get_states():
            for edge in self.transitions[state].values():
                if edge.info.variable != "":
                    result[state] = int(edge.info.variable[prefix:])
        return result

    # for testing purposes (normalization checking -> sorted var occurrence)
    def get_var_occurence(self, sorted=True) -> list:
        prefix_len = len(self.get_var_prefix())
        result = []
        for edge in iterate_edges(self):
            if edge.info.variable == "":
                continue
            var: int = int(edge.info.variable[prefix_len:])
            result.append(var)
        if sorted:
            result.sort()
        return result

    def get_var_max(self) -> int:
        max_var = 0
        prefix_len = len(self.get_var_prefix())
        for edge in iterate_edges(self):
            if edge.info.variable != "":
                var = int(edge.info.variable[prefix_len:])
                max_var = max(max_var, var)
        return max_var

    # Returns a reachability dictionary: state q -> states reachable from q
    # TODO: Check this function so that it does not consider initial rootstate as a visited state
    # NOTE: similar to reachable_top_down, but this function does not consider
    # tree viability (a.k.a. each branch needs to end with a leaf transition),
    # only which states are accessible through any part of the 'hyper-edges'
    def get_reachable_states_from(self, state: str) -> set:
        original_rootstates = [i for i in self.roots]
        self.roots = [state]
        result = set()
        root = True
        for state in iterate_states_bfs(self):
            if root:  # this should be here so that it does not the first 'state'
                root = False  # is not considered initial upon first exploration, only after a second visit
                continue
            result.add(state)
        self.roots = original_rootstates
        return result

    # def get_reachable_states_from(self, state: str) -> set:
    #     queue = [state]
    #     visited = set()
    #     result = set()
    #     while queue != []:
    #         current = queue.pop(0)
    #         visited.add(current)
    #         for edge in self.transitions[current].values():
    #             for child in edge.children:
    #                 result.add(child)
    #                 if child not in visited:
    #                     queue.append(child)
    #     return result

    # Returns a list of all states that can be reached through 1 transition
    # from a specific state (only one directional)
    def get_neighbors_of(self, state: str) -> set:
        if state not in self.transitions:
            return []
        result = set()

        for edge in self.transitions[state].values():
            for child in edge.children:
                if child not in result:
                    result.add(child)
        return result

    # Calculates the smallest "hop" distance to the specified state from root
    # Works similarly to BFS but uses helping list to stop an iteration after
    # initial stack is exhausted and increases the distance counter
    def get_root_distance(self, state: str) -> int:
        distance = 0
        visited = set()  # cuts looping (BFS)
        worklist = [i for i in self.roots]  # work list =>
        state_count = len(self.get_states())

        while len(visited) != state_count:
            next_iteration = []
            while worklist != []:
                current = worklist.pop(0)
                if current == state:
                    return distance
                visited.add(current)
                for i in self.get_neighbors_of(current):
                    if i not in visited:
                        next_iteration.append(i)
            worklist = [i for i in next_iteration]
            distance += 1

        raise Exception(f"get_root_distance(): {state} not found in {self.name}")

    # Calculates all possible paths (acyclic) through the TA.
    # Path must begin with a root state and end with a leaf
    # note: based on DFS
    # result is a list of paths, path is a lists of states
    def calculate_paths(self) -> list:
        def pre_order_dfs(state, path, result):
            path.append(state)
            if state in leaves:
                result.append(copy.copy(path))
            for i in self.get_neighbors_of(state):
                if i not in path:
                    pre_order_dfs(i, path, result)
            path.pop()

        leaves = set(self.get_output_states())
        result = []

        for root in self.roots:
            pre_order_dfs(root, [], result)
        return result

    # explore the state space (BFS-like) of the TA and remember the paths taken
    # return the dictionary of state -> paths
    # paths are represented as strings of '0's and '1's
    def get_shortest_state_paths_dict(self) -> dict[str, str]:
        # note: we assume 'boxes' (tree automata used in ABDDs) need root-uniqueness to be well-defined,
        # so the state space is not traversed in parallel
        queue = [(i, "") for i in self.roots]
        result = {i: "" for i in self.roots}
        while queue != []:
            state, path = queue.pop(0)
            for edge in self.transitions[state].values():
                if len(edge.children) == 0:
                    continue
                for i, child in enumerate(edge.children):
                    if child not in result:
                        newpath = f"{path}{i}"
                        result[child] = newpath
                        queue.append((child, newpath))
                    elif result[child] > f"{path}{i}":
                        result[child] = f"{path}{i}"
        return {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Modifying functions # - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # creates a copy of a state dictionary (with isomorphic edges)
    # - state: name of the state to copy edges from
    # - name: state name of the copy
    # e.g. copying the state a with edges:
    # original: a  -> (b, c),   a  -> (a,  a )
    # copy:     a' -> (b, c),   a' -> (a', a')
    def copy_state(self, state: str, name: str) -> dict:
        pass

    # needed for union (and testing) - name collision resolving
    def rename_state(self, old_name: str, new_name: str):
        # renaming state in roots array (1st layer)
        if old_name in self.roots:
            self.roots.remove(old_name)
            self.roots.append(new_name)

        if old_name not in self.transitions:
            return
        # supposing only one state with the old_name exists in tree_aut
        # renaming state in the dictionary of states (1st layer)
        self.transitions[new_name] = self.transitions.pop(old_name)

        # renaming name of the state inside transitions (2nd layer)
        for edge in iterate_edges(self):
            if edge.src == old_name:
                edge.src = str(new_name)
            # renaming state name inside the children array (3rd layer)
            for i in range(len(edge.children)):
                if edge.children[i] == old_name:
                    edge.children[i] = new_name

    def remove_state(self, state: str):
        if state in self.roots:
            self.roots.remove(state)

        if state in self.transitions:
            self.transitions.pop(state)

        for content in self.transitions.values():
            keys_to_delete = []
            for key, edge in content.items():
                if state in edge.children:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                content.pop(key)

    def remove_transition(self, state: str, key: str):
        if state not in self.transitions:
            return
        if key not in self.transitions[state]:
            return
        self.transitions[state].pop(key)

    def remove_output_transitions(self):
        for state in self.get_states():
            keys = []
            for k, tr in self.transitions[state].items():
                if len(tr.children) == 0:
                    keys.append(k)
            for k in keys:
                self.remove_transition(state, k)

    # Removes total or partial self looping transitions.
    # If soft is True, self loops are only removed if there is a viable
    # non-self looping transition present within a state.
    def remove_self_loops(self, soft=False):
        for state, edges in self.transitions.items():
            keys_to_delete = []
            for k, edge in edges.items():
                if edge.src in edge.children:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                self.transitions[state].pop(k)

    # Creates a better readable state names for more clear images (DOT).
    # Useful after unfolding, determinization/normalization, etc.
    def reformat_states(self, prefix="q", start_from=0):
        temp = {}  # state -> idx
        i = start_from
        for state in iterate_states_bfs(self):
            if state not in temp:
                temp[state] = i
                i += 1
        # old version:
        # for state, idx in temp.items():
        #     self.rename_state(state, f"temporary_name{idx}")
        # for idx in temp.values():
        #     self.rename_state(f"temporary_name{idx}", f"{prefix}{idx}")

        # optimized version:
        new_roots = []
        for root in self.roots:
            new_roots.append(f"{prefix}{temp[root]}")
        self.roots = new_roots
        new_transitions = {}
        for state, edges in self.transitions.items():
            new_transitions[f"{prefix}{temp[state]}"] = edges
        self.transitions = new_transitions
        for edge in iterate_edges(self):
            edge.src = f"{prefix}{temp[edge.src]}"
            for i in range(len(edge.children)):
                edge.children[i] = f"{prefix}{temp[edge.children[i]]}"

    def reformat_keys(self, prefix="k"):  # k as in 'key'
        counter: int = self.count_edges() + 2  # for no collisions
        for state in iterate_states_bfs(self):
            swap = [key for key in self.transitions[state].keys()]
            for old_key in swap:
                new_key = counter
                counter += 1
                self.transitions[state][new_key] = self.transitions[state].pop(old_key)
        counter = 1
        for state in iterate_states_bfs(self):
            swap = [key for key in self.transitions[state].keys()]
            for old_key in swap:
                new_key = f"{prefix}{counter}"
                counter += 1
                self.transitions[state][new_key] = self.transitions[state].pop(old_key)

    # note:
    # since TAs do not have to be deterministic, some states can have the same shortest path
    # thus the state order we obtain is not necessarily total, but only partial
    # that is why the inverted dictionary will have a path pointing to a list (set) of states
    def reformat_ports(self):
        paths_dict = self.get_shortest_state_paths_dict()
        counter = 0

        # we assume max one port transition per state
        for state in paths_dict.keys():
            for edge in self.transitions[state].values():
                if edge.info.label.startswith("Port"):
                    edge.info.label = f"Port_{counter}"
                    counter += 1

    def check_var_type(self):
        var_type = type("")
        for edge in iterate_edges(self):
            if type(edge.info.variable) != var_type:
                return False
        return True

    # Shrinks the tree automaton
    # such that it only contain the states from list (reachable states)
    def shrink_tree_aut(self, reachable: list):
        to_delete = [x for x in self.roots if x not in reachable]
        for state_name, content in self.transitions.items():
            if state_name not in reachable:
                to_delete.append(state_name)
            for edge in content.values():
                if edge.src not in reachable:
                    to_delete.append(edge.src)
                for i in edge.children:
                    if i not in reachable:
                        to_delete.append(i)

        for i in set(to_delete):
            self.remove_state(i)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Building functions #  - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Prefix, suffix and infix creation was initially thought of as a means
    # of obtaining a partial order over the box alphabet.
    # Creating a total order over the box alphabet is necessary for canonical
    # form of folding/unfolding algorithms.

    def create_prefix(self, extra_output_edges):
        result = copy.deepcopy(self)

        result.name = f"prefix({self.name}, {extra_output_edges})"

        for state_name, content in result.transitions.items():
            temp_dict = {}
            if state_name in self.roots:
                continue
            for symbol in extra_output_edges:
                temp_str = str(state_name) + "-" + str(symbol) + "-()"
                temp_dict[temp_str] = TTransition(state_name, TEdge(symbol, [], ""), [])
            for temp_name, temp_edge in temp_dict.items():
                # checking for non-port output edge
                non_port_output = False
                for edge in content.values():
                    label = edge.info.label
                    if not label.startswith("Port") and len(edge.children) == 0:
                        non_port_output = True
                # skip adding non-port output edge
                # if another non-port output present
                if not temp_edge.info.label.startswith("Port") and non_port_output:
                    continue
                else:
                    content[temp_name] = temp_edge
        result.port_arity = result.get_port_arity()
        return result

    def create_suffix(self):
        result = copy.deepcopy(self)
        result.name = f"suffix({result.name})"
        for state_name, edge_dict in result.transitions.items():
            check = True
            for edge in edge_dict.values():
                edge_label = edge.info.label
                if edge_label.startswith("Port"):
                    check = False
                    break
            if check and state_name not in result.roots:
                result.roots.append(state_name)
        return result

    def create_infix(self, extra_output_edges: dict[str, list[str]]):
        result: TTreeAut = copy.deepcopy(self)
        ports = [
            sym for sym in extra_output_edges if (sym.startswith("Port") and sym not in result.get_output_symbols())
        ]
        result.name = f"infix({self.name}, {ports})"
        for state in result.get_states():
            # A) make all states rootstates
            if state in result.roots:
                continue
            result.roots.append(state)

            # B) add output ports from extra_output_edges to every state
            for i in ports:
                key = f"{state}-{i}->()"
                edge = [state, TEdge(i, [], ""), []]
                result.transitions[state][key] = edge
        result.port_arity = result.get_port_arity()
        return result


# sorts the state names while ignoring the prefix
def state_name_sort(states: list[str]) -> list:
    if states == []:
        return []

    prefix_len = 0
    for i in range(len(states[0])):
        if not states[0][i:].isnumeric():
            prefix_len += 1
    prefix = states[0][:prefix_len]
    try:
        result = [int(i.lstrip(prefix)) for i in states]
        result.sort()
        result = [f"{prefix}{i}" for i in result]
    except ValueError:
        result = [i for i in states]
    return result


# TODO rewrite this to be TTreeAut methods


def iterate_edges(obj) -> Generator[TTransition, None, None]:
    dict_obj = obj
    if isinstance(obj, TTreeAut):
        dict_obj = obj.transitions

    for inner_obj in dict_obj.values():
        if isinstance(inner_obj, dict):
            for edge in iterate_edges(inner_obj):
                yield edge
        else:
            yield inner_obj


def iterate_key_edge_tuples(obj) -> Generator[Tuple[str, TTransition], None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_key_edge_tuples can only work with TTreeAut.")

    for edges in obj.transitions.values():
        for key, edge in edges.items():
            yield key, edge


def iterate_keys(obj) -> Generator[str, None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_keys can only work with TTreeAut.")
    for edges in obj.transitions.values():
        for key in edges.keys():
            yield key


def iterate_edges_from_state(obj, state):
    dict_obj = obj
    if isinstance(obj, TTreeAut):
        for edge in dict_obj.transitions[state].values():
            yield edge


# Depth-first search iterator over states of a tree automaton
def iterate_states_dfs(ta: TTreeAut):
    stack = [root for root in ta.roots]
    stack.reverse()
    visited = set()
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        yield state
        for edge in ta.transitions[state].values():
            for child in edge.children:
                if child not in visited:
                    stack.append(child)


# Breadth-first search iterator over states of a tree automaton
def iterate_states_bfs(ta: TTreeAut):
    queue = [root for root in ta.roots]
    visited = set()
    while queue:
        state = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        yield state
        for edge in ta.transitions[state].values():
            for child in edge.children:
                if child not in visited:
                    queue.append(child)


class TTreeAutMetaData:
    """Contains string lengths for tidy formatting (tables, etc.)."""

    def __init__(self, ta: TTreeAut):
        self.ta: TTreeAut = ta

        self.state: int = 0
        self.child: int = 0
        self.key: int = 0
        self.variable: int = 0
        self.label: int = 0
        self.edge: int = 0
        self.box_name: int = 0
        self.arity: int = 0

        self.key_prefix: int = 0
        self.state_prefix: int = 0
        self.var_prefix: int = 0

    def __repr__(self):
        return (
            f"[TTreeAutMetaData]\n"
            + f"Max State Length        = {self.state}\n"
            + f"Max Child Length        = {self.child}\n"
            + f"Max Key Length          = {self.key}\n"
            + f"Max Variable Length     = {self.variable}\n"
            + f"Max Edge Label Length   = {self.label}\n"
            + f"Max Box Name Length     = {self.box_name}\n"
        )

    def recompute(self):
        def get_prefix_len(string: str) -> int:
            prefix_len = 0
            for i in range(len(string)):
                if not string[i:].isnumeric():
                    prefix_len += 1
            return prefix_len

        prefixes_are_set = False
        # for edges in self.ta.transitions.values():
        for key, edge in iterate_key_edge_tuples(self.ta):
            self.state = max(self.state, len(edge.src))
            self.label = max(self.label, len(edge.info.label))
            self.variable = max(self.variable, len(edge.info.variable))
            self.key = max(self.key, len(key))
            self.edge = max(self.edge, len(str(edge.info)))

            if edge.info.variable != "" and not prefixes_are_set:
                self.key_prefix = get_prefix_len(key)
                self.state_prefix = get_prefix_len(edge.src)
                self.var_prefix = get_prefix_len(edge.info.variable)
                prefixes_are_set = True

            for box in edge.info.box_array:
                if type(box) == str:
                    self.box_name = max(self.box_name, len(box))
                if type(box) == TTreeAut:
                    self.box_name = max(self.box_name, len(box.name))
            for child in edge.children:
                self.child = max(self.child, len(child))

        for arity in self.ta.get_symbol_arity_dict().values():
            self.arity = max(self.arity, arity)
