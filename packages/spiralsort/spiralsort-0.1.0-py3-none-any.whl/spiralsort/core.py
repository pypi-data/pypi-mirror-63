"""
info:
    file        :  core.py
    author      :  Thanasis Mattas
    license     :  GNU General Public License v3
    description :  Usually, does some spiralsorting stuff

SpiralSort is free software; you may redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version. You should have received a copy of the GNU
General Public License along with this program. If not, see
<https://www.gnu.org/licenses/>.
"""


import numpy as np
import pandas as pd

from spiralsort import utilities as util


def master_offset(nodes, master_node_id):
    """offsets all nodes, so that master_node becomes the origin"""
    master_index = nodes.loc[nodes.node_id == master_node_id].index[0]
    nodes.x = nodes.x - nodes.loc[master_index, "x"]
    nodes.y = nodes.y - nodes.loc[master_index, "y"]
    nodes.z = nodes.z - nodes.loc[master_index, "z"]
    return nodes


def distances_from_node(nodes, node):
    """evaluates the distances (norm I2) of nodes from node

    Args:
        nodes (df)    :  has node_id, x, y, z columns
        node (df)

    Returns:
        distances (array)
    """
    distances = np.sqrt(
        (nodes.x - node.x) ** 2
        + (nodes.y - node.y) ** 2
        + (nodes.z - node.z) ** 2
    )
    return distances


def prev_node_gradient(prev_node):
    """returns the angle of the prev_node vector from the 0x axis

    this is the angle that the point cloud will be rotated, in order to
    filter the counterclockwise side of the prev_node vector

    Args:
        prev_node (df) :  columns: ["node_id", 'x', 'y', 'z', ...]

    Returns:
        theta (float)  :  the gradient of the prev_node in radians
    """
    if ((prev_node.x < 0.001) and (prev_node.x > -0.001)
            and (prev_node.y >= 0)):
        theta = np.pi / 2
    elif ((prev_node.x < 0.001) and (prev_node.x > -0.001)
            and (prev_node.y < 0)):
        theta = - np.pi / 2
    elif prev_node.x >= 0.001:
        theta = np.arctan(prev_node.y / prev_node.x)
    # elif prev_node.iloc[0].x <= -0.001:
    else:
        theta = np.arctan(prev_node.y / prev_node.x) + np.pi
    return theta


def z_rotation(nodes, prev_node):
    """2D rotation on z axis (linear transformation), such as prev_node
    will fall on the 0x axis

    transformation matrix:

        | cos(theta)  sin(theta)|
        |-sin(theta)  cos(theta)|

    theta > 0 : clockwise
    theta < 0 : counterclockwise

    Args:
        nodes (df)         :  the point cloud
        prev_node (df) :  the node that will fall on the 0x axis

    Returns:
        rotated (df)       :  the point cloud after the rotation
    """
    theta = prev_node_gradient(prev_node)
    rotated = nodes.copy()
    rotated.x = np.cos(theta) * nodes.x + np.sin(theta) * nodes.y
    rotated.y = - np.sin(theta) * nodes.x + np.cos(theta) * nodes.y
    return rotated


def counterclockwise_filter(nodes, prev_node):
    """The goal is to force the algorithm to rotate anti-clockwise.
    Rotating the nodes, so that the vector of prev_node becomes the 0x
    axis, we keep only nodes with positive y, to find the next node from.

    Args:
        nodes (df)     :  the point cloud
        prev_node (df) :  the last popped node

    Returns:
        (index)        :  the indexes of the filtered nodes
    """
    nodes_rotated = z_rotation(nodes, prev_node)
    nodes_filtered_index = nodes_rotated[nodes_rotated.y > 0].index

    # don't counterclockwise filter if prev_node is the master_node
    # or no nodes are left after the filter
    if len(nodes_filtered_index):
        return nodes_filtered_index
    else:
        return nodes.index


def cost(nodes, prev_node):
    """|node - master| + |node - prev_node|

    Args:
        nodes (df)         : the point cloud
        prev_node (df)     : the node from which to calculate the cost

    Returns:
        cost_ (series)     : the cost column, to be inserted to the df
    """
    cost_ = nodes["|node - master|"].add(
        distances_from_node(nodes, prev_node)
    )
    return cost_


