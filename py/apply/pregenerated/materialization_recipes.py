from apply.materialization.abdd_pattern import MaterializationRecipe, ABDDPattern
from apply.materialization.pattern_generate import VariablePredicate


# fmt: off
predicate_set_X_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_X_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='q0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_X_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_X_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='q0<2,2>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_X_2 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_X_2 = MaterializationRecipe(init_box='X', init_targets=[
    ABDDPattern(new=True, name='q1<3,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_X_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_X_3 = MaterializationRecipe(init_box='X', init_targets=[
    ABDDPattern(new=True, name='q1<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_L0_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='r0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_L0_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='r0<2,2>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_L0_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='r0<2,2>', level='mat', low_box='X', high_box='L0', low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_L0_3 = MaterializationRecipe(init_box='L0', init_targets=[
    ABDDPattern(new=True, name='r0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_L0_4 = MaterializationRecipe(init_box='L0', init_targets=[
    ABDDPattern(new=True, name='r0<2,3>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L0_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_L0_5 = MaterializationRecipe(init_box='L0', init_targets=[
    ABDDPattern(new=True, name='r0<2,3>', level='mat', low_box='X', high_box='L0', low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_L1_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='s0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='1', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_L1_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='s0<2,2>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_L1_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='s0<2,2>', level='mat', low_box='X', high_box='L1', low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_L1_3 = MaterializationRecipe(init_box='L1', init_targets=[
    ABDDPattern(new=True, name='s0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='1', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_L1_4 = MaterializationRecipe(init_box='L1', init_targets=[
    ABDDPattern(new=True, name='s0<2,3>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_L1_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_L1_5 = MaterializationRecipe(init_box='L1', init_targets=[
    ABDDPattern(new=True, name='s0<2,3>', level='mat', low_box='X', high_box='L1', low=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_H0_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='t0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_H0_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='t0<2,2>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_H0_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='t0<2,2>', level='mat', low_box='H0', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_H0_3 = MaterializationRecipe(init_box='H0', init_targets=[
    ABDDPattern(new=True, name='t0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_H0_4 = MaterializationRecipe(init_box='H0', init_targets=[
    ABDDPattern(new=True, name='t0<2,3>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H0_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_H0_5 = MaterializationRecipe(init_box='H0', init_targets=[
    ABDDPattern(new=True, name='t0<2,3>', level='mat', low_box='H0', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_H1_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='u0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='1', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_H1_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='u0<2,2>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_H1_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='u0<2,2>', level='mat', low_box='H1', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "leaf"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_H1_3 = MaterializationRecipe(init_box='H1', init_targets=[
    ABDDPattern(new=True, name='u0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='1', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "leaf")])

materialization_recipe_H1_4 = MaterializationRecipe(init_box='H1', init_targets=[
    ABDDPattern(new=True, name='u0<2,3>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_H1_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "leaf"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_H1_5 = MaterializationRecipe(init_box='H1', init_targets=[
    ABDDPattern(new=True, name='u0<2,3>', level='mat', low_box='H1', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='0', level='leaf', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "1<", "out1")])

materialization_recipe_LPort_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='v0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out1"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_LPort_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='v0<2,2>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_LPort_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='v0<2,2>', level='mat', low_box='X', high_box='LPort', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "1<", "out1")])

materialization_recipe_LPort_3 = MaterializationRecipe(init_box='LPort', init_targets=[
    ABDDPattern(new=True, name='v1<3,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='v0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0")])

materialization_recipe_LPort_4 = MaterializationRecipe(init_box='LPort', init_targets=[
    ABDDPattern(new=True, name='v1<3,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
])

predicate_set_LPort_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out1"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_LPort_5 = MaterializationRecipe(init_box='LPort', init_targets=[
    ABDDPattern(new=True, name='v1<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='v0<2,3>', level='mat', low_box='X', high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_6 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_LPort_6 = MaterializationRecipe(init_box='LPort', init_targets=[
    ABDDPattern(new=True, name='v1<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='v0<2,3>', level='mat', low_box='X', high_box='LPort', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_LPort_7 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "out0")])

materialization_recipe_LPort_7 = MaterializationRecipe(init_box='LPort', init_targets=[
    ABDDPattern(new=True, name='v1<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
])

predicate_set_HPort_0 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "1<", "out1")])

materialization_recipe_HPort_0 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='w0<2,2>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_1 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_HPort_1 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='w0<2,2>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_2 = frozenset([VariablePredicate("in", "1<", "mat"), VariablePredicate("mat", "<<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_HPort_2 = MaterializationRecipe(init_box=None, init_targets=[
    ABDDPattern(new=True, name='w0<2,2>', level='mat', low_box='HPort', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_3 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "1<", "out1")])

materialization_recipe_HPort_3 = MaterializationRecipe(init_box='HPort', init_targets=[
    ABDDPattern(new=True, name='w0<2,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='w2<3,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_4 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_HPort_4 = MaterializationRecipe(init_box='HPort', init_targets=[
    ABDDPattern(new=True, name='w0<2,3>', level='mat', low_box=None, high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='w2<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_5 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "1<", "out1")])

materialization_recipe_HPort_5 = MaterializationRecipe(init_box='HPort', init_targets=[
    ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
    ABDDPattern(new=True, name='w2<3,3>', level='mat', low_box=None, high_box=None, low=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_6 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "out0"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_HPort_6 = MaterializationRecipe(init_box='HPort', init_targets=[
    ABDDPattern(new=True, name='w0<2,3>', level='mat', low_box='HPort', high_box='X', low=[
        ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ]),
    ABDDPattern(new=True, name='w2<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

predicate_set_HPort_7 = frozenset([VariablePredicate("in", "<<", "mat"), VariablePredicate("mat", "<<", "out1")])

materialization_recipe_HPort_7 = MaterializationRecipe(init_box='HPort', init_targets=[
    ABDDPattern(new=False, name='out0', level='out0', low_box=None, high_box=None, low=[], high=[]),
    ABDDPattern(new=True, name='w2<3,3>', level='mat', low_box='X', high_box='X', low=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ], high=[
        ABDDPattern(new=False, name='out1', level='out1', low_box=None, high_box=None, low=[], high=[])
    ])
])

cached_materialization_recipes: dict[str, dict[frozenset[VariablePredicate], MaterializationRecipe]] = {
    'X': {
        predicate_set_X_0: materialization_recipe_X_0,
        predicate_set_X_1: materialization_recipe_X_1,
        predicate_set_X_2: materialization_recipe_X_2,
        predicate_set_X_3: materialization_recipe_X_3,
    },
    'L0': {
        predicate_set_L0_0: materialization_recipe_L0_0,
        predicate_set_L0_1: materialization_recipe_L0_1,
        predicate_set_L0_2: materialization_recipe_L0_2,
        predicate_set_L0_3: materialization_recipe_L0_3,
        predicate_set_L0_4: materialization_recipe_L0_4,
        predicate_set_L0_5: materialization_recipe_L0_5,
    },
    'L1': {
        predicate_set_L1_0: materialization_recipe_L1_0,
        predicate_set_L1_1: materialization_recipe_L1_1,
        predicate_set_L1_2: materialization_recipe_L1_2,
        predicate_set_L1_3: materialization_recipe_L1_3,
        predicate_set_L1_4: materialization_recipe_L1_4,
        predicate_set_L1_5: materialization_recipe_L1_5,
    },
    'H0': {
        predicate_set_H0_0: materialization_recipe_H0_0,
        predicate_set_H0_1: materialization_recipe_H0_1,
        predicate_set_H0_2: materialization_recipe_H0_2,
        predicate_set_H0_3: materialization_recipe_H0_3,
        predicate_set_H0_4: materialization_recipe_H0_4,
        predicate_set_H0_5: materialization_recipe_H0_5,
    },
    'H1': {
        predicate_set_H1_0: materialization_recipe_H1_0,
        predicate_set_H1_1: materialization_recipe_H1_1,
        predicate_set_H1_2: materialization_recipe_H1_2,
        predicate_set_H1_3: materialization_recipe_H1_3,
        predicate_set_H1_4: materialization_recipe_H1_4,
        predicate_set_H1_5: materialization_recipe_H1_5,
    },
    'LPort': {
        predicate_set_LPort_0: materialization_recipe_LPort_0,
        predicate_set_LPort_1: materialization_recipe_LPort_1,
        predicate_set_LPort_2: materialization_recipe_LPort_2,
        predicate_set_LPort_3: materialization_recipe_LPort_3,
        predicate_set_LPort_4: materialization_recipe_LPort_4,
        predicate_set_LPort_5: materialization_recipe_LPort_5,
        predicate_set_LPort_6: materialization_recipe_LPort_6,
        predicate_set_LPort_7: materialization_recipe_LPort_7,
    },
    'HPort': {
        predicate_set_HPort_0: materialization_recipe_HPort_0,
        predicate_set_HPort_1: materialization_recipe_HPort_1,
        predicate_set_HPort_2: materialization_recipe_HPort_2,
        predicate_set_HPort_3: materialization_recipe_HPort_3,
        predicate_set_HPort_4: materialization_recipe_HPort_4,
        predicate_set_HPort_5: materialization_recipe_HPort_5,
        predicate_set_HPort_6: materialization_recipe_HPort_6,
        predicate_set_HPort_7: materialization_recipe_HPort_7,
    },
}
# fmt: on
