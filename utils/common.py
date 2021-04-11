from utils.attr_dict import AttrDict
import numpy as np
from typing import Callable, List, Optional, Tuple
import matplotlib.pyplot as plt


class OptimizerSettings(AttrDict):
    """
    Args:
        results (np.ndarray): The shape is visualization dependent
        name (str): The name used for the legend
        row (int):
            the index for the row in subplots
        col (int):
            the index for the column in subplots
        color (str): the color of the plot
        marker (str): the marker of the plot
        s (int): the size of marker
    """
    results: np.ndarray
    name: str
    color: str
    row: int = 0
    col: int = 0
    marker: Optional[str] = None
    s: Optional[int] = None


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
    width_ratios: Optional[List[int]] = None
    height_ratios: Optional[List[int]] = None
    wspace: float = 0.025
    hspace: float = 0.05
    standard_error: bool = False
    grid: bool = True
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
        loc (str):
            The location of the legend either of the followings:
            "upper left", "upper right", "lower left", "lower right"
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
        log_scale (bool):
            if using log scale
    """
    legend: bool = True
    labelleft: bool = True
    left: bool = True
    labelbottom: bool = True
    bottom: bool = True
    loc: Optional[str] = None
    xlim: Optional[Tuple[float, float]] = None
    ylim: Optional[Tuple[float, float]] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    log_scale: bool = False


class Optimizers(AttrDict):
    # opt1_name: OptimizerSettings
    # opt2_name: OptimizerSettings
    ...


PlotSettings = List[List[SubplotSettings]]
SubplotFunc = Callable[[plt.Axes,
                        VisualizerSettings,
                        OptimizerSettings,
                        SubplotSettings], None]


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
        ax.legend(loc=subplot_settings.loc)
    if vis_settings.grid:
        ax.grid()
    if subplot_settings.log_scale:
        ax.set_yscale("log")


def plot_target(vis_settings: VisualizerSettings,
                all_opts: Optimizers,
                plot_settings: PlotSettings,
                target_subplot: SubplotFunc) -> None:

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
            target_subplot(ax=axes[r][c],
                           vis_settings=vis_settings,
                           opts=opts,
                           subplot_settings=subplot_settings)

            subplot_setter(axes[r][c], vis_settings, subplot_settings)

    if vis_settings.title is not None:
        plt.title(vis_settings.title)

    if vis_settings.save:
        plt.tight_layout()
        plt.savefig(f"fig/{vis_settings.fig_name}.pdf")
    else:
        plt.show()