def cost_sort(nodes, prev_node, ignore_index=True):
    """sorts the nodes by cost from prev_node

    cost = |node - master| + |node - prev_node|

    Args:
        nodes (df)          : the point cloud
        prev_node (df)      : the node from which to calculate the cost
        ignore_index (bool) : whether to keep or reset the old index
                              (default True)

    Returns:
        nodes (df)          : the point cloud, cost-sorted
    """
    with pd.option_context("mode.chained_assignment", None):
        nodes.loc[:, "cost"] = cost(nodes, prev_node)
        nodes.sort_values("cost", inplace=True, kind="mergesort",
                          na_position="first", ignore_index=ignore_index)
    return nodes


def pop_next_node(nodes, prev_node):
    """
    1. evaluate cost
    2. pop the next_node (the one with the min cost)

    Args:
        nodes (df)          : the point cloud
        prev_node (df)      : the last popped node

    Returns:
        nodes (df)          : the point cloud, without the currently
                              popped node
        next_node_id (str)
        next_node (series)
    """
    nodes_filtered = nodes.loc[counterclockwise_filter(nodes, prev_node)]

    # 1. evaluate cost
    nodes_filtered.loc[:, "cost"] = cost(nodes_filtered, prev_node)

    # 2. pop the next_node
    next_node_idx = nodes_filtered["cost"].idxmin()
    next_node = nodes_filtered.loc[next_node_idx]
    next_node_id = next_node.node_id
    nodes = nodes[~nodes.index.isin([next_node.name])]
    return nodes, next_node_id, next_node


def spiral_stride(nodes,
                  node_ids,
                  prev_node,
                  spiral_window,
                  stride):
    """moves one stride inside the spiral_window, iteretively popping
    nodes with respect to the min cost

    Args:
        nodes (df)          :  the nodes batch that the algorithm is
                               woring on
        node_ids (list)     :  the so far spiral-sorted list of node_ids
        prev_node (df)      :  the last sorted (popped) node
        spiral_window (int) :  the window of nodes that the algorithm
                               will iteretively search for the next node
        stride (int)        :  the number of nodes to be sorted, before
                               moving to the next spiral_window

    Returns:
        nodes (df)          :  the initially nodes batch, without the
                               nodes popped at this stride
        node_ids (list)     :  the so far spiral-sorted list of node_ids
                               updated with the nodes popped at this
                               stride
        prev_node (df)      :  the last popped node at this stride
    """
    # keep a temp node_ids list, not to search through the whole list
    node_ids_inner = []

    # for the first 1000 nodes dont filter the counterclockwise side
    # nodes, to prevent from oscilating on a lobe (half spherical disk)
    if len(node_ids) <= 1000:
        nodes_filtered = nodes[slice(0, spiral_window)]
    else:
        nodes_filtered = nodes.loc[counterclockwise_filter(nodes, prev_node)]
        nodes_filtered = cost_sort(nodes, prev_node)
        nodes_filtered = nodes_filtered[slice(0, spiral_window)]

    iters = min(stride, len(nodes_filtered.index))

    for _ in range(iters):
        nodes_filtered, prev_node_id, prev_node = pop_next_node(
            nodes_filtered,
            prev_node
        )
        node_ids_inner.append(prev_node_id)

    # drop node_ids_inner from nodes remainder
    nodes = nodes[~nodes.node_id.isin(node_ids_inner)]

    # update node_ids
    node_ids += node_ids_inner

    return nodes, node_ids, prev_node


def check_duplicated_ids(nodes):
    """check node_ids uniqueness"""
    duplicated_ids = nodes[nodes.node_id.duplicated()].node_id.to_list()
    if duplicated_ids:
        raise Exception("node_id column has duplicated entries: {}"
                        .format(duplicated_ids))


