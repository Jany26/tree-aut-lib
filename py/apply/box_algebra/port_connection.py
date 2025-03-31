from typing import Optional


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
        target1: Optional[int] = None,
        target2: Optional[int] = None,
        recursion: bool = False,
        negation: bool = False,
    ):
        # target1 and target2 will be indices into the child lists in the initial ABDD
        self.target1: Optional[int] = target1
        self.target2: Optional[int] = target2
        # if neither states are None -> recursion=True is assumed
        # but is explicit here for clarity (in case unary op. is used etc...)
        self.recursion = recursion
        self.negation = negation

    def __repr__(self):
        cname = self.__class__.__name__
        attributes = [f"{k}={v}" for k, v in self.__dict__.items()]
        return f"{cname}({', '.join(attributes)})"

    def __eq__(self, other: "PortConnectionInfo") -> bool:
        return all(
            [
                type(self.target1) == type(other.target1),
                self.target1 is None or self.target1 == other.target1,
                type(self.target2) == type(other.target2),
                self.target2 is None or self.target2 == other.target2,
                self.recursion == other.recursion,
                self.negation == other.negation,
            ]
        )
