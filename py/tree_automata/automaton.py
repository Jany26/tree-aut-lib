import copy
from typing import Generator

from tree_automata.transition import TEdge, TTransition
from helpers.string_manipulation import state_name_sort, get_var_prefix_from_list


class TTreeAut:
    """
    Tree automaton class has two main attributes
    1) Root state array.
    2) Dictionary of states and their transitions.
    Transitions = dict (A) of dicts (B) referenced by state name.
    Inner dicts (B) are then referenced by transition names (arbitrary).

    The transition itself consists of:
    - input state,
    - edge object (edge label, edge boxes, edge variable label)
    - array of output states (size of array = arity of the node)
        * all state and label names are considered as strings

    In documentation, the naming convention will be:
    - TTreeAut consists of: array of root states and "state" dictionary
    - state dictionaries are referenced by names of the states
    - each state in the state dictionary references another dictionary
        - this will be called "transition" dictionary (for the current state)
        - the transition dictionary is referenced by arbitrary keys (for now)
    """

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
        result: str = ""
        # result = "-" * 78 + '\n'
        result += f"  [TreeAut]: '{self.name}'\n"
        result += f"  > Root States = {self.roots}\n"

        src_str: str = "source"
        edge_str: str = "edge"
        child_str: str = "child #"
        key_str: str = "key"

        # computing lengths
        self.meta_data.recompute()
        src_len: int = max(len(src_str), self.meta_data.state)
        edge_len: int = max(len(edge_str), self.meta_data.edge)
        child_len: int = max(len(child_str), self.meta_data.child)
        key_len: int = max(len(key_str), self.meta_data.key)

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

    def __eq__(self, ta):
        """
        Check if two TAs are equivalent... NOTE: wip
        An attempt to create an on-the-fly isomorphism check.

        - unique counter value will be used to compare states
        - states will be stored in two separate hash-maps, values will be counters
        - need to compare child counts,
        - different, 'redundant' edges are stored in two separate places (maybe no)
        """
        if len(self.roots) != len(ta.roots):
            return False
        state_mapper: dict[str, (str, str)] = {}
        pass

    def get_edge_string(self, edge: TTransition) -> str:
        """
        Pretty formatting for an edge, the edge content fields are adjusted
        based on the maximal lengths across all edges within the automaton object.
        """
        result: str = ""
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

    def get_states(self) -> list[str]:
        """
        Get a list of all states that are in any way referenced within the TA structure.
        """
        result: set[str] = set()
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

    def get_self_looping_states(self) -> set[str]:
        result: set[str] = set()
        for edge in iterate_edges(self):
            if edge.src in edge.children:
                result.add(edge.src)
        return result

    def get_output_symbols(self) -> list[str]:
        """
        Get a list of all edge 'symbols' labeling the output edges from the TA.
        """
        result: list[str] = []
        for edge in iterate_edges(self):
            if len(edge.children) == 0:
                result.append(edge.info.label)
        return result

    def get_output_states(self) -> set[str]:
        """
        Get a set of all states that have an output transition (i.e. transition with 0 child states).
        """
        result: set[str] = set()
        for state_name, edges in self.transitions.items():
            for data in edges.values():
                if len(data.children) == 0:
                    result.add(state_name)
                    break
        return result

    def get_output_edges(self, inverse=False) -> dict[str, list[str]]:
        """
        Get a dictionary of all output edge symbols
        which correspond to a list of states,
        from which the transitions with the specific symbol originate.

        note: It is a sort of a combination of
        `TTreeAut.get_output_symbols()` and
        `TTreeAut.get_output_states()`.

        * inverse=False: `{symbol: list[states]}`
        * inverse=True: `{state: list[symbols]}`
        """
        result: dict[str, list[str]] = {}
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

    def get_terminable_transitions(self) -> set[TTransition]:
        """
        Find all transitions, whose children (>=1) have some output edge.
        Returned as a set of (statename, transition key) tuples.

        Terminable != Output edges.
        Terminable transitions have at least the arity of 1.
        And all child states of this transition have output edges,
        i.e. transitions with 0 children.
        """
        leaves = self.get_output_states()
        result = set()
        for tr in iterate_edges(self):
            # all states have to be able to terminate, ie. have an output transition
            if len(tr.children) > 0 and all([c in leaves for c in tr.children]):
                result.add(tr)
        return result

    def get_loopable_transitions(self) -> set[TTransition]:
        """
        Find all transitions, such that all children can self-loop (even indirectly,
        i.e.. through more than one transition).

        The self-looping property of a state is evaluated as true, iff the state 's'
        belongs to the set of top-down reachable states of 's'.

        Note: a transition can be loopable and terminable at the same time.
        I.e. in case of Lport, Hport, X boxes -> the "sink" state has to be able to loop,
        so that it can reach the final variable, and then can terminate with a port transition, or 0/1.
        """
        from tree_automata.functions.reachability import get_all_state_reachability

        reachability_cache = get_all_state_reachability(self)
        loopstates = set([state for state, reachable_set in reachability_cache.items() if state in reachable_set])
        result = set()
        for tr in iterate_edges(self):
            # all states have to be able to loop, otherwise we could get unbalanced
            if len(tr.children) > 0 and all([c in loopstates for c in tr.children]):
                result.add(tr)
        return result

    def get_terminating_transitions(self) -> set[TTransition]:
        """
        Find all transitions such that there is no way of getting back to the source state.
        This differs from 'terminable' transitions, i.e. port/output transitions are terminating, but not terminable.
        """
        from tree_automata.functions.reachability import get_all_state_reachability

        reachability_cache = get_all_state_reachability(self)
        # loopstates = set([state for state, reachable_set in reachability_cache.items() if state in reachable_set])
        result = set()
        for tr in iterate_edges(self):
            # all states have to be able to loop, otherwise we could get unbalanced
            if len(tr.children) == 0 or all([tr.src not in reachability_cache[c] for c in tr.children]):
                result.add(tr)
        return result

    def get_output_transitions(self) -> set[TTransition]:
        """
        Return a set of all transitions that have 0 child states, i.e. output/leaf transitions.
        These include port transitions, as well as "0"/"1" transitions.

        Compared to get_output_edges(), this does not return a state<->output symbol lookup,
        just a set of TTransition objects.
        """
        return set([e for e in iterate_edges(self) if len(e.children) == 0])

    def get_port_order(self):
        """
        Get lexicographically sorted (ascending) list of port-state tuples.
        Low (index 0) children are lexicographically smaller than high (index 1).
        """
        path_list = self.get_shortest_state_paths_dict()
        result: list[tuple[str, str]] = []
        for s, _ in path_list:
            for edge in self.transitions[s].values():
                if edge.children == [] and edge.info.label.startswith("Port"):
                    result.append((edge.info.label, s))
        return result

    def get_symbol_arity_dict(self) -> dict[str, int]:
        """
        Find all edge symbols used within the TA/BDA, along with their arities.

        Note: Arity of a symbol = how many child nodes stem from this symbol.
        """
        result: dict[str, int] = {}
        for edges in self.transitions.values():
            for edge in edges.values():
                if edge.info.label not in result:
                    if edge.info.box_array == []:
                        result[edge.info.label] = len(edge.children)
                    else:
                        result[edge.info.label] = len(edge.info.box_array)
        return result

    def get_port_arity(self) -> int:
        """
        Count all transitions with different port names.
        """
        port_set: set[str] = set()
        for edge in iterate_edges(self):
            sym = edge.info.label
            if sym.startswith("Port"):
                port_set.add(sym)
        return len(port_set)

    def get_statename_prefix(self) -> str:
        res: set[str] = set()
        for state in self.get_states():
            prefix_len = 0
            for char_idx in range(len(state)):
                if not state[char_idx:].isnumeric():
                    prefix_len += 1
            res.add(state[:prefix_len])
        if len(res) > 1:
            raise ValueError("Inconsistent prefix")
        el: str = res.pop()
        return el

    def is_top_down_deterministic(self) -> bool:
        """
        Check whether a TA is top-down deterministic, i.e. if for each state and
        for each edge symbol there is at most one possible transition to do.
        """
        for edges in self.transitions.values():
            # Now we are checking all transitions stemming from one state.
            used_symbols: set[str] = set()
            for e in edges.values():
                if e.info.label in used_symbols:
                    return False
                used_symbols.add(e.info.label)
        return True

    def is_bottom_up_deterministic(self) -> bool:
        """
        Check whether a TA is bottom-up deterministic, i.e. if for each edge symbol (with n-arity) and each
        possible n-tuple of states there is at most one transition that can reach this children n-tuple.
        """
        pass

    def count_edges(self) -> int:
        counter: int = 0
        for _ in iterate_edges(self):
            counter += 1
        return counter

    def count_boxes(self) -> int:
        boxes: int = 0
        for edge in iterate_edges(self):
            for box in edge.info.box_array:
                if box is not None and box != "_":
                    boxes += 1
        return boxes

    def get_edge_counts(self) -> dict[str, int]:
        """
        Returns a map of states to number of edges starting in that state.
        """
        return {s: len(e) for s, e in self.transitions.items()}

    def get_reachable_states_from(self, state: str) -> set[str]:
        """
        Returns a reachability dictionary: state q -> states reachable from q

        TODO: Check this function so that it does not consider initial rootstate as a visited state

        NOTE: similar to reachable_top_down, but this function does not consider
        tree viability (a.k.a. each branch needs to end with a leaf transition),
        only which states are accessible through any part of the 'hyper-edges'
        """
        original_rootstates: list[str] = [i for i in self.roots]
        self.roots = [state]
        result: set[str] = set()
        # because by default, the root state (origin) is explored first,
        # and since we only want it to be considered reachable if there is a non-trivial path from 'state' to itself,
        # we introduce this flag, so that only if it is reached
        root: bool = True
        for state in iterate_states_bfs(self):
            if root:
                root = False
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

    def get_neighbors_of(self, state: str) -> set[str]:
        """
        Returns a list of all states that can be reached through 1 transition
        from a specific state (only one directional)
        """
        if state not in self.transitions:
            return []
        result: set[str] = set()

        for edge in self.transitions[state].values():
            for child in edge.children:
                if child not in result:
                    result.add(child)
        return result

    def get_root_distance(self, state: str) -> int:
        """
        Calculates the smallest "hop" distance to the specified state from root
        Works similarly to BFS but uses helping list to stop an iteration after
        initial stack is exhausted and increases the distance counter.
        """
        distance: int = 0
        visited: set[str] = set()  # cuts looping (BFS)
        worklist: list[str] = [i for i in self.roots]  # work list =>
        state_count: int = len(self.get_states())

        while len(visited) != state_count:
            next_iteration: list[str] = []
            while worklist != []:
                current: str = worklist.pop(0)
                if current == state:
                    return distance
                visited.add(current)
                for i in self.get_neighbors_of(current):
                    if i not in visited:
                        next_iteration.append(i)
            worklist = [i for i in next_iteration]
            distance += 1

        raise Exception(f"get_root_distance(): {state} not found in {self.name}")

    def calculate_paths(self) -> list[list[str]]:
        """
        Calculates all possible paths (acyclic) through the TA.
        Path must begin with a root state and end with a leaf
        note: based on DFS
        result is a list of paths, path is a lists of states
        """

        def pre_order_dfs(state, path: list, result: list[list[str]]) -> None:
            path.append(state)
            if state in leaves:
                result.append(copy.copy(path))
            for i in self.get_neighbors_of(state):
                if i not in path:
                    pre_order_dfs(i, path, result)
            path.pop()

        leaves: set[str] = self.get_output_states()
        result: list[list[str]] = []

        for root in self.roots:
            pre_order_dfs(root, [], result)
        return result

    def get_shortest_state_paths_dict(self) -> list[tuple[str, str]]:
        """
        explore the state space (BFS-like) of the TA and remember the paths taken
        return a list of (state, path) tuples, lexicographically sorted
        paths are represented as strings of '0's and '1's
        note: we assume 'boxes' (tree automata used in ABDDs) need root-uniqueness to be well-defined,
        so the state space is not traversed in parallel

        note:
        Since TAs do not have to be deterministic, some states can have the same shortest path
        thus the state order we obtain is not necessarily total, but only partial
        that is why the inverted dictionary would have a path pointing to a list (set) of states
        """
        # tuple = state, shortest path string
        queue: list[tuple[str, str]] = [(i, "") for i in self.roots]
        result: dict[str, str] = {i: "" for i in self.roots}
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
        return [(k, v) for k, v in sorted(result.items(), key=lambda item: item[1])]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Extract information about variables - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def get_var_order(self) -> list[str]:
        """
        Return a (lexically sorted) list of variables used within the TA (UBDA) structure.
        """
        vars: set[str] = set()
        for edge in iterate_edges(self):
            vars.add(edge.info.variable)
        if "" in vars:
            vars.remove("")
        return state_name_sort(list(vars))

    def get_var_prefix(self) -> str:
        """
        Returns largest prefix of a variable in a TA,
        that does not contain only numeric symbols.

        Examples:
            'x1' - returns 'x'
            'var5ta01 - returns 'var5ta'
        """
        res: set[str] = set()
        for edge in iterate_edges(self):
            if edge.info.variable != "":
                prefix_len = 0
                for i in range(len(edge.info.variable)):
                    if not edge.info.variable[i:].isnumeric():
                        prefix_len += 1
                var = edge.info.variable[:prefix_len]
                res.add(var)
        if len(res) > 1:
            raise ValueError("inconsistent variable prefix")
        el: str = res.pop()
        return el

    def get_var_visibility(self, reverse=False) -> dict[str, set[str]]:
        """
        Returns a dictionary of states, each of which has a set of variables,
        that the state can "see" = i.e. the state has a transition with
        this variable. e.g. {'q0': {'x1', 'x2'}, 'q1': {'x5'}}

        if reverse==True: the dictionary is referenced by variables, and values
        are lists of states. e.g. {'x1': {'q0'}, 'x2': {'q0'}, 'x5': {'q1'}}
        """
        result: dict[str, set[str]] = {}
        for edge in iterate_edges(self):
            if edge.info.variable == "":
                continue
            lookup: str = edge.info.variable if reverse else edge.src
            value: str = edge.src if reverse else edge.info.variable
            if lookup not in result:
                result[lookup] = set()
            result[lookup].add(value)
        return result

    def get_var_visibility_deterministic(self) -> dict[str, int]:
        """
        Works similarly to get_var_visibility(), but instead assigns only one
        variable to each state (assumes 'determinism' wrt. variable visibility).
        Throws an exception if more variables are visible from one state.

        NOTE: does not have a "reverse" version, like the 'nondeterministic' counterpart.
        """
        result: dict[str, int] = {}
        prefix = len(self.get_var_prefix())
        # for state in self.get_states():
        for edge in iterate_edges(self):
            if edge.info.variable == "":
                continue
            var = int(edge.info.variable[prefix:])
            if edge.src in result and result[edge.src] != var:
                raise ValueError(f"get_var_visibility_deterministic() -> state {edge.src} sees >1 variables")
            result[edge.src] = var
        return result

    def get_var_occurence(self, sorted=True) -> list[int]:
        """
        Get a sorted list of all variable indexes found across all transitions of a TTreeAut object.

        E.g. UBDA has 4 transitions with variables 'x4', 'x3', 'x3', 'x1' -> result: [1,3,3,4]
        """
        prefix_len: int = len(self.get_var_prefix())
        result: list[int] = []
        for edge in iterate_edges(self):
            if edge.info.variable == "":
                continue
            var: int = int(edge.info.variable[prefix_len:])
            result.append(var)
        if sorted:
            result.sort()
        return result

    def get_var_max(self) -> int:
        """
        Omitting any non-numeric prefix, get the index of the highest variable used.
        E.g. UBDA has 4 transitions with variables 'x7', 'x3', 'x1' -> result: 7
        """
        max_var: int = 0
        prefix_len: int = len(self.get_var_prefix())
        for edge in iterate_edges(self):
            if edge.info.variable != "":
                var: int = int(edge.info.variable[prefix_len:])
                max_var = max(max_var, var)
        return max_var

    def get_var_lookup(self, maxvar: int) -> dict[str, int]:
        """
        For each variable 'string', get its corresponding index.
        """
        prefix = get_var_prefix_from_list()
        pass

    def check_var_str_consistency(self) -> bool:
        """
        Return True if all variables on edges are of type 'str'.
        """
        var_type = type("")
        for edge in iterate_edges(self):
            if type(edge.info.variable) != var_type:
                return False
        return True

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Modifying functions # - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def copy_state(self, state: str, name: str) -> dict[str, TTransition]:
        """
        creates a copy of a state dictionary (with isomorphic edges)
        - state: name of the state to copy edges from
        - name: state name of the copy
        e.g. copying the state a with edges:
        original: a  -> (b, c),   a  -> (a,  a )
        copy:     a' -> (b, c),   a' -> (a', a')
        """
        pass

    def rename_state(self, old_name: str, new_name: str) -> None:
        """
        Needed for union (and testing) - name collision resolving.
        """
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

    def remove_state(self, state: str) -> None:
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

    def remove_transition(self, state: str, key: str) -> None:
        if state not in self.transitions:
            return
        if key not in self.transitions[state]:
            return
        self.transitions[state].pop(key)

    def remove_output_transitions(self) -> None:
        for state in self.get_states():
            keys: list[str] = []
            for k, tr in self.transitions[state].items():
                if len(tr.children) == 0:
                    keys.append(k)
            for k in keys:
                self.remove_transition(state, k)

    def remove_self_loops(self, soft=False) -> None:
        """
        Removes total or partial self looping transitions.
        If soft is True, self loops are only removed if there is a viable
        non-self looping transition present within a state.
        """
        for state, edges in self.transitions.items():
            keys_to_delete: list[str] = []
            for k, edge in edges.items():
                if edge.src in edge.children:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                self.transitions[state].pop(k)

    def reformat_states(self, prefix="q", start_from=0) -> None:
        """
        Creates a better readable state names for more clear images (DOT).
        Useful after unfolding, determinization/normalization, etc.

        NOTE: Make sure all unreachable states are removed before renaming,
        since this works using BFS traversal of states (which are top-down reachable).
        """
        temp: dict[str, int] = {}  # state -> idx
        i: int = start_from
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
        new_roots: list[str] = []
        for root in self.roots:
            new_roots.append(f"{prefix}{temp[root]}")
        self.roots = new_roots
        new_transitions: dict[str, dict[str, TTransition]] = {}
        for state, edges in self.transitions.items():
            new_transitions[f"{prefix}{temp[state]}"] = edges
        self.transitions = new_transitions
        for edge in iterate_edges(self):
            edge.src = f"{prefix}{temp[edge.src]}"
            for i in range(len(edge.children)):
                edge.children[i] = f"{prefix}{temp[edge.children[i]]}"

    def reformat_keys(self, prefix="k") -> None:  # k as in 'key'
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

    def reformat_ports(self) -> None:
        """
        Rename port transitions in a lexicographical order given by each port's
        state's shortest path to reach.
        Useful for comparing box properties, like isomorphism etc.
        """
        paths_list: list[tuple[str, str]] = self.get_shortest_state_paths_dict()
        counter: int = 0

        # we assume max one port transition per state
        for state, _ in paths_list:
            for edge in self.transitions[state].values():
                if edge.info.label.startswith("Port"):
                    edge.info.label = f"Port_{counter}"
                    counter += 1

    def shrink_tree_aut(self, reachable: list[str]) -> None:
        """
        Shrinks the tree automaton, such that it only contain the states from list (reachable states).
        """
        to_delete: list[str] = [x for x in self.roots if x not in reachable]
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

    def create_prefix(self, extra_output_edges: list[str]) -> "TTreeAut":
        result: TTreeAut = copy.deepcopy(self)

        result.name = f"prefix({self.name}, {extra_output_edges})"

        for state_name, content in result.transitions.items():
            temp_dict: dict[str, TTransition] = {}
            if state_name in self.roots:
                continue
            for symbol in extra_output_edges:
                temp_str: str = str(state_name) + "-" + str(symbol) + "-()"
                temp_dict[temp_str] = TTransition(state_name, TEdge(symbol, [], ""), [])
            for temp_name, temp_edge in temp_dict.items():
                # checking for non-port output edge
                non_port_output: bool = False
                for edge in content.values():
                    label: str = edge.info.label
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

    def create_suffix(self) -> "TTreeAut":
        result: TTreeAut = copy.deepcopy(self)
        result.name = f"suffix({result.name})"
        for state_name, edge_dict in result.transitions.items():
            check: bool = True
            for edge in edge_dict.values():
                edge_label = edge.info.label
                if edge_label.startswith("Port"):
                    check = False
                    break
            if check and state_name not in result.roots:
                result.roots.append(state_name)
        return result

    def create_infix(self, extra_output_edges: dict[str, list[str]]) -> "TTreeAut":
        result: TTreeAut = copy.deepcopy(self)
        ports: list[str] = [
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
                key: str = f"{state}-{i}->()"
                edge = TTransition(state, TEdge(i, [], ""), [])
                result.transitions[state][key] = edge
        result.port_arity = result.get_port_arity()
        return result


# TODO: rewrite this sometime to be TTreeAut methods


def iterate_edges(obj: TTreeAut) -> Generator[TTransition, None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_edges() can only work with TTreeAut.")

    for edge_dict in obj.transitions.values():
        for edge in edge_dict.values():
            yield edge


def iterate_key_edge_tuples(obj: TTreeAut) -> Generator[tuple[str, TTransition], None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_key_edge_tuples() can only work with TTreeAut.")

    for edges in obj.transitions.values():
        for key, edge in edges.items():
            yield key, edge


def iterate_keys(obj: TTreeAut) -> Generator[str, None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_keys() can only work with TTreeAut.")
    for edges in obj.transitions.values():
        for key in edges.keys():
            yield key


def iterate_edges_from_state(obj: TTreeAut, state: str) -> Generator[TTransition, None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_edges_from_state() can only work with TTreeAut")

    for edge in obj.transitions[state].values():
        yield edge


def iterate_output_edges(obj: TTreeAut) -> Generator[TTransition, None, None]:
    if not isinstance(obj, TTreeAut):
        raise ValueError("iterate_output_edges() can only work with TTreeAut")

    for state in obj.get_output_states():
        for edge in obj.transitions[state].values():
            if len(edge.children) == 0:
                yield edge


def iterate_states_dfs(ta: TTreeAut) -> Generator[str, None, None]:
    """
    Depth-first-like search iterator over states of a tree automaton.
    Every state is visited max. once.
    """
    stack: list[str] = [root for root in ta.roots]
    stack.reverse()
    visited: set[str] = set()
    while stack:
        state: str = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        yield state
        for edge in ta.transitions[state].values():
            for child in edge.children:
                if child not in visited:
                    stack.append(child)


def iterate_states_bfs(ta: TTreeAut) -> Generator[str, None, None]:
    """
    Breadth-first-like search iterator over states of a tree automaton.
    Every state is visited max. once.
    """
    queue: list[str] = [root for root in ta.roots]
    visited: set[str] = set()
    while queue:
        state: str = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        yield state
        for edge in ta.transitions[state].values():
            for child in edge.children:
                if child not in visited:
                    queue.append(child)


class TTreeAutMetaData:
    """
    Contains string lengths for tidy formatting (tables, etc.).
    """

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

    def recompute(self) -> None:
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
