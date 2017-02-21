from estimators.AbstractEstimator import AbstractEstimator


class NodeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimisation, avoids calling `degree` all the time.
        # The graph doesn't change anyway, so it's OK to cache degrees.
        self.degrees = {i: self.G.degree(i) for i in self.G.nodes_iter()}

    def _edge_weight_func(self, u, v):
        return 1 / self.degrees[u] + 1 / self.degrees[v]

    def _node_weight_func(self, u):
        vs = self.G.neighbors(u)
        return 1 + sum(map(lambda v: 1 / self.degrees[v], vs))

    def _compute_metric(self, node, k, t):
        return t * self._node_weight_func(node) / (2 * k)
