from estimators.AbstractEstimator import AbstractEstimator


class FormulaNodeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _accum_func(self, u):
        return 1 / self.degrees[u]

    def _compute_metric(self, node, k, t, accum):
        return accum / k * self._node_weight_func(node)

    def _compute_metric_stddev(self, node, k, t_var):
        return float('inf')  # Not supported
