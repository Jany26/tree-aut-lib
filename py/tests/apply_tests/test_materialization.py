import unittest

from apply.abdd import ABDD, import_abdd_from_abdd_file
from apply.abdd_pattern import ABDDPattern, MaterializationRecipe
from apply.box_materialization import create_materialized_box
from apply.pattern_finding import abdd_subsection_create
from tree_automata.automaton import TTreeAut


class TestMaterializationLPortUneven(unittest.TestCase):
    abdd: ABDD = import_abdd_from_abdd_file("../tests/apply/materialization-inputs/materialization-lport-10-7.dd")
    direction = False  # false = low, true = high
    nodelist = abdd.root.high if direction else abdd.root.low

    def test_materialization_lport_10_7_at_level_2(self):
        materialization_level = 2
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box=None,
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="LPort",
                    high=[ABDDPattern(level=10, name=self.nodelist[0]), ABDDPattern(level=7, name=self.nodelist[1])],
                )
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_3(self):
        materialization_level = 3
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="LPort",
                    high=[ABDDPattern(level=10, name=self.nodelist[0]), ABDDPattern(level=7, name=self.nodelist[1])],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_4(self):
        materialization_level = 4
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="LPort",
                    high=[ABDDPattern(level=10, name=self.nodelist[0]), ABDDPattern(level=7, name=self.nodelist[1])],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_6(self):
        materialization_level = 6
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=7, name=self.nodelist[1])],
                ),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_7(self):
        materialization_level = 7
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(level=7, name=self.nodelist[1]),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_8(self):
        materialization_level = 8
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box="X",
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box="X",
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(level=7, name=self.nodelist[1]),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

    def test_materialization_lport_10_7_at_level_9(self):
        materialization_level = 9
        res = create_materialized_box(
            self.abdd.root, self.direction, materialization_level, self.abdd.variable_count + 1
        )
        recipe = abdd_subsection_create(self.abdd, self.abdd.root, self.direction, res)

        expected_recipe = MaterializationRecipe(
            init_box="LPort",
            init_targets=[
                ABDDPattern(
                    new=True,
                    level=materialization_level,
                    low_box=None,
                    low=[ABDDPattern(level=10, name=self.nodelist[0])],
                    high_box=None,
                    high=[ABDDPattern(level=10, name=self.nodelist[0])],
                ),
                ABDDPattern(level=7, name=self.nodelist[1]),
            ],
        )
        self.assertEqual(recipe, expected_recipe)

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
