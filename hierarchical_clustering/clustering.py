import copy
from showtree import showtree


def read_distance_matrix(dm_file):
    with open(dm_file, 'r') as f:
        content = [line.strip().split() for line in f.readlines()]  # Remove spaces and newlines
    distance_dict = dict()  # Initialize outer dictionary
    for k in range(1, len(content)):
        # Use dictionary comprehension to quickly iterate through
        distance_dict[content[k][0]] = {key: int(value) for (key, value) in zip(content[0], content[k][1:])}
    return distance_dict


def count_nested_tuples(nested_tuple):
    """
    Uses recursion to count the number of elementary objects in a nested tuple
    :param nested_tuple: An object with tuple(s) nested within tuple(s)
    :return: Number of objects in all nested tuples
    """
    num_obj = 0
    for ele in nested_tuple:
        if len(ele) > 1:
            num_obj += count_nested_tuples(ele)
        else:
            num_obj += 1
    return num_obj


import copy
def merge_clusters(distance_dict, clus1, clus2):
    clus1_size = len(distance_dict[clus1])
    clus2_size = len(distance_dict[clus2])
    keys = copy.deepcopy(list(distance_dict.keys()))  # Need a deep copy of original list of keys
    distance_dict[(clus1, clus2)] = dict()  # Add cluster value to new cluster dictionary entry
    for cluster in keys:
        clus1_dist = distance_dict[clus1][cluster]  # Get distances from each merged cluster to iterated cluster
        clus2_dist = distance_dict[clus2][cluster]
        new_cluster_distance = (clus1_size*clus1_dist + clus2_size*clus2_dist)/(clus1_size + clus2_size)
        distance_dict[cluster][(clus1, clus2)] = new_cluster_distance  # Set both dict entries to calc value
        distance_dict[(clus1, clus2)][(clus1, clus2)] = 0  # Set distance to self to 0
        if cluster != clus1 and cluster != clus2:
            distance_dict[(clus1, clus2)][cluster] = new_cluster_distance
    for cluster in keys:
        del distance_dict[cluster][clus1]  # Delete previous, unmerged iterations of clusters
        del distance_dict[cluster][clus2]
    del distance_dict[clus1]
    del distance_dict[clus2]
    return distance_dict


# Should I make a list of possibilities if several combinations have same smallest distance?
def closest_clusters(distance_dict):
    min_dist = (None, None, 100)
    for clus1 in distance_dict.keys():
        for clus2 in distance_dict[clus1].keys():
            # Don't want to return a value of 0 since that's the distance of a cluster to itself
            if distance_dict[clus1][clus2] < min_dist[2] and distance_dict[clus1][clus2] != 0:
                min_dist = (clus1, clus2, distance_dict[clus1][clus2])
        # maximum = min(distance_dict[clus1], key=distance_dict[clus1].get)
    return min_dist


def hiercluster(distance_dict):
    # Create a height dictionary for each cluster and initialize to 0
    cluster_heights = dict()
    for key in distance_dict.keys():
        cluster_heights[key] = 0
    closest_height = 0
    while len(cluster_heights.keys()) > 1:
        closest = closest_clusters(distance_dict)  # Find closest clusters
        closest_height = distance_dict[closest[0]][closest[1]]/2 + closest_height  # Find height between two clusters
        distance_dict = merge_clusters(distance_dict, closest[0], closest[1])  # Merge closest clusters
        del cluster_heights[closest[0]]  # Remove single cluster from height dictionary
        del cluster_heights[closest[1]]
        cluster_heights[(closest[0], closest[1])] = closest_height  # Update height dictionary with new cluster/height
    return list(cluster_heights.keys())[0], list(cluster_heights.values())[0]  # Return tuple (node, height)


df = read_distance_matrix('small-distances.txt')
# showtree(hiercluster(df))

class HierTree:


class Cluster:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def set_left(self, group):
        self.left = group

    def set_right(self, group):
        self.right = group

    def get_name(self):
        return self.name

class Leaf:
    def __init__(self, name):
        self.name = name