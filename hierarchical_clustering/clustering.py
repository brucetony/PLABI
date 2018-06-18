import copy


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


def merge_clusters(distance_dict, clus1, clus2):
    clus1_size = len(distance_dict[clus1])
    clus2_size = len(distance_dict[clus2])
    keys = copy.deepcopy(list(distance_dict.keys()))  # Need a deep copy of original list of keys
    for cluster in keys:
        distance_dict[(clus1, clus2)] = dict()  # Add cluster value to new cluster dictionary entry
        clus1_dist = distance_dict[clus1][cluster]  # Get distances from each merged cluster to iterated cluster
        clus2_dist = distance_dict[clus2][cluster]
        new_cluster_distance = (clus1_size*clus1_dist + clus2_size*clus2_dist)/(clus1_size + clus2_size)
        distance_dict[cluster][(clus1, clus2)] = new_cluster_distance  # Set both dict entries to calc value
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
            if distance_dict[clus1][clus2] < min_dist[2] and distance_dict[clus1][clus2] != 0:
                min_dist = (clus1, clus2, distance_dict[clus1][clus2])
        # maximum = min(distance_dict[clus1], key=distance_dict[clus1].get)
    return min_dist


df = read_distance_matrix('distances.txt')
# df = merge_clusters(df, 'B', 'E')
print(closest_clusters(df))
