from format_vtf import *
# from all_tests import *
from ta_functions import *
from apply import *
from utils import *
from bdd import createTAfromBDD
from dimacs import dimacsRead
from simulation import simulateAndCompare, computeAdditionalVariables, leafify

import format_abdd as abdd
import render_dot as dot
import blif_parser as blif
import os

from unfolding import unfold
from normalization import treeAutNormalize
from folding import treeAutFolding, createIntersectoid
from test_data import boxCatalogue

import blif_analysis

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# FOLDING testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TestOptions:
    def __init__(
        self, vars: int, output_path: str="",
        cli=False, debug=False, vtf=False, png=False, log=False,
        sim=False, prog=False
    ):
        self.vars: int = vars  # how many variables the benchmark consists of
        self.output_path: str = output_path  # where to store the exported images and TA files

        # debugging purposes (automatic, visual, etc.)
        self.cli: bool = cli  # print out semiresults to stdout, 
        self.debug: bool = debug  # print out extra information during normalization, folding process, etc.
        self.export_vtf: bool = vtf  # exporting semiresults to vtf files
        self.export_png: bool = png  # exporting results as DOT graphs to png
        self.logging: bool = log  # log semi-results/debug info to files
        self.sim: bool = sim  # check equivalence (before/after folding)
                              # simulates all variable assignments (time-consuming)
        self.progress: bool = prog  # show % progress of simulation
        self.box_order = boxOrders["abdd-short"]  # if explicit box order is needed
        self.var_order = None  # if explicit variable order is needed
