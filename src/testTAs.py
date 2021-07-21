# testTAs.py
# Examples of basic boxes - needed for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from taLib import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Basic boxes from the article
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Testing boxes = with top-down/bottom-up unreachable states ...
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

unreachableTest1 = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q0']],
    },
    'q1': {
        'b': ['q1', '1', []]
    }
}

# basically H1 box with extra 2 states = q3, q4 and 3 transitions f-h
unreachableTest2a = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q2']],
        'b': ['q0', 'LH', ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1','Port', []],
    },
    'q2': {
        'd': ['q2', 'LH', ['q2', 'q2']],
        'e': ['q2', '1', []],
        'f': ['q2', 'LH', ['q2', 'q3']],
    },
    'q3': {
        'g': ['q3', '1', []],
    },
    'q4': {
        'h': ['q4', 'LH', ['q4','q3']],
    }
}

# same as unreachableTest2, but 'f' transition connects to root not to itself 
unreachableTest2b = {
    'q0': {
        'a': ['q0', 'LH', ['q1', 'q2']],
        'b': ['q0', 'LH', ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1','Port', []],
    },
    'q2': {
        'd': ['q2', 'LH', ['q2', 'q2']],
        'e': ['q2', '1', []],
        'f': ['q2', 'LH', ['q0', 'q3']],
    },
    'q3': {
        'g': ['q3', '1', []],
    },
    'q4': {
        'h': ['q4', 'LH', ['q4','q3']],
    }
}

# End of file testTAs.py
