from estimators.abstract_estimator import AbstractEstimator
from util import edge_triangles, node_triangles
from math import sqrt


class WeightedTriangleEstimator(AbstractEstimator):
    def __init__(self, *args, num_edges, C=1, **kwargs):
        self.num_edges = num_edges
        self.C = C
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        if self.ew_cache:
            return self.ew_cache[(u, v)]
        return 1 + self.C * edge_triangles(self.G, u, v)

    def _node_weight_func(self, u):
        if self.nw_cache:
            return self.nw_cache[u]
        return self.degrees[u] + self.C * 2 * node_triangles(self.G, u)

    def _compute_metric(self, node, k, t, accum):
        return 1 / self.C * max(0, t * self._node_weight_func(node) / (6 * k) -
                                self.num_edges / 3)

    def _compute_metric_stddev(self, node, k, t_var):
        # Ignore the 0 case of `max`
        return (self._node_weight_func(node) / (6 * self.C)) * sqrt(t_var / k)
