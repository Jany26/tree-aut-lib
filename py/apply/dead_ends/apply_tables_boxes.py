from typing import Optional, Union
from apply.box_algebra.box_trees import BoxTreeNode
from apply.box_algebra.port_connection import PortConnectionInfo


# TODO: Figure out what kind of information should be stored wrt. to ports
# TODO: Find out an efficient way to store and use this info

# first of all


# these "tables" use two lookups (boxname in first operand ABDD, boxname in second operand ABBDD),
# the lookup result is a tuple of:
#   - box tree (leaf nodes will contain list of port connection information)
#   - port connection info array (sorted by lexicographic positions of ports within box structure)

x_node = BoxTreeNode("X")
l0_node = BoxTreeNode("L0")
l1_node = BoxTreeNode("L1")
h0_node = BoxTreeNode("H0")
h1_node = BoxTreeNode("H1")

lport_node = BoxTreeNode("LPort")
hport_node = BoxTreeNode("HPort")

iff0_node = BoxTreeNode("n", low=h0_node, high=l0_node)
iff1_node = BoxTreeNode("n", low=h1_node, high=l1_node)
iffport_node = BoxTreeNode("n", low=hport_node, high=lport_node)

mapping: dict[str, int] = {"X": 0, "L0": 1, "L1": 2, "H0": 3, "H1": 4, "LPort": 5, "HPort": 6}

# fmt: off

