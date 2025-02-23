# decision diagram format (.dd)

An attempt to unify storing information about decision diagrams (BDDs, ZBDDs, etc.)
such that it can support ABDD requirements, such as:
- edge-specified reductions = boxes = tree automata references
- multiple targets for one edge (low/high) in case of multi-port boxes
- metadata about DD itself (especially number of variables), 
    - metadata could possibly be further extended to include box order,
    in which reductions are applied, i.e. reduction rule priority

Line comments start with `#`.
Each line from the node records explains exactly one node so no duplicate entries should be found.
Blank lines and comments do not break syntax, and are just simply ignored.

# syntax

FILE = `TYPE PREAMBLE NODERECORDS EOF`
TYPE = `@str`
PREAMBLE = `%Name str \n %Vars int \n %Root int\n`
NODERECORDS = `NODERECORD \n NODERECORDS | NODERECORD`
NODERECORD = `NODEIDX NODEVAR TARGET RULE TARGET RULE`
NODEIDX = `int`
NODEVAR = `[int]`
TARGET = `<leaf> |or (NODELIST) | NODEIDX`
NODELIST = `int, NODELIST | int`
RULE = `[str] | eps`

Some conventions:

TYPE = `ABDD`, `ZBDD`, `BDD`, ...
NODEIDX starts from 1
Variables also start from 1
leaf = 0 or 1 (could be extended to more in case of MTBDDs)

# extending to other types
in case of other types, the semantics of some fields might change
- i.e. rule in TBDDs is not a box, but a variable/bot symbol
- in case of CBDDs/CZDDs, variable would have to be a string `A:B`, where A, B are variables labeling chains
- in CESRBDDs, the rule would also have to contain the complement bit
- etc.