# end of TestOptions class


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def testDimacsBenchmark(path, options: TestOptions) -> Tuple[bool | None, str]:
    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)
    if path.endswith('.cnf') or path.endswith('.dnf'):
        dnf = dimacsRead(path)
        initial = createTAfromBDD(dnf)
    elif path.endswith('.vtf'):
        initial = importTAfromVTF(path)
    else: 
        print("unknown format")
        return None, None

    initial.reformatStates()
    initial.reformatKeys()

    tree_auts = canonizeBenchmark(initial, options)
    eq, report = checkEquivalence(tree_auts, options)
    names = [
        'init', 'init-X', 'unfold', 'unfold-extra', 'normal', 'normal-clean',
        'fold', 'fold-trim', 'unfold-2', 'unfold-2-extra'
    ]

    skip = []
    if not options.export_png and not options.export_vtf:
        return eq, report
    
    for i, ta in enumerate(tree_auts.values()):
        ta.metaData.Frecompute()
        if options.export_vtf:
            exportTAtoVTF(ta, f"{options.output_path}/{i:02d}-{names[i]}.vtf")
        if options.export_png:
            dot.exportToFile(ta, f"{options.output_path}/{i:02d}-{names[i]}")
        if not options.export_png and (i not in skip and eq is not True):
            dot.exportToFile(ta, f"{options.output_path}/{i:02d}-{names[i]}")
    return eq, report


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def checkEquivalence(tree_auts: dict, options: TestOptions):
    result = None
    if options.sim:
        simLogFile = open(f"{options.output_path}/log_simulation.txt", 'w')
        result = simulateAndCompare(
            tree_auts["initial"],
            tree_auts["unfolded_2_extra"], 
            options.vars, debug=options.progress, output=simLogFile
        )
        simLogFile.close()
    
    if result is False:
        intersectoidPath = f"{options.output_path}/intersectoids/"
        ubdaPath = f"{options.output_path}/ubdas/"
        for intersectoid in os.listdir(intersectoidPath):
            ta = importTAfromVTF(intersectoid)
            dot.exportToFile(ta, ta.name)
        for ubda in os.listdir(ubdaPath):
            ta = importTAfromVTF(ubda)
            dot.exportToFile(ta, ta.name)

    unfoldCount = len(tree_auts["initial"].getStates())
    foldCount = len(tree_auts["folded_trimmed"].getStates())
    report = f"{options.output_path :<50}: counts: {unfoldCount :<5} | {foldCount :<5} equivalent: {result}"
    return result, report


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def canonizeBenchmark(initial: TTreeAut, options: TestOptions):
    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)
    if options.progress:
        print(f"\rPreparing data for {options.output_path} (1/8)...", end='')
    path = options.output_path
    logFile = open(f"{path}/log.txt", 'w')
    logFile.write(f"INITIAL\n\n{initial}\n\n")

    # varOrder = initial.getVariableOrder()
    # boxesOrder = boxOrder if "box_order" not in options else boxOrders[options.box_order]

    if options.progress:
        print(f"\r{'Adding extra boxes (2/8)...': <80}", end='')
    initialChanged = addDontCareBoxes(initial, options.vars)
    logFile.write(f"INITIAL (with X edge-correction)\n\n{initialChanged}\n\n")

    if options.progress:
        print(f"\r{'Unfolding (3/8)...': <80}", end='')
    unfolded = unfold(initialChanged)
    logFile.write(f"UNFOLDED\n\n{unfolded}\n")

    if options.progress:
        print(f"\r{'Computing extra variables (4/8)...': <80}", end='')
    unfolded_extra = copy.deepcopy(unfolded)
    computeAdditionalVariables(unfolded_extra, options.vars)
    logFile.write(f"UNFOLDED (additional variables)\n\n{unfolded_extra}\n\n")

    if options.progress:
        print(f"\r{'Normalizing (5/8)...': <80}", end='')
    normalizationLogFile = open(f"{path}/log_normalization.txt", 'w')
    normalizationLogFile.write(f"INPUT\n\n{unfolded_extra}\n\n")
    var_order = createVarOrder('', options.vars+2, start=0)
    # print(var_order)
    normalized = treeAutNormalize(unfolded_extra, 
        var_order,
        verbose=options.debug, output=normalizationLogFile
    )
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    computeAdditionalVariables(normalized_clean, options.vars+2)
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    
    normalizationLogFile.write(f"OUTPUT\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED\n\n{normalized}\n\n")
    logFile.write(f"NORMALIZED CLEAN\n\n{normalized_clean}\n\n")

    if options.progress:
        print(f"\r{'Folding (6/8)...': <80}", end='')
    foldingLogFile = open(f"{path}/log_folding.txt", 'w')
    foldingLogFile.write(f"INPUT\n\n{normalized_clean}\n\n")
    if options.export_vtf:
        if not os.path.exists(f"{options.output_path}/vtf/"):
            os.makedirs(f"{options.output_path}/vtf/")
        names = [
        "00-init", "01-init-X", "02-unfold", "03-unfold-extra", "04-normal",
        "05-normal-clean", "06-fold", "07-fold-trim", "08-unfold-2", "09-unfold-2-extra"
        ]
        exportTAtoVTF(initial, f"{options.output_path}/vtf/{names[0]}.vtf")
        exportTAtoVTF(initialChanged, f"{options.output_path}/vtf/{names[1]}.vtf")
        exportTAtoVTF(unfolded, f"{options.output_path}/vtf/{names[2]}.vtf")
        exportTAtoVTF(unfolded_extra, f"{options.output_path}/vtf/{names[3]}.vtf")
        exportTAtoVTF(normalized, f"{options.output_path}/vtf/{names[4]}.vtf")
        exportTAtoVTF(normalized_clean, f"{options.output_path}/vtf/{names[5]}.vtf")

    folded = treeAutFolding(normalized_clean, options.box_order, options.vars+1,
        verbose=options.debug,
        export_vtf=options.export_vtf,
        export_png=options.export_png,
        output=foldingLogFile, exportPath=options.output_path,
    )
    foldingLogFile.write(f"OUTPUT\n\n{folded}\n\n")
    logFile.write(f"FOLDED\n\n{folded}\n\n")
    
    folded_trimmed = removeUselessStates(folded)
    logFile.write(f"FOLDED TRIMMED\n\n{folded}\n\n")

    if options.progress:
        print(f"\r{'Unfolding again (7/8)...': <80}", end='')
    unfolded_after = unfold(folded)
    logFile.write(f"UNFOLDED AFTER FOLDING\n\n{unfolded_after}\n\n")

    if options.progress:
        print(f"\r{'Computing extra variables again (8/8)...': <80}", end='')
    unfolded_after_extra = copy.deepcopy(unfolded_after)
    computeAdditionalVariables(unfolded_after_extra, options.vars)
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
    skip = [1, 2, 3, 4, 6, 8, 9]
    # skip = []
    if options.export_png:  # or options.export_vtf:
        for i, ta in enumerate(result.values()):
            ta.metaData.recompute()
            # exportTAtoVTF(ta, f"{path}/{i:02d}-{names[i]}.vtf")
            if i not in skip:
                dot.exportToFile(ta, f"{path}/{i:02d}-{names[i]}")
  
    if options.cli:
        print(f"INITIAL\n\n{initial}\n")
        print(f"INITIAL (with X edge-correction)\n\n{initialChanged}\n")
        print(f"UNFOLDED\n\n{unfolded}\n")
        print(f"NORMALIZED\n\n{normalized}\n")
        print(f"FOLDED\n\n{folded}\n")
        print(f"UNFOLDED AFTER\n\n{unfolded_after}\n")

    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
            dot.exportToFile(results[name], f"{outputPath}/png/{name}")

    log0.close()
    log1.close()
    log2.close()
    log3.close()

    nodeCount1 = len(results['00-init'].getStates())
    nodeCount2 = len(results["07-fold-trim"].getStates())
    result = f"equivalent = {equivalent}, node counts: {nodeCount1} | {nodeCount2}"
    print(result)
    return equivalent, result


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
    tree_auts = canonizeBenchmark(raw, options)
    test = tree_auts["folded_trimmed"]
    test.reformatStates()
    print(test)
    abdd.exportTAtoABDD(test, "results/test-comments.dd", comments=True)
    abdd.exportTAtoABDD(test, "results/test.dd", comments=False)
    result = abdd.importTAfromABDD("results/test-comments.dd")
    result.reformatStates()
    print(result)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# DIMACS Benchmark testing and debugging
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def runAllDimacs20BenchmarkTests(options: TestOptions, already_done: int):
    simulationResults = open('results/dimacs/simulationResults.txt', "a")
    for i in range(1000):
        simulationResults.flush()
        if i+1 <= already_done:
            continue
        filename = f"./tests/dimacs/uf20/uf20-0{i+1}.cnf"
        if not filename.endswith(".cnf"):
            continue
        base = os.path.basename(filename).split('.')[0]
        options = TestOptions(20, f"./results/dimacs/{base}", vtf=True)
        # if not os.path.exists(f"results/{base}"):
        #     os.makedirs(f"results/{base}")
        if os.path.isfile(filename):
            try:
                eq, report = testDimacsBenchmark(filename, options)
                print(report)
                simulationResults.write(f"{report}\n")
            except:
                simulationResults.write(f"{filename :<50}: error\n")
    simulationResults.close()


