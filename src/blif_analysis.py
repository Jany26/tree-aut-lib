import re
import os
import format_abdd as abdd
import ta_classes as self

import render_dot as dot

from unfolding import *
from normalization import *
from folding import *
from simulation import computeAdditionalVariables
from bdd import addDontCareBoxes
from utils import *

def checkVariableNaming(file):
    variable_map: dict[int, set[str]] = {}
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] not in [".inputs", ".outputs", ".names"]:
            continue
        for i in words[1:]:
            # print(i)
            # for j in matches:
            match = re.search(r"\(([^()]*)\)", i)
            if match:
                var = int(match.group(0)[1:-1])
                if var not in variable_map:
                    variable_map[var] = set([i])
                if i not in variable_map[var]:
                    print(f"{file.name}:{idx}: trying to add '{i}' to variable {var} = {variable_map[var]}")


def checkOutputs(file):
    outputs_initial = set()
    inputs_initial = set()
    current_outputs = set()
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".outputs":
            for i in line.split()[1:]:
                outputs_initial.add(i)
        if words[0] == ".inputs":
            for i in line.split()[1:]:
                inputs_initial.add(i)
        if words[0] == ".names":
            output = words[-1]
            current_outputs.add(output)
    file.seek(0)
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".names":
            output = words[-1]
            for i in words[1:-1]:
                if i in current_outputs:
                    if i in outputs_initial:
                        print(f"{file.name}:{idx}: initial .outputs entry {i} used as input")
                    current_outputs.remove(i)
    sorted_initial = list(outputs_initial)
    sorted_final = list(current_outputs)
    sorted_initial.sort()
    sorted_final.sort()
    for i in current_outputs:
        if i not in outputs_initial:
            print(f"{file.name}: output variable {i} not in .outputs line")
    sorted_difference = []
    for i in outputs_initial:
        if i not in current_outputs:
            print(f"{file.name}: initial .outputs variable {i} used as input")
            sorted_difference.append(i)
    sorted_difference.sort()
    print(file.name)
    print(f".outputs =", sorted_initial)
    print(f"not used =", sorted_final)
    print(f"diff     =", sorted_difference)


def checkDuplicateOutputs(file):
    output_occurence: dict[str, int] = {}  # variable -> line-number in file
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".names":
            output = words[-1]
            if output not in output_occurence:
                output_occurence[output] = idx
            else:
                print(f"{file.name}:{idx}: duplicate occurence of {output} as output detected (first on line {output_occurence[output]})")


def checkHierarchy(file):
    inputs_initial = set()
    outputs_parsed = set()
    for idx, line in enumerate(file, start=1):
        if line.startswith("#") or line == "\n":
            continue
        words = line.split()
        if words[0] == ".inputs":
            for i in words[1:]:
                inputs_initial.add(i)
        if words[0] == ".names":
            output = words[-1]
            for i in words[1:-1]:
                if i in inputs_initial:
                    continue
                if i not in outputs_parsed:
                    print(f"{file.name}:{idx}: unparsed variable {i} used as an input")
            outputs_parsed.add(output)


def getAllNodeCounts(filePath: str) -> dict:
    treeauts = abdd.importTAfromABDD(filePath)
    # print([treeaut.name for ta in tas])
    result: dict[str, dict[str, int]] = {}
    if type(treeauts) != list:
        treeauts = [treeauts]
    for treeaut in treeauts:
        # originalRoots = [r for r in treeaut.rootStates]
        subtreeSizes: dict[str, int] = {}
        for state in self.iterateStatesBFS(treeaut):
            treeaut.rootStates = [state]
            reachableStates = set()
            for s in self.iterateStatesBFS(treeaut):
                reachableStates.add(s)
            # subtreeSizes[state] = len(reachableStates)
            subtreeSizes[state] = len(reachableStates)
        # treeaut.rootStates = originalRoots
        result[treeaut.name] = subtreeSizes
    return result
        
def printSubtrees(filePath, reportPath):
    files = []
    report = open(f"{reportPath}", 'w')
    path = f"{filePath}"
    results = getAllNodeCounts(path)
    for taName, taResults in results.items():
        report.write(f"{taName}\n")
        # print(f"{taName} -> full node count = ")
        sorter: set[int] = set()
        temp: dict[int, list[str]] = {}
        for state, nodeCount in taResults.items():
            if nodeCount not in temp:
                temp[nodeCount] = []
            sorter.add(nodeCount)
            temp[nodeCount].append(state)
        sorter = list(sorter)
        sorter.sort()
        max = sorter[-1]
        # found = False
        for nc in sorter:
            if nc < 100:
                continue
            if len(temp[nc]) <= 10:
                report.write(f"{nc};{temp[nc]}\n")
            else:
                report.write(f"{nc};{temp[nc][0::10]}\n")
        # if not found:
        #     report.write(f"{sorter[-1]};{temp[nc]}\n")
    report.close()
    if max < 100:
        os.remove(reportPath)

benchmarks = [432, 499, 880, 1355, 1908]
# benchmarks = [432, 499, 880, 1355, 1908, 2670, 3540, 5315, 6288, 7552]

def countBoxesOnEdges(treeaut: TTreeAut):
    result = {}
    for edge in iterateEdges(treeaut):
        for box in edge.info.boxArray:
            if box is None:
                continue
            if box not in result:
                result[box] = 0
            result[box] += 1
    return result


