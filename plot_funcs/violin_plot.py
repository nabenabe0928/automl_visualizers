import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Union
from utils.common import (
    Optimizers,
    OptimizerSettings,
    SubplotSettings,
    VisualizerSettings
)


def whisker_values(vals: np.ndarray, q25: Union[float, int], q75: Union[float, int]) \
        -> Tuple[Union[float, int], Union[float, int]]:
    sorted_vals = np.sort(vals)
    upper_val = q75 + (q75 - q25) * 1.5
    upper_val = np.clip(upper_val, q75, sorted_vals[-1])
    lower_val = q25 - (q75 - q25) * 1.5
    lower_val = np.clip(lower_val, sorted_vals[0], q25)

    return lower_val, upper_val


def ax_formatter(ax: plt.Axes, labels: List[str]) -> None:
    ax.xaxis.set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)


def subplot_result(ax: plt.Axes, name: str, opt_settings: OptimizerSettings) -> None:

    results = opt_settings.results

    if not isinstance(results, dict):
        raise ValueError("results must be dict. "
                         f"But got {type(results)}.")

    labels = list(results.keys())

    parts = ax.violinplot(list(results.values()),
                          showmeans=False, showmedians=False,
                          showextrema=False)

    for pc in parts['bodies']:
        pc.set_facecolor(opt_settings.color)
        pc.set_edgecolor('black')
        pc.set_alpha(1)

    q25s, medians, q75s = np.percentile(list(results.values()), [25, 50, 75], axis=1)
    whiskers = np.array([whisker_values(vals, q25, q75)
                         for vals, q25, q75 in zip(results.values(), q25s, q75s)])
    whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

    xs = np.arange(1, len(medians) + 1)
    ax.vlines(xs, q25s, q75s, color="k", linestyle="-", lw=5)
    ax.vlines(xs, whiskers_min, whiskers_max, color="k", linestyle="-", lw=1)
    ax.scatter(xs, medians, marker="o", color="white")

    ax_formatter(ax, labels)


def subplot_violin(ax: plt.Axes,
                   vis_settings: VisualizerSettings,
                   opts: Optimizers,
                   subplot_settings: SubplotSettings) -> None:

    for name, opt_settings in opts.items():

        subplot_result(ax=ax,
                       name=name,
                       opt_settings=opt_settings)
