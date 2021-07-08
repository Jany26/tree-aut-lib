# boxes.py
# Examples of basic boxes - needed for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)
from treeAut import *

testTransitionsBoxX = {
    'q0': {
        'a': ('q0', 'LH', ['q0', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q1'])
        }, 
    'q1': {
        'c': ('q1', 'Port_X', [])
    }
}

testTransitionsBoxL0 = {
    'q0': {
        'a': ('q0', 'LH', ['q1', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'LH', ['q1', 'q1']),
        'd': ('q1', '0', [])
    },
    'q2': {
        'e': ('q2', 'Port_L0', [])
    }
}

testTransitionsBoxL1 = {
    'q0': {
        'a': ('q0', 'LH', ['q1', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'LH', ['q1', 'q1']),
        'd': ('q1', '1', [])
    },
    'q2': {
        'e': ('q2', 'Port_L1', [])
    }
}

testTransitionsBoxH0 = {
    'q0': {
        'a': ('q0', 'LH', ['q0', 'q2']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'Port_H0', [])
    },
    'q2': {
        'd': ('q2', 'LH', ['q2', 'q2']),
        'e': ('q2', '0', [])
    }
}

testTransitionsBoxH1 = {
    'q0': {
        'a': ('q0', 'LH', ['q0', 'q2']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'Port_H1', [])
    },
    'q2': {
        'd': ('q2', 'LH', ['q2', 'q2']),
        'e': ('q2', '1', [])
    }
}

testTransitionsBoxLPort = {
    'q0': {
        'a': ('q0', 'LH', ['q1', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'LH', ['q1', 'q1']),
        'd': ('q1', 'Port_LPort0', [])
    },
    'q2': {
        'e': ('q2', 'Port_LPort1', [])
    }
}

# first argument is a list of all "root" states
# "leaf" states are recognized by having at least one transition which
# has an empty tuple at the end (descendants) -> "output edge"

boxX = TTreeAut(["q0"], testTransitionsBoxX)
boxL0 = TTreeAut(["q0"], testTransitionsBoxL0)
boxL1 = TTreeAut(["q0"], testTransitionsBoxL1)
boxH0 = TTreeAut(["q0"], testTransitionsBoxH0)
boxH1 = TTreeAut(["q0"], testTransitionsBoxH1)
boxLPort = TTreeAut(["q0"], testTransitionsBoxLPort)