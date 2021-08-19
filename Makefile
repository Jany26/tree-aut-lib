# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

.SILENT: all clean

all:
	cd src/ && python3 main.py

clean:
	-cd src/ && rm -r __pycache__/
	-cd src/ && rm *.pyc *.pyo *.pyd
	-cd src/dot && rm *
	-cd src/tmb && rm *
	-cd src/vtf && rm *
	-cd src/vtf-to-dot && rm *

# End of file Makefile
