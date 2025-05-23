"""
[file] materialize.py
[author] Jany26  (Jan Matufka)  <xmatuf00@stud.fit.vutbr.cz>
[description] Node materialization in ABDD Apply for synchronized simultaneousrecursive traversal.
"""

from apply.abdd_apply_helper import ABDDApplyHelper
from apply.abdd_node import ABDDNode
from apply.apply_edge import ApplyEdge
from apply.materialization.abdd_pattern import MaterializationRecipe


def materialize_abdd_pattern(
    edge: ApplyEdge, mat_recipe: MaterializationRecipe, mat_level: int, helper: ABDDApplyHelper
) -> ApplyEdge:
    """
    Creates an edge that points to materialized nodes to replace the initial edge from the initial ABDD Apply call.

    Based on the retrieved 'mat_recipe' and the given 'edge' to be materialized
    (from which concrete values are retrieved to replace symbolic values in the recipe),
    the edge pointing to intermediate (materialized) nodes is returned.
    The materialized nodes are stored inside the node cache, which contain edges from materialized nodes to the
    original 'edge' targets -- these edges will be visited during further Apply calls.
    """
    if len(mat_recipe.init_targets) > 1:
        raise ValueError("Materialization above root has more than one target. Don't know what to do.")
    workset = [i for i in mat_recipe.init_targets]
    nodemap = {f"out{i}": n for i, n in enumerate(edge.target)}
    nodemap["0"] = edge.abdd.terminal_0
    nodemap["1"] = edge.abdd.terminal_1
    varmap = {f"out{i}": n.var for i, n in enumerate(edge.target)}
    varmap["mat"] = mat_level

    # initial targets node creation (for correctly being able to map edge targets etc.)
    for i in workset:
        if i.new:
            nodemap[i.name] = ABDDNode(helper.counter)
            helper.counter += 1

    # traversing
    while workset != []:
        # nodes are always created when their parents are processed
        pattern = workset.pop(0)
        if not pattern.new:
            continue

        # new node reference
        currentnode = nodemap[pattern.name]
        currentnode.low_box = pattern.low_box
        currentnode.high_box = pattern.high_box
        currentnode.var = varmap[pattern.level]
        currentnode.is_leaf = False

        # creating references to low edge target nodes
        newlow = []
        for i in pattern.low:
            if i.new:
                nodemap[i.name] = ABDDNode(helper.counter)
                helper.counter += 1
            newlow.append(nodemap[i.name])
            workset.append(i)

        # creating references to high edge target nodes
        newhigh = []
        for i in pattern.high:
            if i.new:
                nodemap[i.name] = ABDDNode(helper.counter)
                helper.counter += 1
            newhigh.append(nodemap[i.name])
            workset.append(i)
        currentnode.low = newlow
        currentnode.high = newhigh

        # checking the materialized node against the node cache
        cache_hit = helper.node_cache.find_node(currentnode)
        if cache_hit is not None:
            nodemap[pattern.name] = cache_hit
        else:
            helper.node_cache.insert_node(currentnode)

    # redirecting initial targets and rules in the ABDD
    result = ApplyEdge(edge.abdd, edge.source, edge.direction)
    result.rule = mat_recipe.init_box
    tgt = [nodemap[i.name] for i in mat_recipe.init_targets]
    result.target = tgt
    return result


# End of file materialize.py
