from typing import Optional, Union
from apply import materialization
from apply.abdd import ABDD, convert_ta_to_abdd
from apply.apply_edge import ApplyEdge
from apply.box_algebra.apply_intersectoid import BooleanOperation
from apply.box_algebra.box_trees import BoxTreeNode
from apply.box_algebra.port_connection import PortConnectionInfo
from apply.materialization.abdd_pattern import MaterializationRecipe
from apply.materialization.pattern_generate import obtain_predicates
from helpers.utils import box_catalogue
from tree_automata.automaton import TTreeAut
from apply.abdd_node import ABDDNode

from apply.pregenerated.box_algebrae import boxtree_cache
from apply.pregenerated.materialization_recipes import cached_materialization_recipes


materialization_map: dict[str, int] = {"out0": 0, "out1": 1}

default_boxtree = BoxTreeNode(
    node=None, port_info=[PortConnectionInfo(target1=0, target2=0, recursion=True, negation=False)]
)


class ABDDApplyHelper:
    """
    Helper class with necessary cache and information
    needed during the recursive apply function.

    'call_cache' - Stores results of recursive apply calls.

    'node_cache' - Makes sure that identical nodes are not duplicated.
    This differs from ApplyCallCache in the sense that two different apply
    calls might create two nodes that represent the same boolean function.

    """

    # cache[ op, var, node_a, box_a, node_b, box_b ] -> node
    call_cache: dict[
        tuple[
            BooleanOperation,  # operation used in the apply call
            int,  # at which variable level is apply called
            int,  # node index of the first operand node
            str,  # box used on the edge leading to the first operand node
            int,  # node index of the second operand node
            str,  # box used on the edge leading to the second operand node
        ],
        ABDDNode,
    ]

    # cache [ var, low_box, low_target, high_box, high_target ] -> node
    node_cache: dict[
        tuple[
            int,  # variable of the node
            Optional[str],  # low-edge box              / None in case of leaf nodes
            Optional[int],  # low-edge target node idx  / None in case of leaf nodes
            Optional[str],  # high-edge box             / None in case of leaf nodes
            Optional[int],  # high-edge target node idx / None in case of leaf nodes
        ],
        ABDDNode,
    ]

    def __init__(self, in1: ABDD, in2: ABDD, maxvar: Optional[int] = None):
        self.call_cache = {}
        self.node_cache = {}

        self.abdd1: ABDD = in1
        self.abdd2: ABDD = in2

        self.counter_1: int = in1.count_nodes()
        self.counter_2: int = in2.count_nodes()
        self.counter: int = 0
        self.maxvar = maxvar

    def insert_call(self, op: BooleanOperation, edge1: ApplyEdge, edge2: ApplyEdge) -> None:
        pass

    def find_call(self, op: BooleanOperation, edge1: ApplyEdge, edge2: ApplyEdge) -> Optional[ABDDNode]:
        pass

    def insert_node(self, node: ABDDNode) -> None:
        pass

    def find_node(self, node: ABDDNode) -> Optional[ABDDNode]:
        pass


def abdd_apply(
    op: BooleanOperation, in1: Union[TTreeAut, ABDD], in2: Union[TTreeAut, ABDD], maxvar: Optional[int] = None
) -> ABDD:
    """
    This serves as a wrapper to the recursive abdd_apply_from(), where actual apply takes place.

    Herein, we just precompute and create some initial information and then call abdd_apply_from() on root nodes
    of the two given ABDDs.

    Apply can change/modify the structures of initial inputs (materialization), so it is advised to always create
    copies before apply calls.
    """
    # some preliminary typecasting and checking
    if maxvar is None:
        maxvar = max(in1.get_var_max(), in2.get_var_max())
    if type(in1) == TTreeAut:
        in1 = convert_ta_to_abdd(in1, var_count=maxvar)
    if type(in2) == TTreeAut:
        in2 = convert_ta_to_abdd(in2, var_count=maxvar)

    if not (maxvar is not None and type(in1) == ABDD and type(in2) == ABDD):
        ValueError("invalid parameters")

    # manual materialization override for root nodes
    helper = ABDDApplyHelper(in1, in2, maxvar=maxvar)
    matlevel = min(in1.root.var, in2.root.var)
    res1 = obtain_predicates(in1, None, None, matlevel)
    res2 = obtain_predicates(in2, None, None, matlevel)
    recipe1 = None if res1 == frozenset() else cached_materialization_recipes[in1.root_rule][res1]
    recipe2 = None if res2 == frozenset() else cached_materialization_recipes[in2.root_rule][res2]
    if recipe1 is not None:
        materialize_abdd_pattern(ApplyEdge(in1, None, None), recipe1, matlevel)
    if recipe2 is not None:
        materialize_abdd_pattern(ApplyEdge(in2, None, None), recipe2, matlevel)

    root = abdd_apply_from(op, in1.root, in2.root, helper)
    abdd = ABDD(f"{in1.name} {op.name} {in2.name}", maxvar, root)
    abdd.root_rule = None if root.var == 1 else "X"
    return abdd


