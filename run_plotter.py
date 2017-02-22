import numpy as np
from matplotlib.ticker import ScalarFormatter, FuncFormatter
import matplotlib.pyplot as plt
import os.path

def produce_plot(G, est_class,
                 num_estimators=10, num_estimates=12000,
                 true_val=None,
                 est_quant_name='Estimated quantity',
                 *est_args, **est_kwargs):

    result_file_name = "{0}_{1}x{2}.npy".format(est_class.__name__,
                                                num_estimators, num_estimates)

    est = est_class(G, *est_args, **est_kwargs)
    # TODO: zvv_bound = 1 / util.eigenvalue_gap(...)

    if os.path.exists(result_file_name):
        results = np.load(result_file_name)
    else:
        results = np.zeros((num_estimators, num_estimates), dtype=np.float32)
        start_node = est.compute_start_node()  # Reuse start_node for efficiency

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

    if true_val:
        ax.axhline(y=true_val, color='r', linestyle='-')

    nice_blue = '#4286f4'
    ax.semilogx(x, y_mean, color=nice_blue)
    ax.semilogx(x, y_mean - y_std, color=nice_blue, alpha=0.3)
    ax.semilogx(x, y_mean + y_std, color=nice_blue, alpha=0.3)

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: '%1.1fM' % (x*1e-6)))

    mid = true_val if true_val else y_mean[0]
    plt.axis([1, num_estimates, mid-0.5*y_std[0], mid+0.5*y_std[0]])
    plt.xlabel('k = Number of returns')
    plt.ylabel(est_quant_name)
    fig.savefig(figure_name)
