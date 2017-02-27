import networkx as nx
import scipy as sp
from math import log
import util
from random_walker import RandomWalker


class AbstractEstimator(object):
    def __init__(self, G,  edge_weight_cache=None, node_weight_cache=None):
        self.G = G
        # Optimisation, avoids calling `degree` all the time.
        # The graph doesn't change anyway, so it's OK to cache.
        self.ew_cache = edge_weight_cache
        self.nw_cache = node_weight_cache
        self.degrees = {i: self.G.degree(i) for i in self.G.nodes_iter()}

    def _edge_weight_func(self, u, v):
        return 1

    def _node_weight_func(self, u):
        return self.degrees[u]

    def _cached_edge_weight(self, u, v):
        return self.ew_cache[(u, v)] \
            if self.ew_cache else self._edge_weight_func(u, v)

    def _cached_node_weight(self, u):
        return self.nw_cache[u] if self.nw_cache else self._node_weight_func(u)

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

    def compute_weight_caches(self):
        ew_cache = {}
        for u, v in self.G.edges_iter():
            val = self._edge_weight_func(u, v)
            ew_cache[(u, v)] = val
            ew_cache[(v, u)] = val

        nw_cache = {}
        for u in self.G.nodes_iter():
            nw_cache[u] = self._node_weight_func(u)

        return ew_cache, nw_cache

    def transition_prob(self, u, v):
        return self._cached_edge_weight(u, v) / self._cached_node_weight(v)

    def transition_matrix(self):
        # At this point it matters that a graph is directed
        G = nx.DiGraph(self.G)
        for u, v, d in G.edges_iter(data=True):
            d['weight'] = self.transition_prob(u, v)
        return nx.adjacency_matrix(G)

    def compute_start_node(self):
        return util.pick_highest_weight_node(self.G, self._cached_node_weight)

    def estimates(self, num_estimates, start_node=None):
        rw = RandomWalker(self.G,
                          self._edge_weight_func,
                          self._accum_func)

        if start_node is None:
            start_node = self.compute_start_node()

        prev_t = 0
        for k, t, accum in rw.return_times(start_node, num_estimates):
            met = self._compute_metric(start_node, k, t, accum)
            yield k - 1, met, t - prev_t
            prev_t = t

    def stat_distr(self, node):
        w_G = sum(self._cached_node_weight(i) for i in self.G.nodes_iter())
        return self._cached_node_weight(node) / w_G

    def _compute_return_time_variance(self, Zvv, stat_distr):
        return (2 * Zvv + stat_distr - 1) / (stat_distr ** 2)

    def tvar_zvv_bound(self, stat_distr):
        A = self.transition_matrix()
        eigenvalues = sorted(sp.sparse.linalg.eigs(A)[0])
        Zvv = 1 / (1 - eigenvalues[-2].real)
        return self._compute_return_time_variance(Zvv, stat_distr)

    def tvar_zvv_estimate(self, t, y_t, stat_distr):
        Zvv = -t * stat_distr / log(1 - y_t)
        return self._compute_return_time_variance(Zvv, stat_distr)

    def deviations(self, t_var, start_node):
        return lambda k: self._compute_metric_stddev(start_node, k, t_var)
