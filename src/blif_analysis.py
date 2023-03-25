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
        for state in self.iterateBFS(treeaut):
            treeaut.rootStates = [state]
            reachableStates = set()
            for s in self.iterateBFS(treeaut):
                reachableStates.add(s)
            # subtreeSizes[state] = len(reachableStates)
            subtreeSizes[state] = len(reachableStates)
        # treeaut.rootStates = originalRoots
        result[treeaut.name] = subtreeSizes
    return result
        
def printSubtrees(benchmarks: list):
    files = []
    for num in benchmarks:
        # path = f"./tests/blif/C{num}.blif"
        report = open(f"./tests/blif/reports/C{num}.txt", 'w')
        path = f"../cpp/benchmarks/C{num}.abdd"
        results = getAllNodeCounts(path)
        for taName, taResults in results.items():
            report.write(f"{taName}")
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
            # max = 0
            # print(sorter)
            # report.write(f"{sorter[-1]}\n")
            found = False
            for nc in sorter:
                # max = nc
                if nc < 100:
                    continue
                if not found and nc >= 100 and nc <= 300:
                    found = True
                    report.write(f";{nc};{temp[nc][0]}\n")
            if not found:
                report.write(f";{sorter[-1]};{temp[nc][0]}\n")
            # if max <= 300:
            #     report.write(f"  > {max} : {len(temp[max])} states = {temp[max][:5]}\n")
        # report.close()

benchmarks = [432, 499, 880, 1355, 1908]
# benchmarks = [432, 499, 880, 1355, 1908, 2670, 3540, 5315, 6288, 7552]


def exportSubBlifs(filePath):
    results: list[self.TTreeAut] = abdd.importTAfromABDD(filePath)
    if type(results) != list:
        return
    for treeaut in results:
        abdd.exportTAtoABDD(treeaut, f"./tests/blif/subfiles/{treeaut.name}")


def relabelVars(treeaut: TTreeAut):
    mapping = {}
    # for edge in transitions(ta):
    #     if edge.
    vars = treeaut.getVariableOrder()
    print(vars)


def removeUselessStatesTD(ta: TTreeAut) -> TTreeAut:
    workTA = copy.deepcopy(ta)
    # reachableStatesBU = reachableBU(workTA)
    # workTA.shrinkTA(reachableStatesBU)
    reachableStatesTD = reachableTD(workTA)
    workTA.shrinkTA(reachableStatesTD)
    return workTA


def testFoldingOnSubBenchmarks(path, export, rootNum=None):
    # boxesOrder = boxOrder if "box_order" not in opt else boxOrders[opt["box_order"]]
    initial = abdd.importTAfromABDD(path)
    if rootNum is not None:
        initial.rootStates = [f"{rootNum}"]
        initial = removeUselessStatesTD(initial)
    
    initial.reformatKeys()
    initial.reformatStates()
    # relabelVars(initial)
    # exit()
    vars = int(initial.getVariableOrder()[-1])
    initialChanged = addDontCareBoxes(initial, vars)
    # print("unfolding")
    unfolded = unfold(initialChanged)
    unfolded_extra = copy.deepcopy(unfolded)
    computeAdditionalVariables(unfolded_extra, vars)
    var_order = createVarOrder('', vars+2, start=0)
    # print("normalizing")
    normalized = treeAutNormalize(unfolded_extra, var_order)
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    computeAdditionalVariables(normalized_clean, vars+2)
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    print(f"{initial.name}\t| {len(initial.getStates())}\t| {len(normalized_clean.getStates())}", end='')

    result = {
        "initial": initial,
        "initial_extra": initialChanged,
        "unfolded": unfolded,
        "unfolded_extra": unfolded_extra,
        "normalized": normalized,
        "normalized_clean": normalized_clean
    }

    dot.exportToFile(result["initial"], f"{export}/1-init")
    dot.exportToFile(result["unfolded"], f"{export}/2-unfold")
    dot.exportToFile(result["normalized_clean"], f"{export}/3-normal")
    nums = []
    for name, boxorder in boxOrders.items():
        folded = treeAutFolding(normalized_clean, boxorder, vars+1)
        folded_trimmed = removeUselessStates(folded)
        # print(f"{export}/4-{name}-folded")
        nums.append(len(folded_trimmed.getStates()))
        dot.exportToFile(folded, f"{export}/4-{name}-folded")
        dot.exportToFile(folded_trimmed, f"{export}/4-{name}-folded-trimmed")
    for num in nums:
        print(f"\t| {num}", end='')
    print()
    # exportToFile(initial, )

    
    return result


if __name__ == "__main__":
    # C432.iscas.var195, 100, 17170
    # C432.iscas.var194, 100, 16269
    # C432.iscas.var193, 101, 15336
    # C432.iscas.var188, 120, 12114
    # C432.iscas.var163, 100, 4875
    # C432.iscas.var133, 75,  1607
    # C432.iscas.var84,  20,  517
    report = open("./tests/blif/report.txt", "r")
    for line in report:
        if not (line.startswith("C1908") or line.startswith("C1355")):
            continue
        data = line.split(';')
        name = data[0]
        nameData = name.split('.')
        benchmark = nameData[0]
        varname = nameData[2]
        root = int(data[2])
        testFoldingOnSubBenchmarks(
            f"./tests/blif/{benchmark}/{name}.abdd",  # import path
            f"./results/blif/{benchmark}/{varname}",  # export path
            rootNum=root  # root
        )