box_table_AND: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , l0_node     , lport_node  , h0_node     , hport_node  , lport_node  , hport_node  , ], # X
    [ l0_node     , l0_node     , l0_node     , 0           , l0_node     , l0_node     , l0_node     , ], # L0
    [ lport_node  , l0_node     , l1_node     , h0_node     , iff1_node   , lport_node  , iffport_node, ], # L1
    [ h0_node     , 0           , h0_node     , h0_node     , h0_node     , h0_node     , h0_node     , ], # H0
    [ hport_node  , l0_node     , iff1_node   , h0_node     , h1_node     , iffport_node, hport_node  , ], # H1
    [ lport_node  , l0_node     , lport_node  , h0_node     , iffport_node, lport_node  , iffport_node, ], # LPort
    [ hport_node  , l0_node     , iffport_node, h0_node     , hport_node  , iffport_node, hport_node  , ], # HPort
]
box_table_OR: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , lport_node  , l1_node     , hport_node  , h1_node     , lport_node  , hport_node  , ], # X
    [ lport_node  , l0_node     , l1_node     , iff0_node   , h1_node     , lport_node  , iffport_node, ], # L0
    [ l1_node     , l1_node     , l1_node     , l1_node     , 1           , l1_node     , l1_node     , ], # L1
    [ hport_node  , iff0_node   , l1_node     , h0_node     , h1_node     , iffport_node, hport_node  , ], # H0
    [ h1_node     , h1_node     , 1           , h1_node     , h1_node     , h1_node     , h1_node     , ], # H1
    [ lport_node  , lport_node  , l1_node     , iffport_node, h1_node     , lport_node  , iffport_node, ], # LPort
    [ hport_node  , iffport_node, l1_node     , hport_node  , h1_node     , iffport_node, hport_node  , ], # HPort
]
box_table_XOR: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , lport_node  , lport_node  , hport_node  , hport_node  , lport_node  , hport_node  , ], # X
    [ lport_node  , l0_node     , l1_node     , iff0_node   , iff1_node   , lport_node  , iffport_node, ], # L0
    [ lport_node  , l1_node     , l0_node     , iff1_node   , iff0_node   , lport_node  , iffport_node, ], # L1
    [ hport_node  , iff0_node   , iff1_node   , h0_node     , h1_node     , iffport_node, hport_node  , ], # H0
    [ hport_node  , iff1_node   , iff0_node   , h1_node     , h0_node     , iffport_node, hport_node  , ], # H1
    [ lport_node  , lport_node  , lport_node  , iffport_node, iffport_node, lport_node  , iffport_node, ], # LPort
    [ hport_node  , iffport_node, iffport_node, hport_node  , hport_node  , iffport_node, hport_node  , ], # HPort
]
box_table_IFF: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , lport_node  , lport_node  , hport_node  , hport_node  , lport_node  , hport_node  , ], # X
    [ lport_node  , l1_node     , l0_node     , iff1_node   , iff0_node   , lport_node  , iffport_node, ], # L0
    [ lport_node  , l0_node     , l1_node     , iff0_node   , iff1_node   , lport_node  , iffport_node, ], # L1
    [ hport_node  , iff1_node   , iff0_node   , h1_node     , h0_node     , iffport_node, hport_node  , ], # H0
    [ hport_node  , iff0_node   , iff1_node   , h0_node     , h1_node     , iffport_node, hport_node  , ], # H1
    [ lport_node  , lport_node  , lport_node  , iffport_node, iffport_node, lport_node  , iffport_node, ], # LPort
    [ hport_node  , iffport_node, iffport_node, hport_node  , hport_node  , iffport_node, hport_node  , ], # HPort
]
box_table_NAND: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , l1_node     , lport_node  , h1_node     , hport_node  , lport_node  , hport_node  , ], # X
    [ l1_node     , l1_node     , l1_node     , 1           , l1_node     , l1_node     , l1_node     , ], # L0
    [ lport_node  , l1_node     , l0_node     , h1_node     , iff0_node   , lport_node  , iffport_node, ], # L1
    [ h1_node     , 1           , h1_node     , h1_node     , h1_node     , h1_node     , h1_node     , ], # H0
    [ hport_node  , l1_node     , iff0_node   , h1_node     , h0_node     , iffport_node, hport_node  , ], # H1
    [ lport_node  , l1_node     , lport_node  , h1_node     , iffport_node, lport_node  , iffport_node, ], # LPort
    [ hport_node  , l1_node     , iffport_node, h1_node     , hport_node  , iffport_node, hport_node  , ], # HPort
]
box_table_NOR: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , lport_node  , l0_node     , hport_node  , h0_node     , lport_node  , hport_node  , ], # X
    [ lport_node  , l1_node     , l0_node     , iff1_node   , h0_node     , lport_node  , iffport_node, ], # L0
    [ l0_node     , l0_node     , l0_node     , l0_node     , 0           , l0_node     , l0_node     , ], # L1
    [ hport_node  , iff1_node   , l0_node     , h1_node     , h0_node     , iffport_node, hport_node  , ], # H0
    [ h0_node     , h0_node     , 0           , h0_node     , h0_node     , h0_node     , h0_node     , ], # H1
    [ lport_node  , lport_node  , l0_node     , iffport_node, h0_node     , lport_node  , iffport_node, ], # LPort
    [ hport_node  , iffport_node, l0_node     , hport_node  , h0_node     , iffport_node, hport_node  , ], # HPort
]
box_table_IMPLY: list[list[Union[BoxTreeNode, int]]] = [
    # X             L0            L1            H0            H1            LPort         HPort
    [ x_node      , lport_node  , l1_node     , hport_node  , h1_node     , lport_node  , hport_node  , ], # X
    [ l1_node     , l1_node     , l1_node     , l1_node     , 1           , l1_node     , l1_node     , ], # L0
    [ lport_node  , l0_node     , l1_node     , iff0_node   , h1_node     , lport_node  , iffport_node, ], # L1
    [ h1_node     , h1_node     , 1           , h1_node     , h1_node     , h1_node     , h1_node     , ], # H0
    [ hport_node  , iff0_node   , l1_node     , h0_node     , h1_node     , iffport_node, hport_node  , ], # H1
    [ lport_node  , lport_node  , l1_node     , iffport_node, h1_node     , lport_node  , iffport_node, ], # LPort
    [ hport_node  , iffport_node, l1_node     , hport_node  , h1_node     , iffport_node, hport_node  , ], # HPort
]


# fmt: on
