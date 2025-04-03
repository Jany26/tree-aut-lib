from typing import NewType, Optional, Union
from apply import materialization
from apply.abdd import ABDD, convert_ta_to_abdd
from apply.apply_edge import ApplyEdge
from apply.box_algebra import port_connection
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
            tuple[int],  # low-edge target node idx
            Optional[str],  # high-edge box             / None in case of leaf nodes
            tuple[int],  # high-edge target node idx
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
        self.depth = 0

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
    e1 = ApplyEdge(in1, None, None)
    e2 = ApplyEdge(in2, None, None)
    rule, roots = abdd_apply_from(op, e1, e2, helper)
    root = roots[0]
    abdd = ABDD(f"{in1.name} {op.name} {in2.name}", maxvar, root)
    abdd.root_rule = rule
    return abdd


def process_boxtree_leafcase(
    boxtree: BoxTreeNode, e1: ApplyEdge, e2: ApplyEdge, op, helper: ABDDApplyHelper, varlevel: int
) -> tuple[Optional[str], list[ABDDNode]]:
    if boxtree.is_leaf:
        rule = boxtree.node
        nodes = []
        for pc in boxtree.port_info:
            if pc.target1 is not None and pc.target2 is not None:
                nodes.append(
                    produce_terminal(e1.target[pc.target1].leaf_val, e2.target[pc.target2].leaf_val, op, helper)
                )
            elif pc.target1 is not None:
                nodes.append(e1.target[pc.target1])
            elif pc.target2 is not None:
                nodes.append(e2.target[pc.target2])
        return rule, nodes

    low_rule, low_targets = (
        process_boxtree_leafcase(boxtree.low, e1, e2, op, helper, varlevel + 1) if boxtree.low else (None, [])
    )
    high_rule, high_targets = (
        process_boxtree_leafcase(boxtree.high, e1, e2, op, helper, varlevel + 1) if boxtree.high else (None, [])
    )

    new_abdd_node = ABDDNode(helper.counter)
    new_abdd_node.var = varlevel  # not sure with the variable
    new_abdd_node.low_box = low_rule
    new_abdd_node.low = low_targets
    new_abdd_node.high_box = high_rule
    new_abdd_node.high = high_targets
    helper.counter += 1
    return None, [new_abdd_node]


def process_boxtree_innercase(
    boxtree: BoxTreeNode, e1: ApplyEdge, e2: ApplyEdge, op, helper: ABDDApplyHelper, varlevel: int
) -> tuple[Optional[str], list[ABDDNode]]:
    if boxtree.node == "True":
        return "X", [e1.abdd.terminal_1]
    if boxtree.node == "False":
        return "X", [e1.abdd.terminal_0]
    if boxtree.is_leaf:
        rule = boxtree.node
        nodes = []
        for pc in boxtree.port_info:
            if pc.target1 is not None and pc.target2 is not None:
                edge1low = ApplyEdge(e1.abdd, e1.target[pc.target1], False)
                edge2low = ApplyEdge(e2.abdd, e2.target[pc.target2], False)
                edge1high = ApplyEdge(e1.abdd, e1.target[pc.target1], True)
                edge2high = ApplyEdge(e2.abdd, e2.target[pc.target2], True)
                l_rule, l_target = abdd_apply_from(op, edge1low, edge2low, helper)
                h_rule, h_target = abdd_apply_from(op, edge1high, edge2high, helper)
                node = ABDDNode(helper.counter)
                node.var = varlevel
                node.low_box = l_rule
                node.low = l_target
                node.high_box = h_rule
                node.high = h_target
                node.is_leaf = False
                helper.counter += 1
                nodes.append(node)
            elif pc.target1 is not None:
                nodes.append(e1.target[pc.target1])
            elif pc.target2 is not None:
                nodes.append(e2.target[pc.target2])
        return rule, nodes

    low_rule, low_targets = (
        process_boxtree_innercase(boxtree.low, e1, e2, op, helper, varlevel + 1) if boxtree.low else (None, [])
    )
    high_rule, high_targets = (
        process_boxtree_innercase(boxtree.high, e1, e2, op, helper, varlevel + 1) if boxtree.high else (None, [])
    )
    new_abdd_node = ABDDNode(helper.counter)
    new_abdd_node.var = varlevel
    new_abdd_node.low_box = low_rule
    new_abdd_node.low = low_targets
    new_abdd_node.high_box = high_rule
    new_abdd_node.high = high_targets
    new_abdd_node.is_leaf = False
    helper.counter += 1
    return None, [new_abdd_node]


# NOTE: we probably need to have rule1, rule2 as operands too, since we need the
def abdd_apply_from(
    op: BooleanOperation, e1: ApplyEdge, e2: ApplyEdge, helper: ABDDApplyHelper
) -> tuple[Optional[str], list[ABDDNode]]:
    # TODO: check "call_cache" first
    # NOTE: perhaps here we should do something about "early" return (in case one operand is leaf and we can do early return)

    # materialization
    min1 = min(n.var if not n.is_leaf else helper.abdd1.variable_count for n in e1.target)
    min2 = min(n.var if not n.is_leaf else helper.abdd2.variable_count for n in e2.target)
    max1 = max(n.var if not n.is_leaf else helper.abdd1.variable_count for n in e1.target)
    max2 = max(n.var if not n.is_leaf else helper.abdd2.variable_count for n in e2.target)
    matlevel = min(min1, min2)

    if matlevel != max1:
        predicates1 = obtain_predicates(helper.abdd1, e1.source, e1.direction, matlevel)
        if predicates1 != frozenset() and e1.rule:
            pattern = cached_materialization_recipes[e1.rule][predicates1]
            e1 = materialize_abdd_pattern(e1, pattern, matlevel)
            return abdd_apply_from(op, e1, e2, helper)
    if matlevel != max2:
        predicates2 = obtain_predicates(helper.abdd2, e2.source, e2.direction, matlevel)
        if predicates2 != frozenset() and e2.rule:
            pattern = cached_materialization_recipes[e2.rule][predicates2]
            e2 = materialize_abdd_pattern(e2, pattern, matlevel)
            return abdd_apply_from(op, e1, e2, helper)

    # now we can assume that e1 and e2 have targets with the same variable

    # edges to leaves
    if all([i.is_leaf for i in e1.target] + [i.is_leaf for i in e2.target]):
        boxtree = boxtree_cache[(e1.rule, op, e2.rule)]
        helper.depth += 1
        rule, nodes = process_boxtree_leafcase(boxtree, e1, e2, op, helper, matlevel)
        # TODO: modify result structure during returns here
        helper.depth -= 1
        return rule, nodes

    # create a resulting edge object (node, rule), check the node against "node_cache"
    # insert node into "node_cache" if necessary

    # TODO: insert into "call_cache"

    boxtree = boxtree_cache[(e1.rule, op, e2.rule)]
    helper.depth += 1
    # TODO: fix depth -> matlevel is in cases of non-leaf boxtree nodes incorrect
    rule, nodes = process_boxtree_innercase(boxtree, e1, e2, op, helper, matlevel)
    # TODO: modify result structure during returns here
    helper.depth -= 1
    return rule, nodes


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
    return ApplyEdge(edge.abdd, edge.source, edge.direction)


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
    helper.counter += 1
    node.set_as_leaf(op_translate[op])
    if node in helper.node_cache:
        return helper.node_cache[node]
    else:
        helper.node_cache[node] = node
        return node


## Make the materialization take ABDD, and two nodes (or one in case it is above root node) in between which the materialized node will sit
