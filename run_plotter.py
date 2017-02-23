import numpy as np
from matplotlib.ticker import ScalarFormatter, FuncFormatter
import matplotlib.pyplot as plt
import os.path

def produce_plot(G, est_class, true_val,
                 num_estimators=10, num_estimates=12000,
                 est_quant_name='Estimated quantity',
                 *est_args, **est_kwargs):

    result_file_name = "{0}_{1}x{2}.npy".format(est_class.__name__,
                                                num_estimators, num_estimates)

    est = est_class(G, *est_args, **est_kwargs)
    start_node = est.compute_start_node()  # Reuse start_node for efficiency
    bound_func = est.bound_on_deviation(start_node)
    max_T = 7979
    zvv_dev_func = est.zvv_deviation(num_estimates, max_T, start_node)

    if os.path.exists(result_file_name):
        results = np.load(result_file_name)
    else:
        results = np.zeros((num_estimators, num_estimates), dtype=np.float32)

        for i in range(num_estimators):
            est = est_class(G, *est_args, **est_kwargs)
            estims = est.estimates(num_estimates, start_node=start_node)
            print("Walking {0} out of {1}...".format(i + 1, num_estimators))
            for j, val in enumerate(estims):
                results[i, j] = val

        np.save(result_file_name, results)

    figure_name = est_class.__name__ + ".png"

    x = np.arange(1, num_estimates+1)
    y_mean = np.mean(results, axis=0)
    y_std = np.std(results, axis=0)

    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    for i in range(num_estimators):
        ax.semilogx(x, results[i, :], '.',
                    color='grey', alpha=0.1, markersize=1)

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
    y_dev_bound = np.array([bound_func(k) for k in x])
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
