from random import random
from itertools import accumulate
from bisect import bisect


def random_choice(population, weights):
    accum_weights = list(accumulate(weights))
    return population[bisect(accum_weights, random() * accum_weights[-1])]


def pick_highest_weight_node(G, nw_func):
    return max(G.nodes_iter(), key=nw_func)


def edge_triangles(G, u, v):
    common_neigh = \
        filter(lambda n: G.has_edge(n, u), G.neighbors_iter(v))
    return len(list(common_neigh))


def node_triangles(G, u):
    # Counted u-B-C and u-C-B twice, so divide by 2
    return sum(map(lambda v: edge_triangles(G, u, v), G.neighbors_iter(u))) // 2
