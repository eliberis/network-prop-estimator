from random import random
from itertools import accumulate
from bisect import bisect


def random_choice(population, weights):
    accum_weights = list(accumulate(weights))
    return population[bisect(accum_weights, random() * accum_weights[-1])]

def pick_highest_weight_node(G, nw_func):
    return max(G.nodes_iter(), key=nw_func)
