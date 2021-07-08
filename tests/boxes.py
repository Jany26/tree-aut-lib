# boxes.py
# Examples of basic boxes - needed for testing
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)

testTransitionsBoxX = {
    'q0': {
        'a': ('q0', 'LH', ['q0', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q1'])
        }, 
    'q1': {
        'c': ('q1', 'Port', [])
    }
}

testTransitionsBoxL1 = {
    'q0': {
        'LH': ('q0', 'LH', ['q1', 'q0']),
        'LH': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'LH': ('q1', 'LH', ['q1', 'q1']),
        '0': ('q1', '0', [])
    },
    'q2': {
        'Port': ('q2', 'Port', [])
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
        'e': ('q2', 'Port', [])
    }
}

testTransitionsBoxH0 = {
    'q0': {
        'a': ('q0', 'LH', ['q0', 'q2']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'Port', [])
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
        'c': ('q1', 'Port', [])
    },
    'q2': {
        'd': ('q2', 'LH', ['q2', 'q2']),
        'e': ('q2', '1', [])
    }
}

testTransitionsBoxL1 = {
    'q0': {
        'a': ('q0', 'LH', ['q1', 'q0']),
        'b': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'c': ('q1', 'LH', ['q1', 'q1']),
        'd': ('q1', 'Port0', [])
    },
    'q2': {
        'e': ('q2', 'Port1', [])
    }
}