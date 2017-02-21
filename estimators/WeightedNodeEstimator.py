from estimators.AbstractEstimator import AbstractEstimator


class WeightedNodeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        return 1 / self.degrees[u] + 1 / self.degrees[v]

    def _node_weight_func(self, u):
        vs = self.G.neighbors(u)
        return 1 + sum(map(lambda v: 1 / self.degrees[v], vs))

    def _compute_metric(self, node, k, t, accum):
        return t * self._node_weight_func(node) / (2 * k)
