testTransitionsBoxX = {
    'q0': {
        'LH': ('q0', 'LH', ['q0', 'q0']),
        'LH': ('q0', 'LH', ['q1', 'q1'])
        }, 
    'q1': {
        'Port': ('q1', 'Port', [])
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
        'LH': ('q0', 'LH', ['q1', 'q0']),
        'LH': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'LH': ('q1', 'LH', ['q1', 'q1']),
        '1': ('q1', '1', [])
    },
    'q2': {
        'Port': ('q2', 'Port', [])
    }
}

testTransitionsBoxH0 = {
    'q0': {
        'LH': ('q0', 'LH', ['q0', 'q2']),
        'LH': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'Port': ('q1', 'Port', [])
    },
    'q2': {
        'LH': ('q2', 'LH', ['q2', 'q2']),
        '0': ('q2', '0', [])
    }
}

testTransitionsBoxH1 = {
    'q0': {
        'LH': ('q0', 'LH', ['q0', 'q2']),
        'LH': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'Port': ('q1', 'Port', [])
    },
    'q2': {
        'LH': ('q2', 'LH', ['q2', 'q2']),
        '1': ('q2', '1', [])
    }
}

testTransitionsBoxL1 = {
    'q0': {
        'LH': ('q0', 'LH', ['q1', 'q0']),
        'LH': ('q0', 'LH', ['q1', 'q2'])
        }, 
    'q1': {
        'LH': ('q1', 'LH', ['q1', 'q1']),
        'Port0': ('q1', 'Port0', [])
    },
    'q2': {
        'Port1': ('q2', 'Port1', [])
    }
}