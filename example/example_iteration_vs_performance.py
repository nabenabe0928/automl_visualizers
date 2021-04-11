import numpy as np
from plot_funcs.iteration_vs_performance import subplot_iteration_vs_performance
from utils.common import (
    Optimizers,
    OptimizerSettings,
    plot_target,
    SubplotSettings,
    VisualizerSettings
)


if __name__ == '__main__':
    """
    The shape of results must be (n_trials, n_iterations).
    results[i][j] := the performance metric at
                     the j-th iteration of the i-th trial
    """
    shape = (2, 100)
    n_rows, n_cols = 2, 2
    vis_settings = VisualizerSettings(minimize=True, n_rows=n_rows, n_cols=n_cols,
                                      height_ratios=[3, 1], width_ratios=[3, 1], figsize=(10, 4))
    plot_settings = [[
        SubplotSettings(
            legend=(c == 0 and r == 0),
            labelleft=(c == 0),
            left=(c == 0),
            labelbottom=(r == n_rows - 1),
            bottom=(r == n_rows - 1)
        ) for c in range(n_cols)
    ] for r in range(n_rows)]

    opts = {}

    colors = ["red", "green", "blue", "purple"]

    for r in range(n_rows):
        for c in range(n_cols):
            for i in range(4):
                opts[f"dummy{i}{r}{c}"] = OptimizerSettings(
                    name=f"dummy{i}",
                    results=np.random.random((5, shape[1])),
                    color=colors[i],
                    row=r,
                    col=c
                )

    all_opts = Optimizers(**opts)

    plot_target(vis_settings=vis_settings,
                all_opts=all_opts,
                plot_settings=plot_settings,
                target_subplot=subplot_iteration_vs_performance)
