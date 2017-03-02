import numpy as np
import networkx as nx
from matplotlib.ticker import ScalarFormatter, FuncFormatter
import matplotlib.pyplot as plt
from math import log
import os.path
import pickle


def produce_plot(G, est_class, true_val,
                 num_estimators=10, num_estimates=12000,
                 est_quant_name='Estimated quantity',
                 mixing_time=570,
                 *est_args, **est_kwargs):
    """
    Plot estimates of a property as a function of returns.
    :param G: The graph
    :param est_class: Estimator class for a property
    :param true_val: Known true value of the property
    :param num_estimators: Number of walks to run
    :param num_estimates: Number of estimates for each walker to produce
    :param est_quant_name: The name of the estimated quantity (axis title)
    :param mixing_time: Mixing time for the walk
    :param est_args: Additional arguments for an estimator
    :param est_kwargs: Additional arguments for an estimator
    :return:
    """

    result_file_name = "{0}_{1}x{2}.p".format(est_class.__name__,
                                              num_estimators, num_estimates)

    est = est_class(G, *est_args, **est_kwargs)
    # All `num_estimators` estimators share this cache.
    ew_cache, nw_cache = est.compute_weight_caches()

    # Walk results are pickled for quick access next time
    if os.path.exists(result_file_name):
        with open(result_file_name, "rb") as f:
            to_load = pickle.load(f)
        results = to_load["results"]
        start_node = to_load["start_node"]
        tvar_bound = to_load["tvar_bound"]
        tvar_estim = to_load["tvar_estim"]
    else:
        start_node = est.compute_start_node()  # Reuse start_node for efficiency
        results = np.zeros((num_estimators, num_estimates), dtype=np.float32)
        returns = np.zeros((num_estimators, num_estimates), dtype=np.uint64)

        for i in range(num_estimators):
            est = est_class(G,
                            node_weight_cache=nw_cache,
                            edge_weight_cache=ew_cache,
                            *est_args, **est_kwargs)
            estims = est.estimates(num_estimates, start_node=start_node)
            print("Walking {0} out of {1}...".format(i + 1, num_estimators))
            for j, val, t in estims:
                results[i, j] = val
                returns[i, j] = t

        print("Estimating bounds...")
        t = mixing_time * log(nx.number_of_nodes(G))
        select_fn = np.vectorize(lambda x: x <= t, otypes=[np.bool])
        y_t = np.sum(select_fn(returns)) / returns.size

        stat_distr = est.stat_distr(start_node)
        tvar_bound = est.tvar_zvv_bound(stat_distr)
        tvar_estim = est.tvar_zvv_estimate(t, y_t, stat_distr)

        to_save = {"results": results,
                   "return_times": returns,
                   "start_node": start_node,
                   "tvar_bound": tvar_bound,
                   "tvar_estim": tvar_estim}

        with open(result_file_name, "wb") as f:
            pickle.dump(to_save, f)

    bound_func = est.deviations(tvar_bound, start_node)
    dev_est_func = est.deviations(tvar_estim, start_node)

    figure_name = est_class.__name__ + ".png"

    x = np.arange(1, num_estimates+1)

    # Compute mean and std-dev across all walkers
    y_mean = np.mean(results, axis=0)
    y_std = np.std(results, axis=0)

    # Plot estimates
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    for i in range(num_estimators):
        ax.semilogx(x, results[i, :], '.',
                    color='grey', alpha=0.1, markersize=1)

    # Plot ground truth
    ax.axhline(y=true_val, color='r', linestyle='-')

    # Plot experiments' average and deviation
    nice_blue = '#4286f4'
    ax.semilogx(x, y_mean, color=nice_blue)
    ax.semilogx(x, y_mean - y_std, color=nice_blue, alpha=0.3)
    ax.semilogx(x, y_mean + y_std, color=nice_blue, alpha=0.3)

    # Plot bounds on deviation
    l_green = '#9bcca9'
    y_dev_bound = np.array([bound_func(k) for k in x])
    ax.semilogx(x, true_val + y_dev_bound, color=l_green, linestyle='dashdot')
    ax.semilogx(x, true_val - y_dev_bound, color=l_green, linestyle='dashdot')

    # Plot estimated Zvv deviation
    l_purple = '#e899ff'
    y_dev_bound = np.array([dev_est_func(k) for k in x])
    ax.semilogx(x, true_val + y_dev_bound, color=l_purple, linestyle='dashed')
    ax.semilogx(x, true_val - y_dev_bound, color=l_purple, linestyle='dashed')

    # Axis formatting
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: '%1.1fM' % (x*1e-6)))
    plt.axis([1, num_estimates, true_val-0.5*y_std[0], true_val+0.5*y_std[0]])
    plt.xlabel('k = Number of returns')
    plt.ylabel(est_quant_name)

    fig.savefig(figure_name)
