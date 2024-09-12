from tree_automata import TTreeAut, TTreeNode


# # Logical equivalent to function accept(DFA, string)
#   works recursively, as all children from array have to be matched
def match_tree_top_down(ta: TTreeAut, root: TTreeNode) -> bool:

    # Helper function for match_tree_top_down  - - - - - - - - - - - - - - - - -

    def match_top_down(ta: TTreeAut, node: TTreeNode, state: str) -> bool:
        child_tuples = []

        for state_name, edge in ta.transitions.items():
            for data in edge.values():
                if state_name == state and node.value == data.info.label:
                    child_tuples.append(data.children)

        for tuple in child_tuples:
            b = True
            # when tree unexpected amount children than expected
            if len(tuple) != len(node.children):
                break
            for i in range(len(tuple)):
                # recursive matching for all children
                b = match_top_down(ta, node.children[i], tuple[i])
                if not b:
                    break
            if b:
                return True
        return False

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for r in ta.roots:
        if match_top_down(ta, root, r) is True:
            return True
    return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Logical equivalent to function accept(DFA, string)
#  works recursively, but starts the matching process from the leaves
#  instead of starting from the root
def match_tree_bottom_up(ta: TTreeAut, root: TTreeNode) -> bool:
    # Helper function for match_tree_bottomup - - - - - - - - - - - - - - - - -
    def match_bottom_up(ta: TTreeAut, root: TTreeNode) -> list:
        result = []
        if len(root.children) == 0:
            for state_name, edge in ta.transitions.items():
                for data in edge.values():
                    if (
                        data.info.label == root.value  # or symbol
                        and len(data.children) == 0
                        and state_name not in result
                    ):
                        result.append(state_name)
            return result

        else:
            child_symbols = []
            for i in range(len(root.children)):
                child_symbols.append(match_bottom_up(ta, root.children[i]))
            for state_name, edge in ta.transitions.items():
                for data in edge.values():
                    if data.info.label == root.value:  # or symbol
                        x = True
                        for i in range(len(data.children)):
                            if data.children[i] not in child_symbols[i]:
                                x = False
                                break
                        if x:
                            result.append(state_name)
            return result

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    result = match_bottom_up(ta, root)
    temp = []
    for value in result:
        if value in ta.roots:
            temp.append(value)
    return len(temp) != 0
