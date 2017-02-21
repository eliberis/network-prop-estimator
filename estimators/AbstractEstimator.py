import util
from random_walker import RandomWalker


class AbstractEstimator(object):
    def __init__(self, G):
        self.G = G

    def _edge_weight_func(self, u, v):
        raise NotImplementedError()

    def _node_weight_func(self, u):
        return sum(map(lambda v: self._edge_weight_func(u, v),
                       self.G.neighbors_iter(u)))

    def _compute_metric(self, node, k, t):
        raise NotImplementedError()

    def estimates(self, num_estimates, start_node=None):
        rw = RandomWalker(self.G, self._edge_weight_func)

        if start_node is None:
            start_node = \
                util.pick_highest_weight_node(self.G, self._node_weight_func)

        # Damn, Python 3
        return map(lambda r: self._compute_metric(start_node, r[0], r[1]),
                   rw.return_times(start_node, num_estimates))
