from estimators.AbstractEstimator import AbstractEstimator


class FormulaNodeEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _node_weight_func(self, u):
        return self.degrees[u]

    def _accum_func(self, u):
        return 1 / self.degrees[u]

    def _compute_metric(self, node, k, t, accum):
        return accum / k * self._node_weight_func(node)
