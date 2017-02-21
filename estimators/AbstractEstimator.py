import util
from random_walker import RandomWalker


class AbstractEstimator(object):
    def __init__(self, G):
        self.G = G
        # Optimisation, avoids calling `degree` all the time.
        # The graph doesn't change anyway, so it's OK to cache degrees.
        self.degrees = {i: self.G.degree(i) for i in self.G.nodes_iter()}

    def _edge_weight_func(self, u, v):
        # Simple random walk
        return 1 / self.degrees[u]

    def _node_weight_func(self, u):
        return sum(map(lambda v: self._edge_weight_func(u, v),
                       self.G.neighbors_iter(u)))

    def _compute_metric(self, node, k, t, accum):
        raise NotImplementedError()

    def _accum_func(self, u):
        return 0

    def estimates(self, num_estimates, start_node=None):
        rw = RandomWalker(self.G,
                          self._edge_weight_func,
                          self._accum_func)

        if start_node is None:
            start_node = \
                util.pick_highest_weight_node(self.G, self._node_weight_func)

        # Damn, Python 3
        return map(lambda r: self._compute_metric(start_node, r[0], r[1], r[2]),
                   rw.return_times(start_node, num_estimates))
