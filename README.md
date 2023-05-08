# A library for working with tree automata

This project was created for the purposes of testing the effectivity 
of using tree automata (TAs) in binary decision diagrams (BDDs) 
as a means of their reduction.

Part of a work on an article on ABDDs = Automata-based Binary Decision Diagrams.

# Authors

Student: Jany26 / Jan Matufka <xmatuf00@stud.fit.vutbr.cz>
Supervisor: ondrik / Ing. Ondrej Lengal, PhD. <lengal@fit.vutbr.cz>

# File structure and content

- py/ 

    - these files implement the functions and algorithms for tree-aut-lib

    * ta_classes.py   ... tree node and tree automaton classes
    * ta_lib.py       ... basic library (operations) for working with tree automata

    - these files and directories are used for testing: 

    * main.py         ... runs all test units from all_tests.py
    * tests/          ... test boxes (TAs) in vtf format
    * all_tests.py    ... contains test units for all functions from other modules
    * test_data.py    ... helpful structures used in tests (mainly TAs)
    * test_trees.py   ... small tree examples used in tests (+ helping functions)

    - these files are for importing and exporting TAs:

    * format_dot.py   ... export TA to DOT format
    * format_tmb.py   ... import/export TA to/from TMB format
    * format_vtf.py   ... import/export TA to/from VATA format

    * render_dot.py      ... integrates automata image export into Jupyter Notebook
    


    - these following directories are created as a result of tests:
    - (can be removed using `make clean`)

    * dot/            ... output data from export to DOT format
    * tmb/            ... output data from export to TMB format
    * vtf/            ... output data from export to VTF format
    * vtf-to-dot/     ... output data from export to DOT from VTF format

- benchmark/ ... test TAs - larger, more complex than in basic tests 
    - more info at https://github.com/ondrik/automata-benchmarks

    * tmb/ 
    * vtf/