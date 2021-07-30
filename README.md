# A library for working with tree automata

This project was created for the purposes of testing the effectivity 
of using tree automata in BDDs as a means of their reduction.
Part of a work on an article on ABDDs = Automata-based Binary Decision Diagrams.

# Authors

Student: Jany26 <xmatuf00@stud.fit.vutbr.cz>
Supervisor: ondrik

# File content

src/
    out/ ... output data created during testing (export to VATA format)

    taClasses.py ... tree node and tree automaton classes
    taLib.py ... basic library (operations) for working with tree automata
    testData.py ... references for all data used in testSuite.py
    testSuite.py ... all unit tests for all taLib functions
    testExamples.py ... basic tree automata and small trees used in testSuite.py
    formatVTF.py ... functions for .vtf (VATA format) import and export
    formatDOT.py ... functions for exporting to .dot 

nta/ 
    ... test data (tree automatons) - larger, more complex than in testTAs.py

