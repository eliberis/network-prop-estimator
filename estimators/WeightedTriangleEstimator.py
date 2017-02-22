from estimators.AbstractEstimator import AbstractEstimator
from util import edge_triangles, node_triangles

class WeightedTriangleEstimator(AbstractEstimator):
    def __init__(self, *args, num_edges, **kwargs):
        self.num_edges = num_edges
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        return 1 + edge_triangles(self.G, u, v)

    def _node_weight_func(self, u):
        return self.degrees[u] + 2 * node_triangles(self.G, u)

    def _compute_metric(self, node, k, t, accum):
        return max(0, t * self._node_weight_func(node) / (6 * k) -
                      self.num_edges / 3)
