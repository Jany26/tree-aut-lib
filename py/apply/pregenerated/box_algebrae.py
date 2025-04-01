from apply.box_algebra.apply_tables import BooleanOperation
from apply.box_algebra.box_trees import BoxTreeNode
from apply.box_algebra.port_connection import PortConnectionInfo


# fmt: off
boxtree_cache: dict[tuple[str, BooleanOperation, str], BoxTreeNode] = {
    (None, BooleanOperation.AND, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),
    ("X", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.AND, "X"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="False", port_info=[]
    ),
    ("L0", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),
    ("L0", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.AND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("L1", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="(s0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L1", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="(s0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("H0", BooleanOperation.AND, "X"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="False", port_info=[]
    ),
    ("H0", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),
    ("H0", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.AND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H1", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H1", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="(u0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H1", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="(u0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        )
    ),
    ("H1", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),
    ("LPort", BooleanOperation.AND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="(v0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        )
    ),
    ("LPort", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.AND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="(w0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),
    ("HPort", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.OR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),
    ("X", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.OR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="(r0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L0", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("L0", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="(r0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("L1", BooleanOperation.OR, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),
    ("L1", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("L1", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.OR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H0", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="(t0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H0", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H0", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="(t0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        )
    ),
    ("H0", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),
    ("H1", BooleanOperation.OR, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),
    ("H1", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("H1", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="(v0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        )
    ),
    ("LPort", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.OR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="(w0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),
    ("HPort", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.XOR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),
    ("X", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="(r0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L0", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="(r0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L0", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="(r0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("L1", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="(s0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L1", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="(s0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L1", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="(s0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1, negation=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("H0", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H0", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="(t0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H0", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="(t0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H0", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="(t0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        )
    ),
    ("H0", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),
    ("H1", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H1", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="(u0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H1", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="(u0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H1", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="(u0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        )
    ),
    ("H1", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),
    ("LPort", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="(v0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        )
    ),
    ("LPort", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="(v0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        )
    ),
    ("LPort", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="(w0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="(w0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, negation=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),
    ("HPort", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),
    ("HPort", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.IFF, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),
    ("X", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="(r0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L0", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="(r0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L0", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="(r0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1, negation=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("L1", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="(s0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L1", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="(s0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        )
    ),
    ("L1", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="(s0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("H0", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H0", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="(t0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H0", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="(t0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H0", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="(t0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        )
    ),
    ("H0", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),
    ("H1", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H1", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="(u0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H1", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="(u0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H1", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="(u0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        )
    ),
    ("H1", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),
    ("LPort", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="(v0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        )
    ),
    ("LPort", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="(v0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        )
    ),
    ("LPort", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="(w0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, negation=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="(w0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0),
                PortConnectionInfo(target1=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),
    ("HPort", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),
    ("HPort", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.NAND, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("L0", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="(s0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L1", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="(s0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1, negation=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("H0", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("H0", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("H0", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H1", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H1", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="(u0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H1", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="(u0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        )
    ),
    ("H1", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="(v0,u0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        )
    ),
    ("LPort", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="(w0,s0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, negation=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),
    ("HPort", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.NOR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="(r0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L0", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="(r0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1, negation=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("L1", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("L1", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="False", port_info=[]
    ),
    ("L1", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H0", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="(t0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H1", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L1", port_info=[
                PortConnectionInfo(target2=0, negation=True),
            ]
        )
    ),
    ("H0", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),
    ("H0", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="(t0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0, negation=True),
                PortConnectionInfo(target2=1, negation=True),
            ]
        )
    ),
    ("H0", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="False", port_info=[]
    ),
    ("H1", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="(v0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        )
    ),
    ("LPort", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="(w0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, negation=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),
    ("HPort", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


    (None, BooleanOperation.IMPLY, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("X", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("L0", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L0", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="(s0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        )
    ),
    ("L1", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),
    ("L1", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="(s0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=1),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        )
    ),
    ("H0", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),
    ("H0", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="True", port_info=[]
    ),
    ("H0", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H0", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H1", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="(u0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="H0", port_info=[
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="L0", port_info=[
                PortConnectionInfo(target2=0),
            ]
        )
    ),
    ("H1", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),
    ("H1", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("H1", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="(u0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target2=0),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target2=0),
                PortConnectionInfo(target2=1),
            ]
        )
    ),
    ("H1", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="(v0,t0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        )
    ),
    ("LPort", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),
    ("LPort", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="(v0,w0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=0, target2=1, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=0, target2=1, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="(w0,r0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, negation=True),
                PortConnectionInfo(target1=1, negation=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, negation=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),
    ("HPort", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),
    ("HPort", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="(w0,v0)", port_info=[], is_leaf=False,
        low=BoxTreeNode(
            node="HPort", port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=0, recursion=True),
            ]
        ),
        high=BoxTreeNode(
            node="LPort", port_info=[
                PortConnectionInfo(target1=1, target2=0, recursion=True),
                PortConnectionInfo(target1=1, target2=1, recursion=True),
            ]
        )
    ),
    ("HPort", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),


}

# fmt: on
