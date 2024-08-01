"""
[file] all_tests.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Some basic testing for tree implementation and tree automata
"""

from io import TextIOWrapper
import os
import gc

from test_data import function_ptrs
from format_vtf import *
from format_tmb import *
from format_dot import *

from coocurrence import *
from unfolding import *
from normalization import *
from folding import *
from simulation import *
from bdd import add_dont_care_boxes, BDD, BDDnode, compare_bdds
from bdd_apply import apply_function

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HELPER FUNCTIONS FOR TEST SUITES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


verbose = False


def print_failed_tests(failed_tests_array):
    try:
        assert failed_tests_array == []
    except AssertionError:
        print("   ## Tests failed (" + str(len(failed_tests_array)) + "):")
        for i in failed_tests_array:
            print("      " + i)


def match_test(function: str, ta: str, tree: str, expected_result, failures):
    func = function_ptrs[function]
    box = boxes_dict[ta]
    test_tree = test_tree_dict[tree]
    actual_result = func(box, test_tree)
    if expected_result != actual_result:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"{function}({ta}, {tree})", str(expected_result), str(actual_result)
        ))


def non_empty_test(function: str, ta: str, expected_result, failures):
    func = function_ptrs[function]
    box = boxes_dict[ta]
    test_tree, test_str = func(box)
    actual_result = False if (test_tree is None or test_str == "") else True
    if expected_result != actual_result:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"{function}({ta})", str(expected_result), str(actual_result)
        ))


def well_defined_test(ta: str, expected_result, err_display, failures):
    box = boxes_dict[ta]
    actual_result = is_well_defined(box, err_display)
    if actual_result != expected_result:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"is_well_defined({ta})", str(expected_result), str(actual_result)
        ))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TESTS FOR SUBFUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_output_states_tests():
    print(" > SUBUNIT TEST: testing get_output_states_tests() ...")
    failures = []

    if not box_X.get_output_states() == ['q1']:
        failures.append("boxX.get_output_states_tests()")
    if not box_H1.get_output_states() == ['u1', 'u2']:
        failures.append("boxH1.get_output_states_tests()")

    print_failed_tests(failures)


def get_arity_dict_tests():
    print(" > SUBUNIT TEST: testing get_arity_dict() ...")
    failures = []

    if box_X.get_symbol_arity_dict() != {'LH': 2, 'Port_X': 0}:
        failures.append("boxX.get_symbol_arity_dict()")
    if box_L0.get_symbol_arity_dict() != {'LH': 2, '0': 0, 'Port_L0': 0}:
        failures.append("boxL0.get_symbol_arity_dict()")
    if box_L1.get_symbol_arity_dict() != {'LH': 2, '1': 0, 'Port_L1': 0}:
        failures.append("boxL1.get_symbol_arity_dict()")
    if box_H0.get_symbol_arity_dict() != {'LH': 2, 'Port_H0': 0, '0': 0}:
        failures.append("boxH0.get_symbol_arity_dict()")
    if box_H1.get_symbol_arity_dict() != {'LH': 2, 'Port_H1': 0, '1': 0}:
        failures.append("boxH1.get_symbol_arity_dict()")
    if box_LPort.get_symbol_arity_dict() != {'LH': 2, 'Port_LPort0': 0, 'Port_LPort1': 0}:
        failures.append("boxLPort.get_symbol_arity_dict()")

    print_failed_tests(failures)


def remove_state_tests():
    print(" > SUBUNIT TEST: testing removeState() ...")
    failures = []

    box_L0_without_r2 = copy.deepcopy(box_L0)
    box_L0_without_r2.remove_state('r2')
    boxes_dict["boxL0withoutR2"] = box_L0_without_r2
    box_L1_without_s0 = copy.deepcopy(box_L1)
    box_L1_without_s0.remove_state('s0')
    boxes_dict["boxL1withoutS0"] = box_L1_without_s0

    match_test("match_tree_top_down", "boxL0withoutR2", "treeL0test1", False, failures)
    match_test("match_tree_top_down", "boxL0withoutR2", "treeL0test2", False, failures)
    match_test("match_tree_top_down", "boxL0withoutR2", "treeL0test3", False, failures)
    match_test("match_tree_top_down", "boxL0withoutR2", "treeL0test4", False, failures)

    match_test("match_tree_top_down", "boxL1withoutS0", "treeL1test1", False, failures)
    match_test("match_tree_top_down", "boxL1withoutS0", "treeL1test2", False, failures)
    match_test("match_tree_top_down", "boxL1withoutS0", "treeL1test3", False, failures)
    match_test("match_tree_top_down", "boxL1withoutS0", "treeL1test4", False, failures)

    print_failed_tests(failures)


