"""
[file] dimacs_analysis.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Folding tests on processed Boolean functions in
conjuntive normal form (CNF) - DIMACS format.
[note] Also gets box usage statistics for ABDD model.
"""


import os
import copy

from blif_analysis import testFoldingOnSubBenchmarks, translation, formatBoxCounts
from utils import boxOrders, createVarOrder
from folding import treeAutFolding
from ta_functions import reachableTD
from format_abdd import importTAfromABDD
from bdd import addDontCareBoxes
from simulation import addVariablesBU
from normalization import treeAutNormalize
from unfolding import unfold

def getFoldedDIMACS(initial, order):
    vars = int(initial.getVariableOrder()[-1])
    initialChanged = addDontCareBoxes(initial, vars)
    unfolded = unfold(initialChanged)

    unfolded_extra = copy.deepcopy(unfolded)
    addVariablesBU(unfolded_extra, vars)
    var_order = createVarOrder('', vars+2, start=0)
    normalized = treeAutNormalize(unfolded_extra, var_order)
    normalized_clean = copy.deepcopy(normalized)
    normalized_clean.reformatKeys()
    normalized_clean.reformatStates()
    addVariablesBU(normalized_clean, vars+2)
    normalized.metaData.recompute()
    normalized_clean.metaData.recompute()
    folded = treeAutFolding(normalized_clean, boxOrders[order], normalized_clean.getVariableMax())
    return folded

def createFileOrder(dirPath: str) -> list:
    dimacsSorter: dict[int, str] = {}
    for subdir, dirs, files in os.walk(dirPath):
        for file in files:
            benchmark = int(file.split('-')[-1].split('.')[0])
            dimacsSorter[benchmark] = f"{subdir}{file}"
    return dimacsSorter


def printBoxCountsDIMACS():
    order = 'full'
    initialString = f"{'path' :<30} = {'norm' :<5}, {order :<5}, "
    for val in translation.values():
        initialString += f"{val :<5}, "
    print(initialString)
    dimacsSorter = createFileOrder(f"../tests/uf20/")
    for benchmark in sorted(dimacsSorter.keys()):
        path = dimacsSorter[benchmark]
        name = path.split('/')[-1]
        initial = importTAfromABDD(path)
        folded = getFoldedDIMACS(initial, order)
        print(f"{name :<30} = {len(initial.getStates()) :<5}, {len(reachableTD(folded)) :<5}, {formatBoxCounts(folded)}")


def foldingTestDIMACS():
    report_line = f"{'name of the benchmark' :<30}\t| init\t| unfo\t| norm"
    for orderName in boxOrders.keys():
        report_line += f"\t| {orderName}"
    print(report_line)

    dimacsSorter = createFileOrder("../tests/uf20/")
    for benchmark in sorted(dimacsSorter.keys()):
        filename = dimacsSorter[benchmark]
        print(f"{filename}", end='\r')

        testFoldingOnSubBenchmarks(
            f"{filename}",
            f"../data/dimacs/uf20/{filename.split('.')[-1]}",
            orders=None,
            rootNum=None
        )

if __name__ == "__main__":
    # printBoxCountsDIMACS()
    foldingTestDIMACS()