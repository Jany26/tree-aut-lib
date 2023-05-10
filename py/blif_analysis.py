"""
[file] blif_analysis.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Analysing properties of processed combinational circuits
from BLIF files (benchmarks).
[note] Also performs folding tests on BLIF benchmarks with all compared models
(box orders) and gets box usage statistics for ABDD model.
"""

import re
import os
import format_abdd as abdd
import ta_classes as self

import render_dot as dot

from unfolding import *
from normalization import *
from folding import *
from simulation import addVariablesBU
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
        subtreeSizes: dict[str, int] = {}
        for state in self.iterateStatesBFS(treeaut):
            treeaut.rootStates = [state]
            reachableStates = set()
            for s in self.iterateStatesBFS(treeaut):
                reachableStates.add(s)
            subtreeSizes[state] = len(reachableStates)
        result[treeaut.name] = subtreeSizes
    return result

        
def printSubtrees(filePath, reportPath):
    report = open(f"{reportPath}", 'w')
    path = f"{filePath}"
    results = getAllNodeCounts(path)
    for taName, taResults in results.items():
        report.write(f"{taName}\n")
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
        abdd.exportTAtoABDD(treeaut, f"../data/blif/subfiles/{treeaut.name}")


def testFoldingOnSubBenchmarks(path, export, orders=None, rootNum=None):
    test = orders if orders is not None else boxOrders.keys()
    if not os.path.exists(export):
        os.makedirs(export)
    print(f"importing...", end='\r')
    initial = abdd.importTAfromABDD(path)
    if rootNum is not None:
        print(f"trimming...", end='\r')
        initial.rootStates = [f"{rootNum}"]
        initial = removeUselessStatesTD(initial)

    vars = int(initial.getVariableOrder()[-1])
    initialChanged = addDontCareBoxes(initial, vars)
    print(f"unfolding...", end='\r')
    unfolded = unfold(initialChanged)

    unfolded_extra = copy.deepcopy(unfolded)
    addVariablesBU(unfolded_extra, vars)
    var_order = createVarOrder('', vars+2, start=0)
    print(f"normalizing...", end='\r')
    normalized = treeAutNormalize(unfolded_extra, var_order)
    print(f"reformatting...", end='\r')
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    addVariablesBU(normalized_clean, vars+2)
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

    nums = [len(initial.getStates()), len(unfolded.getStates()), len(normalized_clean.getStates())]

    for name in test:
        boxorder = boxOrders[name]
        print(f"folding {name}", end='\r')
        folded = treeAutFolding(normalized_clean, boxorder, vars+1)
        nodeCount = len(reachableTD(folded))
        nums.append(nodeCount)
    result_print = f"{initial.name :<30}"
    for num in nums:
        result_print += f"\t| {num}"
    print(result_print)
    return result


def foldingTestBLIF(test=None):
    report = open("../tests/blif-report.txt", "r")

    report_line = f"{'name of the benchmark' :<30}\t| init\t| unfo\t| norm"
    for orderName in boxOrders.keys():
        report_line += f"\t| {orderName}"
    print(report_line)
    for line in report:
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
            f"../tests/blif/{benchmark}/{name}.abdd",  # import path
            f"../data/blif/{benchmark}/{varname}",  # export path
            # rootNum=None  # root
            orders=test,
            rootNum=root
        )


def analyzeNodeCounts():
    benchmarks = [432, 499, 880, 1355, 1908]
    if not os.path.exists('../data/blif-reports/'):
        os.makedirs('../data/blif-reports/')
    for num in benchmarks:
        for subdir, dirs, files in os.walk(f"../data/blif/C{num}"):
            for file in files:
                reportPath = f"'../data/blif-reports/{file.replace('.abdd', '.txt')}"
                printSubtrees(f"{subdir}/{file}", reportPath)


translation = {
    'boxX': 'X',
    'boxL0': 'L0',
    'boxL1': 'L1',
    'boxLPort': 'L+',
    'boxH0': 'H0',
    'boxH1': 'H1',
    'boxHPort': 'H+',
}


def formatBoxCounts(ta: TTreeAut):
    midResult = countBoxesOnEdges(ta)
    result = {}
    for longName, shortName in translation.items():
        count = midResult[longName] if longName in midResult else 0
        result[shortName] = count
    resultString = ""
    for key, val in result.items():
        resultString += f"{val :<5}, "
    return resultString


def printBoxCountsBLIF():
    initialString = f"{'path' :<30} = {'norm' :<5}, {'full' :<5}, "
    for val in translation.values():
        initialString += f"{val :<5}, "
    print(initialString)
    report = open(f"../tests/blif-report.txt", 'r')
    for line in report:
        if line.startswith('#') or line == "":
            continue
        data = line.strip().split(';')
        name = data[0]
        print(name, end='\r')
        ta = importTAfromVTF(f"../data/blif-normalized/{name}.vtf")
        folded = treeAutFolding(ta, boxOrders['full'], ta.getVariableMax())
        print(f"{name :<30} = {len(ta.getStates()) :<5}, {len(reachableTD(folded)) :<5}, {formatBoxCounts(folded)}")


def blifConsistencyCheck(path):
    file = open(path, 'r')
    file.seek(0)
    checkDuplicateOutputs(file)
    file.seek(0)
    checkOutputs(file)
    file.seek(0)
    checkHierarchy(file)
    file.seek(0)
    checkVariableNaming(file)


if __name__ == "__main__":
    path = "../tests/blif/"
    #blifConsistencyCheck()
    foldingTestBLIF()
    # printBoxCountsBLIF()
