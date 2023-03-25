# main.py
# All unit tests "control panel".
# Implementation of tree automata for article about automata-based BDDs
# Author: Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>

from all_tests import *

verbose = False  # printing more detailed info on output during tests


def main(config: dict):
    if "helpers" in config and config['helpers']:
        print(">> UNIT TEST: helper functions ...")
        getOuptutStatesTests()
        getArityDictTests()
        removeStateTests()
        generateTuplesTest()

    if "match" in config and config["match"]:
        print(">> UNIT TEST: matching trees to TAs ...")
        matchTestsTD()
        matchTestsBU()

    if "empty" in config and config["empty"]:
        print(">> UNIT TEST: empty language check ...")
        nonEmptyTDTests()
        nonEmptyBUTests()

    if "treeaut_op" in config and config["treeaut_op"]:
        print(">> UNIT TEST: basic automata operations ...")
        determinizationTests()
        unionTests()
        intersectionTests()
        complementTests()

    if "reachability" in config and config["reachability"]:
        print(">> UNIT TEST: reachable states ...")
        reachabilityTDTests()
        reachabilityBUTests()
        removeUselessStatesTests()

    if "export" in config and config["export"]:
        print(">> UNIT TEST: VATA/TMB/DOT format import/export ...")
        vtfExportTests()
        # vtfImportTests() # time consuming
        tmbExportTests()
        # tmbImportTests() # time consuming
        dotExportTests()
        dotExportFromVTFTests()

    if "boxorder" in config and config["boxorder"]:
        print(">> UNIT TEST: testing structures for finding boxorder  ...")
        wellDefinedTests(verbose)
        commutativityTests(verbose)
        comparabilityTests()
        productTests()
        extensionTests()

    # sanityTests()
    if "canonicity" in config and config["canonicity"]:
        print(">> UNIT TEST: canonicity tests ...")
        unfoldingTests()
        normalizationTests()
        foldingTests()


if __name__ == '__main__':
    config = {
        "helpers": False,
        "match": False,
        "empty": False,
        "treeaut_op": False,
        "reachability": False,
        "export": False,
        "boxorder": False,
        "canonicity": True,
    }
    print("[MAIN UNIT TESTS START!]")
    main(config)
    print("[MAIN UNIT TESTS DONE!]")
    print("[EXTRA TESTS START!]")
    extraTests()
    print("[EXTRA TESTS DONE!]")

# End of file main.py
