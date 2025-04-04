from apply.box_algebra.apply_tables import BooleanOperation
from apply.box_algebra.box_trees import BoxTreeNode
from apply.box_algebra.port_connection import PortConnectionInfo


# fmt: off
boxtree_cache: dict[tuple[str, BooleanOperation, str], BoxTreeNode] = {
    (None, BooleanOperation.AND, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None AND None
    ("X", BooleanOperation.AND, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X AND X
    ("X", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X AND L0
    ("X", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X AND L1
    ("X", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X AND H0
    ("X", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),  # X AND H1
    ("X", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X AND LPort
    ("X", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X AND HPort
    ("L0", BooleanOperation.AND, "X"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 AND X
    ("L0", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 AND L0
    ("L0", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 AND L1
    ("L0", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="False", port_info=[]
    ),  # L0 AND H0
    ("L0", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),  # L0 AND H1
    ("L0", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 AND LPort
    ("L0", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 AND HPort
    ("L1", BooleanOperation.AND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 AND X
    ("L1", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 AND L0
    ("L1", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 AND L1
    ("L1", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # L1 AND H0
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
    ),  # L1 AND H1
    ("L1", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 AND LPort
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
    ),  # L1 AND HPort
    ("H0", BooleanOperation.AND, "X"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 AND X
    ("H0", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="False", port_info=[]
    ),  # H0 AND L0
    ("H0", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),  # H0 AND L1
    ("H0", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 AND H0
    ("H0", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 AND H1
    ("H0", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 AND LPort
    ("H0", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 AND HPort
    ("H1", BooleanOperation.AND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),  # H1 AND X
    ("H1", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # H1 AND L0
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
    ),  # H1 AND L1
    ("H1", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 AND H0
    ("H1", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 AND H1
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
    ),  # H1 AND LPort
    ("H1", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),  # H1 AND HPort
    ("LPort", BooleanOperation.AND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort AND X
    ("LPort", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort AND L0
    ("LPort", BooleanOperation.AND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort AND L1
    ("LPort", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # LPort AND H0
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
    ),  # LPort AND H1
    ("LPort", BooleanOperation.AND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort AND LPort
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
    ),  # LPort AND HPort
    ("HPort", BooleanOperation.AND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort AND X
    ("HPort", BooleanOperation.AND, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort AND L0
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
    ),  # HPort AND L1
    ("HPort", BooleanOperation.AND, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # HPort AND H0
    ("HPort", BooleanOperation.AND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),  # HPort AND H1
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
    ),  # HPort AND LPort
    ("HPort", BooleanOperation.AND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort AND HPort


    (None, BooleanOperation.OR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None OR None
    ("X", BooleanOperation.OR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X OR X
    ("X", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X OR L0
    ("X", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X OR L1
    ("X", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),  # X OR H0
    ("X", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X OR H1
    ("X", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X OR LPort
    ("X", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X OR HPort
    ("L0", BooleanOperation.OR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 OR X
    ("L0", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 OR L0
    ("L0", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 OR L1
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
    ),  # L0 OR H0
    ("L0", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # L0 OR H1
    ("L0", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 OR LPort
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
    ),  # L0 OR HPort
    ("L1", BooleanOperation.OR, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 OR X
    ("L1", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 OR L0
    ("L1", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 OR L1
    ("L1", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),  # L1 OR H0
    ("L1", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="True", port_info=[]
    ),  # L1 OR H1
    ("L1", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 OR LPort
    ("L1", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 OR HPort
    ("H0", BooleanOperation.OR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),  # H0 OR X
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
    ),  # H0 OR L0
    ("H0", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # H0 OR L1
    ("H0", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 OR H0
    ("H0", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 OR H1
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
    ),  # H0 OR LPort
    ("H0", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),  # H0 OR HPort
    ("H1", BooleanOperation.OR, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 OR X
    ("H1", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0),
        ]
    ),  # H1 OR L0
    ("H1", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="True", port_info=[]
    ),  # H1 OR L1
    ("H1", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 OR H0
    ("H1", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 OR H1
    ("H1", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 OR LPort
    ("H1", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 OR HPort
    ("LPort", BooleanOperation.OR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort OR X
    ("LPort", BooleanOperation.OR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort OR L0
    ("LPort", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort OR L1
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
    ),  # LPort OR H0
    ("LPort", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # LPort OR H1
    ("LPort", BooleanOperation.OR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort OR LPort
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
    ),  # LPort OR HPort
    ("HPort", BooleanOperation.OR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort OR X
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
    ),  # HPort OR L0
    ("HPort", BooleanOperation.OR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort OR L1
    ("HPort", BooleanOperation.OR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),  # HPort OR H0
    ("HPort", BooleanOperation.OR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # HPort OR H1
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
    ),  # HPort OR LPort
    ("HPort", BooleanOperation.OR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort OR HPort


    (None, BooleanOperation.XOR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None XOR None
    ("X", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X XOR X
    ("X", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X XOR L0
    ("X", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X XOR L1
    ("X", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),  # X XOR H0
    ("X", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # X XOR H1
    ("X", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X XOR LPort
    ("X", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X XOR HPort
    ("L0", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 XOR X
    ("L0", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 XOR L0
    ("L0", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 XOR L1
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
    ),  # L0 XOR H0
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
    ),  # L0 XOR H1
    ("L0", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 XOR LPort
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
    ),  # L0 XOR HPort
    ("L1", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 XOR X
    ("L1", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 XOR L0
    ("L1", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 XOR L1
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
    ),  # L1 XOR H0
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
    ),  # L1 XOR H1
    ("L1", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 XOR LPort
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
    ),  # L1 XOR HPort
    ("H0", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),  # H0 XOR X
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
    ),  # H0 XOR L0
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
    ),  # H0 XOR L1
    ("H0", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 XOR H0
    ("H0", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 XOR H1
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
    ),  # H0 XOR LPort
    ("H0", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),  # H0 XOR HPort
    ("H1", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H1 XOR X
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
    ),  # H1 XOR L0
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
    ),  # H1 XOR L1
    ("H1", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 XOR H0
    ("H1", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 XOR H1
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
    ),  # H1 XOR LPort
    ("H1", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),  # H1 XOR HPort
    ("LPort", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort XOR X
    ("LPort", BooleanOperation.XOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort XOR L0
    ("LPort", BooleanOperation.XOR, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort XOR L1
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
    ),  # LPort XOR H0
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
    ),  # LPort XOR H1
    ("LPort", BooleanOperation.XOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort XOR LPort
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
    ),  # LPort XOR HPort
    ("HPort", BooleanOperation.XOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort XOR X
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
    ),  # HPort XOR L0
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
    ),  # HPort XOR L1
    ("HPort", BooleanOperation.XOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),  # HPort XOR H0
    ("HPort", BooleanOperation.XOR, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),  # HPort XOR H1
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
    ),  # HPort XOR LPort
    ("HPort", BooleanOperation.XOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort XOR HPort


    (None, BooleanOperation.IFF, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None IFF None
    ("X", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IFF X
    ("X", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IFF L0
    ("X", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IFF L1
    ("X", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # X IFF H0
    ("X", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0),
        ]
    ),  # X IFF H1
    ("X", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X IFF LPort
    ("X", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X IFF HPort
    ("L0", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IFF X
    ("L0", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IFF L0
    ("L0", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IFF L1
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
    ),  # L0 IFF H0
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
    ),  # L0 IFF H1
    ("L0", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 IFF LPort
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
    ),  # L0 IFF HPort
    ("L1", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IFF X
    ("L1", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IFF L0
    ("L1", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IFF L1
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
    ),  # L1 IFF H0
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
    ),  # L1 IFF H1
    ("L1", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 IFF LPort
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
    ),  # L1 IFF HPort
    ("H0", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H0 IFF X
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
    ),  # H0 IFF L0
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
    ),  # H0 IFF L1
    ("H0", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IFF H0
    ("H0", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IFF H1
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
    ),  # H0 IFF LPort
    ("H0", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),  # H0 IFF HPort
    ("H1", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),  # H1 IFF X
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
    ),  # H1 IFF L0
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
    ),  # H1 IFF L1
    ("H1", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 IFF H0
    ("H1", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 IFF H1
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
    ),  # H1 IFF LPort
    ("H1", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),  # H1 IFF HPort
    ("LPort", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IFF X
    ("LPort", BooleanOperation.IFF, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IFF L0
    ("LPort", BooleanOperation.IFF, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IFF L1
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
    ),  # LPort IFF H0
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
    ),  # LPort IFF H1
    ("LPort", BooleanOperation.IFF, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort IFF LPort
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
    ),  # LPort IFF HPort
    ("HPort", BooleanOperation.IFF, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort IFF X
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
    ),  # HPort IFF L0
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
    ),  # HPort IFF L1
    ("HPort", BooleanOperation.IFF, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),  # HPort IFF H0
    ("HPort", BooleanOperation.IFF, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1),
        ]
    ),  # HPort IFF H1
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
    ),  # HPort IFF LPort
    ("HPort", BooleanOperation.IFF, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort IFF HPort


    (None, BooleanOperation.NAND, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None NAND None
    ("X", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NAND X
    ("X", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NAND L0
    ("X", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NAND L1
    ("X", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NAND H0
    ("X", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # X NAND H1
    ("X", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X NAND LPort
    ("X", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X NAND HPort
    ("L0", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NAND X
    ("L0", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NAND L0
    ("L0", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NAND L1
    ("L0", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="True", port_info=[]
    ),  # L0 NAND H0
    ("L0", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # L0 NAND H1
    ("L0", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 NAND LPort
    ("L0", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 NAND HPort
    ("L1", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NAND X
    ("L1", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NAND L0
    ("L1", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NAND L1
    ("L1", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # L1 NAND H0
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
    ),  # L1 NAND H1
    ("L1", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 NAND LPort
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
    ),  # L1 NAND HPort
    ("H0", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NAND X
    ("H0", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="True", port_info=[]
    ),  # H0 NAND L0
    ("H0", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # H0 NAND L1
    ("H0", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NAND H0
    ("H0", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NAND H1
    ("H0", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NAND LPort
    ("H0", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NAND HPort
    ("H1", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H1 NAND X
    ("H1", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H1 NAND L0
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
    ),  # H1 NAND L1
    ("H1", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NAND H0
    ("H1", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NAND H1
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
    ),  # H1 NAND LPort
    ("H1", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),  # H1 NAND HPort
    ("LPort", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NAND X
    ("LPort", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NAND L0
    ("LPort", BooleanOperation.NAND, "L1"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NAND L1
    ("LPort", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # LPort NAND H0
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
    ),  # LPort NAND H1
    ("LPort", BooleanOperation.NAND, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort NAND LPort
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
    ),  # LPort NAND HPort
    ("HPort", BooleanOperation.NAND, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort NAND X
    ("HPort", BooleanOperation.NAND, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort NAND L0
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
    ),  # HPort NAND L1
    ("HPort", BooleanOperation.NAND, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # HPort NAND H0
    ("HPort", BooleanOperation.NAND, "H1"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),  # HPort NAND H1
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
    ),  # HPort NAND LPort
    ("HPort", BooleanOperation.NAND, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort NAND HPort


    (None, BooleanOperation.NOR, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None NOR None
    ("X", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NOR X
    ("X", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NOR L0
    ("X", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NOR L1
    ("X", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # X NOR H0
    ("X", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X NOR H1
    ("X", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X NOR LPort
    ("X", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X NOR HPort
    ("L0", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NOR X
    ("L0", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NOR L0
    ("L0", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 NOR L1
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
    ),  # L0 NOR H0
    ("L0", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # L0 NOR H1
    ("L0", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0, negation=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 NOR LPort
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
    ),  # L0 NOR HPort
    ("L1", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NOR X
    ("L1", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NOR L0
    ("L1", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 NOR L1
    ("L1", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # L1 NOR H0
    ("L1", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="False", port_info=[]
    ),  # L1 NOR H1
    ("L1", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 NOR LPort
    ("L1", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 NOR HPort
    ("H0", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H0 NOR X
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
    ),  # H0 NOR L0
    ("H0", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target2=0, negation=True),
        ]
    ),  # H0 NOR L1
    ("H0", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NOR H0
    ("H0", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 NOR H1
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
    ),  # H0 NOR LPort
    ("H0", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1, negation=True),
        ]
    ),  # H0 NOR HPort
    ("H1", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NOR X
    ("H1", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # H1 NOR L0
    ("H1", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="False", port_info=[]
    ),  # H1 NOR L1
    ("H1", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NOR H0
    ("H1", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NOR H1
    ("H1", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NOR LPort
    ("H1", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 NOR HPort
    ("LPort", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NOR X
    ("LPort", BooleanOperation.NOR, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NOR L0
    ("LPort", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort NOR L1
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
    ),  # LPort NOR H0
    ("LPort", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # LPort NOR H1
    ("LPort", BooleanOperation.NOR, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort NOR LPort
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
    ),  # LPort NOR HPort
    ("HPort", BooleanOperation.NOR, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort NOR X
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
    ),  # HPort NOR L0
    ("HPort", BooleanOperation.NOR, "L1"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort NOR L1
    ("HPort", BooleanOperation.NOR, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),  # HPort NOR H0
    ("HPort", BooleanOperation.NOR, "H1"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # HPort NOR H1
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
    ),  # HPort NOR LPort
    ("HPort", BooleanOperation.NOR, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort NOR HPort


    (None, BooleanOperation.IMPLY, None): BoxTreeNode(
        node=None, port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # None IMPLY None
    ("X", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="X", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IMPLY X
    ("X", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IMPLY L0
    ("X", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IMPLY L1
    ("X", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # X IMPLY H0
    ("X", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # X IMPLY H1
    ("X", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X IMPLY LPort
    ("X", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # X IMPLY HPort
    ("L0", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IMPLY X
    ("L0", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IMPLY L0
    ("L0", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L0 IMPLY L1
    ("L0", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # L0 IMPLY H0
    ("L0", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="True", port_info=[]
    ),  # L0 IMPLY H1
    ("L0", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 IMPLY LPort
    ("L0", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L0 IMPLY HPort
    ("L1", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IMPLY X
    ("L1", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="L0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IMPLY L0
    ("L1", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # L1 IMPLY L1
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
    ),  # L1 IMPLY H0
    ("L1", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # L1 IMPLY H1
    ("L1", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target2=0),
            PortConnectionInfo(target1=0, target2=1, recursion=True),
        ]
    ),  # L1 IMPLY LPort
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
    ),  # L1 IMPLY HPort
    ("H0", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IMPLY X
    ("H0", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, negation=True),
        ]
    ),  # H0 IMPLY L0
    ("H0", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="True", port_info=[]
    ),  # H0 IMPLY L1
    ("H0", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IMPLY H0
    ("H0", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IMPLY H1
    ("H0", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IMPLY LPort
    ("H0", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H0 IMPLY HPort
    ("H1", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=0),
        ]
    ),  # H1 IMPLY X
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
    ),  # H1 IMPLY L0
    ("H1", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target2=0),
        ]
    ),  # H1 IMPLY L1
    ("H1", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="H0", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 IMPLY H0
    ("H1", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # H1 IMPLY H1
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
    ),  # H1 IMPLY LPort
    ("H1", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target2=1),
        ]
    ),  # H1 IMPLY HPort
    ("LPort", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IMPLY X
    ("LPort", BooleanOperation.IMPLY, "L0"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, negation=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IMPLY L0
    ("LPort", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # LPort IMPLY L1
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
    ),  # LPort IMPLY H0
    ("LPort", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # LPort IMPLY H1
    ("LPort", BooleanOperation.IMPLY, "LPort"): BoxTreeNode(
        node="LPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # LPort IMPLY LPort
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
    ),  # LPort IMPLY HPort
    ("HPort", BooleanOperation.IMPLY, "X"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort IMPLY X
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
    ),  # HPort IMPLY L0
    ("HPort", BooleanOperation.IMPLY, "L1"): BoxTreeNode(
        node="L1", port_info=[
            PortConnectionInfo(target1=1, target2=0, recursion=True),
        ]
    ),  # HPort IMPLY L1
    ("HPort", BooleanOperation.IMPLY, "H0"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, negation=True),
        ]
    ),  # HPort IMPLY H0
    ("HPort", BooleanOperation.IMPLY, "H1"): BoxTreeNode(
        node="H1", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
        ]
    ),  # HPort IMPLY H1
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
    ),  # HPort IMPLY LPort
    ("HPort", BooleanOperation.IMPLY, "HPort"): BoxTreeNode(
        node="HPort", port_info=[
            PortConnectionInfo(target1=0, target2=0, recursion=True),
            PortConnectionInfo(target1=1, target2=1, recursion=True),
        ]
    ),  # HPort IMPLY HPort


}

# fmt: on
