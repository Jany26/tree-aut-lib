# treeAut.py
# Basic classes needed for implementing tree automata
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

.SILENT: all clean

all:
	cd src/ && python3 main.py

clean:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace src/*.ipynb
	-cd src/ && rm -r __pycache__/
	-cd src/ && rm *.pyc *.pyo *.pyd
	-rm -r src/dot/ src/tmb/ src/vtf/ src/vtf-to-dot/

# End of file Makefile
