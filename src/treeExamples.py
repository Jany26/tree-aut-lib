# treeExamples.py
# Some basic trees for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

from treeAut import *

# maybe load trees from this template form instead of calling class methods manually ???

XTreeExample1 = "LH[Port_X;Port_X]"
XTreeExample2 = "LH[LH[LH[Port_X;Port_X];Port_X];LH[Port_X;LH[Port_X;Port_X]]]"
XTreeExample3 = "LH[LH[Port_X;Port_X];LH[LH[LH[Port_X;Port_X];LH[Port_X;Port_X]];LH[Port_X;Port_X]]]"

L0TreeExample1 = "LH[0;LH[0;Port_L0]]"
L0TreeExample2 = "LH[0;LH[LH[LH[0;0];LH[0;0]];LH[0;Port_L0]]]"
L0TreeExample3 = "LH[LH[LH[0;0];LH[0;0]];LH[LH[0;0];LH[0;Port_L0]]]"

L1TreeExample1 = "LH[1;LH[1;Port_L1]]"
L1TreeExample2 = "LH[1;LH[LH[LH[1;1];LH[1;1]];LH[1;Port_L1]]]"
L1TreeExample3 = "LH[LH[LH[1;1];LH[1;1]];LH[LH[1;1];LH[1;Port_L1]]]"

H0TreeExample1 = "LH[LH[Port_H0;0];0]"
H0TreeExample2 = "LH[LH[LH[Port_H0;0];LH[LH[0;0];LH[0;0]]];0]"
H0TreeExample3 = "LH[LH[LH[Port_H0;0];LH[0;0]];LH[LH[0;0];LH[0;0]]]"

H1TreeExample1 = "LH[LH[Port_H1;1];1]"
H1TreeExample2 = "LH[LH[LH[Port_H1;1];LH[LH[1;1];LH[1;1]]];1]"
H1TreeExample3 = "LH[LH[LH[Port_H1;1];LH[1;1]];LH[LH[1;1];LH[1;1]]]"

treeXtest1 = buildTreeFromString(None, XTreeExample1)
treeXtest2 = buildTreeFromString(None, XTreeExample2)
treeXtest3 = buildTreeFromString(None, XTreeExample3)

treeL0test1 = buildTreeFromString(None, L0TreeExample1)
treeL0test2 = buildTreeFromString(None, L0TreeExample2)
treeL0test3 = buildTreeFromString(None, L0TreeExample3)

treeL1test1 = buildTreeFromString(None, L1TreeExample1)
treeL1test2 = buildTreeFromString(None, L1TreeExample2)
treeL1test3 = buildTreeFromString(None, L1TreeExample3)

treeH0test1 = buildTreeFromString(None, H0TreeExample1)
treeH0test2 = buildTreeFromString(None, H0TreeExample2)
treeH0test3 = buildTreeFromString(None, H0TreeExample3)

treeH1test1 = buildTreeFromString(None, H1TreeExample1)
treeH1test2 = buildTreeFromString(None, H1TreeExample2)
treeH1test3 = buildTreeFromString(None, H1TreeExample3)
