"""
[file] helpers.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Helper functions for tree automata operations.
"""

from itertools import product

# Helper function for bottom-up tree parsing
# - (reachability, non_emptiness)


def generate_possible_children(state: str, parents: list[str], size: int) -> list[list[str]]:
    """
    Creates all possible variations (with repetition) of items
    from list of "parents" of a given length ("size"),
    such that the variation (stored in a list)
    contains the "state" item at least once
    note: assumes, that the "state" is in parents "list"
    """
    possibilities = product(parents, repeat=size)
    result = [list(k) for k in possibilities if state in k]
    return result


# End of file helpers.py
