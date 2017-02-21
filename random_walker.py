from util import random_choice


class RandomWalker(object):
    def __init__(self, graph, ew_func, accum_func=None):
        self.ew_func = ew_func
        self.G = graph
        self.accumulator = 0
        self.accum_func = accum_func

    def return_times(self, start_node, K):
        k = 0
        t = 0
        u = start_node  # Current node
        self.accumulator = self.accum_func(u)

        while k < K:
            # Compute un-normalised transition probabilities
            w = map(lambda v: self.ew_func(u, v), self.G.neighbors_iter(u))
            next_node = random_choice(self.G.neighbors(u), w)

            if next_node == start_node:
                yield (k + 1, t + 1, self.accumulator)
                k += 1

            self.accumulator += self.accum_func(next_node)

            t += 1
            u = next_node