def foldingDebug(idx):
    options = TestOptions(20, f'./results/dimacs/uf20-0{idx}')

    path = f"./tests/dimacs/uf20/uf20-0{idx}.cnf"
    options.path = path
    initial = createTAfromBDD(dimacsRead(path))
    initial.reformatKeys()
    initial.reformatStates()
    initial.name = f"uf20-0{idx}"
    initial = removeUselessStates(initial)
    
    tree_auts = canonizeBenchmark(initial, options)
    print(tree_auts['initial'])
    print(tree_auts['folded_trimmed'])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BLIF Benchmark testing and debugging
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def blifTestC17():
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
    for edge in iterateEdges(init):
        if edge.info.variable in varMapping:
            edge.info.variable = varMapping[edge.info.variable]
    results = canonizeBenchmark(init, options)
    print("folded =", len(results["folded_trimmed"].getStates()))
    print(results["folded_trimmed"])


def blifTestNodeCounts(path):
    tas = abdd.importTAfromABDD(path)
    if type(tas) != list:
        tas = [tas]
    initial_total = 0
    folded_total = 0
    for i in range(len(tas)):
        ta = tas[i]

        options = {
            "vars": int(ta.getVariableOrder()[-1]),
            "image": f'./results/blif/{ta.name}',
            "cli": False, "debug": False, "sim": True, "progress": True,
            "export_vtf": True, "export_png": False,
        }
        print("var =", int(ta.getVariableOrder()[-1]))
        print(f"testing... {ta.name}")
        results = canonizeBenchmark(ta, options)
        initial = len(ta.getStates())
        folded = len(results['folded_trimmed'].getStates())
        print(f"{ta.name}, init = {initial}, fold = {folded}")
        initial_total += initial
        folded_total += folded
    print("total before folding =", initial_total)
    print("total after folding  =", folded_total)



