import unittest

from apply.box_algebra.apply_tables import BooleanOperation
from apply.box_algebra.apply_intersectoid import apply_intersectoid_create
from apply.box_algebra.box_trees import BoxTreeNode, build_box_tree

from apply.box_algebra.port_connection import PortConnectionInfo
from helpers.utils import box_catalogue


class TestBoxTreeSimpleNonX(unittest.TestCase):
    def test_boxtree_l1_or_l0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["L1"], box_catalogue["L0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="L1", port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_l1_and_l0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["L1"], box_catalogue["L0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="L0", port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_h0_or_l1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["L1"], box_catalogue["H0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="L1", port_info=[PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_h0_and_l1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["L1"], box_catalogue["H0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="H0", port_info=[PortConnectionInfo(target1=None, target2=0, recursion=False, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)


class TestBoxTreeSimpleX(unittest.TestCase):
    def test_boxtree_x_or_l0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["X"], box_catalogue["L0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="LPort",
            port_info=[
                PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False),
                PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
            ],
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_x_or_h0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["X"], box_catalogue["H0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="HPort",
            port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
                PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False),
            ],
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_x_or_h1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["X"], box_catalogue["H1"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="H1", port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_x_and_l0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["X"], box_catalogue["L0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="L0", port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_x_and_l1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["X"], box_catalogue["L1"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="LPort",
            port_info=[
                PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False),
                PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
            ],
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_x_and_h1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["X"], box_catalogue["H1"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="HPort",
            port_info=[
                PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
                PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False),
            ],
        )
        self.assertEqual(boxtree, expected_boxtree)


class TestBoxTreeTrivial(unittest.TestCase):
    def test_boxtree_l0_and_h0(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["L0"], box_catalogue["H0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(node="False")
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_l1_or_h1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["L1"], box_catalogue["H1"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(node="True")
        self.assertEqual(boxtree, expected_boxtree)


class TestBoxTreeMultinode(unittest.TestCase):
    def test_boxtree_l1_and_h1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["L1"], box_catalogue["H1"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="non-leaf",
            is_leaf=False,
            low=BoxTreeNode(
                node="H1", port_info=[PortConnectionInfo(target1=None, target2=0, recursion=False, negation=False)]
            ),
            high=BoxTreeNode(
                node="L1", port_info=[PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False)]
            ),
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_l1_or_h1(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["L0"], box_catalogue["H0"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="non-leaf",
            is_leaf=False,
            low=BoxTreeNode(
                node="H0", port_info=[PortConnectionInfo(target1=None, target2=0, recursion=False, negation=False)]
            ),
            high=BoxTreeNode(
                node="L0", port_info=[PortConnectionInfo(target1=0, target2=None, recursion=False, negation=False)]
            ),
        )
        self.assertEqual(boxtree, expected_boxtree)


class TestBoxTreeMultiportBoxes(unittest.TestCase):
    def test_boxtree_lport_and_hport(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.AND, box_catalogue["LPort"], box_catalogue["HPort"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="non-leaf",
            is_leaf=False,
            low=BoxTreeNode(
                node="HPort",
                port_info=[
                    PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
                    PortConnectionInfo(target1=0, target2=1, recursion=True, negation=False),
                ],
            ),
            high=BoxTreeNode(
                node="LPort",
                port_info=[
                    PortConnectionInfo(target1=0, target2=1, recursion=True, negation=False),
                    PortConnectionInfo(target1=1, target2=1, recursion=True, negation=False),
                ],
            ),
        )
        self.assertEqual(boxtree, expected_boxtree)

    def test_boxtree_lport_or_hport(self):
        aut, pmap = apply_intersectoid_create(BooleanOperation.OR, box_catalogue["LPort"], box_catalogue["HPort"])
        boxtree = build_box_tree(aut, pmap)
        expected_boxtree = BoxTreeNode(
            node="non-leaf",
            is_leaf=False,
            low=BoxTreeNode(
                node="HPort",
                port_info=[
                    PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False),
                    PortConnectionInfo(target1=0, target2=1, recursion=True, negation=False),
                ],
            ),
            high=BoxTreeNode(
                node="LPort",
                port_info=[
                    PortConnectionInfo(target1=0, target2=1, recursion=True, negation=False),
                    PortConnectionInfo(target1=1, target2=1, recursion=True, negation=False),
                ],
            ),
        )
        self.assertEqual(boxtree, expected_boxtree)