def abdd_apply_from(op: BooleanOperation, node1: ABDDNode, node2: ABDDNode, helper: ABDDApplyHelper) -> ABDDNode:

    # TODO: check "call_cache" first
    # NOTE: perhaps here we should do something about "early" return (in case one operand is leaf and we can do early return)

    if node1.is_leaf and node2.is_leaf:
        return produce_terminal(node1.leaf_val, node2.leaf_val, op, helper)

    # low/low apply - materialization

    # TODO: make this more compact -> return boolean (materialization needed - yes/no) and integer (materialization level)
    min1low = min(n.var if not n.is_leaf else helper.abdd1.variable_count for n in node1.low)
    min2low = min(n.var if not n.is_leaf else helper.abdd2.variable_count for n in node2.low)
    max1low = max(n.var if not n.is_leaf else helper.abdd1.variable_count for n in node1.low)
    max2low = max(n.var if not n.is_leaf else helper.abdd2.variable_count for n in node2.low)

    if min1low != min2low or max1low != max2low:
        min1 = min(helper.abdd1.variable_count if n.is_leaf else n.var for n in node1.low)
        min2 = min(helper.abdd2.variable_count if n.is_leaf else n.var for n in node2.low)
        mat_level = min(min1, min2)
        predicates1 = obtain_predicates(helper.abdd1, node1, False, mat_level)
        predicates2 = obtain_predicates(helper.abdd2, node2, False, mat_level)
        if predicates1 != frozenset() and node1.low_box:
            pattern = cached_materialization_recipes[node1.low_box][predicates1]
            materialize_abdd_pattern(ApplyEdge(helper.abdd1, node1, False), pattern, mat_level)
        if predicates2 != frozenset() and node2.low_box:
            pattern = cached_materialization_recipes[node2.low_box][predicates2]
            materialize_abdd_pattern(ApplyEdge(helper.abdd2, node2, False), pattern, mat_level)

    # high/high apply - materialization

    # TODO: same as with low/low materialization -> compactness
    # TODO: maybe even make this into one function, same for low/high just switching with one bool
    min1high = min(n.var if not n.is_leaf else helper.abdd1.variable_count for n in node1.high)
    min2high = min(n.var if not n.is_leaf else helper.abdd2.variable_count for n in node2.high)
    max1high = max(n.var if not n.is_leaf else helper.abdd1.variable_count for n in node1.high)
    max2high = max(n.var if not n.is_leaf else helper.abdd2.variable_count for n in node2.high)

    if min1high != min2high or max1high != max2high:
        min1 = min(helper.abdd1.variable_count if n.is_leaf else n.var for n in node1.high)
        min2 = min(helper.abdd2.variable_count if n.is_leaf else n.var for n in node2.high)
        mat_level = min(min1, min2)
        predicates1 = obtain_predicates(helper.abdd1, node1, True, mat_level)
        predicates2 = obtain_predicates(helper.abdd2, node2, True, mat_level)
        if predicates1 != frozenset() and node1.high_box:
            pattern = cached_materialization_recipes[node1.high_box][predicates1]
            materialize_abdd_pattern(ApplyEdge(helper.abdd1, node1, True), pattern, mat_level)
        if predicates2 != frozenset() and node2.high_box:
            pattern = cached_materialization_recipes[node2.high_box][predicates2]
            materialize_abdd_pattern(ApplyEdge(helper.abdd2, node2, True), pattern, mat_level)

    low_boxtree = default_boxtree
    high_boxtree = default_boxtree

    if node1.low_box is not None and node2.low_box is not None:
        low_boxtree = boxtree_cache[(node1.low_box, op, node2.low_box)]
    elif node1.high_box is not None and node2.high_box is not None:
        high_boxtree = boxtree_cache[(node1.high_box, op, node2.high_box)]

    # TODO: create target nodes from the box trees, which include invoking recursive apply calls
    # queue = [box_tree_node]
    # while queue != []:
    #     node = queue.pop(0)
    #     if not node.is_leaf:
    #         newnode = ABDDNode(matlevel + box_tree_node.depth(node))
    #     if node.low:
    #         queue.append(node.low)
    #     if node.high:
    #         queue.append(node.high)
    #     low, lowrule = abdd_apply_from(op, edge1, edge2, helper)
    #     high, highrule = abdd_apply_from(op, edge1, edge2, helper)

    # create a resulting edge object (node, rule), check the node against "node_cache"
    # insert node into "node_cache" if necessary

    # TODO: insert into "call_cache"

    return [], None


