from format_vtf import *
from all_tests import *
from ta_functions import *
from apply import *
from utils import *
from bdd import BDDnode, BDD
from dimacs import dimacsRead, createTAfromBDD
from simulation import simulateAndCompare, simulateRunTAdict, computeAdditionalVariables

import format_abdd as abdd
import render_dot as dot
import blif_parser as blif
import os

from unfolding import unfold
from normalization import treeAutNormalize
from folding import treeAutFolding
from time import localtime, strftime


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


# options = {
#     'vars':       int => how many variables the benchmark consists of
#     'image':      str => where to store the exported images and TA files
#     'cli':        bool => print out semiresults to stdout, 
#     'debug':      bool => logging normalization, folding process,
#     'export':     bool => exporting semiresults to png, vtf... for debugging
#     'sim':        bool => check equivalence (before/after folding)
#                     - simulating all variable assignments,
#     'progress':   bool => show % progress of simulation,
# }
def testBenchmark(path, options: dict) -> Tuple[bool | None, str]:
    filename, file_extension = os.path.splitext(path)
    basename = os.path.basename(filename)
    imagePath = f'results/dimacs/{basename}'
    # print(imagePath)
    if 'file' in options:
        print(options['file'])
        imagePath = options['file']
    if type(path) == TTreeAut:
        initial = path
    else:
        if not os.path.exists(imagePath):
            os.makedirs(imagePath)
        if file_extension in ['.cnf', '.dnf']:
            dnf = dimacsRead(path)
            initial = createTAfromBDD(dnf)
        elif file_extension == '.vtf':
            initial = importTAfromVTF(path)
        else: 
            print("unknown format")
            return None, None
    
    initial.reformatStates()
    initial.reformatKeys()

    options["image"] = imagePath
    options["path"] = imagePath

    tree_auts = canonizeBenchmarkCheck(initial, options)
    eq, report = simulateBenchmarkCheck(tree_auts, options)
    names = [
        'init', 'init-X', 'unfold', 'unfold-extra', 'normal', 'normal-clean',
        'fold', 'fold-trim', 'unfold-2', 'unfold-2-extra'
    ]

    skip = []
    if options["export_png"] or options["export_vtf"]:
        image = options["image"]
        for i, ta in enumerate(tree_auts.values()):
            ta.metaData.Frecompute()
            if options["export_vtf"]:
                exportTAtoVTF(ta, f"{image}/{i:02d}-{names[i]}.vtf")
            if options["export_png"]:
                dot.exportToFile(ta, f"{image}/{i:02d}-{names[i]}")
            else:
                if i not in skip and eq is not True:
                    dot.exportToFile(ta, f"{image}/{i:02d}-{names[i]}")
    return eq, report


def simulateBenchmarkCheck(tree_auts: dict, options: dict):
    result = None
    path = options["path"]
    if options["sim"]:
        simLogFile = open(f"{path}/log_simulation.txt", 'w')
        result = simulateAndCompare(
            tree_auts["initial"],
            tree_auts["unfolded_2_extra"], 
            options["vars"], debug=options["progress"], output=simLogFile
        )
        simLogFile.close()
    
    if result is False:
        intersectoidPath = f"{path}/intersectoids/"
        ubdaPath = f"{path}/ubdas/"
        for intersectoid in os.listdir(intersectoidPath):
            ta = importTAfromVTF(intersectoid)
            exportToFile(ta, ta.name)
        for ubda in os.listdir(ubdaPath):
            ta = importTAfromVTF(ubda)
            exportToFile(ta, ta.name)

    unfoldCount = len(tree_auts["initial"].getStates())
    foldCount = len(tree_auts["folded_trimmed"].getStates())
    report = f"{path :<50}: counts: {unfoldCount :<5} | {foldCount :<5} equivalent: {result}"
    return result, report


