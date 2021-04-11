import numpy as np
from plot_funcs.vs_different_budgets import subplot_scatter_diff_budgets
from utils.common import (
    Optimizers,
    OptimizerSettings,
    plot_target,
    SubplotSettings,
    VisualizerSettings
)


if __name__ == '__main__':
    """
    The shape of results must be (2, n_configurations).
    """
    n_rows, n_cols = 1, 3
    vis_settings = VisualizerSettings(minimize=True, n_rows=n_rows, n_cols=n_cols,
                                      figsize=(10, 4))
    plot_settings = [[
        SubplotSettings(
            legend=True,
            loc="upper left",
            labelleft=(c == 0),
            left=(c == 0),
            labelbottom=(r == n_rows - 1),
            bottom=(r == n_rows - 1)
        ) for c in range(n_cols)
    ] for r in range(n_rows)]

    opts = {}
    dummies = []
    for i in range(3):
        x = np.random.random(100)
        dummies.append(x)

    for r in range(n_rows):
        for c in range(n_cols):
            opts[f"dummy{r}{c}"] = OptimizerSettings(
                name=f"dummy{c % 3} vs dummy{(c + 1) % 3}",
                results=np.array(np.array([dummies[c % 3], dummies[(c + 1) % 3]])),
                color="blue",
                row=r,
                col=c
            )

    all_opts = Optimizers(**opts)

    plot_target(vis_settings=vis_settings,
                all_opts=all_opts,
                plot_settings=plot_settings,
                target_subplot=subplot_scatter_diff_budgets)
