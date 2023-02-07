from format_vtf import *
from normalization import *
from folding import *
from all_tests import *
from ta_functions import *
from bdd import *
from apply import *
from utils import *
from dimacs import *
from simulation import *
import format_abdd as abdd
import render_dot as dot
import os


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BDD testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def bddTest():

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
    print(compareBDDs(bdd1, bdd2))
    bdd1.printBDD()
    bdd2.printBDD()
    print(bdd1.getVariableList())


def applyTest():
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x4', t0, t1)
    n2 = BDDnode('n2', 'x2', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd1 = BDD('test1', n3)
    # bdd1.printBDD()
    t0 = BDDnode('t0', 0)
    t1 = BDDnode('t1', 1)
    n1 = BDDnode('n1', 'x2', t0, t1)
    n2 = BDDnode('n2', 'x4', t0, t1)
    n3 = BDDnode('n3', 'x1', n1, n2)
    bdd2 = BDD('test2', n3)
    # bdd2.printBDD()
    bdd3 = applyFunction('or', bdd1, bdd2, varOrder=None)
    print(bdd3)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# normalization testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def normalizationTest():
    ta1 = importTAfromVTF("tests/unfoldingTest1.vtf")
    ta1 = unfold(ta1)
    ta1.reformatStates()
    ta1 = treeAutNormalize(ta1, createVarOrder('x', 4))
    print(ta1)

    ta2 = importTAfromVTF("tests/newNormTest5.vtf")  # already unfolded
    ta2 = copy.deepcopy(ta2)
    ta2 = treeAutNormalize(ta2, createVarOrder('x', 7))
    print(ta2)

    ta3 = importTAfromVTF("tests/newNormTest4-loops.vtf")
    ta3 = unfold(ta3)
    ta3.reformatStates()
    ta3 = treeAutNormalize(ta3, createVarOrder('x', 9))
    print(ta3)


def lexicographicOrderTest():
    ta = importTAfromVTF("../nta/vtf/A0053.vtf", 'f')
    ta = treeAutDeterminization(ta, ta.getSymbolArityDict())
    ta.rootStates = [ta.rootStates[0]]
    ta.reformatStates()
    ta = removeUselessStates(ta)
    ta = normalize(ta, ta.getSymbolArityDict(), createVarOrder('x', 5))
    print(ta)
    test = lexicographicalOrder(ta)
    print(test)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# folding testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def testBenchmark(vars: int, path, cli=False, debug=False, export=False, simulate=True, progress=True):
    filename, file_extension = os.path.splitext(path)
    basename = os.path.basename(filename)
    imagePath = f'results/dimacs/{basename}'
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    if file_extension in ['.cnf', '.dnf']:
        dnf = dimacsRead(path)
        initial = createTAfromBDD(dnf)
    elif file_extension == '.vtf':
        initial = importTAfromVTF(path)
    else: 
        print("unknown format")
        return
    
    initial.reformatStates()
    initial.reformatKeys()

    options = {
        "vars": vars,
        "image": imagePath,
        "cli": cli,
        "debug": debug,
        "export": export,
        "sim": simulate,
        "progress": progress,
    }
    tree_auts = canonizeBenchmarkCheck(initial, options)

    res = None
    if simulate:
        res = simulateBenchmarkCheck(
            tree_auts["initial"], 
            tree_auts["unfolded_2_extra"], 
            options
        )
    unfoldCount = len(tree_auts["initial"].getStates())
    foldCount = len(tree_auts["folded_trimmed"].getStates())
    print(f"{path :<50}: counts: {unfoldCount :<5} | {foldCount :<5} equivalent: {res}")


def canonizeBenchmarkCheck(initial: TTreeAut, opt: dict):
    if not os.path.exists(opt["image"]):
        os.makedirs(opt["image"])
    path = opt["image"]
    logFile = open(f"{path}/log.txt", 'w')
    logFile.write(f"INITIAL\n\n{initial}\n\n")

    varOrder = initial.getVariableOrder()
    initialChanged = addDontCareBoxes(initial, varOrder, vars=opt["vars"])
    logFile.write(f"INITIAL (with X edge-correction)\n\n{initialChanged}\n\n")


    unfolded = unfold(initialChanged)
    logFile.write(f"UNFOLDED\n\n{unfolded}\n")

    unfolded_extra = copy.deepcopy(unfolded)
    computeAdditionalVariables(unfolded_extra, opt["vars"])
    logFile.write(f"UNFOLDED (additional variables)\n\n{unfolded_extra}\n\n")

    normalizationLogFile = open(f"{path}/log_normalization.txt", 'w')
    normalizationLogFile.write(f"INPUT\n\n{unfolded_extra}\n\n")
    normalized = treeAutNormalize(
        unfolded_extra,
        createVarOrder('', opt["vars"]+1),
        verbose=opt["debug"],
        output=normalizationLogFile
    )
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    
    normalizationLogFile.write(f"OUTPUT\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED CLEAN\n\n{normalized_clean}\n\n")

    foldingLogFile = open(f"{path}/log_folding.txt", 'w')
    foldingLogFile.write(f"INPUT\n\n{normalized_clean}\n\n")
    folded = newFold(
        normalized_clean,
        boxOrder,
        verbose=opt["debug"],
        export=opt["export"],
        output=foldingLogFile,
        exportPath=opt["image"]
    )
    foldingLogFile.write(f"OUTPUT\n\n{folded}\n\n")
    logFile.write(f"FOLDED\n\n{folded}\n\n")
    
    folded_trimmed = removeUselessStates(folded)
    logFile.write(f"FOLDED TRIMMED\n\n{folded}\n\n")

    unfolded_after = unfold(folded)
    logFile.write(f"UNFOLDED AFTER FOLDING\n\n{unfolded_after}\n\n")

    unfolded_after_extra = copy.deepcopy(unfolded_after)
    computeAdditionalVariables(unfolded_after_extra, opt["vars"])
    logFile.write(f"UNFOLDED AFTER FOLDING (additional variables)\n\n{unfolded_after_extra}\n\n")

    logFile.close()
    normalizationLogFile.close()
    foldingLogFile.close()
    result = {
        "initial": initial,
        "initial_extra": initialChanged,
        "unfolded": unfolded,
        "unfolded_extra": unfolded_extra,
        "normalized": normalized,
        "normalized_clean": normalized_clean,
        "folded": folded,
        "folded_trimmed": folded_trimmed,
        "unfolded_2": unfolded_after,
        "unfolded_2_extra": unfolded_after_extra,
    }
    names = [
        'init', 'init-X', 'unfold', 'unfold-extra', 'normal', 'normal-clean',
        'fold', 'fold-trim', 'unfold-2', 'unfold-2-extra'
    ]
    skip = [1, 2, 3, 4, 6, 8]
    for ta in result.values():
        ta.metaData.recompute()

    if opt["export"]:
        i = 0
        for ta in result.values():
            if i not in skip:
                dot.exportToFile(ta, f"{path}/{i:02d}-{names[i]}")
            exportTAtoVTF(ta, f"{path}/{i:02d}-{names[i]}.vtf")
            i += 1
        # exportTAtoVTF(initial, f'{path}/1a-initial')
        # dot.exportToFile(initial, f'{path}/1a-initial')
        # dot.exportToFile(initialChanged, f'{path}/1b-initial-with-X')
        # dot.exportToFile(unfolded, f'{path}/2a-unfolded')
        # dot.exportToFile(unfolded_extra, f'{path}/2b-unfolded-extra-vars')
        # dot.exportToFile(normalized, f'{path}/3a-normalized')
        # dot.exportToFile(normalized_clean, f'{path}/3b-normalized-clean')
        # dot.exportToFile(folded, f'{path}/4a-folded')
        # dot.exportToFile(folded_trimmed, f'{path}/4b-folded-trimmed')
        # dot.exportToFile(unfolded_after, f'{path}/5a-unfolded-2')
        # dot.exportToFile(unfolded_after_extra, f'{path}/5b-unfolded-2-extra-vars')
  
    if opt["cli"]:
        print(f"INITIAL\n\n{initial}")
        print(f"INITIAL (with X edge-correction)\n\n{initialChanged}")
        print(f"UNFOLDED\n\n{unfolded}")
        print(f"NORMALIZED\n\n{normalized}")
        print(f"FOLDED\n\n{folded}")
        print(f"UNFOLDED AFTER\n\n{unfolded_after}")

    return result

def simulateBenchmarkCheck(ta1, ta2, opt: dict):
    if opt["sim"]:
        path = opt["image"]
        simLogFile = open(f"{path}/log_simulation.txt", 'w')
        res = simulateAndCompare(ta1, ta2, opt["vars"], debug=opt["progress"], output=simLogFile)
        simLogFile.close()
        return res
    


# testBenchmark(20, f"./tests/dimacs/uf20/uf20-01.cnf", cli=False, debug=False, export=False)
# testBenchmark(5, f"./tests/dimacs/test-varskip.dnf", cli=False, debug=False, export=True)
# testBenchmark(8, f"./tests/normalization/newNormTest4.vtf", cli=True, export=True)
# testBenchmark(6, f"./tests/dimacs/test-varskip-3.vtf", cli=True, export=True)
# testBenchmark(3, f"./tests/dimacs/test-varskip-3.vtf", cli=True, export=True)


def testABDDformat():
    options = {
        "vars": 6,
        "image": f'results/uf20-01-error-1-minimized',
        "cli": False, "debug": False, "export": True, "sim": False,
    }
    raw = importTAfromVTF(f"./tests/dimacs/folding-error-1.vtf")
    tree_auts = canonizeBenchmarkCheck(raw, options)
    test = tree_auts["folded_trimmed"]
    test.reformatStates()
    print(test)
    abdd.exportTAtoABDD(test, "results/test-comments.dd", comments=True)
    abdd.exportTAtoABDD(test, "results/test.dd", comments=False)
    result = abdd.importTAfromABDD("results/test-comments.dd")
    result.reformatStates()
    print(result)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# folding debugging
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def testDimacs20Benchmarks():
    for i in range(1000):
        if i+1 in [1, 10, 100, 101, 102, 103, 104, 105, 106, 1000]:
            continue
        filename = f"./tests/dimacs/uf20/uf20-0{i+1}.cnf"
        if not filename.endswith(".cnf"):
            continue
        base = os.path.basename(filename).split('.')[0]
        if not os.path.exists(f"results/{base}"):
            os.makedirs(f"results/{base}")
        if os.path.isfile(filename):
            try:
                testBenchmark(20, filename, cli=False, debug=True, export=True, simulate=True, progress=False)
            except:
                print(f"{filename :<50}: error")


def foldingError():
    options = {
        "vars": 20,
        "image": f'results/dimacs/uf20-06-error-1',
        "cli": False, "debug": True, "export": True, "sim": False,
    }
    # filename = f"./tests/dimacs/uf20/uf20-06.cnf"
    # testBenchmark(20, filename, cli=False, debug=True, export=True, simulate=False, progress=False)
    # raw.rootStates = ['q10']
    # leafify(raw, 'q29', '1')
    
    cnf = dimacsRead(f"./tests/dimacs/uf20/uf20-06.cnf")
    raw = createTAfromBDD(cnf)
    raw.name = "uf20-06-error-1"
    raw.reformatStates()
    raw.reformatKeys()
    
    # raw.rootStates = ['q16']
    # leafify(raw, 'q56', '1')
    # raw = removeUselessStates(raw)
    tree_auts = canonizeBenchmarkCheck(raw, options)

    # test = {
    #     1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 1, 10: 0, 
    #     11: 0, 12: 1, 13: 1, 14: 0, 15: 1, 16: 0, 17: 0, 18: 0, 19: 1, 20: 1
    # }
    # test = {1: 1, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 1, 11: 1, 12: 1, 13: 0, 14: 1, 15: 1, 16: 1, 17: 1, 18: 0, 19: 0, 20: 1}

    test1 = {1: 1, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 1, 11: 1, 12: 1, 13: 0, 14: 1, 15: 1, 16: 1, 17: 1, 18: 0, 19: 0, 20: 1}
    test2 = {1: 1, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 1, 11: 1, 12: 1, 13: 0, 14: 1, 15: 1, 16: 1, 17: 1, 18: 0, 19: 1, 20: 1}

    simulateRunTAdict(tree_auts["initial"], test1, verbose=True)
    simulateRunTAdict(tree_auts["unfolded_2_extra"], test1, verbose=True)
    simulateRunTAdict(tree_auts["initial"], test2, verbose=True)
    simulateRunTAdict(tree_auts["unfolded_2_extra"], test2, verbose=True)


def intersectoidRelationTest():
    bda1 = importTAfromVTF("./tests/reachability/1_bda.vtf")
    bda2 = importTAfromVTF("./tests/reachability/2_bda.vtf")

    test1a = importTAfromVTF("./tests/reachability/1_intersectoid_a.vtf")
    test1b = importTAfromVTF("./tests/reachability/1_intersectoid_b.vtf")
    test1c = importTAfromVTF("./tests/reachability/1_intersectoid_c.vtf")
    test2a = importTAfromVTF("./tests/reachability/2_intersectoid_a.vtf")
    test2b = importTAfromVTF("./tests/reachability/2_intersectoid_b.vtf")

    print(getMaximalMappingFixed(test1a, bda1, portToStateMapping(test1a)))
    print(getMaximalMappingFixed(test1b, bda1, portToStateMapping(test1b)))
    print(getMaximalMappingFixed(test1c, bda1, portToStateMapping(test1c)))
    print(getMaximalMappingFixed(test2a, bda2, portToStateMapping(test2a)))
    print(getMaximalMappingFixed(test2b, bda2, portToStateMapping(test2b)))
    print()
    print(f"result = {getMapping(test1a, bda1)}")
    print(f"result = {getMapping(test1b, bda1)}")
    print(f"result = {getMapping(test1c, bda1)}")
    print(f"result = {getMapping(test2a, bda2)}")
    print(f"result = {getMapping(test2b, bda2)}")

if __name__ == '__main__':
    # intersectoidRelationTest()
    foldingError()
# End of file main.py
