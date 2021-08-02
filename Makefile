# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

.SILENT: all

all:
	cd src/ && python3 all_tests.py

clean:
	cd src/ && rm -r __pycache__/
	cd src/ && rm *.pyc *.pyo *.pyd

# End of file Makefile
