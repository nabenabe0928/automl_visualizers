import numpy as np
import matplotlib.pyplot as plt
from utils.attr_dict import AttrDict
from typing import List, Optional, Tuple


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 18


class OptimizerSettings(AttrDict):
    """
    Args:
        results (np.ndarray):
            the shape of (n_trials, n_iterations).
            results[i][j] := the performance metric at
                             the j-th iteration of the i-th trial
        name (str): The name used for the legend
        row (int):
            the index for the row in subplots
        col (int):
            the index for the column in subplots
        color (str): the color of the plot
        marker (str): the marker of the plot
    """
    results: np.ndarray
    name: str
    color: str
    row: int = 0
    col: int = 0
    marker: Optional[str] = None


class VisualizerSettings(AttrDict):
    """
    Args:
        minimize (bool):
            if minimization problem, True
        n_rows (int):
            the number of rows in subplots
        n_cols (int):
            the number of columns in subplots
        width_ratios (List[int]):
            the width ratios of each subplot
            The shape must be (n_cols)
        height_ratios (List[int]):
            the height ratios of each subplot
            The shape must be (n_rows)
        wspace (float):
            Adapt how much we reduce the margin
            between each col
        hspace (float):
            Adapt how much we reduce the margin
            between each row
        standard_error (bool):
            if True, use standard error
            otherwise, use standard deviation
        grid (bool):
            if writing grid lines
        log_scale (bool):
            if using log scale
        save (bool):
            if saving as PDF
        figsize (Optional[Tuple[int, int]]):
            The figure size
        title (Optional[str]):
            the title of the figure.
            If None, do not put the title
    """
    minimize: bool = True
    n_rows: int = 1
    n_cols: int = 1
    width_ratios: List[int] = None
    height_ratios: List[int] = None
    wspace: float = 0.025
    hspace: float = 0.05
    standard_error: bool = False
    grid: bool = True
    log_scale: bool = False
    save: bool = False
    figsize: Optional[Tuple[int, int]] = None
    title: Optional[str] = None


class SubplotSettings(AttrDict):
    """
    Args:
        legend (bool):
            if adding legend
        labelleft (bool):
            if showing the value for x-axis
        left (bool):
            if showing the tick for x-axis
        labelbottom (bool):
            if showing the value for y-axis
        bottom (bool):
            if showing the tick for y-axis
        xlim (Optional[Tuple[float, float]]):
            the range of x axis
        ylim (Optional[Tuple[float, float]]):
            the range of y axis
        xlabel (Optional[str]):
            the xlabel of the figure.
            If None, do not put the xlabel
        ylabel (Optional[str]):
            the ylabel of the figure.
            If None, do not put the ylabel
    """
    legend: bool = True
    labelleft: bool = True
    left: bool = True
    labelbottom: bool = True
    bottom: bool = True
    xlim: Optional[Tuple[float, float]] = None
    ylim: Optional[Tuple[float, float]] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None


PlotSettings = List[List[SubplotSettings]]


class Optimizers(AttrDict):
    # opt1_name: OptimizerArgs
    # opt2_name: OptimizerArgs
    ...


def subplot_result(ax: plt.Axes, name: str, minimize: bool, opt_settings: OptimizerSettings) -> None:

    results = opt_settings.results
    if len(results.shape) != 2:
        raise ValueError("The shape of results must be (n_trials, n_iterations). "
                         f"However, got the shape {results.shape}.")

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


def subplot_setter(ax: plt.Axes,
                   vis_settings: VisualizerSettings,
                   subplot_settings: SubplotSettings) -> None:
    tick_params = {
        "labelleft": subplot_settings.labelleft,
        "left": subplot_settings.left,
        "labelbottom": subplot_settings.labelbottom,
        "bottom": subplot_settings.bottom
    }

    ax.tick_params(**tick_params)

    if subplot_settings.xlabel is not None:
        ax.set_xlabel(subplot_settings.xlabel)
    if subplot_settings.ylabel is not None:
        ax.set_ylabel(subplot_settings.ylabel)
    if subplot_settings.xlim is not None:
        ax.set_xlim(subplot_settings.xlim)
    if subplot_settings.ylim is not None:
        ax.set_ylim(subplot_settings.ylim)
    if subplot_settings.legend:
        ax.legend()
    if vis_settings.grid:
        ax.grid()
    if vis_settings.log_scale:
        ax.set_yscale("log")


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
                             f"However, got {opt_settings.results.shape} in {name}.")
        subplot_result(ax=ax,
                       name=name,
                       minimize=minimize,
                       opt_settings=opt_settings)

    subplot_setter(ax, vis_settings, subplot_settings)


def plot_iteration_vs_performance(vis_settings: VisualizerSettings,
                                  all_opts: Optimizers,
                                  plot_settings: PlotSettings) -> None:

    n_rows, n_cols = vis_settings.n_rows, vis_settings.n_cols

    if len(plot_settings) != n_rows or len(plot_settings[0]) != n_cols:
        raise ValueError(f"The shape of plot_settings must match ({n_rows}, {n_cols}). "
                         f"But got ({len(plot_settings)}, {len(plot_settings[0])})")

    gridspec_kw = {"width_ratios": vis_settings.width_ratios,
                   "height_ratios": vis_settings.height_ratios,
                   "hspace": vis_settings.hspace,
                   "wspace": vis_settings.wspace}

    fig, axes = plt.subplots(n_rows, n_cols, squeeze=False,
                             gridspec_kw=gridspec_kw, figsize=vis_settings.figsize)

    for r in range(n_rows):
        for c in range(n_cols):
            subplot_settings = plot_settings[r][c]
            opts = Optimizers(**{
                name: opt for name, opt in all_opts.items()
                if opt.row == r and opt.col == c
            })
            subplot_iteration_vs_performance(ax=axes[r][c],
                                             vis_settings=vis_settings,
                                             opts=opts,
                                             subplot_settings=subplot_settings)

    if vis_settings.title is not None:
        plt.title(vis_settings.title)

    if vis_settings.save:
        plt.tight_layout()
        plt.savefig(f"fig/{vis_settings.fig_name}.pdf")
    else:
        plt.show()


if __name__ == '__main__':
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

    plot_iteration_vs_performance(vis_settings=vis_settings,
                                  all_opts=all_opts,
                                  plot_settings=plot_settings)
