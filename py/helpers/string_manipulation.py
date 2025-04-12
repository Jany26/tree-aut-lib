import re


def state_name_sort(states: list[str]) -> list[str]:
    """
    Sort the state names while ignoring the prefix.
    Also used with variables that have a non-numeric prefix.
    """
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


def create_var_order_list(prefix: str, count: int, start=1) -> list[str]:
    return [f"{prefix}{i+start}" for i in range(count)]


def get_var_prefix_from_list(var_list: list[str]) -> str:
    if var_list == []:
        return ""
    prefix_len: int = 0
    for i in range(len(var_list[0])):
        if not var_list[0][i:].isnumeric():
            prefix_len += 1
    prefix: str = var_list[0][:prefix_len]
    return prefix


def get_var_translate(variables: list[str]) -> dict[str, int]:
    prefix = get_var_prefix_from_list(variables)
    plen = len(prefix)
    return {var: int(var[plen:]) for var in variables}


# def macrostring(macrostate: list[str]) -> str:
#     return create_string_from_name_set(state_name_sort(macrostate))


def create_string_from_name_set(state_list: list[str]) -> str:
    """
    Create a string (state name) from list of states -- e.g. '{a,b,c}'
    """
    my_list: list[str] = state_name_sort(state_list)
    return "{" + ",".join(my_list) + "}"


def create_string_from_name_list(state_list: list) -> str:
    """
    Create a tuple-like (i.e. ordereed) string representation of a list of states.

    E.g: [s1, s2, s3] -> '(s1,s2,s3)'
    """
    result: str = "("
    for i in range(len(state_list)):
        result += state_list[i]
        if i < len(state_list) - 1:
            result += ","
    result += ")"
    return result


def tuple_name(tup: tuple[str, str]) -> str:
    """
    Create a string from a 2-tuple of strings.
    Used in intersection, and similar product-like automata operations.
    E.g.: (s1, s2) -> '(s1,s2)'
    """
    return f"({tup[0]},{tup[1]})"


def get_first_name_from_tuple_str(string: str) -> str:
    """
    Extract the first statename from a tuple-like string format.
    Useful in functions that work with cartesian product of states (intersection etc.).

    E.g.: '(s1,s2)' -> 's1'
    """
    match = re.search("^\(.*,", string)
    result = match.group(0)[1:-1]
    return result
