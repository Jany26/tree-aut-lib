## A library for working with tree automata

This project was created for the purposes of testing the effectivity
of using tree automata (TAs) in binary decision diagrams (BDDs)
as a means of their reduction.

Part of a work on an article on ABDDs = Automata-based Binary Decision Diagrams.

Keep in mind that this work is not yet supposed to be used in practice, 
it is merely a proof-of-concept that demonstrates that combining tree automata 
(using them as reduction rules) and binary decision diagrams can lead to some 
interesting results and allows more flexibility in how reductions can be applied.

# Authors

Student: Jany26 / Jan Matufka <xmatuf00@stud.fit.vutbr.cz>
Supervisor: ondrik / Ing. Ondrej Lengal, Ph.D. <lengal@fit.vutbr.cz>

# Notes

- this is a continuation of the work on Automata-based Binary Decision Diagrams
- the workspace should be opened using `./py` as a root directory for imports etc. to work properly
- for demonstration examples of implemented features, see Jupyter Notebooks in the `./py` directory

# Requirements

- `BuDDy` (2.4+) Binary Decision Diagram Library:
    - can be downloaded from: https://github.com/jgcoded/BuDDy 
    - or https://github.com/SSoelvsten/buddy (this repository is currently maintained)
    - documentation: https://buddy.sourceforge.net/manual/main.html
- `graphviz` (2.43.0+)- OS support for DOT language: https://graphviz.org/download/
- C++14 (for BLIF and DIMACS parsers in `./cpp`)
- Python 3.12+
- Python Virtual Environment + installing the dependencies in `abdds/requirements.txt`
    - Graphviz Python API for visualization of ABDDs/Tree Automata/UBDAs
    - Pandas, Matplotlib for creating graphs/plots
    - all other items in requirements are for working with Jupyter Notebooks

# Contents

```shell
├── benchmark  # contains all benchmarks used for evaluation/testing
│   ├── bdds  # n-queens and tictactoe (unused) instances
│   ├── blif  # collection of BLIF combinational circuits
│   ├── blif-processed  # preprocessed BLIF used during testing
│   ├── cnf-20var-processed  # preprocessed DIMACS CNFs into BDDs
│   ├── dimacs  # DIMACS CNF formulae
│   └── nta  # NTAs (sanity tests of tree automata operations)
├── cpp  # BLIF and DIMACS parsers to create BDDs using BuDDy library (C++)
├── py  # proof-of-concept implementation of ABDDs (Python)
│   ├── apply  # implementation of Apply on ABDDs <MAIN FOCUS>
│   │   ├── box_algebra  # reduced edge combining using automata operations
│   │   ├── materialization  # how to split reduced edges during Apply
│   │   └── pregenerated  # cached patterns for fast lookup during Apply
│   ├── bdd  # initial attempt to create benchmark BDDs
│   ├── box_ordering  # canonically order boxes based on language properties
│   ├── canonization  # algorithms for reducing ABDDs to canonical form
│   ├── experiments  # benchmark evaluation
│   ├── formats  # different parsers, and DOT visualization
│   ├── helpers  # some useful utilities
│   ├── tests  # unittests for important submodules
│   └── tree_automata  # tree automata class and some basic operations
├── results
│   ├── csv  # results of node count comparisons
│   ├── dimacs_analysis  # results of apply experiment
│   ├── figures  # generated plots for experiments
│   └── raw
└── tests  # test inputs
```
