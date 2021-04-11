import numpy as np
import matplotlib.pyplot as plt
from utils.common import (
    Optimizers,
    OptimizerSettings,
    subplot_setter,
    SubplotSettings,
    VisualizerSettings
)


def subplot_result(ax: plt.Axes, name: str, minimize: bool, opt_settings: OptimizerSettings) -> None:

    results = opt_settings.results
    if len(results.shape) != 2:
        """
        The shape of results must be (n_trials, n_iterations).
        results[i][j] := the performance metric at
                         the j-th iteration of the i-th trial
        """
        raise ValueError("The shape of results must be (n_trials, n_iterations). "
                         f"But got the shape {results.shape}.")
    if not isinstance(results, np.ndarray):
        raise ValueError("results must be np.ndarray. "
                         f"But got {type(results)}.")

    iterations = np.arange(1, results.shape[1] + 1)

    if minimize:
        cumulative = np.minimum.accumulate(results, axis=-1)
    else:
        cumulative = np.maximum.accumulate(results, axis=-1)

    mean = cumulative.mean(axis=0)
    std = cumulative.std(axis=0)

    ax.plot(iterations, mean, color=opt_settings.color,
            marker=opt_settings.marker,
            label=f"{opt_settings.name}: $\\mu \\pm \\sigma$")
    ax.fill_between(iterations, mean - std, mean + std,
                    color=opt_settings.color, alpha=0.2)


def subplot_iteration_vs_performance(ax: plt.Axes,
                                     vis_settings: VisualizerSettings,
                                     opts: Optimizers,
                                     subplot_settings: SubplotSettings) -> None:

    shape, minimize = None, vis_settings.minimize

    for name, opt_settings in opts.items():

        if shape is None:
            shape = opt_settings.results.shape
        if shape != opt_settings.results.shape:
            raise ValueError("The shape for all the results must be identical. "
                             f"But got {opt_settings.results.shape} in {name}.")
        subplot_result(ax=ax,
                       name=name,
                       minimize=minimize,
                       opt_settings=opt_settings)

    subplot_setter(ax, vis_settings, subplot_settings)
