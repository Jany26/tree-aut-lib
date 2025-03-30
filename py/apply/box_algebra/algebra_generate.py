from apply.box_algebra.apply_intersectoid import BooleanOperation, apply_intersectoid_create
from apply.box_algebra.box_trees import build_box_tree
from helpers.utils import box_catalogue, box_arities


def print_generated_algebrae(filename: str):
    f = open(filename, "w")
    f.write(f"from apply.box_algebra.apply_tables import BooleanOperation\n")
    f.write(f"from apply.box_algebra.box_trees import BoxTreeNode\n")
    f.write(f"from apply.box_algebra.port_connection import PortConnectionInfo\n")
    f.write(f"\n")
    f.write(f"\n")
    f.write(f"# fmt: off\n")
    f.write(f"boxtree_cache: dict[tuple[str, BooleanOperation, str], BoxTreeNode] = {{\n")
    ind = " " * 4

    for operation in BooleanOperation.__members__.values():
        if operation in [BooleanOperation.NOP, BooleanOperation.NOT]:
            continue
        for boxname1 in box_arities.keys():
            box1 = box_catalogue[boxname1]
            for boxname2 in box_arities.keys():
                box2 = box_catalogue[boxname2]
                applied_aut, portmap = apply_intersectoid_create(operation, box1, box2)
                boxtree = build_box_tree(applied_aut, portmap)
                f.write(f'{ind}("{boxname1}", {operation}, "{boxname2}"): ')
                f.write(f"{boxtree.__repr__(level=8)},\n")
    f.write(f"}}\n\n")
    f.write(f"# fmt: on\n")
    f.close()
