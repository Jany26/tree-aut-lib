# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

.SILENT: all clean

all:
	cd src/ && python3 main.py
test:
	cd src/ && python3 test.py
clean:
#	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace *.ipynb
	-cd src/ && rm -r __pycache__/
	-cd src/ && rm *.pyc *.pyo *.pyd
	-cd src/ && rm -r dot/ tmb/ vtf/ vtf-to-dot/ dimacs-out/

# End of file Makefile
