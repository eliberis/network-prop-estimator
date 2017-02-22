from estimators.AbstractEstimator import AbstractEstimator
from util import node_triangles
from functools import lru_cache

class FormulaTriangleEstimator(AbstractEstimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @lru_cache(maxsize=None)
    def _accum_func(self, u):
        return node_triangles(self.G, u) / self.degrees[u]

    def _compute_metric(self, node, k, t, accum):
        return accum / (2 * 3 * k) * self._node_weight_func(node)
