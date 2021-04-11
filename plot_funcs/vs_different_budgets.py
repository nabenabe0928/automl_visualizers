import numpy as np
import matplotlib.pyplot as plt
from utils.common import (
    Optimizers,
    OptimizerSettings,
    SubplotSettings,
    VisualizerSettings
)


def subplot_result(ax: plt.Axes, name: str, opt_settings: OptimizerSettings) -> None:

    results = opt_settings.results
    if len(results.shape) != 2 or results.shape[0] != 2:
        """
        The shape of results must be (2, n_configurations).
        results[:][j] := the performance metric of the j-th configuration
        """
        raise ValueError("The shape of results must be (2, n_configurations). "
                         f"But got the shape {results.shape}.")
    if not isinstance(results, np.ndarray):
        raise ValueError("results must be np.ndarray. "
                         f"But got {type(results)}.")

    corr = np.corrcoef(results)
    ax.scatter(results[0], results[1],
               color=opt_settings.color, s=opt_settings.s,
               marker=opt_settings.marker,
               label=f"{opt_settings.name}: $\\rho$ = {corr[0, 1]:.2f}")


def subplot_scatter_diff_budgets(ax: plt.Axes,
                                 vis_settings: VisualizerSettings,
                                 opts: Optimizers,
                                 subplot_settings: SubplotSettings) -> None:

    if len(opts) != 1:
        raise ValueError(f"len(opts) must be 1. But got {len(opts)}")

    for name, opt_settings in opts.items():
        subplot_result(ax=ax,
                       name=name,
                       opt_settings=opt_settings)
