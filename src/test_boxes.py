# test_boxes.py
# Some basic tree automata for testing (and helper functions)
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from ta_classes import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTING DATA - TREE AUTOMATA (Basic boxes from the article)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

testTransitionsBoxX = {
    'q0': {
        'a': ['q0', TEdge("LH", [None, None], ""), ['q0', 'q0']],
        'b': ['q0', TEdge("LH", [None, None], ""), ['q1', 'q1']]
        }, 
    'q1': {
        'c': ['q1', TEdge("Port_X", [], ""), []]
    }
}

testTransitionsBoxL0 = {
    'r0': {
        'a': ['r0', TEdge("LH", [None, None], ""), ['r1', 'r0']],
        'b': ['r0', TEdge("LH", [None, None], ""), ['r1', 'r2']]
        }, 
    'r1': {
        'c': ['r1', TEdge("LH", [None, None], ""), ['r1', 'r1']],
        'd': ['r1', TEdge("0", [], ""), []]
    },
    'r2': {
        'e': ['r2', TEdge("Port_L0", [], ""), []]
    }
}

testTransitionsBoxL1 = {
    's0': {
        'a': ['s0', TEdge("LH", [None, None], ""), ['s1', 's0']],
        'b': ['s0', TEdge("LH", [None, None], ""), ['s1', 's2']]
        }, 
    's1': {
        'c': ['s1', TEdge("LH", [None, None], ""), ['s1', 's1']],
        'd': ['s1', TEdge("1", [], ""), []]
    },
    's2': {
        'e': ['s2', TEdge("Port_L1", [], ""), []]
    }
}

testTransitionsBoxH0 = {
    't0': {
        'a': ['t0', TEdge("LH", [None, None], ""), ['t0', 't2']],
        'b': ['t0', TEdge("LH", [None, None], ""), ['t1', 't2']]
        }, 
    't1': {
        'c': ['t1', TEdge("Port_H0", [], ""), []]
    },
    't2': {
        'd': ['t2', TEdge("LH", [None, None], ""), ['t2', 't2']],
        'e': ['t2', TEdge("0", [], ""), []]
    }
}

testTransitionsBoxH1 = {
    'u0': {
        'a': ['u0', TEdge("LH", [None, None], ""), ['u0', 'u2']],
        'b': ['u0', TEdge("LH", [None, None], ""), ['u1', 'u2']]
        }, 
    'u1': {
        'c': ['u1', TEdge("Port_H1", [], ""), []]
    },
    'u2': {
        'd': ['u2', TEdge("LH", [None, None], ""), ['u2', 'u2']],
        'e': ['u2', TEdge("1", [], ""), []]
    }
}

testTransitionsBoxLPort = {
    'v0': {
        'a': ['v0', TEdge("LH", [None, None], ""), ['v1', 'v0']],
        'b': ['v0', TEdge("LH", [None, None], ""), ['v1', 'v2']]
        }, 
    'v1': {
        'c': ['v1', TEdge("LH", [None, None], ""), ['v1', 'v1']],
        'd': ['v1', TEdge("Port_LPort0", [], ""), []]
    },
    'v2': {
        'e': ['v2', TEdge("Port_LPort1", [], ""), []]
    }
}

testTransitionsBoxHPort = { # symmetric alternative to LPort
    'w0': {
        'a': ['w0', TEdge("LH", [None, None], ""), ['w1', 'w0']],
        'b': ['w0', TEdge("LH", [None, None], ""), ['w1', 'w2']]
        }, 
    'w1': {
        'c': ['w1', TEdge("Port_HPort0", [], ""), []]
    },
    'w2': {
        'd': ['w2', TEdge("LH", [None, None], ""), ['w2', 'w2']],
        'e': ['w2', TEdge("Port_HPort1", [], ""), []]
    }
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Testing boxes = with top-down/bottom-up unreachable states ...
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

unreachableTest1 = {
    'q0': {
        'a': ['q0', TEdge("LH", [None, None], ""), ['q1', 'q0']],
    },
    'q1': {
        'b': ['q1', TEdge("1", [], ""), []]
    }
}

# basically H1 box with extra 2 states = q3, q4 and 3 transitions f-h
unreachableTest2a = {
    'q0': {
        'a': ['q0', TEdge("LH", [None, None], ""), ['q1', 'q2']],
        'b': ['q0', TEdge("LH", [None, None], ""), ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1',TEdge("Port", [], ""), []],
    },
    'q2': {
        'd': ['q2', TEdge("LH", [None, None], ""), ['q2', 'q2']],
        'e': ['q2', TEdge("1", [], ""), []],
        'f': ['q2', TEdge("LH", [None, None], ""), ['q2', 'q3']],
    },
    'q3': {
        'g': ['q3', TEdge("1", [], ""), []],
    },
    'q4': {
        'h': ['q4', TEdge("LH", [None, None], ""), ['q4','q3']],
    }
}

# same as unreachableTest2, but 'f' transition connects to root not to itself 
unreachableTest2b = {
    'q0': {
        'a': ['q0', TEdge("LH", [None, None], ""), ['q1', 'q2']],
        'b': ['q0', TEdge("LH", [None, None], ""), ['q0', 'q2']],
    },
    'q1': {
        'c': ['q1', TEdge("Port", [], ""), []],
    },
    'q2': {
        'd': ['q2', TEdge("LH", [None, None], ""), ['q2', 'q2']],
        'e': ['q2', TEdge("1", [], ""), []],
        'f': ['q2', TEdge("LH", [None, None], ""), ['q0', 'q3']],
    },
    'q3': {
        'g': ['q3', TEdge("1", [], ""), []],
    },
    'q4': {
        'h': ['q4', TEdge("LH", [None, None], ""), ['q4','q3']],
    }
}

# End of file test_boxes.py
