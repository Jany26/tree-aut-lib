import unittest

from apply.abdd import ABDD, import_abdd_from_abdd_file
from apply.materialization.abdd_pattern import ABDDPattern, MaterializationRecipe
from apply.materialization.box_materialization import create_materialized_box_wrapper
from apply.materialization.pattern_finding import abdd_subsection_create_wrapper
from tree_automata.automaton import TTreeAut


class TestMaterializationLPortUneven(unittest.TestCase):
    abdd: ABDD = import_abdd_from_abdd_file("../tests/apply/materialization-inputs/materialization-lport-10-7.dd")
    direction = False  # false = low, true = high
    # nodelist = abdd.roots[0].high if direction else abdd.roots[0].low
    nodelist = ["out0", "out1"]
    # varlist = [10, 7]
    varlist = ["out0", "out1"]
    matlevel = "mat"

    def test_materialization_lport_10_7_at_level_2(self):
        materialization_level = 2
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="LPort",
                    high=[
                        ABDDPattern(level=self.varlist[0], name=self.nodelist[0]),
                        ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_3(self):
        materialization_level = 3
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="LPort",
                    high=[
                        ABDDPattern(level=self.varlist[0], name=self.nodelist[0]),
                        ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
                    ],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_4(self):
        materialization_level = 4
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="LPort",
                    high=[
                        ABDDPattern(level=self.varlist[0], name=self.nodelist[0]),
                        ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
                    ],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_6(self):
        materialization_level = 6
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=self.varlist[1], name=self.nodelist[1])],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_7(self):
        materialization_level = 7
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
            ],
        )
        print(recipe)
        print(expected_recipe)
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_8(self):
        materialization_level = 8
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_9(self):
        materialization_level = 9
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                ),
                ABDDPattern(level=self.varlist[1], name=self.nodelist[1]),
            ],
        )
        self.assertEqual(recipe, expected_recipe)


class TestMaterializationLPortShort(unittest.TestCase):
    abdd: ABDD = import_abdd_from_abdd_file("../tests/apply/materialization-inputs/materialization-lport-10-7.dd")
    direction = False  # false = low, true = high
    # nodelist = abdd.roots[0].high if direction else abdd.roots[0].low
    nodelist = ["out0", "out1"]
    # varlist = [10, 7]
    varlist = ["out0", "out1"]
    matlevel = "mat"

    def test_materialization_lport_3_3_at_level_2(self):
        self.abdd.roots[0].low[0].var = 3
        self.abdd.roots[0].low[1].var = 3
        materialization_level = 2
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=self.varlist[1], name=self.nodelist[1])],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_3_at_level_2(self):
        # self.abdd.roots[0].low[0].var = 3
        self.abdd.roots[0].low[1].var = 3
        materialization_level = 2
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    low=[ABDDPattern(level=self.varlist[0], name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=self.varlist[1], name=self.nodelist[1])],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)


class TestMaterializationX(unittest.TestCase):
    abdd: ABDD = import_abdd_from_abdd_file("../tests/apply/materialization-inputs/materialization-x-4.dd")
    direction = False
    outnode = "out0"
    outlevel = "out0"
    matlevel = "mat"

    def test_materialization_x_3_at_level_2(self):
        self.abdd.roots[0].low[0].var = 3
        materialization_level = 2
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)
        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_x_4_at_level_2(self):
        self.abdd.roots[0].low[0].var = 4
        materialization_level = 2
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)
        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box="X",
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_x_4_at_level_3(self):
        self.abdd.roots[0].low[0].var = 4
        materialization_level = 3
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)
        expected_recipe = MaterializationRecipe(
            init_box="X",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_x_5_at_level_3(self):
        self.abdd.roots[0].low[0].var = 5
        materialization_level = 3
        res = create_materialized_box_wrapper(
            self.abdd.roots[0], self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)
        expected_recipe = MaterializationRecipe(
            init_box="X",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box="X",
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)


class TestMaterializationL0(unittest.TestCase):
    abdd: ABDD = import_abdd_from_abdd_file("../tests/apply/materialization-inputs/materialization-x-4.dd")
    abdd.roots[0].low_box = "L0"
    direction = False
    outnode = "out0"
    outlevel = "out0"
    matlevel = "mat"
    leafnode = "0"
    leaflevel = "leaf"

    def test_materialization_l0_3_at_level_2_leaf_3(self):
        self.abdd.roots[0].low[0].var = 3
        materialization_level = 2
        leaf_level = 3
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)
        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_l0_3_at_level_2_leaf_4(self):
        self.abdd.roots[0].low[0].var = 3
        materialization_level = 2
        leaf_level = 4
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_l0_4_at_level_2_leaf_4(self):
        self.abdd.roots[0].low[0].var = 4
        materialization_level = 2
        leaf_level = 4
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box="L0",
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_l0_4_at_level_3_leaf_4(self):
        self.abdd.roots[0].low[0].var = 4
        materialization_level = 3
        leaf_level = 4
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="L0",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box=None,
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_l0_4_at_level_3_leaf_5(self):
        self.abdd.roots[0].low[0].var = 4
        materialization_level = 3
        leaf_level = 5
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="L0",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box=None,
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_l0_5_at_level_3_leaf_5(self):
        self.abdd.roots[0].low[0].var = 5
        materialization_level = 3
        leaf_level = 5
        res = create_materialized_box_wrapper(self.abdd.roots[0], self.direction, materialization_level, leaf_level)
        recipe = abdd_subsection_create_wrapper(self.abdd, self.abdd.roots[0], self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="L0",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=self.matlevel,
                    low_box="X",
                    high_box="L0",
                    low=[
                        ABDDPattern(
                            new=False,
                            name=self.leafnode,
                            level=self.leaflevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                    high=[
                        ABDDPattern(
                            new=False,
                            name=self.outnode,
                            level=self.outlevel,
                            low_box=None,
                            high_box=None,
                            low=[],
                            high=[],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)


class TestMaterializationLPortOther(unittest.TestCase):

    def test_lport_hport_partial_mismatches_uneven(self):
        # LPort-07-04 | HPort-04-07
        # LPort-07-04 | HPort-04-10
        # LPort-07-04 | HPort-04-13
        # LPort-07-04 | HPort-07-10
        # LPort-07-04 | HPort-07-13

        # LPort-10-04 | HPort-04-07
        # LPort-10-04 | HPort-04-10
        # LPort-10-04 | HPort-04-13
        # LPort-10-04 | HPort-07-10
        # LPort-10-04 | HPort-10-13

        # LPort-13-04 | HPort-04-07
        # LPort-13-04 | HPort-04-10
        # LPort-13-04 | HPort-04-13
        # LPort-13-04 | HPort-07-13
        # LPort-13-04 | HPort-10-13

        # not worth to check other ways
        pass

    def test_lport_hport_partial_mismatches_even(self):
        # TODO: create some even LPort/HPort boxes -- i.e. HPort-04-04, HPort-07-07, HPort-10-10
        pass

    def test_lport_x_mismatches(self):
        pass

    def test_hport_x_mismatches(self):
        pass