def canonizeBenchmarkCheck(initial: TTreeAut, opt: dict):
    if not os.path.exists(opt["image"]):
        os.makedirs(opt["image"])
    if opt["progress"]:
        print(f"\rPreparing data for {opt['image']} (1/8)...", end='')
    path = opt["image"]
    logFile = open(f"{path}/log.txt", 'w')
    logFile.write(f"INITIAL\n\n{initial}\n\n")

    varOrder = initial.getVariableOrder()
    if opt["progress"]:
        print(f"\r{'Adding extra boxes (2/8)...': <80}", end='')
    initialChanged = addDontCareBoxes(initial, opt["vars"])
    logFile.write(f"INITIAL (with X edge-correction)\n\n{initialChanged}\n\n")

    if opt["progress"]:
        print(f"\r{'Unfolding (3/8)...': <80}", end='')
    unfolded = unfold(initialChanged)
    logFile.write(f"UNFOLDED\n\n{unfolded}\n")

    if opt["progress"]:
        print(f"\r{'Computing extra variables (4/8)...': <80}", end='')
    unfolded_extra = copy.deepcopy(unfolded)
    computeAdditionalVariables(unfolded_extra, opt["vars"])
    logFile.write(f"UNFOLDED (additional variables)\n\n{unfolded_extra}\n\n")

    if opt["progress"]:
        print(f"\r{'Normalizing (5/8)...': <80}", end='')
    normalizationLogFile = open(f"{path}/log_normalization.txt", 'w')
    normalizationLogFile.write(f"INPUT\n\n{unfolded_extra}\n\n")
    var_order = createVarOrder('', opt["vars"]+2, start=0)
    print(var_order)
    normalized = treeAutNormalize(unfolded_extra, 
        var_order,
        verbose=opt["debug"], output=normalizationLogFile
    )
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()

    computeAdditionalVariables(normalized_clean, opt["vars"]+2)
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    
    normalizationLogFile.write(f"OUTPUT\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED CLEAN\n\n{normalized_clean}\n\n")

    if opt["progress"]:
        print(f"\r{'Folding (6/8)...': <80}", end='')
    foldingLogFile = open(f"{path}/log_folding.txt", 'w')
    foldingLogFile.write(f"INPUT\n\n{normalized_clean}\n\n")
    if opt["export_vtf"]:
        names = [
        "00-init", "01-init-X", "02-unfold", "03-unfold-extra", "04-normal",
        "05-normal-clean", "06-fold", "07-fold-trim", "08-unfold-2", "09-unfold-2-extra"
        ]
        exportTAtoVTF(initial, f"{opt['image']}/vtf/{names[0]}.vtf")
        exportTAtoVTF(initialChanged, f"{opt['image']}/vtf/{names[1]}.vtf")
        exportTAtoVTF(unfolded, f"{opt['image']}/vtf/{names[2]}.vtf")
        exportTAtoVTF(unfolded_extra, f"{opt['image']}/vtf/{names[3]}.vtf")
        exportTAtoVTF(normalized, f"{opt['image']}/vtf/{names[4]}.vtf")
        exportTAtoVTF(normalized_clean, f"{opt['image']}/vtf/{names[5]}.vtf")

    folded = treeAutFolding(normalized_clean, boxOrder, opt["vars"]+1,
        verbose=opt["debug"],
        export_vtf=opt["export_vtf"],
        export_png=opt["export_png"],
        output=foldingLogFile, exportPath=opt["image"],
    )
    foldingLogFile.write(f"OUTPUT\n\n{folded}\n\n")
    logFile.write(f"FOLDED\n\n{folded}\n\n")
    
    folded_trimmed = removeUselessStates(folded)
    logFile.write(f"FOLDED TRIMMED\n\n{folded}\n\n")

    if opt["progress"]:
        print(f"\r{'Unfolding again (7/8)...': <80}", end='')
    unfolded_after = unfold(folded)
    logFile.write(f"UNFOLDED AFTER FOLDING\n\n{unfolded_after}\n\n")

    if opt["progress"]:
        print(f"\r{'Computing extra variables again (8/8)...': <80}", end='')
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

    # names = [
    #     'init', 'init-X', 'unfold', 'unfold-extra', 'normal', 'normal-clean',
    #     'fold', 'fold-trim', 'unfold-2', 'unfold-2-extra'
    # ]
    # # skip = [1, 2, 3, 4, 6]
    # skip = []
    # if opt["export"]:
    #     for i, ta in enumerate(result.values()):
    #         ta.metaData.recompute()
    #         exportTAtoVTF(ta, f"{path}/{i:02d}-{names[i]}.vtf")
    #         if i not in skip:
    #             dot.exportToFile(ta, f"{path}/{i:02d}-{names[i]}")
  
    if opt["cli"]:
        print(f"INITIAL\n\n{initial}\n")
        print(f"INITIAL (with X edge-correction)\n\n{initialChanged}\n")
        print(f"UNFOLDED\n\n{unfolded}\n")
        print(f"NORMALIZED\n\n{normalized}\n")
        print(f"FOLDED\n\n{folded}\n")
        print(f"UNFOLDED AFTER\n\n{unfolded_after}\n")

    return result
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ABDD format testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def testABDDformat():
    options = {
        "vars": 6,
        "image": f'results/uf20-01-error-1-minimized',
        "cli": False, "debug": False, "export_vtf": True, "sim": False,
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
def testDimacs20Benchmarks(options: dict, already_done: int):
    simulationResults = open('results/simulationResults.txt', "a")
    for i in range(1000):
        simulationResults.flush()
        if i+1 <= already_done:
            continue
        filename = f"./tests/dimacs/uf20/uf20-0{i+1}.cnf"
        if not filename.endswith(".cnf"):
            continue
        base = os.path.basename(filename).split('.')[0]
        # if not os.path.exists(f"results/{base}"):
        #     os.makedirs(f"results/{base}")
        if os.path.isfile(filename):
            try:
                eq, report = testBenchmark(filename, options)
                print(report)
                simulationResults.write(f"{report}\n")
            except:
                simulationResults.write(f"{filename :<50}: error\n")


def foldingError(idx):
    options = {
        "vars": 20,
        "image": f'./results/dimacs/uf20-0{idx}',
        "cli": False, "debug": False, "sim": False, "progress": False,
        "export_vtf": False, "export_png": False,
    }

    path = f"./tests/dimacs/uf20/uf20-0{idx}.cnf"
    options["path"] = path
    initial = createTAfromBDD(dimacsRead(path))
    initial.reformatKeys()
    initial.reformatStates()
    initial.name = f"uf20-0{idx}"
    initial = removeUselessStates(initial)
    
    tree_auts = canonizeBenchmarkCheck(initial, options)
    print(tree_auts['initial'])
    print(tree_auts['folded_trimmed'])


# path = "path-to-vtf-or-cnf"
def simulateBenchmark(inputPath: str, vars: int, outputPath, simulate=False, images=False):
    results: dict[str, TTreeAut] = {}
    names = [
        "00-init", "01-init-X", "02-unfold", "03-unfold-extra", "04-normal",
        "05-normal-clean", "06-fold", "07-fold-trim", "08-unfold-2", "09-unfold-2-extra"
    ]
    if inputPath.endswith(".vtf"):
        results["00-init"] = importTAfromVTF(inputPath)
    elif inputPath.endswith(".cnf") or inputPath.endswith(".dnf"):
        bdd = dimacsRead(inputPath)
        results["00-init"] = createTAfromBDD(bdd)
    else:
        raise Exception(f"Unknown format: {inputPath}")

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    if not os.path.exists(f"{outputPath}/vtf/"):
        os.makedirs(f"{outputPath}/vtf/")

    log0 = open(f"{outputPath}/log0.txt", 'w')
    log1 = open(f"{outputPath}/log1_normalization.txt", 'w')
    log2 = open(f"{outputPath}/log2_folding.txt", 'w')
    log3 = open(f"{outputPath}/log3_simulation.txt", 'w')

    results["00-init"].reformatKeys()
    results["00-init"].reformatStates()
    results["01-init-X"] = addDontCareBoxes(results["00-init"], vars)
    results["02-unfold"] = unfold(results["01-init-X"])
    results["03-unfold-extra"] = copy.deepcopy(results["02-unfold"])
    computeAdditionalVariables(results["03-unfold-extra"], vars)
    results["04-normal"] = treeAutNormalize(results["03-unfold-extra"], createVarOrder('', vars+1), verbose=True, output=log1)
    results["05-normal-clean"] = copy.deepcopy(results["04-normal"])
    results["05-normal-clean"].reformatKeys()
    results["05-normal-clean"].reformatStates()
    results["06-fold"] = treeAutFolding(results["05-normal-clean"], boxOrder, vars, verbose=True, export_vtf=True, export_png=False, output=log2, exportPath=outputPath)
    results["07-fold-trim"] = removeUselessStates(results["06-fold"])
    results["08-unfold-2"] = unfold(results["07-fold-trim"])
    results["09-unfold-2-extra"] = copy.deepcopy(results["08-unfold-2"])
    computeAdditionalVariables(results["09-unfold-2-extra"], vars)
    for name in names:
        exportTAtoVTF(results[name], f"{outputPath}/vtf/{name}.vtf")
        log0.write(f"{name}\n\n{results[name]}\n\n")

    equivalent = None
    if simulate:
        equivalent = simulateAndCompare(results["00-init"], results["09-unfold-2-extra"], vars, debug=True, output=log3)

    if equivalent is False or images is True:
        results["06-fold"] = treeAutFolding(results["05-normal-clean"], boxOrder, vars, verbose=False, export_vtf=False, export_png=True, output=log2, exportPath=outputPath)
        os.makedirs(f"{outputPath}/png/")
        for name in names:
            exportToFile(results[name], f"{outputPath}/png/{name}")

    log0.close()
    log1.close()
    log2.close()
    log3.close()

    nodeCount1 = len(results['00-init'].getStates())
    nodeCount2 = len(results["07-fold-trim"].getStates())
    result = f"equivalent = {equivalent}, node counts: {nodeCount1} | {nodeCount2}"
    print(result)
    return equivalent, result


def foldingDebugMarch8():
    # eq, results = simulateBenchmark(
    #     f"./tests/blif/C17.vtf",
    #     11,
    #     f"./results/blif/C17",
    #     simulate=False,
    #     images=True
    # )
    box = importTAfromVTF("./tests/folding/foldingTest2-box.vtf")
    box.name = 'test'
    ta = importTAfromVTF("./tests/folding/foldingTest2-ta.vtf")
    boxCatalogue['test'] = box
    taFold = treeAutFolding(ta, ['test'], 8, verbose=False)
    taFold.reformatKeys()
    taFold.reformatStates()
    print(taFold)
    exportToFile(taFold, "results/temp/folding-test-2")
    # print('-'*50)
    # # - - - - - -
    # init = importTAfromVTF("./tests/folding/folding-error-6.vtf")
    # taVars = 5
    # ta = addDontCareBoxes(init, taVars)
    # ta = unfold(ta)
    # computeAdditionalVariables(ta, taVars)
    # ta.reformatKeys()
    # ta.reformatStates()

    # norm = treeAutNormalize(ta, createVarOrder('', taVars + 1))
    # norm.reformatKeys()
    # norm.reformatStates()
    # # print(norm)
    # fold = treeAutFolding(norm, boxOrder, taVars)
    # fold = removeUselessStates(fold)
    # # print(fold)
    # test2 = unfold(fold)
    # computeAdditionalVariables(test2, taVars)
    # # print('INIT\n', init)
    # # print('FOLD\n', fold)
    # # print('-'*50)
    # # simulateRunTAdict(init, {1: 1, 2: 1, 3: 0, 4: 0, 5: 1}, verbose=True)
    # # simulateRunTAdict(test2, {1: 1, 2: 1, 3: 0, 4: 0, 5: 1}, verbose=True)
    # print(simulateAndCompare(init, test2, taVars))
    # simulateBenchmark("./tests/dimacs/uf20/uf20-01.cnf", 20, "./results/temp/uf20-01", simulate=True)
    # simulateBenchmark("./tests/dimacs/uf20/uf20-06.cnf", 20, "./results/temp/uf20-06", simulate=True)
    # simulateBenchmark("./tests/dimacs/uf20/uf20-099.cnf", 20, "./results/temp/uf20-099", simulate=True)

def blifTest():
    # eq, results = simulateBenchmark(
    #     f"./tests/blif/C17.vtf",
    #     11,
    #     f"./results/blif/C17",
    #     simulate=True,
    #     images=True
    # )
    options = {
        "vars": 11,
        "image": f'./results/blif/c17',
        "cli": False, "debug": False, "sim": False, "progress": False,
        "export_vtf": False, "export_png": False,
    }
    init = importTAfromVTF("./tests/blif/C17.vtf")
    print("initial =", len(init.getStates()))
    print(init)
    varMapping = {f"{i}": f"{i+1}" for i in range(11)}
    for edge in transitions(init):
        if edge.info.variable in varMapping:
            edge.info.variable = varMapping[edge.info.variable]
    # print(varMapping)
    # print(init)
    results = canonizeBenchmarkCheck(init, options)
    print("folded =", len(results["folded_trimmed"].getStates()))
    print(results["folded_trimmed"])

def testBlif(path):
    tas = abdd.importTAfromABDD(path)
    if type(tas) != list:
        tas = [tas]
    initial_total = 0
    folded_total = 0
    for i in range(len(tas)):
        # if i != 6:
        #     continue
        ta = tas[i]

        options = {
            "vars": int(ta.getVariableOrder()[-1]),
            "image": f'./results/blif/{ta.name}',
            "cli": False, "debug": False, "sim": True, "progress": True,
            "export_vtf": True, "export_png": False,
        }
        print("var =", int(ta.getVariableOrder()[-1]))
        print(f"testing... {ta.name}")
        results = canonizeBenchmarkCheck(ta, options)
        initial = len(ta.getStates())
        folded = len(results['folded_trimmed'].getStates())
        print(f"{ta.name}, init = {initial}, fold = {folded}")
        initial_total += initial
        folded_total += folded
    print("total before folding =", initial_total)
    print("total after folding  =", folded_total)

if __name__ == '__main__':
    # testBlif("../cpp/testfiles/C432.abdd")
    path = "./results/blif/C432.iscas.var195/vtf/00-init.vtf"
    # path = "./results/blif/C432.iscas.var195/ubdas/79-q783-1:boxL1-q737.vtf"
    # test = importTAfromVTF(path)
    # print(test.getVariableOrder())
    # exportToFile(test, path)
    # computeAdditionalVariables(test, 36)
    # result = treeAutFolding(test, boxOrder, 36, verbose=True)
    # exportTAtoVTF(result, "./results/blif/C432.iscas.var195/vtf/06-fold.vtf")

    # ta = importTAfromVTF("./results/blif/C432.iscas.var195/vtf/06-fold.vtf")
    # ta_trim = removeUselessStates(result)
    # print(len(ta_trim.getStates()))




# End of file test.py