def isTopDownDeterministic(treeaut: TTreeAut) -> bool:
    for state in treeaut.getStates():
        if len(treeaut.transitions[state].values()) > 1:
            return False
    return True

def bddIsomorphicCheck(ta1: TTreeAut, ta2: TTreeAut) -> bool:
    outputs1 = ta1.getOutputEdges(inverse=True)
    outputs2 = ta2.getOutputEdges(inverse=True)
    varVis1 = ta1.getVariableVisibilityCache()
    varVis2 = ta2.getVariableVisibilityCache()
    def compareNode(ta1: TTreeAut, ta2: TTreeAut, state1: str, state2: str):
        found1 = state1 in outputs1
        found2 = state2 in outputs2
        if found1 or found2:
            if found1 == found2:
                return True
            else:
                print(f"outputs not agreeing => {state1}, {state2}")
                return False
            # return found1 == found2
        if found1 and found2:
            if outputs1[state1] != outputs2[state2]:
                print(f"outputs => {state1}, {state2}")
                return False
        if varVis1[state1] != varVis2[state2]:
            print(f"varvis => {state1}, {state2}")
            return False
        
        for edge1 in ta1.transitions[state1].values():
            for edge2 in ta2.transitions[state2].values():
                if len(edge1.children) != len(edge2.children):
                    print(f"children length => {edge1}, {edge2}")
                    return False
                for idx in range(len(edge1.children)):
                    child1 = edge1.children[idx]
                    child2 = edge2.children[idx]
                    if not compareNode(ta1, ta2, child1, child2):
                        return False
        return True

    if len(ta1.rootStates) != len(ta2.rootStates) or len(ta1.rootStates) != 1:
        raise AssertionError("treeAutIsomorphic(): Nondeterminism - rootstates > 1.")

    if not isTopDownDeterministic(ta1):
        raise AssertionError(f"treeAutIsomorphic(): {ta1.name} is not top-down deterministic")
    if not isTopDownDeterministic(ta2):
        raise AssertionError(f"treeAutIsomorphic(): {ta2.name} is not top-down deterministic")

    return compareNode(ta1, ta2, ta1.rootStates[0], ta2.rootStates[0])


def isomorphicCheckBLIF():
    for subdir, dirs, files in os.walk("./results/blif/"):
        init: TTreeAut = None
        bdd: TTreeAut = None
        for file in files:
            if file.endswith("1-init.vtf"):
                init = importTAfromVTF(f"{subdir}/{file}")
            if file.endswith("4-bdd-fold.vtf"):
                bdd = importTAfromVTF(f"{subdir}/{file}")
        if init is None or bdd is None:
            continue
        isomorphic = bddIsomorphicCheck(init, bdd)
        # print(subdir, "isomorphic", bddIsomorphicCheck(init, bdd))
        if not isomorphic:
            return False
    return True

def LPort_test():
    path = "./results/blif/C1355/var558/vtf-4-abdd-short-fold.vtf"
    test = importTAfromVTF(path)
    test.reformatStates()
    folder = "./c1355-558"
    fold = treeAutFolding(test, ['LPort'], test.getVariableMax(),
                          export_png=True, export_vtf=False, exportPath=folder)
    fold = removeUselessStates(fold)
    dot.exportToFile(test, f"{folder}/init")
    dot.exportToFile(fold, f"{folder}/fold")
    print(len(test.getStates()), len(fold.getStates()))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    # LPort_test()
    blif_analysis.testFoldingOnSubBenchmarks(
        f"./tests/blif/C432/C432.iscas.var195.abdd",  # import path
        f"./results/blif-6-4/C432/var195",  # export path
        rootNum=None  # root
    )

# End of file test.py