def generate_tuples_test():
    print(" > SUBUNIT TEST: testing generator of possible_children_tuples ...")
    failures = []

    if len(generate_possible_children('q0', ['q0', 'q1', 'q2'], 3)) != 19:
        failures.append("generate_possible_children('q0', ['q0', 'q1', 'q2'], 3)")
    if len(generate_possible_children('q0', ['q0', 'q1'], 3)) != 7:
        failures.append("generate_possible_children('q0', ['q0', 'q1'], 3)")
    if len(generate_possible_children('q0', ['q0', 'q1'], 2)) != 3:
        failures.append("generate_possible_children('q0', ['q0', 'q1'], 2)")
    if len(generate_possible_children('q0', ['q0', 'q1', 'q2', 'q3', 'q4'], 3)) != 61:
        failures.append("generate_possible_children('q0', ['q0', 'q1', 'q2', 'q3', 'q4'], 3)")
    if len(generate_possible_children('q0', ['q0', 'q1'], 4)) != 15:
        failures.append("generate_possible_children('q0', ['q0', 'q1'], 4)")

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def match_tests_top_down():
    print(" > SUBUNIT TEST: testing top-down match() ...")
    failures = []

    match_test("match_tree_top_down", "boxX", "treeXtest1", True, failures)
    match_test("match_tree_top_down", "boxX", "treeXtest2", False, failures)
    match_test("match_tree_top_down", "boxX", "treeXtest3", True, failures)
    match_test("match_tree_top_down", "boxL0", "treeL0test1", True, failures)
    match_test("match_tree_top_down", "boxL0", "treeL0test2", True, failures)
    match_test("match_tree_top_down", "boxL0", "treeL0test3", True, failures)
    match_test("match_tree_top_down", "boxL0", "treeL0test4", True, failures)
    match_test("match_tree_top_down", "boxL0", "treeXtest1", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeXtest2", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeXtest3", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeL1test1", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeL1test2", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeL1test3", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeL1test4", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH0test1", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH0test2", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH0test3", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH0test4", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH1test1", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH1test2", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH1test3", False, failures)
    match_test("match_tree_top_down", "boxL0", "treeH1test4", False, failures)
    match_test("match_tree_top_down", "boxL1", "treeL1test1", True, failures)
    match_test("match_tree_top_down", "boxL1", "treeL1test2", True, failures)
    match_test("match_tree_top_down", "boxL1", "treeL1test3", True, failures)
    match_test("match_tree_top_down", "boxL1", "treeL1test4", True, failures)
    match_test("match_tree_top_down", "boxH0", "treeH0test1", True, failures)
    match_test("match_tree_top_down", "boxH0", "treeH0test2", True, failures)
    match_test("match_tree_top_down", "boxH0", "treeH0test3", True, failures)
    match_test("match_tree_top_down", "boxH0", "treeH0test4", True, failures)
    match_test("match_tree_top_down", "boxH1", "treeH1test1", True, failures)
    match_test("match_tree_top_down", "boxH1", "treeH1test2", True, failures)
    match_test("match_tree_top_down", "boxH1", "treeH1test3", True, failures)
    match_test("match_tree_top_down", "boxH1", "treeH1test4", True, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def match_tests_bottom_up():
    print(" > SUBUNIT TEST: testing bottom-up match() ...")
    failures = []

    match_test("match_tree_bottom_up", "boxX", "treeXtest1", True, failures)
    match_test("match_tree_bottom_up", "boxX", "treeXtest2", False, failures)
    match_test("match_tree_bottom_up", "boxX", "treeXtest3", True, failures)

    match_test("match_tree_bottom_up", "boxL0", "treeL0test1", True, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL0test2", True, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL0test3", True, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL0test4", True, failures)

    match_test("match_tree_bottom_up", "boxL0", "treeL1test1", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL1test2", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL1test3", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeL1test4", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH0test1", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH0test2", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH0test3", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH0test4", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH1test1", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH1test2", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH1test3", False, failures)
    match_test("match_tree_bottom_up", "boxL0", "treeH1test4", False, failures)

    match_test("match_tree_bottom_up", "boxL1", "treeL1test1", True, failures)
    match_test("match_tree_bottom_up", "boxL1", "treeL1test2", True, failures)
    match_test("match_tree_bottom_up", "boxL1", "treeL1test3", True, failures)
    match_test("match_tree_bottom_up", "boxL1", "treeL1test4", True, failures)

    match_test("match_tree_bottom_up", "boxH0", "treeH0test1", True, failures)
    match_test("match_tree_bottom_up", "boxH0", "treeH0test2", True, failures)
    match_test("match_tree_bottom_up", "boxH0", "treeH0test3", True, failures)
    match_test("match_tree_bottom_up", "boxH0", "treeH0test4", True, failures)

    match_test("match_tree_bottom_up", "boxH1", "treeH1test1", True, failures)
    match_test("match_tree_bottom_up", "boxH1", "treeH1test2", True, failures)
    match_test("match_tree_bottom_up", "boxH1", "treeH1test3", True, failures)
    match_test("match_tree_bottom_up", "boxH1", "treeH1test4", True, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def determinization_tests():
    print(" > SUBUNIT TEST: testing determinization() ...")
    failures = []
    boxes_dict["deterministicX"] = tree_aut_determinization(boxes_dict["boxX"], full_alphabet)
    boxes_dict["deterministicL0"] = tree_aut_determinization(boxes_dict["boxL0"], full_alphabet)
    boxes_dict["deterministicL1"] = tree_aut_determinization(boxes_dict["boxL1"], full_alphabet)
    boxes_dict["deterministicH0"] = tree_aut_determinization(boxes_dict["boxH0"], full_alphabet)
    boxes_dict["deterministicH1"] = tree_aut_determinization(boxes_dict["boxH1"], full_alphabet)
    boxes_dict["deterministicLPort"] = tree_aut_determinization(boxes_dict["boxLPort"], full_alphabet)

    match_test("match_tree_top_down", "deterministicX", "treeXtest1", True, failures)
    match_test("match_tree_top_down", "deterministicX", "treeXtest2", False, failures)
    match_test("match_tree_top_down", "deterministicX", "treeXtest3", True, failures)

    match_test("match_tree_top_down", "deterministicL0", "treeL0test1", True, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL0test2", True, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL0test3", True, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL0test4", True, failures)

    match_test("match_tree_top_down", "deterministicL0", "treeXtest1", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeXtest2", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeXtest3", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL1test1", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL1test2", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL1test3", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeL1test4", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH0test1", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH0test2", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH0test3", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH0test4", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH1test1", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH1test2", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH1test3", False, failures)
    match_test("match_tree_top_down", "deterministicL0", "treeH1test4", False, failures)

    match_test("match_tree_top_down", "deterministicL1", "treeL1test1", True, failures)
    match_test("match_tree_top_down", "deterministicL1", "treeL1test2", True, failures)
    match_test("match_tree_top_down", "deterministicL1", "treeL1test3", True, failures)
    match_test("match_tree_top_down", "deterministicL1", "treeL1test4", True, failures)

    match_test("match_tree_top_down", "deterministicH0", "treeH0test1", True, failures)
    match_test("match_tree_top_down", "deterministicH0", "treeH0test2", True, failures)
    match_test("match_tree_top_down", "deterministicH0", "treeH0test3", True, failures)
    match_test("match_tree_top_down", "deterministicH0", "treeH0test4", True, failures)

    match_test("match_tree_top_down", "deterministicH1", "treeH1test1", True, failures)
    match_test("match_tree_top_down", "deterministicH1", "treeH1test2", True, failures)
    match_test("match_tree_top_down", "deterministicH1", "treeH1test3", True, failures)
    match_test("match_tree_top_down", "deterministicH1", "treeH1test4", True, failures)

    print_failed_tests(failures)


def sanity_unit_test(box: TTreeAut, f: TextIOWrapper):
    f.write(f"\ncomplement({box.name}) ... ")
    f.flush()
    print(f"complement({box.name}) ... ", flush=True)

    comp = tree_aut_complement(box, box.get_symbol_arity_dict(), verbose=False)

    f.write(f"\nintersection({box.name}, {comp.name}) ... ")
    f.flush()
    print(f"intersection({box.name}, {comp.name}) ... ", flush=True)

    inter = tree_aut_intersection(box, comp, verbose=False)

    f.write(f"\nnon_emptiness({inter.name}) ... ")
    f.flush()
    print(f"non_emptiness({inter.name}) ... ", flush=True)

    witness_tree, witness_str = non_empty_top_down(inter, verbose=False)

    f.write(f"\nsanity_test({str(box.name)}) result = ")
    f.write("OK" if witness_tree is None else "ERROR")
    f.write("\n")
    f.flush()


def sanity_tests():
    print(" > SUBUNIT TEST: testing determinization() with sanity tests ...")
    file_list = []
    f = open("../progress.txt", "w")
    f.write("---- SANITY TESTS START ----\n")
    for subdir, dirs, files in os.walk("../nta/"):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            file_list.append(filepath)
    file_list.sort()
    for i in file_list:
        test_box = import_treeaut_from_vtf(i)
        sanity_unit_test(test_box, f)
        file_list.remove(i)
        gc.collect()
    f.write("\n---- SANITY TESTS END ----\n")
    f.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def union_tests():
    print(" > SUBUNIT TEST: testing union() ...")
    failures = []
    match_test("match_tree_top_down", "unionL0H0", "treeL0test1", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL0test2", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL0test3", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL0test4", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH0test1", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH0test2", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH0test3", True, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH0test4", True, failures)

    match_test("match_tree_top_down", "unionL0H0", "treeL1test1", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL1test2", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL1test3", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeL1test4", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH1test1", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH1test2", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH1test3", False, failures)
    match_test("match_tree_top_down", "unionL0H0", "treeH1test4", False, failures)

    match_test("match_tree_top_down", "unionL0H1", "treeL0test1", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeL0test2", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeL0test3", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeL0test4", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeH1test1", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeH1test2", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeH1test3", True, failures)
    match_test("match_tree_top_down", "unionL0H1", "treeH1test4", True, failures)

    match_test("match_tree_top_down", "unionXL1", "treeXtest1", True, failures)
    match_test("match_tree_top_down", "unionXL1", "treeXtest2", False, failures)
    match_test("match_tree_top_down", "unionXL1", "treeXtest3", True, failures)
    match_test("match_tree_top_down", "unionXL1", "treeL1test1", True, failures)
    match_test("match_tree_top_down", "unionXL1", "treeL1test2", True, failures)
    match_test("match_tree_top_down", "unionXL1", "treeL1test3", True, failures)
    match_test("match_tree_top_down", "unionXL1", "treeL1test4", True, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def intersection_tests():
    print(" > SUBUNIT TEST: testing intersection() ...")
    failures = []

    match_test("match_tree_top_down", "intersectionL0H0", "treeL0test1", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeL0test2", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeL0test3", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeL0test4", False, failures)

    match_test("match_tree_top_down", "intersectionL0H0", "treeH0test1", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeH0test2", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeH0test3", False, failures)
    match_test("match_tree_top_down", "intersectionL0H0", "treeH0test4", False, failures)

    boxes_dict["intersectionXX"] = tree_aut_intersection(boxes_dict["boxX"], boxes_dict["boxX"])
    boxes_dict["intersectionL0L0"] = tree_aut_intersection(boxes_dict["boxL0"], boxes_dict["boxL0"])
    boxes_dict["intersectionL1L1"] = tree_aut_intersection(boxes_dict["boxL1"], boxes_dict["boxL1"])
    boxes_dict["intersectionH0H0"] = tree_aut_intersection(boxes_dict["boxH0"], boxes_dict["boxH0"])
    boxes_dict["intersectionH1H1"] = tree_aut_intersection(boxes_dict["boxH1"], boxes_dict["boxH1"])
    boxes_dict["intersectionLPortLPort"] = tree_aut_intersection(boxes_dict["boxLPort"], boxes_dict["boxLPort"])

    match_test("match_tree_top_down", "intersectionL0H0", "treeH0test4", False, failures)

    non_empty_test("non_empty_top_down", "intersectionXX", True, failures)
    non_empty_test("non_empty_top_down", "intersectionL0L0", True, failures)
    non_empty_test("non_empty_top_down", "intersectionL1L1", True, failures)
    non_empty_test("non_empty_top_down", "intersectionH0H0", True, failures)
    non_empty_test("non_empty_top_down", "intersectionH1H1", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionXX", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL0L0", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL1L1", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionH0H0", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionH1H1", True, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def complement_tests():
    print(" > SUBUNIT TEST: testing complement() ...")
    failures = []

    match_test("match_tree_bottom_up", "complementX", "treeXtest1", False, failures)
    match_test("match_tree_bottom_up", "complementX", "treeXtest2", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeXtest3", False, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL0test1", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL0test2", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL0test3", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL0test4", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL1test1", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL1test2", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL1test3", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeL1test4", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH0test1", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH0test2", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH0test3", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH0test4", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH1test1", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH1test2", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH1test3", True, failures)
    match_test("match_tree_bottom_up", "complementX", "treeH1test4", True, failures)

    match_test("match_tree_bottom_up", "complementL0", "treeXtest1", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeXtest2", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeXtest3", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL0test1", False, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL0test2", False, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL0test3", False, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL0test4", False, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL1test1", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL1test2", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL1test3", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeL1test4", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH0test1", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH0test2", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH0test3", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH0test4", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH1test1", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH1test2", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH1test3", True, failures)
    match_test("match_tree_bottom_up", "complementL0", "treeH1test4", True, failures)

    match_test("match_tree_bottom_up", "complementL1", "treeXtest1", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeXtest2", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeXtest3", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL0test1", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL0test2", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL0test3", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL0test4", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL1test1", False, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL1test2", False, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL1test3", False, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeL1test4", False, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH0test1", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH0test2", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH0test3", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH0test4", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH1test1", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH1test2", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH1test3", True, failures)
    match_test("match_tree_bottom_up", "complementL1", "treeH1test4", True, failures)

    match_test("match_tree_bottom_up", "complementH0", "treeXtest1", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeXtest2", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeXtest3", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL0test1", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL0test2", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL0test3", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL0test4", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL1test1", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL1test2", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL1test3", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeL1test4", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH0test1", False, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH0test2", False, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH0test3", False, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH0test4", False, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH1test1", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH1test2", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH1test3", True, failures)
    match_test("match_tree_bottom_up", "complementH0", "treeH1test4", True, failures)

    match_test("match_tree_bottom_up", "complementH1", "treeXtest1", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeXtest2", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeXtest3", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL0test1", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL0test2", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL0test3", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL0test4", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL1test1", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL1test2", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL1test3", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeL1test4", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH0test1", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH0test2", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH0test3", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH0test4", True, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH1test1", False, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH1test2", False, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH1test3", False, failures)
    match_test("match_tree_bottom_up", "complementH1", "treeH1test4", False, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def non_empty_top_down_tests():
    print(" > SUBUNIT TEST: testing top-down witnessGeneration() ...")
    failures = []

    non_empty_test("non_empty_top_down", "boxX", True, failures)
    non_empty_test("non_empty_top_down", "boxL0", True, failures)
    non_empty_test("non_empty_top_down", "boxL1", True, failures)
    non_empty_test("non_empty_top_down", "boxH0", True, failures)
    non_empty_test("non_empty_top_down", "boxH1", True, failures)
    non_empty_test("non_empty_top_down", "intersectionXL0", False, failures)
    non_empty_test("non_empty_top_down", "intersectionXL1", False, failures)
    non_empty_test("non_empty_top_down", "intersectionXH0", False, failures)
    non_empty_test("non_empty_top_down", "intersectionXH1", False, failures)
    non_empty_test("non_empty_top_down", "intersectionL0L1", False, failures)
    non_empty_test("non_empty_top_down", "intersectionL0H0", False, failures)
    non_empty_test("non_empty_top_down", "intersectionL0H1", False, failures)
    non_empty_test("non_empty_top_down", "intersectionL1H0", False, failures)
    non_empty_test("non_empty_top_down", "intersectionL1H1", False, failures)
    non_empty_test("non_empty_top_down", "intersectionH0H1", False, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def non_empty_bottom_up_tests():
    print(" > SUBUNIT TEST: testing bottom-up witnessGeneration() ...")
    failures = []

    non_empty_test("non_empty_bottom_up", "boxX", True, failures)
    non_empty_test("non_empty_bottom_up", "boxL0", True, failures)
    non_empty_test("non_empty_bottom_up", "boxL1", True, failures)
    non_empty_test("non_empty_bottom_up", "boxH0", True, failures)
    non_empty_test("non_empty_bottom_up", "boxH1", True, failures)
    non_empty_test("non_empty_bottom_up", "intersectionXL0", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionXL1", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionXH0", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionXH1", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL0L1", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL0H0", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL0H1", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL1H0", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionL1H1", False, failures)
    non_empty_test("non_empty_bottom_up", "intersectionH0H1", False, failures)

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def reachability_top_down_tests():
    print(" > SUBUNIT TEST: testing top-down reachability() ...")
    failures = []

    if set(reachable_top_down(test_unreachable_1)) != set(['q0', 'q1']):
        failures.append("reachable_top_down(test_unreachable_1)")
    if set(reachable_top_down(test_unreachable_2)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachable_top_down(test_unreachable_2")
    if set(reachable_top_down(test_unreachable_3)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachable_top_down(test_unreachable_3)")
    if set(reachable_top_down(copy.deepcopy(box_L0))) != set(['r0', 'r1', 'r2']):
        failures.append("reachable_top_down(boxL0copy)")

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def reachability_bottom_up_tests():
    print(" > SUBUNIT TEST: testing bottom-up reachability() ...")
    failures = []

    if set(reachable_bottom_up(test_unreachable_1)) != set(['q1']):
        failures.append("reachable_bottom_up(test_unreachable_1)")
    if set(reachable_bottom_up(test_unreachable_2)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachable_bottom_up(test_unreachable_2")
    if set(reachable_bottom_up(test_unreachable_3)) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("reachable_bottom_up(test_unreachable_3)")
    if set(reachable_bottom_up(copy.deepcopy(box_L0))) != set(['r0', 'r1', 'r2']):
        failures.append("reachable_bottom_up(boxL0copy)")

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def trimming_tests():
    print(" > SUBUNIT TEST: testing remove_useless_states() ...")
    failures = []

    clean_test_box_1 = remove_useless_states(test_unreachable_1)
    clean_test_box_2a = remove_useless_states(test_unreachable_2)
    clean_test_box_2b = remove_useless_states(test_unreachable_3)

    if set(clean_test_box_1.get_states()) != set([]):
        failures.append("remove_useless_states(test_unreachable_1)")
    if set(clean_test_box_2a.get_states()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("remove_useless_states(test_unreachable_2)")
    if set(clean_test_box_2b.get_states()) != set(['q0', 'q1', 'q2', 'q3']):
        failures.append("remove_useless_states(test_unreachable_3)")

    # now this test will fail, as edges are not simply strings,
    # but objects on different addresses (even though they contain the same data)

    # if copy.deepcopy(boxL0).transitions != boxL0.transitions:
    #     failures.append("remove_useless_states(copy.deepcopy(boxL0))")

    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def vtf_import_tests():
    print(" > SUBUNIT TEST: importing from VATA format ...")
    failures = []
    for subdir, dirs, files in os.walk("../tests/"):
        for file in files:
            filepath = subdir + os.sep + file
            if not filepath.endswith(".vtf"):
                continue
            else:
                try:
                    test_box = import_treeaut_from_vtf(filepath, 'f')
                except Exception as e:
                    failures.append(f"import_treeaut_from_vtf({filepath})")
    print_failed_tests(failures)


def vtf_export_tests():
    print(" > SUBUNIT TEST: exporting to VATA format ...")
    failures = []

    if not os.path.exists("../data/vtf"):
        os.makedirs("../data/vtf")

    for name, box in boxes_dict.items():
        try:
            export_treeaut_to_vtf(box, f"../data/vtf/{name}.vtf", 'f')
        except Exception as e:
            failures.append(f"export_treeaut_to_vtf(out/{name}.vtf)")
    print_failed_tests(failures)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def dot_export_tests():
    print(" > SUBUNIT TEST: exporting to DOT format ...")
    failures = []

    if not os.path.exists("../data/dot"):
        os.makedirs("../data/dot")

    for name, box in boxes_dict.items():
        try:
            export_treeaut_to_dot(box, f"../data/dot/{name}.dot")
        except Exception as e:
            failures.append(f"export_to_dot(out/{name}.dot)")
    print_failed_tests(failures)


def dot_export_from_vtf_tests():
    print(" > SUBUNIT TEST: exporting from VTF to DOT format ...")
    failures = []

    if not os.path.exists("../data/vtf-to-dot"):
        os.makedirs("../data/vtf-to-dot")

    for subdir, dirs, files in os.walk("../tests/"):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".vtf"):
                try:
                    dot_filepath = "../data/vtf-to-dot/"
                    dot_filepath += file
                    dot_filepath = dot_filepath[:-4] + ".dot"
                    ta = import_treeaut_from_vtf(filepath, 'f')
                    export_treeaut_to_dot(ta, dot_filepath)
                except Exception as e:
                    failures.append(f"export_from_vtf_to_dot({filepath}, {dot_filepath})")
    print_failed_tests(failures)


def tmb_import_tests():
    print(" > SUBUNIT TEST: importing from TMB format ...")
    failures = []

    for subdir, dirs, files in os.walk("./tests/"):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".tmb"):
                try:
                    test_box = import_treeaut_from_tmb(filepath)
                except Exception as e:
                    failures.append(f"import_treeaut_from_tmb({filepath})")

    print_failed_tests(failures)


def tmb_export_tests():
    print(" > SUBUNIT TEST: exporting to TMB format ...")

    if not os.path.exists("../data/tmb"):
        os.makedirs("../data//tmb")

    failures = []
    for name, box in boxes_dict.items():
        try:
            export_treeaut_to_tmb(box, f"../data/tmb/{name}.tmb")
        except Exception as e:
            failures.append(f"exportTreeAutToTMB(data/tmb/{name}.tmb)")

    print_failed_tests(failures)


def well_defined_tests(verbose=False):
    print(" > SUBUNIT TEST: checking if the boxes are well-defined ...")
    failures = []

    well_defined_test("boxX", True, verbose, failures)
    well_defined_test("boxL0", True, verbose, failures)
    well_defined_test("boxL1", True, verbose, failures)
    well_defined_test("boxH0", True, verbose, failures)
    well_defined_test("boxH1", True, verbose, failures)
    well_defined_test("boxLPort", True, verbose, failures)

    well_defined_test("unionXL0", False, verbose, failures)
    well_defined_test("unionXL1", False, verbose, failures)
    well_defined_test("unionXH0", False, verbose, failures)
    well_defined_test("unionXH1", False, verbose, failures)
    well_defined_test("unionL0H0", False, verbose, failures)
    well_defined_test("unionL0H1", False, verbose, failures)
    well_defined_test("unionL0L1", False, verbose, failures)
    well_defined_test("unionL1H0", False, verbose, failures)
    well_defined_test("unionL1H1", False, verbose, failures)
    well_defined_test("unionH0H1", False, verbose, failures)

    well_defined_test("intersectionXL0", False, verbose, failures)
    well_defined_test("intersectionXL1", False, verbose, failures)
    well_defined_test("intersectionXH0", False, verbose, failures)
    well_defined_test("intersectionXH1", False, verbose, failures)
    well_defined_test("intersectionL0H0", False, verbose, failures)
    well_defined_test("intersectionL0H1", False, verbose, failures)
    well_defined_test("intersectionL0L1", False, verbose, failures)
    well_defined_test("intersectionL1H0", False, verbose, failures)
    well_defined_test("intersectionL1H1", False, verbose, failures)
    well_defined_test("intersectionH0H1", False, verbose, failures)

    well_defined_test("complementX", False, verbose, failures)
    well_defined_test("complementL0", False, verbose, failures)
    well_defined_test("complementL1", False, verbose, failures)
    well_defined_test("complementH0", False, verbose, failures)
    well_defined_test("complementH1", False, verbose, failures)
    well_defined_test("complementLPort", False, verbose, failures)

    well_defined_test("determinizedX", False, verbose, failures)
    well_defined_test("determinizedL0", False, verbose, failures)
    well_defined_test("determinizedL1", False, verbose, failures)
    well_defined_test("determinizedH0", False, verbose, failures)
    well_defined_test("determinizedH1", False, verbose, failures)
    well_defined_test("determinizedLPort", False, verbose, failures)

    well_defined_test("Xsuffix", True, verbose, failures)
    well_defined_test("L0suffix", False, verbose, failures)
    well_defined_test("L1suffix", False, verbose, failures)
    well_defined_test("H0suffix", False, verbose, failures)
    well_defined_test("H1suffix", False, verbose, failures)

    well_defined_test("XprefixForL0", False, verbose, failures)
    well_defined_test("XprefixForL1", False, verbose, failures)
    well_defined_test("XprefixForH0", False, verbose, failures)
    well_defined_test("XprefixForH1", False, verbose, failures)
    well_defined_test("L0prefixForX", False, verbose, failures)
    well_defined_test("L0prefixForL1", False, verbose, failures)
    well_defined_test("L0prefixForH0", False, verbose, failures)
    well_defined_test("L0prefixForH1", False, verbose, failures)
    well_defined_test("L1prefixForX", False, verbose, failures)
    well_defined_test("L1prefixForL0", False, verbose, failures)
    well_defined_test("L1prefixForH0", False, verbose, failures)
    well_defined_test("L1prefixForH1", False, verbose, failures)
    well_defined_test("H0prefixForX", False, verbose, failures)
    well_defined_test("H0prefixForL0", False, verbose, failures)
    well_defined_test("H0prefixForL1", False, verbose, failures)
    well_defined_test("H0prefixForH1", False, verbose, failures)
    well_defined_test("H1prefixForX", False, verbose, failures)
    well_defined_test("H1prefixForL0", False, verbose, failures)
    well_defined_test("H1prefixForL1", False, verbose, failures)
    well_defined_test("H1prefixForH0", False, verbose, failures)

    print_failed_tests(failures)
    pass


def commutativity_test(ta1: str, ta2: str, expected_result, verbose, failures):
    box1 = boxes_dict[ta1]
    box2 = boxes_dict[ta2]
    actual_result1 = are_commutative(box1, box2)
    actual_result2 = are_commutative(box2, box1)
    if expected_result != actual_result1:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"are_commutative({ta1}, {ta2})", str(expected_result), str(actual_result1)
        ))
    if expected_result != actual_result2:
        failures.append("{:<50} | expected = {:>5} | got = {:>5}".format(
            f"are_commutative({ta2}, {ta1})", str(expected_result), str(actual_result2)
        ))
    if verbose and actual_result1 != actual_result2:
        print("WARNING: commutativity test gives inconsistent results")


def commutativity_tests(verbose=False):
    print(" > SUBUNIT TEST: testing commutativity ...")
    failures = []

    commutativity_test("boxX", "boxL0", False, verbose, failures)
    commutativity_test("boxX", "boxL1", False, verbose, failures)
    commutativity_test("boxX", "boxH0", False, verbose, failures)
    commutativity_test("boxX", "boxH1", False, verbose, failures)
    commutativity_test("boxX", "boxLPort", False, verbose, failures)
    commutativity_test("boxX", "boxHPort", False, verbose, failures)

    commutativity_test("boxL0", "boxL1", True, verbose, failures)  # True !
    commutativity_test("boxL0", "boxH0", False, verbose, failures)
    commutativity_test("boxL0", "boxH1", False, verbose, failures)
    commutativity_test("boxL0", "boxLPort", False, verbose, failures)
    commutativity_test("boxL0", "boxHPort", False, verbose, failures)

    commutativity_test("boxL1", "boxH0", False, verbose, failures)
    commutativity_test("boxL1", "boxH1", False, verbose, failures)
    commutativity_test("boxL1", "boxLPort", False, verbose, failures)
    commutativity_test("boxL1", "boxHPort", False, verbose, failures)

    commutativity_test("boxH0", "boxH1", True, verbose, failures)  # True !
    commutativity_test("boxH0", "boxLPort", False, verbose, failures)
    commutativity_test("boxH0", "boxHPort", False, verbose, failures)

    commutativity_test("boxH1", "boxLPort", False, verbose, failures)
    commutativity_test("boxH1", "boxHPort", False, verbose, failures)

    commutativity_test("boxLPort", "boxHPort", False, verbose, failures)

    print_failed_tests(failures)


def comparability_test_advanced(ta1, expected_result, ta2, failures):
    box1 = boxes_dict[ta1]
    box2 = boxes_dict[ta2]
    res1 = are_comparable(box1, box2)
    res2 = are_comparable(box2, box1)
    print(f"\t res1 = {res1}, res2 = {res2}")
    if expected_result == ">" and res1 is True and res2 is False:
        return
    if expected_result == "<" and res1 is False and res2 is True:
        return
    if expected_result == "?" and res1 is False and res2 is False:
        return
    failures.append("{:<50}".format(f"are_comparable({ta1}, {ta2})"))


def comparability_test_simple(ta1, ta2, exp, failures):
    box1 = boxes_dict[ta1]
    box2 = boxes_dict[ta2]
    res = are_comparable(box1, box2)
    # if res != exp:
    if res != exp:
        failures.append("{:<50} | {:>15} | {:>15}".format(
            f"comparing... {ta1} > {ta2} ?", f"expected = {exp}", f"result = {res}"
        ))
        # failures[len(failures)-1] += "   err"


def comparability_tests():
    print(" > SUBUNIT TEST: testing comparability/partial order ...")
    failures = []

    # boxes = {"boxX":0, "boxLPort":1, "boxHPort":1, "boxL0":2, "boxL1":2, "boxH0":2, "boxH1":2}

    # print("    {:<30} => {:>10} | {:>10}".format("comparing", "result", "expected"))
    # print("-" * 100)
    # for i, ival in boxes.items():
    #     box1 = boxes_dict[i]
    #     for j, jval in boxes.items():
    #         box2 = boxes_dict[j]
    #         result = areComparable(box1, box2)
    #         expected = ival >= jval
    #         print("    {:<30} => {:>10} | {:>10} | {:>5}".format(f"{box1.name} > {box2.name} ?", f"{result}", f"{expected}", f"ERR" if result != expected else ""))

    comparability_test_simple("boxL0", "boxX", True, failures)
    comparability_test_simple("boxL1", "boxX", True, failures)
    comparability_test_simple("boxH0", "boxX", True, failures)
    comparability_test_simple("boxH1", "boxX", True, failures)
    comparability_test_simple("boxLPort", "boxX", True, failures)
    comparability_test_simple("boxHPort", "boxX", True, failures)

    comparability_test_simple("boxL0", "boxLPort", True, failures)
    comparability_test_simple("boxL1", "boxLPort", True, failures)
    comparability_test_simple("boxH0", "boxHPort", True, failures)
    comparability_test_simple("boxH1", "boxHPort", True, failures)

    comparability_test_simple("boxLPort", "boxL0", False, failures)
    comparability_test_simple("boxLPort", "boxL1", False, failures)
    comparability_test_simple("boxHPort", "boxH0", False, failures)
    comparability_test_simple("boxHPort", "boxH1", False, failures)

    comparability_test_simple("boxX", "boxL0", False, failures)
    comparability_test_simple("boxX", "boxL1", False, failures)
    comparability_test_simple("boxX", "boxH0", False, failures)
    comparability_test_simple("boxX", "boxH1", False, failures)

    comparability_test_simple("boxL0", "boxL1", False, failures)
    comparability_test_simple("boxL0", "boxH0", False, failures)
    comparability_test_simple("boxL0", "boxH1", False, failures)
    comparability_test_simple("boxL1", "boxL0", False, failures)
    comparability_test_simple("boxL1", "boxH0", False, failures)
    comparability_test_simple("boxL1", "boxH1", False, failures)
    comparability_test_simple("boxH0", "boxL0", False, failures)
    comparability_test_simple("boxH0", "boxL1", False, failures)
    comparability_test_simple("boxH0", "boxH1", False, failures)
    comparability_test_simple("boxH1", "boxL0", False, failures)
    comparability_test_simple("boxH1", "boxL1", False, failures)
    comparability_test_simple("boxH1", "boxH0", False, failures)

    comparability_test_simple("boxH0", "boxLPort", False, failures)
    comparability_test_simple("boxH1", "boxLPort", False, failures)
    comparability_test_simple("boxL0", "boxHPort", False, failures)
    comparability_test_simple("boxL1", "boxHPort", False, failures)
    comparability_test_simple("boxLPort", "boxHPort", False, failures)
    comparability_test_simple("boxHPort", "boxLPort", False, failures)

    print_failed_tests(failures)


def product_tests():
    def product_unit_test(ta1, ta2, expect, failures):
        result = tree_aut_product(ta1, ta2)
        witness_tree, witness_str = non_empty_top_down(result)
        actual = (witness_tree is not None)  # actual = can witness be produced?
        if expect != actual:
            failures.append("{:<50} {:<20} {:<15} {:<15}".format(
                f"product({ta1.name},{ta2.name})",
                f"has witness?",
                f"exp = {expect}",
                f"got = {actual}"
            ))

    X = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetX.vtf")
    LPort = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetLPort.vtf")
    HPort = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetHPort.vtf")
    L0 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetL0.vtf")
    L1 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetL1.vtf")
    H0 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetH0.vtf")
    H1 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetH1.vtf")

    print(" > SUBUNIT TEST: testing product ...")
    failures = []

    product_unit_test(X, LPort, True, failures)
    product_unit_test(X, HPort, True, failures)
    product_unit_test(X, L0, True, failures)
    product_unit_test(X, L1, True, failures)
    product_unit_test(X, H0, True, failures)
    product_unit_test(X, H1, True, failures)
    product_unit_test(LPort, X, False, failures)
    product_unit_test(HPort, X, False, failures)
    product_unit_test(L0, X, False, failures)
    product_unit_test(L1, X, False, failures)
    product_unit_test(H0, X, False, failures)
    product_unit_test(H1, X, False, failures)

    product_unit_test(LPort, L0, True, failures)
    product_unit_test(LPort, L1, True, failures)
    product_unit_test(HPort, H0, True, failures)
    product_unit_test(HPort, H1, True, failures)

    product_unit_test(LPort, H0, False, failures)
    product_unit_test(LPort, H1, False, failures)
    product_unit_test(HPort, L0, False, failures)
    product_unit_test(HPort, L1, False, failures)
    product_unit_test(LPort, HPort, False, failures)

    product_unit_test(L0, L1, False, failures)
    product_unit_test(L1, L1, True, failures)
    product_unit_test(H0, L1, False, failures)
    product_unit_test(H1, L1, False, failures)
    product_unit_test(L1, L0, False, failures)
    product_unit_test(L1, H0, False, failures)
    product_unit_test(L1, H1, False, failures)
    print_failed_tests(failures)


def extension_tests():
    def extension_unit_test(ta1, ta2, expect, failures):
        actual = is_extension(ta1, ta2)
        if expect != actual:
            failures.append("{:<50} {:<20} {:<15} {:<15}".format(
                f"extension({ta1.name},{ta2.name})",
                f"has witness?",
                f"exp = {expect}",
                f"got = {actual}"
            ))

    X = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetX.vtf")
    LPort = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetLPort.vtf")
    HPort = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetHPort.vtf")
    L0 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetL0.vtf")
    L1 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetL1.vtf")
    H0 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetH0.vtf")
    H1 = import_treeaut_from_vtf("../tests/boxes-top_downdet/tddetH1.vtf")

    print(" > SUBUNIT TEST: testing extension ...")
    failures = []
    # extension je specializovanejsi // mal by byt
    extension_unit_test(X, LPort, True, failures)
    extension_unit_test(X, HPort, True, failures)
    extension_unit_test(X, L0, True, failures)
    extension_unit_test(X, L1, True, failures)
    extension_unit_test(X, H0, True, failures)
    extension_unit_test(X, H1, True, failures)
    extension_unit_test(LPort, X, False, failures)
    extension_unit_test(HPort, X, False, failures)
    extension_unit_test(L0, X, False, failures)
    extension_unit_test(L1, X, False, failures)
    extension_unit_test(H0, X, False, failures)
    extension_unit_test(H1, X, False, failures)

    extension_unit_test(LPort, L0, True, failures)
    extension_unit_test(LPort, L1, True, failures)
    extension_unit_test(HPort, H0, True, failures)
    extension_unit_test(HPort, H1, True, failures)

    extension_unit_test(LPort, H0, False, failures)
    extension_unit_test(LPort, H1, False, failures)
    extension_unit_test(HPort, L0, False, failures)
    extension_unit_test(HPort, L1, False, failures)
    extension_unit_test(LPort, HPort, False, failures)

    extension_unit_test(L0, L1, False, failures)
    extension_unit_test(L1, L1, True, failures)
    extension_unit_test(H0, L1, False, failures)
    extension_unit_test(H1, L1, False, failures)
    extension_unit_test(L1, L0, False, failures)
    extension_unit_test(L1, H0, False, failures)
    extension_unit_test(L1, H1, False, failures)
    print_failed_tests(failures)


def unfolding_tests():
    def test_unfolding(folded_treeaut_path, exp: bool, failures):
        ta = import_treeaut_from_vtf(folded_treeaut_path, 'f')
        ta = unfold(ta)
        res = is_unfolded(ta)
        if res != exp:
            failures.append(
                f"is_unfolded({ta.name}): expected {exp}, got {res}"
            )

    print(" > SUBUNIT TEST: testing unfolding ...")
    failures = []

    test_unfolding("../tests/unfolding/unfoldingTest1.vtf", True, failures)
    test_unfolding("../tests/unfolding/unfoldingTest2.vtf", True, failures)
    test_unfolding("../tests/unfolding/unfoldingTest3.vtf", True, failures)
    test_unfolding("../tests/unfolding/unfoldingTest4.vtf", True, failures)

    print_failed_tests(failures)


def normalization_tests():
    def test_normalization(unfolded_treeaut_path, exp: bool, failures, unfolding=False):
        ta = import_treeaut_from_vtf(unfolded_treeaut_path, 'f')
        symbols = ta.get_symbol_arity_dict()
        variables = [f"x" + f"{i+1}" for i in range(8)]
        if unfolding:
            ta = unfold(ta)
        ta = tree_aut_normalize(ta, symbols, variables)
        res = is_normalized(ta)
        if res != exp:
            failures.append(
                f"is_normalized({ta.name}): expected {exp}, got {res}"
            )
    def normalization_unit_test(
        path, states: list, max_var: int, vars: list, failures: list,
        unfolded=False
    ):
        ta = import_treeaut_from_vtf(path)
        if not unfolded:
            ta = unfold(ta)
            ta.reformat_states()
        ta = tree_aut_normalize(ta, create_var_order('x', max_var))
        result = True
        if ta.get_var_occurence() != vars:
            result = False
        if set(ta.get_states()) != set(states):
            result = False
        if not is_normalized(ta):
            result = False
        if not result:
            failures.append(f"normalization_unit_test(): {path} -> not normalized properly")
        return result

    print(" > SUBUNIT TEST: testing normalization ...")
    failures = []

    test_normalization("../tests/unfolding/unfoldingTest1.vtf", True, failures, unfolding=True)
    test_normalization("../tests/unfolding/unfoldingTest2.vtf", True, failures, unfolding=True)
    test_normalization("../tests/unfolding/unfoldingTest3.vtf", True, failures, unfolding=True)
    test_normalization("../tests/unfolding/unfoldingTest4.vtf", True, failures, unfolding=True)
    test_normalization("../tests/unfolding/unfoldingTest5.vtf", True, failures, unfolding=True)

    test_normalization("../tests/normalization/normalizationTest1.vtf", True, failures)
    test_normalization("../tests/normalization/normalizationTest2.vtf", True, failures)
    test_normalization("../tests/normalization/normalizationTest3.vtf", True, failures)
    test_normalization("../tests/normalization/normalizationTest4.vtf", True, failures)

    path1 = "../tests/unfolding/unfoldingTest1.vtf"
    states1 = ['{q0,q1,q2,q3}', '{q1,q2,q3}', '{q3,q4,q5}', '{q6}', '{q7}']
    normalization_unit_test(path1, states1, 4, [1, 3, 4, 4], failures)

    path2 = "../tests/normalization/newNormTest5.vtf"
    states2 = ['{q1}', '{q3}', '{q2,q4}', '{q2}', '{q6}', '{q5}', '{q7}']
    normalization_unit_test(path2, states2, 7, [1, 7, 7], failures, unfolded=True)

    path3 = "../tests/normalization/newNormTest4-loops.vtf"
    states3 = [
        '{q0}', '{q5,q12}', '{q13,q14,q16}', '{q9,q14}', '{q11,q12,q15}', '{q1,q3,q7}',
        '{q4,q8,q10}', '{q8}', '{q6}', '{q3,q6,q7}', '{q2,q4,q10}', '{q6,q8}'
    ]
    normalization_unit_test(path3, states3, 9, [1, 4, 6, 9, 9], failures)

    print_failed_tests(failures)


def folding_intersectoid_relation_test():
    def compare_mappings(ta, intersectoid, failures):
        map1 = get_maximal_mapping_fixed(intersectoid, ta, port_to_state_mapping(intersectoid))
        map2 = get_mapping(intersectoid, ta)
        if map1 != map2:
            failures.append(
                f"compareMappings({ta.name}, {intersectoid.name}): expected {map1}, got {map2}"
            )
    failures = []
    bda1 = import_treeaut_from_vtf(".../tests/reachability/1_bda.vtf")
    bda2 = import_treeaut_from_vtf(".../tests/reachability/2_bda.vtf")

    test1a = import_treeaut_from_vtf(".../tests/reachability/1_intersectoid_a.vtf")
    test1b = import_treeaut_from_vtf(".../tests/reachability/1_intersectoid_b.vtf")
    test1c = import_treeaut_from_vtf(".../tests/reachability/1_intersectoid_c.vtf")
    test2a = import_treeaut_from_vtf(".../tests/reachability/2_intersectoid_a.vtf")
    test2b = import_treeaut_from_vtf(".../tests/reachability/2_intersectoid_b.vtf")

    compare_mappings(test1a, bda1, failures)
    compare_mappings(test1b, bda1, failures)
    compare_mappings(test1c, bda2, failures)
    compare_mappings(test2a, bda2, failures)
    compare_mappings(test2b, bda2, failures)

    print_failed_tests(failures)


def folding_compare(treeaut: TTreeAut, vars: int, boxorder: list, failures: list) -> bool:
    initial = add_dont_care_boxes(treeaut, vars)
    unfolded = unfold(initial)
    add_variables_bottom_up(unfolded, vars)
    normalized = tree_aut_normalize(unfolded, create_var_order('', vars+1))
    normalized.reformat_keys()
    normalized.reformat_states()
    folded = tree_aut_folding(normalized, boxorder, vars+1)
    folded = remove_useless_states(folded)
    unfolded = unfold(folded)
    add_variables_bottom_up(unfolded, vars)
    result = simulate_and_compare(initial, unfolded, vars)
    if result != True:
        failures.append(f"folding_test: {initial.name} -> not equivalent after folding")
    return result


def folding_tests():
    def folding_debug_march_8() -> bool:
        ta = import_treeaut_from_vtf("../tests/folding/foldingTest2-ta.vtf")
        box = import_treeaut_from_vtf("../tests/folding/foldingTest2-box.vtf")
        box.name = 'test'
        box_catalogue['test'] = box
        treeaut_folded = tree_aut_folding(ta, ['test'], 8, verbose=False)
        treeaut_folded.reformat_keys()
        treeaut_folded.reformat_states()
        boxes = 0
        edges = 0
        for edge in iterate_edges(treeaut_folded):
            edges += 1
            for box in edge.info.box_array:
                if box is not None and box != "_":
                    boxes += 1
        if boxes != 4 or edges != 4 or len(treeaut_folded.get_states()) != 3:
            return False
        return True
    print(" > SUBUNIT TEST: testing folding ...")
    failures = []
    treeaut1 = import_treeaut_from_vtf("../tests/folding/folding-error-1.vtf")
    treeaut2 = import_treeaut_from_vtf("../tests/folding/foldingTest1.vtf")
    treeaut3 = import_treeaut_from_vtf("../tests/folding/folding-error-6.vtf")

    boxorder = box_orders['full']
    res1 = folding_compare(treeaut1, 5, boxorder, failures)
    res2 = folding_compare(treeaut2, 5, boxorder, failures)
    res3 = folding_compare(treeaut3, 5, boxorder, failures)
    res4 = folding_debug_march_8()
    if res4 != True:
        failures.append(f"folding_test: folding_test2 (special box) -> not correct structure")
    print_failed_tests(failures)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BDD testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def bdd_test():

    a = BDDnode('a', 'x1')
    b = BDDnode('b', 'x2')
    c = BDDnode('c', 'x3')
    d = BDDnode('d', 'x4')
    e = BDDnode('0', 'x5')
    f = BDDnode('1', 'x6')

    a.attach(b, c)
    b.attach(e, f)
    c.attach(d, e)
    d.attach(f, f)

    bdd1 = BDD('test1', a)

    q0 = BDDnode('e', 'x1')
    q1 = BDDnode('f', 'x2')
    q2 = BDDnode('g', 'x3')
    q3 = BDDnode('h', 'x4')
    q4 = BDDnode('0', 'x5')
    q5 = BDDnode('1', 'x6')

    q0.attach(q1, q2)
    q1.attach(q4, q5)
    q2.attach(q3, q4)
    q3.attach(q5, q5)

    bdd2 = BDD('test2', q0)
    print(compare_bdds(bdd1, bdd2))
    bdd1.print_bdd()
    bdd2.print_bdd()
    print(bdd1.get_variable_list())


def apply_test():
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x4', t0, t1)
    n2 = BDDnode('n2', 'x2', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd1 = BDD('test1', n3)
    # bdd1.print_bdd()
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x2', t0, t1)
    n2 = BDDnode('n2', 'x4', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd2 = BDD('test2', n3)
    # bdd2.print_bdd()
    bdd3 = apply_function('or', bdd1, bdd2, var_order=None)
    print(bdd3)

def extra_tests():
    pass

def main(config: dict):
    if "helpers" in config and config['helpers']:
        print(">> UNIT TEST: helper functions ...")
        get_output_states_tests()
        get_arity_dict_tests()
        remove_state_tests()
        generate_tuples_test()

    if "match" in config and config["match"]:
        print(">> UNIT TEST: matching trees to TAs ...")
        match_tests_top_down()
        match_tests_bottom_up()

    if "empty" in config and config["empty"]:
        print(">> UNIT TEST: empty language check ...")
        non_empty_top_down_tests()
        non_empty_bottom_up_tests()

    if "treeaut_op" in config and config["treeaut_op"]:
        print(">> UNIT TEST: basic automata operations ...")
        determinization_tests()
        union_tests()
        intersection_tests()
        complement_tests()

    if "reachability" in config and config["reachability"]:
        print(">> UNIT TEST: reachable states ...")
        reachability_top_down_tests()
        reachability_bottom_up_tests()
        trimming_tests()

    if "export" in config and config["export"]:
        print(">> UNIT TEST: VATA/TMB/DOT format import/export ...")
        vtf_export_tests()
        # vtf_import_tests() # time consuming
        tmb_export_tests()
        # tmb_import_tests() # time consuming
        dot_export_tests()
        dot_export_from_vtf_tests()

    if "boxorder" in config and config["boxorder"]:
        print(">> UNIT TEST: testing structures for finding boxorder  ...")
        well_defined_tests(verbose)
        commutativity_tests(verbose)
        comparability_tests()
        product_tests()
        extension_tests()

    # sanity_tests()
    if "canonicity" in config and config["canonicity"]:
        print(">> UNIT TEST: canonicity tests ...")
        unfolding_tests()
        normalization_tests()
        # folding_tests()


if __name__ == '__main__':
    config = {
        "helpers": True,
        "match": True,
        "empty": True,
        "treeaut_op": True,
        "reachability": True,
        "export": True,  # creates a lot of files...
        "boxorder": False,  # not yet fully working...
        "canonicity": False,
    }
    print("[MAIN UNIT TESTS START!]")
    main(config)
    print("[MAIN UNIT TESTS DONE!]")
    print("[EXTRA TESTS START!]")
    extra_tests()
    print("[EXTRA TESTS DONE!]")

# End of file all_tests.py
