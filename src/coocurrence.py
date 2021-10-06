
from ta_classes import *
from ta_functions import *

from itertools import product
from typing import Tuple
import copy

def getCoOccurrentStatesTD(ta:TTreeAut) -> list:
    
    def merge(state, macroList):
        # print(f"> merging {state} with {macroList}")
        result = [state]
        for item in macroList:
            result.extend(item)
        # print(f" - merged: {result}")
        return set(result)

    def process(state, ta, queue):
        # print(f"processing {state}")
        queue.append(state)
        result = []
        for edge in ta.transitions[state].values():
            process_results = []
            for child in edge[2]:
                if child == state:
                    continue
                if child in queue:
                    continue
                # print(f" adding {state}->{child}")
                process_results.append(process(child, ta, queue[:]))

            if edge[2] == [] or process_results != []:
                # print( f"process_results {state}: {process_results}")
                result.extend( [ merge(state, macroList) for macroList in product(*process_results) ])
        return result
    
    # -------------------------------------

    result = []
    for i in ta.rootStates:
        result.append(process(i, ta, []))

    print("RESULT ----")
    for j in result:
        for k in j:
            print(k)
    return result