def exportSubBlifs(filePath):
    results: list[self.TTreeAut] = abdd.importTAfromABDD(filePath)
    if type(results) != list:
        return
    for treeaut in results:
        abdd.exportTAtoABDD(treeaut, f"./tests/blif/subfiles/{treeaut.name}")


def testFoldingOnSubBenchmarks(path, export, rootNum=None):
    # boxesOrder = boxOrder if "box_order" not in opt else boxOrders[opt["box_order"]]
    if not os.path.exists(export):
        os.makedirs(export)
    print(f"importing...", end='\r')
    initial = abdd.importTAfromABDD(path)
    if rootNum is not None:
        print(f"trimming...", end='\r')
        initial.rootStates = [f"{rootNum}"]
        initial = removeUselessStatesTD(initial)

    # initial.reformatKeys()
    # initial.reformatStates()
    vars = int(initial.getVariableOrder()[-1])
    initialChanged = addDontCareBoxes(initial, vars)
    print(f"unfolding...", end='\r')
    unfolded = unfold(initialChanged)

    unfolded_extra = copy.deepcopy(unfolded)
    computeAdditionalVariables(unfolded_extra, vars)
    var_order = createVarOrder('', vars+2, start=0)
    print(f"normalizing...", end='\r')
    normalized = treeAutNormalize(unfolded_extra, var_order)
    print(f"reformatting...", end='\r')
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    computeAdditionalVariables(normalized_clean, vars+2)
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    result = {
        "initial": initial,
        "initial_extra": initialChanged,
        "unfolded": unfolded,
        "unfolded_extra": unfolded_extra,
        "normalized": normalized,
        "normalized_clean": normalized_clean
    }

    # exportTAtoVTF()
    vtfPath = path.split('/')[-1]
    if not os.path.exists("./results/normalized-blif/"):
        os.makedirs("./results/normalized-blif/")
    exportTAtoVTF(result["normalized_clean"], f"./results/normalized-blif/{vtfPath}.vtf")
    # print("init", len(initial.getStates()))
    # print("norm", len(normalized_clean.getStates()))

    # exportTAtoVTF(result["initial"], f"{export}/vtf-1-init.vtf")
    # exportTAtoVTF(result["unfolded_extra"], f"{export}/vtf-2-unfold.vtf")
    # exportTAtoVTF(result["normalized_clean"], f"{export}/vtf-3-normal.vtf")
    # dot.exportToFile(result["initial"], f"{export}/1-init")
    # # dot.exportToFile(result["unfolded"], f"{export}/2-unfold")
    # dot.exportToFile(result["normalized_clean"], f"{export}/3-normal")

    nums = [len(initial.getStates()), len(unfolded.getStates()), len(normalized_clean.getStates())]
    for name, boxorder in boxOrders.items():
        # if name != 'full':
        #     continue
        print(f"{name}-fold.....", end='\r')
        folded = treeAutFolding(normalized_clean, boxorder, vars+1)
        # folded_trimmed = removeUselessStates(folded)
        # nums.append(len(folded_trimmed.getStates()))
        nodeCount = len(reachableTD(folded))
        nums.append(nodeCount)
        # print(f"{name} - {nodeCount}")
        # if name == "full":
            # print(countBoxesOnEdges(folded))
            # exportToFile(removeUselessStatesTD(folded), "./results/temp/c432-84-2")
        # print(name, len(folded_trimmed.getStates()))
        # # dot.exportToFile(folded, f"{export}/4-{name}-folded")
        # exportTAtoVTF(folded_trimmed, f"{export}/vtf-4-{name}-fold.vtf")
        # dot.exportToFile(folded_trimmed, f"{export}/4-{name}-fold")
    result_print = f"{initial.name}"
    for num in nums:
        result_print += f"\t| {num}"
    print(result_print)
    return result


def foldingTest():
    report = open("./results/blif-reports/report.txt", "r")

    report_line = "name of the benchmark\t| init\t| unfo\t| norm"
    for orderName in boxOrders.keys():
        report_line += f"\t| {orderName}"
    print(report_line)
    for line in report:
        # if (line.startswith("C432")):
        #     continue
        if line.startswith('#') or line == "":
            continue
        data = line.strip().split(';')
        name = data[0]
        nameData = name.split('.')
        benchmark = nameData[0]
        varname = nameData[2]
        root = int(data[2])
        print(f"{benchmark}.{varname}", end='\r')
        testFoldingOnSubBenchmarks(
            f"./tests/blif/{benchmark}/{name}.abdd",  # import path
            f"./results/blif/{benchmark}/{varname}",  # export path
            # rootNum=None  # root
            rootNum=root
        )


def analyzeNodeCounts():
    benchmarks = [432, 499, 880, 1355, 1908]
    if not os.path.exists('./results/blif-reports/'):
        os.makedirs('./results/blif-reports/')
    for num in benchmarks:
        for subdir, dirs, files in os.walk(f"./tests/blif/C{num}"):
            for file in files:
                reportPath = f"'./results/blif-reports/{file.replace('.abdd', '.txt')}"
                printSubtrees(f"{subdir}/{file}", reportPath)


if __name__ == "__main__":
    # analyzeNodeCounts()
    foldingTest()
        
