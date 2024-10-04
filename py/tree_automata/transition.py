from typing import Optional


class TEdge:
    """
    Useful in UBDAs (unreduced binary decision automatons), where it is
    important to store more info about edges.
    * `variable`
        - from which variable the edge starts (with the reduction)
    * `box_array`
        - which boxes are used over each part of the "hyper-edge"
        - contains references to boxes which are
            used as a means of reduction over this part of the edge
        - short edges (no box reduction) are just 'None'
    * `label`
        - describes the edge used (usually LH = low-high)
        - could also be '0' / '1' / 'Port...', which have arity 0
            * output transitions, states with these can be considered 'leaves'
    * note: length of the box_array = arity of the edge
    """

    def __init__(self, label: str, box_array: list, variable: str):
        self.label: str = label
        self.box_array: list[Optional[str]] = box_array
        self.variable: str = variable

    def __repr__(self):
        result = f"{self.label}"
        if self.variable != "":
            result += f" <{self.variable}>"
        box_array_empty = True
        for i in self.box_array:
            if i is not None:
                box_array_empty = False

        if not box_array_empty:
            result += " ["
            for i in self.box_array:
                result += "_, " if i is None else (f"{i}, " if type(i) == str else f"{i.name}, ")
            result = result[:-2]
            result += "]"
        return result

    # makes the hyper-edge 'short' (all parts of the edge)
    def shorten_edge(self):
        arity: int = len(self.box_array)
        self.box_array = [None] * arity


class TTransition:
    """
    Transition consists of source state, child states and the "edge" between them
    i.e. the edge is only a necessary part of the transition.
    """

    def __init__(self, src: str, info: TEdge, children: list[str]):
        self.src: str = src
        self.info: TEdge = info  # edge info (symbol, boxes, variable)
        self.children: list[str] = children

    def __repr__(self):
        # comment = " <<< LEAF TRANSITION >>>" if self.children == [] else ""
        return f"{self.src} -- {self.info} --> {self.children}"

    def is_self_loop(self):
        if self.src in self.children:
            return True
        return False

    def is_full_self_loop(self):
        if self.children == []:
            return False
        for i in self.children:
            if i != self.src:
                return False
        return True
