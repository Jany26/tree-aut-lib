"""
[file] algebra_generate.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Create a Python-importable cache of all precomputed op-products of boxes.
"""

from apply.box_algebra.apply_intersectoid import BooleanOperation, apply_intersectoid_create
from apply.box_algebra.box_trees import BoxTreeNode, build_box_tree
from apply.box_algebra.port_connection import PortConnectionInfo
from helpers.utils import box_catalogue, box_arities


def print_generated_algebrae(filename: str):
    f = open(filename, "w")
    f.write(f"from apply.box_algebra.apply_tables import BooleanOperation\n")
    f.write(f"from apply.box_algebra.box_trees import BoxTreeNode\n")
    f.write(f"from apply.box_algebra.port_connection import PortConnectionInfo\n")
    f.write(f"\n")
    f.write(f"\n")
    f.write(f"# fmt: off\n")  # turning autoformatting off
    f.write(f"boxtree_cache: dict[tuple[str, BooleanOperation, str], BoxTreeNode] = {{\n")
    ind = " " * 4

    for operation in BooleanOperation.__members__.values():
        if operation in [BooleanOperation.NOP, BooleanOperation.NOT]:
            continue

        # short-short base case:
        f.write(f"{ind}(None, {operation}, None): ")
        boxtree = BoxTreeNode(
            None, port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
        )
        f.write(f"{boxtree.__repr__(level=8)},  # None {operation.name} None\n")

        # non-short cases:
        for boxname1 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
            box1 = box_catalogue["Xdet" if boxname1 == "X" else boxname1]
            for boxname2 in ["X", "L0", "L1", "H0", "H1", "LPort", "HPort"]:
                box2 = box_catalogue["Xdet" if boxname2 == "X" else boxname2]
                applied_aut, portmap = apply_intersectoid_create(operation, box1, box2)
                boxtree = build_box_tree(applied_aut, portmap)
                f.write(f'{ind}("{boxname1}", {operation}, "{boxname2}"): ')
                f.write(f"{boxtree.__repr__(level=8)},  # {boxname1} {operation.name} {boxname2}\n")
        f.write("\n\n")
    f.write(f"}}\n\n")
    f.write(f"# fmt: on\n")  # turning autoformatting back on
    f.close()


# End of file algebra_generate.py
