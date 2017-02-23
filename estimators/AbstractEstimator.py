import util
from random_walker import RandomWalker
import networkx as nx
import scipy as sp
from math import sqrt

class AbstractEstimator(object):
    def __init__(self, G):
        self.G = G
        # Optimisation, avoids calling `degree` all the time.
        # The graph doesn't change anyway, so it's OK to cache degrees.
        self.degrees = {i: self.G.degree(i) for i in self.G.nodes_iter()}

    def _edge_weight_func(self, u, v):
        return 1

    def _node_weight_func(self, u):
        return self.degrees[u]

    def _compute_metric(self, node, k, t, accum):
        raise NotImplementedError()

    def _compute_metric_stddev(self, node, k, t_var):
        """
        Computes variance associated with the metric
        :param node: Node, usually the start node.
        :param k: Number of the return
        :param t_var: First return time variance (Var[T^+u])
        :return: Variance
        """
        raise NotImplementedError()

    def _accum_func(self, u):
        return 0

    def transition_prob(self, u, v):
        return self._edge_weight_func(u, v) / self._node_weight_func(u)

    def transition_matrix(self):
        # At this point it matters that a graph is directed
        G = nx.DiGraph(self.G)
        for u, v, d in G.edges_iter(data=True):
            d['weight'] = self.transition_prob(u, v)
        return nx.adjacency_matrix(G)

    def compute_start_node(self):
        return util.pick_highest_weight_node(self.G, self._node_weight_func)

    def estimates(self, num_estimates, start_node=None):
        rw = RandomWalker(self.G,
                          self._edge_weight_func,
                          self._accum_func)

        if start_node is None:
            start_node = self.compute_start_node()

        # Damn, Python 3
        return map(lambda r: self._compute_metric(start_node, r[0], r[1], r[2]),
                   rw.return_times(start_node, num_estimates))

    def _compute_stat_distr(self, node):
        w_G = sum(self._node_weight_func(i) for i in self.G.nodes_iter())
        return self._node_weight_func(node) / w_G

    def _compute_return_time_variance(self, Zvv, start_node, stat_distr=None):
        if not stat_distr:
            stat_distr = self._compute_stat_distr(start_node)
        return (2 * Zvv + stat_distr - 1) / (stat_distr ** 2)

    def eigenvalue_gap(self):
        A = self.transition_matrix()
        eigenvalues = sorted(sp.sparse.linalg.eigs(A)[0])
        return 1 - eigenvalues[-2].real

    def _deviations(self, Zvv, start_node, stat_distr=None):
        t_var = self._compute_return_time_variance(Zvv, start_node, stat_distr)
        return lambda k: self._compute_metric_stddev(start_node, k, t_var)

    def bound_on_deviation(self, start_node):
        Zvv = 1 / self.eigenvalue_gap()
        return self._deviations(Zvv, start_node)

    def zvv_deviation(self, K, T, start_node):
        stat_distr = self._compute_stat_distr(start_node)
        Zvv = K - T * stat_distr
        print(stat_distr)
        print(Zvv)
        return self._deviations(Zvv, start_node, stat_distr)
