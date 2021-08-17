# A library for working with tree automata

This project was created for the purposes of testing the effectivity 
of using tree automata in BDDs as a means of their reduction.
Part of a work on an article on ABDDs = Automata-based Binary Decision Diagrams.

# Authors

Student: Jany26 / Jan Matufka <xmatuf00@stud.fit.vutbr.cz>
Supervisor: ondrik / Ing. Ondrej Lengal, PhD. <lengal@fit.vutbr.cz>

# File content

src/
    dot/            ... output data from export to DOT format
    tmb/            ... output data from export to TMB format
    vtf/            ... output data from export to VTF format
    vtf-to-dot/     ... output data from export to DOT from VTF format

    main.py         ... runs all test units from all_tests.py

    all_tests.py    ... contains test units for all functions from other modules
    test_boxes.py   ... transition relations for testing automata
    test_data.py    ... helpful structures used in tests
    test_trees.py   ... small tree examples used in tests (+ helping functions)

    format_dot.py   ... export TA to DOT format
    format_tmb.py   ... import/export TA to/from TMB format
    format_vtf.py   ... import/export TA to/from VATA format

    jupyter.py      ... integrates automata image export into Jupyter Notebook
    
    ta_classes.py   ... tree node and tree automaton classes
    ta_lib.py       ... basic library (operations) for working with tree automata

nta/ 
    tmb/ ... test data (tree automatons) - larger, more complex than in basic tests
    vtf/ ... test data (tree automatons) - larger, more complex than in basic tests

    ... more info at https://github.com/ondrik/automata-benchmarks