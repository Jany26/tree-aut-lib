from typing import List


# sorts the state names while ignoring the prefix
# also works with variables that have a non-numeric prefix
def state_name_sort(states: List[str]) -> List:
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


def create_var_order_dict(prefix: str, count: int, start=1):
    return [f"{prefix}{i+start}" for i in range(count)]


def create_var_order_apply(variables: list[str], terminals: list) -> dict:
    """
    Makes the list into a dictionary for easy lookup of indexing
    """
    if variables is not None:
        variables = state_name_sort(variables)
    result = {}
    i = 1
    for var in variables:
        if var not in result:
            result[var] = i
            i += 1
    # for t in terminals:
    #     result[str(t)] = i
    return result


def get_var_prefix(var_list: list[str]) -> str:
    if var_list == []:
        return ""
    prefix_len = 0
    for i in range(len(var_list[0])):
        if not var_list[0][i:].isnumeric():
            prefix_len += 1
    prefix = var_list[0][:prefix_len]
    return prefix


# creates a list of variable truth-values indexed by their order
# (the order in which they are evaluated during BDD top-down traversal)
# if an ABDD has a variable range of size 10, this function would be used 2^10 times
def assign_variables(num: int, size: int) -> list[int]:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    return result


# creates a int (var index) -> int (0/1 = true/false) dictionary from an integer number
# (iterated number in a cycle)
# if an ABDD has a variable range of size 10, this function is used 2^10 times
def assign_variables_dict(num: int, size: int) -> dict[int, int]:
    result = []
    division = num
    for _ in range(size):
        remainder = division % 2
        division = division // 2
        result.append(remainder)
    result.reverse()
    result_dict = {i + 1: result[i] for i in range(size)}
    return result_dict


# creates a string (state name) from list of states -- e.g. '{a,b,c}'
def create_string_from_name_set(state_list: list) -> str:
    my_list = state_name_sort(state_list)
    return "{" + ",".join(my_list) + "}"