# TODO: edit ABDD structure using a materialization recipe
def materialize_abdd_pattern(edge: ApplyEdge, mat_recipe: MaterializationRecipe, mat_level: int) -> None:
    above_root = edge.source is None
    if above_root:
        edge.abdd.root_rule = mat_recipe.init_box
    if len(mat_recipe.init_targets) > 1:
        raise ValueError("Materialization above root has more than one target. Don't know what to do.")
    workset = [i for i in mat_recipe.init_targets]
    nodemap = {f"out{i}": n for i, n in enumerate(edge.target)}
    nodemap["0"] = edge.abdd.terminal_0
    nodemap["1"] = edge.abdd.terminal_1
    varmap = {f"out{i}": n.var for i, n in enumerate(edge.target)}
    varmap["mat"] = mat_level

    # initial targets node creation
    for i in workset:
        if i.new:
            nodemap[i.name] = ABDDNode(edge.abdd.node_count)
            edge.abdd.node_count += 1

    # traversing
    while workset != []:
        # nodes are always created when their parents are processed
        pattern = workset.pop(0)
        if not pattern.new:
            continue

        # new node reference
        currentnode = nodemap[pattern.name]
        if above_root:
            currentnode.is_root = True
            edge.abdd.root.is_root = False
            edge.abdd.root = currentnode
            above_root = False
        currentnode = nodemap[pattern.name]
        currentnode.low_box = pattern.low_box
        currentnode.high_box = pattern.high_box
        currentnode.var = varmap[pattern.level]
        currentnode.is_leaf = False

        # creating references to low edge target nodes
        newlow = []
        for i in pattern.low:
            if i.new:
                nodemap[i.name] = ABDDNode(edge.abdd.node_count)
                edge.abdd.node_count += 1
            newlow.append(nodemap[i.name])
            workset.append(i)

        # creating references to high edge target nodes
        newhigh = []
        for i in pattern.high:
            if i.new:
                nodemap[i.name] = ABDDNode(edge.abdd.node_count)
                edge.abdd.node_count += 1
            newhigh.append(nodemap[i.name])
            workset.append(i)
        currentnode.low = newlow
        currentnode.high = newhigh

    # redirecting initial targets and rules in the ABDD
    if edge.direction is not None:
        if edge.direction:
            edge.source.high_box = mat_recipe.init_box
            edge.source.high = [nodemap[i.name] for i in mat_recipe.init_targets]
        else:
            edge.source.low_box = mat_recipe.init_box
            edge.source.low = [nodemap[i.name] for i in mat_recipe.init_targets]


def get_boxstate_nodename_dict(edge_obj: ApplyEdge) -> dict[str, ABDDNode]:
    box: TTreeAut = box_catalogue[edge_obj.box_reduction]
    portstates = []
    for sym, states in box.get_output_edges().items():
        if sym.startswith("Port"):
            portstates.extend(states)
    portstates = [state for sym, states in box.get_output_edges().items() if sym.startswith("Port") for state in states]
    # ports = [sym for sym in box.get_output_edges().keys() if sym.startswith('Port')]
    portstates.sort()
    nodes: list[ABDDNode]
    if isinstance(edge_obj.to_node, ABDDNode):
        nodes = [edge_obj.to_node]
    elif isinstance(edge_obj.to_node, ABDDNode):
        nodes = edge_obj.to_node
    elif edge_obj.to_node is None:
        return {}
    return {portstates[i]: nodes[i] for i in range(len(portstates))}


def produce_terminal(val1: int, val2: int, op: BooleanOperation, helper: ABDDApplyHelper) -> ABDDNode:
    op_translate: dict[BooleanOperation, int] = {
        BooleanOperation.NOP: -1,
        BooleanOperation.AND: val1 and val2,
        BooleanOperation.OR: val1 or val2,
        BooleanOperation.XOR: (val1 and not val2) or (not val1 and val2),
        BooleanOperation.IFF: (val1 and val2) or (not val1 and not val2),
        BooleanOperation.NAND: not (val1 and val2),
        BooleanOperation.NOR: not (val1 or val2),
        BooleanOperation.IMPLY: not val1 or val2,
        BooleanOperation.NOT: -1,
    }
    node = ABDDNode(helper.counter)
    node.set_as_leaf(op_translate[op])
    if node in helper.node_cache:
        return helper.node_cache[node]
    else:
        helper.node_cache[node] = node
        return node


## Make the materialization take ABDD, and two nodes (or one in case it is above root node) in between which the materialized node will sit
