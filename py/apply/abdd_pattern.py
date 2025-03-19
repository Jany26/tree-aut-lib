from typing import Optional

from apply.abdd_node import ABDDNode

# note that during apply materialization, this dictionary for symbolic variable lookup will always be available,
# for example:

# class SymbolicVar:
#     IN = 0
#     MAT = 1
#     OUT1 = 2
#     OUT2 = 3
#     LEAF = 4

# symbolic_level: dict[SymbolicVar, int] = {
#     SymbolicVar.IN: 1,
#     SymbolicVar.MAT: 4,
#     SymbolicVar.OUT1: 7,
#     SymbolicVar.OUT2: 10,
#     SymbolicVar.LEAF: 50,
# }


class ABDDPattern:
    """
    A helper class for storing the subtargets of the materialized ABDD pattern.
    Basically represents an ABDD node and is created only such that ABDD patterns
    are allowed to have arbitrarily large number of targets (for arbitrary number of box ports).

    """

    def __init__(
        self,
        new: bool = False,
        name: str | ABDDNode = "",
        level: int = 0,
        low_box: Optional[str] = None,
        low: list["ABDDPattern"] = [],
        high_box: Optional[str] = None,
        high: list["ABDDPattern"] = [],
    ):
        self.new = new
        self.name = name
        self.level = level
        self.low_box = low_box
        self.low = low
        self.high_box = high_box
        self.high = high

    # def __repr__(self):
    #     attr_str = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
    #     return f"{self.__class__.__name__}[{attr_str}]"

    def __repr__(self, level=0):
        indent = "  " * level  # Indentation for nested levels

        # Regular attributes (excluding `low` and `high`)
        normal_attrs = [
            f"new={self.new!r}",
            f"name={self.name!r}",
            f"level={self.level!r}",
            f"low_box={self.low_box!r}",
            f"high_box={self.high_box!r}",
        ]

        # Handle `low` and `high` lists:
        if self.low:
            low_repr = f"low=[\n" + ",\n".join(child.__repr__(level + 2) for child in self.low) + "\n" + indent + "  ]"
        else:
            low_repr = f"low=[]"

        if self.high:
            high_repr = (
                f"high=[\n" + ",\n".join(child.__repr__(level + 2) for child in self.high) + "\n" + indent + "  ]"
            )
        else:
            high_repr = f"high=[]"

        return f"{indent}{self.__class__.__name__}[{', '.join(normal_attrs)}, {low_repr}, {high_repr}]"


class MaterializationRecipe:
    """
    This is a helper class that will be represent the value for
    frozenset(Relationship) -> ABDDPattern lookup during node materialization.

    Utilizing the information stored within will help us to create the necessary
    ABDD substructures such that apply recursive descent works in synchronicity wrt. variable levels.
    """

    def __init__(self, init_box: Optional[str] = None, init_targets: list[ABDDPattern] = []):
        self.init_box = init_box
        self.init_targets = init_targets

    def __repr__(self):
        attr_str = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}[{attr_str}]"
