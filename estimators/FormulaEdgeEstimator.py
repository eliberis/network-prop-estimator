from estimators.AbstractEstimator import AbstractEstimator
from math import sqrt


class FormulaEdgeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _accum_func(self, u):
        return 1

    def _compute_metric(self, node, k, t, accum):
        return accum / (2 * k) * self._node_weight_func(node)

    def _compute_metric_stddev(self, node, k, t_var):
        return (self._node_weight_func(node) / 2) * sqrt(t_var / k)
