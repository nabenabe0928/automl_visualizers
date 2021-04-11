import numpy as np
from plot_funcs.violin_plot import subplot_violin
from utils.common import (
    Optimizers,
    OptimizerSettings,
    SubplotSettings,
    plot_target,
    VisualizerSettings
)


if __name__ == '__main__':
    """
    results must be Dict[str, np.ndarray].
    """
    n_rows, n_cols = 1, 1
    vis_settings = VisualizerSettings(n_rows=n_rows, n_cols=n_cols,
                                      figsize=(10, 2), grid=False)
    plot_settings = [[
        SubplotSettings(
            legend=False,
            bottom=False,
        ) for c in range(n_cols)
    ] for r in range(n_rows)]

    opts = {}
    dummies = {
        "uniform": np.random.random(100),
        "normal": np.random.normal(size=100),
        "multi-modal": np.r_[np.random.normal(loc=3, size=50), np.random.normal(loc=-3, size=50)]
    }

    for r in range(n_rows):
        for c in range(n_cols):
            opts[f"dummy{r}{c}"] = OptimizerSettings(
                name="dummy",
                results=dummies,
                color="red",
                row=r,
                col=c
            )

    all_opts = Optimizers(**opts)

    plot_target(vis_settings=vis_settings,
                all_opts=all_opts,
                plot_settings=plot_settings,
                target_subplot=subplot_violin)
