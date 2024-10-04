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
    # for k in possibilities:
    #     if state in k:
    #         result.append(list(k))
    return result
