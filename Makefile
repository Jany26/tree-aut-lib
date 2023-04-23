# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

.SILENT: all clean

all:
	cd py/ && python3 adhoc_tester.py
test:
	cd py/ && python3 all_tests.py
clean:
#	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace *.ipynb
	-cd py/ && rm -r __pycache__/
	-cd py/ && rm *.pyc *.pyo *.pyd
	-cd py/ && rm -r dot/ tmb/ vtf/ vtf-to-dot/ dimacs-out/

# End of file Makefile
