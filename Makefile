# Implementation of tree automata for article about automata-based BDDs
# [author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

# make test => run regression test suite => can be configured at the bottom
# of all_tests.py

# make => run adhoc_tester.py => used during debugging etc.

.SILENT: all clean

all:
	cd py/ && python3 adhoc_tester.py
test:
	cd py/ && python3 all_tests.py
clean:
#	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace *.ipynb
	-cd py/ && rm -r __pycache__/
	-cd py/ && rm *.pyc *.pyo *.pyd
	-cd data/ && rm -r dot/ tmb/ vtf/ vtf-to-dot/
