from estimators.AbstractEstimator import AbstractEstimator


class WeightedEdgeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        return 1

    def _node_weight_func(self, u):
        return self.G.degree(u)

    def _compute_metric(self, node, k, t):
        return t * self._node_weight_func(node) / (2 * k)
