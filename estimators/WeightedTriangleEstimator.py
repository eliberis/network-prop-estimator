from estimators.AbstractEstimator import AbstractEstimator


class WeightedTriangleEstimator(AbstractEstimator):
    def __init__(self, *args, num_edges, **kwargs):
        self.num_edges = num_edges
        super().__init__(*args, **kwargs)

    def triangles(self, u, v):
        common_neigh = \
            filter(lambda n: self.G.has_edge(n, u), self.G.neighbors_iter(v))
        return len(list(common_neigh))

    def _edge_weight_func(self, u, v):
        return 1 + self.triangles(u, v)

    def _compute_metric(self, node, k, t):
        return max(0, t * self._node_weight_func(node) / (6 * k) -
                      self.num_edges / 3)
