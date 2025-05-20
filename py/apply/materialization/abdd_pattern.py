"""
[file] abdd_pattern.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Classes describing ABDD Patterns and Materialization Recipes.
"""

from typing import Optional


class ABDDPattern:
    """
    A helper class for storing the subtargets of the materialized ABDD pattern.
    Basically represents an ABDD node and is created only such that ABDD patterns
    are allowed to have arbitrarily large number of targets (for arbitrary number of box ports).
    """

    def __init__(
        self,
        new: bool = False,
        name: str = "",
        level: str | int = 0,
        low_box: Optional[str] = None,
        high_box: Optional[str] = None,
        low: list["ABDDPattern"] = [],
        high: list["ABDDPattern"] = [],
    ):
        self.new = new
        self.name = name
        self.level = level
        self.low_box = low_box
        self.low = low
        self.high_box = high_box
        self.high = high

    def __repr__(self, level=0):
        indent = " " * level
        normal_attrs = [
            f"new={self.new!r}",
            f"name={self.name!r}",
            f"level={self.level!r}",
            f"low_box=" + ("None" if self.low_box is None else f"'{self.low_box}'"),
            f"high_box=" + ("None" if self.high_box is None else f"'{self.high_box}'"),
        ]
        low_repr = (
            f"low=[]"
            if not self.low
            else (f"low=[\n" + ",\n".join(child.__repr__(level + 4) for child in self.low) + "\n" + indent + "]")
        )
        high_repr = (
            f"high=[]"
            if not self.high
            else (f"high=[\n" + ",\n".join(child.__repr__(level + 4) for child in self.high) + "\n" + indent + "]")
        )
        return f"{indent}{self.__class__.__name__}({', '.join(normal_attrs)}, {low_repr}, {high_repr})"

    def __eq__(self, other: "ABDDPattern") -> bool:
        if any(
            [
                self.new != other.new,
                type(self.name) != type(other.name),
                self.level != other.level,
                self.low_box != other.low_box,
                self.high_box != other.high_box,
                len(self.low) != len(other.low),
                len(self.high) != len(other.high),
            ]
        ):
            return False
        if any([self.low[i] != other.low[i] for i in range(len(self.low))]):
            return False
        if any([self.high[i] != other.high[i] for i in range(len(self.high))]):
            return False
        return True


class MaterializationRecipe:
    """
    This is a helper class that will be represent the value for
    frozenset(Relationship) -> ABDDPattern lookup during node materialization.

    Materialization Recipe basically represents one edge of the ABDD (that is, a box and a list of targets)
    which replaces the edge that needs materialization in one of the input ABDDs during the recursive descent.

    1:      x1 --ruleA--> [x5, ...]
    2:      x1 --ruleB--> [x10, ...] => needs to be split so that x5 is the target nodes' variable
    New2:   x1 --'init_box'--> [nodes created based on 'init_targets' -> should all have x5 variable]

    Utilizing the information stored within the Recipe will help us to create the necessary
    ABDD substructures such that apply recursive descent works in synchronicity wrt. variable levels.

    Can be precomputed for all possible configurations of materialization and instantly retrieved from a cache
    during Apply. Traversing this structure is then simulating the materialization process.
    ABDD Patterns stored in the recipe then contain symbolic links/names representing the nodes of the modified ABDD.
    """

    def __init__(self, init_box: Optional[str] = None, init_targets: list[ABDDPattern] = []):
        self.init_box = init_box
        self.init_targets = init_targets

    def __repr__(self, level=0):
        indent = " " * level
        boxstr = self.init_box if self.init_box is None else f"'{self.init_box}'"
        result = f"{indent}{self.__class__.__name__}(init_box={boxstr}, init_targets=[\n"
        result += ",\n".join([f"{indent}{i.__repr__(level=level+4)}" for i in self.init_targets])
        result += f"\n{indent}])"
        return result

    def __eq__(self, other: "MaterializationRecipe"):
        if self.init_box != other.init_box:
            return False
        if len(self.init_targets) != len(other.init_targets):
            return False
        if any([self.init_targets[i] != other.init_targets[i] for i in range(len(self.init_targets))]):
            return False
        return True


# End of file abdd_pattern.py
