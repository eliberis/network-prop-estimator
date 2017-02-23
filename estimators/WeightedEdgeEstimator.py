from estimators.AbstractEstimator import AbstractEstimator
from math import sqrt


class WeightedEdgeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _edge_weight_func(self, u, v):
        return 1

    def _node_weight_func(self, u):
        return self.degrees[u]

    def _compute_metric(self, node, k, t, accum):
        return t * self._node_weight_func(node) / (2 * k)

    def _compute_metric_stddev(self, node, k, t_var):
        return (self._node_weight_func(node) / 2) * sqrt(t_var / k)
