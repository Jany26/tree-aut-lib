from ta_classes import *
from ta_functions import *
from test_data import *


def trim(ta:TTreeAut) -> TTreeAut:
    workTA = removeUselessStates(ta)

    # remove transitions over variables which are clearly unnecessary
    # TODO: define/explain ^^
    
    # get all paths from roots to leaves ---> make a function

    return workTA


def intersectoidEdgeKey(e1:list, e2:list) -> str:
    state = f"({e1[0]}, {e2[0]})"
    symb = e2[1].label
    var = f",{e1[1].variable}" if e1[1].variable != "" else ""

    children = f""
    for i in range(len(e1[2])):
        children += f"({e1[2][i]},{e2[2][i]}),"
    children = children[:-1]

    key = f"{state}-<{symb}{var}>-({children})"
    return key


def createIntersectoid(ta:TTreeAut, box:TTreeAut, root:str) -> TTreeAut:

    resultTransitions = {}
    for taEdge in transitions(ta):
        for boxEdge in transitions(box):
            if len(taEdge[2]) != len(boxEdge[2]):
                continue
            aSymb = taEdge[1].label
            bSymb = boxEdge[1].label
            aVar = taEdge[1].variable
            if aSymb != bSymb and not bSymb.startswith("Port"):
                continue
            state = (taEdge[0],boxEdge[0])
            key = intersectoidEdgeKey(taEdge, boxEdge)
            if state not in resultTransitions:
                resultTransitions[state] = {}

            children = [(taEdge[2][i], boxEdge[2][i]) for i in range(len(taEdge[2]))]
            edge = [state, TEdge(bSymb, [], aVar), children]
            resultTransitions[state][key] = edge
    resultRootstates = [(root,b) for b in box.rootStates]
    resultName = f"intersectoid({ta.name}, {box.name}, {root})"
    result = TTreeAut(resultRootstates, resultTransitions, resultName, box.portArity)
    return result


def portToStateMapping(ta:TTreeAut) -> dict:
    result = {e[1].label: None for e in transitions(ta) if e[1].label.startswith("Port")}
    for edge in transitions(ta):
        symb = edge[1].label
        if not symb.startswith("Port"):
            continue
        result[symb] = edge[0]
    return result


def getMaximalMappingDFS(ta:TTreeAut, ports:dict) -> dict:
    pass


def boxFinding(ta:TTreeAut, box:TTreeAut, root:str) -> dict:
    A = createIntersectoid(ta, box, root)
    print(A)
    A = trim(A) # additional functionality maybe needed?
    tree, string = nonEmptyBU(A)
    ports = portToStateMapping(A)
    print(ports)
    ps = getMaximalMappingDFS(A, ports)
    # ^^ this is based on the rootDistances of nodes from "ports" 
    if tree == None:
        return {}

    for i in range(box.portArity):
        pass


# End of normalization.py