def spiralsort(nodes, master_node_id):
    """spiral-sorting the node-cloud, starting from the master node

    Spiral-sorting algorithm:
    1. Sort the point cloud with respect to the distance from the master
       node and segment it into slices.
    2. Take the first slice (2000 nodes
    3. Take a SPIRAL_WINDOW (slice further)
       Spiral windows for the 1st slice consist of 300 nodes, starting
       from the last sorted node (the master_node for the 1st window)
    4. Iteretively pop 20 nodes (a stride), by the minimum cost.
       (cost = |node - master_node| + |node - prev_node|)
       Take the next SPIRAL_WINDOW and pop the next 10 nodes.
       Continue until the remainder of the nodes reaches the size of the
       half slice (1000 nodes for the 1st slice).
    5. Merge the remaining nodes with the next slice
       (This overlap of the slices ensures that there is a continuity
        while selecting the next nodes when the algorithm reaches the
        last nodes of the slice)
    6. For the next slices, a filter is applied, which keeps only nodes
       from the counterclockwise side of the vector starting from the
       master node and ending at the previous node,in order to force the
       algorithm to move to a constant rotation direction
    7. Keep moving by SPIRAL_WINDOWs (or strides), counterclockwise
       filtering at each stride, popping 10s of nodes until the half
       slice thresshold
    8. Upon reaching the last slice, remove the half_slice threshold, to
       pop all the remaining nodes.

    Args:
        nodes (df)           :  the box_nodes (without the bar_nodes)
        master_node_id (str) :  the node on the box surface where the
                                 deformation starts

    Returns:
        nodes_sorted (df)    :  the nodes spiral-sorted, starting from
                                the master node
    """
    # first, check if the node_ids are unique
    check_duplicated_ids(nodes)

    # final sequence of ids, used to sort the final dataframe,
    # initialized with the master node
    node_ids = [master_node_id]

    # make master_node the origin of the axes
    nodes = master_offset(nodes, master_node_id)

    # initialize previous node with the master node (series)
    master_node = nodes.loc[nodes["node_id"] == master_node_id]
    prev_node = master_node.iloc[0]

    # drop master node
    nodes.drop(master_node.index, inplace=True)

    # distance of all nodes from the master node
    nodes["|node - master|"] = distances_from_node(nodes, prev_node)

    # distance-sort from master_node
    nodes.sort_values("|node - master|", inplace=True, kind="mergesort",
                      ignore_index=True)

    # segment nodes into slices, not to work on the whole df
    # [
    #     [0, 2000], [2000, 6000], [6000, 14000], [14000, 30000],
    #     [30000, 62000], [62000, 94000], [94000, 126000], ...
    # ]
    slices = util.create_slices(nodes)

    # number of nodes anti-clockwise filtered and cost_sorted from prev
    # node, in order to iteretively pop the next nodes in the STRIDE
    SPIRAL_WINDOW = 400
    STRIDE = 15

    # this is the container that the sorting algorithm will work with
    remaining_nodes = pd.DataFrame(columns=nodes.columns)

    for idx, slicing_obj in enumerate(slices):

        # moving to more distant slices, spiral_window gets bigger, as
        # the nodes are more spread out away from the master node
        spiral_window = int(SPIRAL_WINDOW + 100 * idx)

        # Concat with the remainder of the nodes (which is the half of
        # the previous slice), in order to have continuity.
        # (For example, previous to last node will only have the last
        # remaining node to find the next cost-sorted node, which is
        # not correct, because there are other candidates, not included
        # in the current slice.)
        remaining_nodes = pd.concat([remaining_nodes, nodes[slicing_obj]])

        half_slice = util.calc_half_slice(slicing_obj)

        # leave half_slice remaining nodes to merge with the next slice
        # except from the last slice
        if (slicing_obj in slices[: -1]) and (len(slices) > 1):
            spiral_iters = (len(remaining_nodes.index) - half_slice) // STRIDE
        else:
            spiral_iters = len(remaining_nodes.index) // STRIDE

        for _ in range(spiral_iters):
            remaining_nodes, node_ids, prev_node = spiral_stride(
                remaining_nodes,
                node_ids,
                prev_node,
                spiral_window,
                STRIDE
            )

    # return master node to nodes
    nodes = pd.concat([master_node, nodes])
    # reorder nodes with respect to the spiral-sorted node_ids
    node_ids = pd.DataFrame({"node_id": node_ids})
    nodes_sorted = node_ids.merge(nodes, on="node_id")            \
                           .loc[:, ["node_id", 'x', 'y', 'z']]    \
                           .reset_index(drop=True, inplace=False)

    return nodes_sorted
