from typing import Union, Optional


# TODO: rework port connection info to contain:
# - indices to both (low-low or high-high) child node lists
# - negation and recursion flag

# Each BoxTreeNode will then contain not only the used box, but also
# a list of port connection info instances

# Then during apply, when materialization is not needed and both input variables and output variables
# agree (are the same level), then we can utilize the box algebrae to obtain the BoxTreeNode
# within each node of this tree is a string representing the used box AND PortConnectionInfo
# that says what the results of each of the target nodes of leaf nodes of this tree are.


class PortConnectionInfo:
    """
    One instance of this class corresponds to one port name within some box of a box tree.
    It has to contain information about:
    - 'state1', 'state2': which state is the port originating from (or rather, a tuple of states
    representing states of the initial boxes whose combination lead to the creation of the box tree).
    - 'recursion': whether or not recursion should be continued
        - recursion=True: the result is not predetermined and has to be further recursively computed using
        additional apply calls
        - recursion=False: the result is clear - terminal node (i.e. False AND something, True OR something, etc.),
        or one argument is omitted and the result is one of the two applied nodes (i.e. return x in case of True OR x, etc.)
    - 'negation': if the result is negated or not
    """

    def __init__(
        self,
        state1: Optional[Union[str, int]],
        state2: Optional[Union[str, int]],
        recursion: bool = False,
        negation: bool = False,
    ):
        self.state1: Optional[Union[str, int]] = state1
        self.state2: Optional[Union[str, int]] = state2
        # if neither states are None -> recursion=True is assumed
        # but is explicit here for clarity (in case unary op. is used etc...)
        self.recursion = recursion
        self.negation = negation


# class PortConnectionInfoTree:
#     def __init__(self, name: str, info: PortConnectionInfo):
#         self.port_name = name
#         self.port_info = info
#         self.low: Optional[PortConnectionInfoTree] = None
#         self.high: Optional[PortConnectionInfoTree] = None
