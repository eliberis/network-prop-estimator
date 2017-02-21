from estimators.AbstractEstimator import AbstractEstimator


class NodeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        return 1 / self.G.degree(u) + 1 / self.G.degree(v)

    def _node_weight_func(self, u):
        vs = self.G.neighbors(u)
        return 1 + sum(map(lambda v: 1 / self.G.degree(v), vs))

    def _compute_metric(self, node, k, t):
        return t * self._node_weight_func(node) / (2 * k)
