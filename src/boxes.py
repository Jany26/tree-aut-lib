# boxes.py
# Examples of basic boxes - needed for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *

testTransitionsBoxX = {
    'q0': {
        'a': ['q0', 'LH', ['q0', 'q0']],
        'b': ['q0', 'LH', ['q1', 'q1']]
        }, 
    'q1': {
        'c': ['q1', 'Port_X', []]
    }
}

testTransitionsBoxL0 = {
    'r0': {
        'a': ['r0', 'LH', ['r1', 'r0']],
        'b': ['r0', 'LH', ['r1', 'r2']]
        }, 
    'r1': {
        'c': ['r1', 'LH', ['r1', 'r1']],
        'd': ['r1', '0', []]
    },
    'r2': {
        'e': ['r2', 'Port_L0', []]
    }
}

testTransitionsBoxL1 = {
    's0': {
        'a': ['s0', 'LH', ['s1', 's0']],
        'b': ['s0', 'LH', ['s1', 's2']]
        }, 
    's1': {
        'c': ['s1', 'LH', ['s1', 's1']],
        'd': ['s1', '1', []]
    },
    's2': {
        'e': ['s2', 'Port_L1', []]
    }
}

testTransitionsBoxH0 = {
    't0': {
        'a': ['t0', 'LH', ['t0', 't2']],
        'b': ['t0', 'LH', ['t1', 't2']]
        }, 
    't1': {
        'c': ['t1', 'Port_H0', []]
    },
    't2': {
        'd': ['t2', 'LH', ['t2', 't2']],
        'e': ['t2', '0', []]
    }
}

testTransitionsBoxH1 = {
    'u0': {
        'a': ['u0', 'LH', ['u0', 'u2']],
        'b': ['u0', 'LH', ['u1', 'u2']]
        }, 
    'u1': {
        'c': ['u1', 'Port_H1', []]
    },
    'u2': {
        'd': ['u2', 'LH', ['u2', 'u2']],
        'e': ['u2', '1', []]
    }
}

testTransitionsBoxLPort = {
    'v0': {
        'a': ['v0', 'LH', ['v1', 'v0']],
        'b': ['v0', 'LH', ['v1', 'v2']]
        }, 
    'v1': {
        'c': ['v1', 'LH', ['v1', 'v1']],
        'd': ['v1', 'Port_LPort0', []]
    },
    'v2': {
        'e': ['v2', 'Port_LPort1', []]
    }
}

# End of file boxes.py
