from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.transforms import blended_transform_factory
import numpy as np


from .preparation import PreparedBarData
_UNSET = object()

class BarPlotter:
    def __init__(self, output_dir: str | Path | None = None):
        self.output_dir = Path(output_dir) if output_dir is not None else None
         # ---- Styling ----
        matplotlib.rcParams["font.family"] = "sans-serif"
        matplotlib.rcParams["font.sans-serif"] = "Arial"

    @staticmethod
    def _cm_to_inches(size_cm: Sequence[float]) -> tuple[float, float]:
        return float(size_cm[0]) / 2.54, float(size_cm[1]) / 2.54

    @staticmethod
    def _validate_label_col(group_cols: list[str], col: str | None) -> str | None:
        if col is None:
            return None
        return col if col in group_cols else None

    @staticmethod
    def _build_grouped_positions(
        index_frame,
        gap_by: str | None = None,
        gap_size: float = 0.8,
    ) -> np.ndarray:
        if gap_by is None or gap_by not in index_frame.columns or len(index_frame) == 0:
            return np.arange(len(index_frame), dtype=float)

        positions: list[float] = []
        pos = 0.0
        prev = None

        for _, row in index_frame.iterrows():
            current = row[gap_by]
            if prev is not None and current != prev:
                pos += gap_size
            positions.append(pos)
            pos += 1.0
            prev = current

        return np.asarray(positions, dtype=float)

    @staticmethod
    def _group_centers(index_frame, positions: np.ndarray, colname: str) -> list[tuple[object, float]]:
        if colname not in index_frame.columns or len(index_frame) == 0:
            return []

        values = index_frame[colname].tolist()
        centers: list[tuple[object, float]] = []
        start = 0

        for i in range(1, len(values) + 1):
            if i == len(values) or values[i] != values[start]:
                center = float(np.mean(positions[start:i]))
                centers.append((values[start], center))
                start = i

        return centers

    @staticmethod
    def _group_boundaries(index_frame, positions: np.ndarray, group_col: str | None) -> list[float]:
        if group_col is None or group_col not in index_frame.columns or len(index_frame) <= 1:
            return []

        values = index_frame[group_col].tolist()
        boundaries: list[float] = []

        for i in range(1, len(values)):
            if values[i] != values[i - 1]:
                boundaries.append((positions[i - 1] + positions[i]) / 2)

        return boundaries

    def _draw_group_separators(
        self,
        ax: plt.Axes,
        index_frame,
        positions: np.ndarray,
        *,
        group_col: str | None,
        orientation: str,
        enabled: bool,
    ) -> None:
        if not enabled:
            return

        for boundary in self._group_boundaries(index_frame, positions, group_col):
            if orientation == "horizontal":
                ax.axhline(boundary, color="gray", linestyle="dashed", linewidth=0.8, zorder=0)
            else:
                ax.axvline(boundary, color="gray", linestyle="dashed", linewidth=0.8, zorder=0)

    def _draw_horizontal_labels(
        self,
        ax: plt.Axes,
        index_frame,
        positions: np.ndarray,
        *,
        left_inner_label_col: str | None,
        left_outer_label_col: str | None,
        right_inner_label_col: str | None,
        right_outer_label_col: str | None,
    ) -> None:
        trans = blended_transform_factory(ax.transAxes, ax.transData)

        ax.set_yticks([])
        ax.tick_params(axis="y", length=0)

        if left_inner_label_col and left_inner_label_col in index_frame.columns:
            for value, y in zip(index_frame[left_inner_label_col], positions):
                ax.text(
                    -0.02,
                    y,
                    str(value),
                    transform=trans,
                    ha="right",
                    va="center",
                )

        if left_outer_label_col and left_outer_label_col in index_frame.columns:
            for value, y in self._group_centers(index_frame, positions, left_outer_label_col):
                ax.text(
                    -0.18,
                    y,
                    str(value),
                    transform=trans,
                    ha="right",
                    va="center",
                )

        right_inner_x = 1.005
        right_outer_x = 1.015

        if right_inner_label_col and right_inner_label_col in index_frame.columns:
            for value, y in zip(index_frame[right_inner_label_col], positions):
                ax.text(
                    right_inner_x,
                    y,
                    str(value),
                    transform=trans,
                    ha="left",
                    va="center",
                )

        if right_outer_label_col and right_outer_label_col in index_frame.columns:
            for value, y in self._group_centers(index_frame, positions, right_outer_label_col):
                ax.text(
                    right_outer_x,
                    y,
                    str(value),
                    transform=trans,
                    ha="left",
                    va="center",
                )

    def _draw_vertical_labels(
        self,
        ax: plt.Axes,
        index_frame,
        positions: np.ndarray,
        *,
        bottom_inner_label_col: str | None,
        bottom_outer_label_col: str | None,
        top_inner_label_col: str | None,
        top_outer_label_col: str | None,
        bottom_inner_rotation: float = 90,
        top_inner_rotation: float = 0,
    ) -> None:
        trans = blended_transform_factory(ax.transData, ax.transAxes)

        ax.set_xticks([])
        ax.tick_params(axis="x", length=0)

        if bottom_inner_label_col and bottom_inner_label_col in index_frame.columns:
            for value, x in zip(index_frame[bottom_inner_label_col], positions):
                ax.text(
                    x,
                    -0.02,
                    str(value),
                    transform=trans,
                    ha="right" if bottom_inner_rotation else "center",
                    va="top",
                    rotation=bottom_inner_rotation,
                )

        if bottom_outer_label_col and bottom_outer_label_col in index_frame.columns:
            for value, x in self._group_centers(index_frame, positions, bottom_outer_label_col):
                ax.text(
                    x,
                    -0.1,
                    str(value),
                    transform=trans,
                    ha="center",
                    va="top",
                )

        if top_inner_label_col and top_inner_label_col in index_frame.columns:
            for value, x in zip(index_frame[top_inner_label_col], positions):
                ax.text(
                    x,
                    1.02,
                    str(value),
                    transform=trans,
                    ha="center",
                    va="bottom",
                    rotation=top_inner_rotation,
                )

        if top_outer_label_col and top_outer_label_col in index_frame.columns:
            for value, x in self._group_centers(index_frame, positions, top_outer_label_col):
                ax.text(
                    x,
                    1.10,
                    str(value),
                    transform=trans,
                    ha="center",
                    va="bottom",
                )

    @staticmethod
    def _plot_stacked(
        ax: plt.Axes,
        df,
        positions: np.ndarray,
        stacks: list[str],
        colors: Mapping[str, str],
        signed: bool,
        orientation: str,
        bar_size: float,
        legend_labels: Mapping[str, str] | None = None,
    ) -> None:
        pos_base = np.zeros(len(df))
        neg_base = np.zeros(len(df))

        for stack in stacks:
            vals = df[stack].to_numpy()
            color = colors.get(stack)
            label = legend_labels.get(stack, stack) if legend_labels else stack

            if signed:
                pos = np.clip(vals, 0, None)
                neg = np.clip(vals, None, 0)

                if orientation == "horizontal":
                    ax.barh(positions, pos, left=pos_base, height=bar_size, color=color, label=label)
                    ax.barh(positions, neg, left=neg_base, height=bar_size, color=color)
                else:
                    ax.bar(positions, pos, bottom=pos_base, width=bar_size, color=color, label=label)
                    ax.bar(positions, neg, bottom=neg_base, width=bar_size, color=color)

                pos_base += pos
                neg_base += neg
            else:
                if orientation == "horizontal":
                    ax.barh(positions, vals, left=pos_base, height=bar_size, color=color, label=label)
                else:
                    ax.bar(positions, vals, bottom=pos_base, width=bar_size, color=color, label=label)

                pos_base += vals

    @staticmethod
    def _apply_limits(
        ax: plt.Axes,
        axis: str,
        df,
        *,
        axis_limits: tuple[float, float] | None,
        mirror_limits: bool,
        signed: bool,
    ) -> None:
        if axis_limits is not None:
            if axis == "x":
                ax.set_xlim(*axis_limits)
            else:
                ax.set_ylim(*axis_limits)
            return

        if not mirror_limits or not signed:
            return

        pos = df.clip(lower=0).sum(axis=1).max()
        neg = abs(df.clip(upper=0).sum(axis=1).min())
        lim = max(float(pos), float(neg), 0.0)

        if axis == "x":
            ax.set_xlim(-lim, lim)
        else:
            ax.set_ylim(-lim, lim)

    @staticmethod
    def _invert_if_requested(ax: plt.Axes, orientation: str, invert_axis: bool) -> None:
        if not invert_axis:
            return

        if orientation == "horizontal":
            ax.invert_xaxis()
        else:
            ax.invert_yaxis()

    @staticmethod
    def _trim_bar_axis_padding(
        ax: plt.Axes,
        positions: np.ndarray,
        *,
        orientation: str,
        bar_size: float,
        edge_padding: float = 0.35,
    ) -> None:
        if len(positions) == 0:
            return

        low = float(np.min(positions) - bar_size / 2 - edge_padding)
        high = float(np.max(positions) + bar_size / 2 + edge_padding)

        if orientation == "horizontal":
            ax.set_ylim(low, high)
        else:
            ax.set_xlim(low, high)

    @staticmethod
    def _style_horizontal_axis(
        ax: plt.Axes,
        *,
        grid: bool = True,
        grid_color: str = "gray",
        grid_linestyle: str = "dashed",
        grid_linewidth: float = 0.8,
        x_major_step: float = 10,
        x_minor_step: float | None = None,
    ) -> None:
        ax.set_axisbelow(True)
        ax.grid(False)

        ax.xaxis.set_major_locator(mticker.MultipleLocator(x_major_step))
        if x_minor_step is not None:
            ax.xaxis.set_minor_locator(mticker.MultipleLocator(x_minor_step))
        else:
            ax.xaxis.set_minor_locator(mticker.NullLocator())

        if grid:
            ax.grid(
                axis="x",
                which="major",
                color=grid_color,
                linestyle=grid_linestyle,
                linewidth=grid_linewidth,
            )
            if x_minor_step is not None:
                ax.grid(
                    axis="x",
                    which="minor",
                    color=grid_color,
                    linestyle=grid_linestyle,
                    linewidth=grid_linewidth,
                    alpha=0.5,
                )

    @staticmethod
    def _style_vertical_axis(
        ax: plt.Axes,
        *,
        grid: bool = True,
        grid_color: str = "gray",
        grid_linestyle: str = "dashed",
        grid_linewidth: float = 0.8,
        y_major_step: float = 10,
        y_minor_step: float | None = None,
    ) -> None:
        ax.set_axisbelow(True)
        ax.grid(False)

        ax.yaxis.set_major_locator(mticker.MultipleLocator(y_major_step))
        if y_minor_step is not None:
            ax.yaxis.set_minor_locator(mticker.MultipleLocator(y_minor_step))
        else:
            ax.yaxis.set_minor_locator(mticker.NullLocator())

        if grid:
            ax.grid(
                axis="y",
                which="major",
                color=grid_color,
                linestyle=grid_linestyle,
                linewidth=grid_linewidth,
            )
            if y_minor_step is not None:
                ax.grid(
                    axis="y",
                    which="minor",
                    color=grid_color,
                    linestyle=grid_linestyle,
                    linewidth=grid_linewidth,
                    alpha=0.5,
                )

    def plot_bar(
        self,
        prepared: PreparedBarData,
        spec: dict,
    ):
        layout = spec.get("layout", {})
        style = spec.get("style", {})
        legend_cfg = spec.get("legend", {})

        orientation = layout.get("orientation", "horizontal")
        facet_col = layout.get("facet_col")
        facet_title_col = layout.get("facet_title_col", facet_col)
        show_facet_ylabels = layout.get("show_facet_ylabels", "first_only")

        group_col = layout.get("group_col")

        left_inner_label_col = layout.get("left_inner_label_col")
        left_outer_label_col = layout.get("left_outer_label_col")
        right_inner_label_col = layout.get("right_inner_label_col")
        right_outer_label_col = layout.get("right_outer_label_col")

        bottom_inner_label_col = layout.get("bottom_inner_label_col")
        bottom_outer_label_col = layout.get("bottom_outer_label_col")
        top_inner_label_col = layout.get("top_inner_label_col")
        top_outer_label_col = layout.get("top_outer_label_col")

        figsize_cm = style.get("figsize_cm", (16, 10))
        colors = style.get("colors", {})
        xlabel = style.get("xlabel", "")
        ylabel = style.get("ylabel", "")
        title = style.get("title")
        xlim = tuple(style["xlim"]) if style.get("xlim") is not None else None
        ylim = tuple(style["ylim"]) if style.get("ylim") is not None else None
        mirror_limits = style.get("mirror_limits", False)
        invert_axis = style.get("invert_axis", False)
        group_gap = float(style.get("group_gap", 0.8))
        bar_size = float(style.get("bar_size", 0.75))
        show_group_separators = bool(style.get("show_group_separators", True))
        legend_labels = style.get("legend_labels")

        grid = style.get("grid", True)
        grid_color = style.get("grid_color", "gray")
        grid_linestyle = style.get("grid_linestyle", "dashed")
        grid_linewidth = float(style.get("grid_linewidth", 0.8))
        x_major_step = float(style.get("x_major_step", 10))
        x_minor_step = style.get("x_minor_step")
        y_major_step = float(style.get("y_major_step", 10))
        y_minor_step = style.get("y_minor_step")

        show_legend = legend_cfg.get("show", True)

        fig_size = self._cm_to_inches(figsize_cm)

        group_col = self._validate_label_col(prepared.group_cols, group_col)
        facet_col = self._validate_label_col(prepared.group_cols, facet_col)
        facet_title_col = self._validate_label_col(prepared.group_cols, facet_title_col)

        left_inner_label_col = self._validate_label_col(prepared.group_cols, left_inner_label_col)
        left_outer_label_col = self._validate_label_col(prepared.group_cols, left_outer_label_col)
        right_inner_label_col = self._validate_label_col(prepared.group_cols, right_inner_label_col)
        right_outer_label_col = self._validate_label_col(prepared.group_cols, right_outer_label_col)

        bottom_inner_label_col = self._validate_label_col(prepared.group_cols, bottom_inner_label_col)
        bottom_outer_label_col = self._validate_label_col(prepared.group_cols, bottom_outer_label_col)
        top_inner_label_col = self._validate_label_col(prepared.group_cols, top_inner_label_col)
        top_outer_label_col = self._validate_label_col(prepared.group_cols, top_outer_label_col)

        if facet_col:
            return self._plot_faceted(
                prepared=prepared,
                orientation=orientation,
                facet_col=facet_col,
                facet_title_col=facet_title_col,
                show_facet_ylabels=show_facet_ylabels,
                group_col=group_col,
                left_inner_label_col=left_inner_label_col,
                left_outer_label_col=left_outer_label_col,
                right_inner_label_col=right_inner_label_col,
                right_outer_label_col=right_outer_label_col,
                bottom_inner_label_col=bottom_inner_label_col,
                bottom_outer_label_col=bottom_outer_label_col,
                top_inner_label_col=top_inner_label_col,
                top_outer_label_col=top_outer_label_col,
                fig_size=fig_size,
                colors=colors,
                xlabel=xlabel,
                ylabel=ylabel,
                title=title,
                xlim=xlim,
                ylim=ylim,
                mirror_limits=mirror_limits,
                invert_axis=invert_axis,
                group_gap=group_gap,
                bar_size=bar_size,
                show_group_separators=show_group_separators,
                show_legend=show_legend,
                legend_labels=legend_labels,
                legend_cfg=legend_cfg,
                grid=grid,
                grid_color=grid_color,
                grid_linestyle=grid_linestyle,
                grid_linewidth=grid_linewidth,
                x_major_step=x_major_step,
                x_minor_step=x_minor_step,
                y_major_step=y_major_step,
                y_minor_step=y_minor_step,
            )

        return self._plot_single_axis(
            prepared=prepared,
            orientation=orientation,
            group_col=group_col,
            left_inner_label_col=left_inner_label_col,
            left_outer_label_col=left_outer_label_col,
            right_inner_label_col=right_inner_label_col,
            right_outer_label_col=right_outer_label_col,
            bottom_inner_label_col=bottom_inner_label_col,
            bottom_outer_label_col=bottom_outer_label_col,
            top_inner_label_col=top_inner_label_col,
            top_outer_label_col=top_outer_label_col,
            fig_size=fig_size,
            colors=colors,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            xlim=xlim,
            ylim=ylim,
            mirror_limits=mirror_limits,
            invert_axis=invert_axis,
            group_gap=group_gap,
            bar_size=bar_size,
            show_group_separators=show_group_separators,
            show_legend=show_legend,
            legend_labels=legend_labels,
            legend_cfg=legend_cfg,
            grid=grid,
            grid_color=grid_color,
            grid_linestyle=grid_linestyle,
            grid_linewidth=grid_linewidth,
            x_major_step=x_major_step,
            x_minor_step=x_minor_step,
            y_major_step=y_major_step,
            y_minor_step=y_minor_step,
        )

    def _plot_single_axis(
        self,
        *,
        prepared: PreparedBarData,
        orientation: str,
        group_col: str | None,
        left_inner_label_col: str | None,
        left_outer_label_col: str | None,
        right_inner_label_col: str | None,
        right_outer_label_col: str | None,
        bottom_inner_label_col: str | None,
        bottom_outer_label_col: str | None,
        top_inner_label_col: str | None,
        top_outer_label_col: str | None,
        fig_size: tuple[float, float],
        colors: Mapping[str, str],
        xlabel: str,
        ylabel: str,
        title: str | None,
        xlim: tuple[float, float] | None,
        ylim: tuple[float, float] | None,
        mirror_limits: bool,
        invert_axis: bool,
        group_gap: float,
        bar_size: float,
        show_group_separators: bool,
        show_legend: bool,
        legend_labels: Mapping[str, str] | None,
        legend_cfg: dict,
        grid: bool,
        grid_color: str,
        grid_linestyle: str,
        grid_linewidth: float,
        x_major_step: float,
        x_minor_step: float | None,
        y_major_step: float,
        y_minor_step: float | None,
    ):
        fig, ax = plt.subplots(figsize=fig_size)

        positions = self._build_grouped_positions(
            prepared.index_frame,
            gap_by=group_col,
            gap_size=group_gap,
        )

        self._plot_stacked(
            ax=ax,
            df=prepared.data,
            positions=positions,
            stacks=prepared.stack_order,
            colors=colors,
            signed=prepared.signed,
            orientation=orientation,
            bar_size=bar_size,
            legend_labels=legend_labels,
        )

        self._draw_group_separators(
            ax=ax,
            index_frame=prepared.index_frame,
            positions=positions,
            group_col=group_col,
            orientation=orientation,
            enabled=show_group_separators,
        )

        self._trim_bar_axis_padding(
            ax=ax,
            positions=positions,
            orientation=orientation,
            bar_size=bar_size,
            edge_padding=0.35,
        )

        if orientation == "horizontal":
            self._draw_horizontal_labels(
                ax=ax,
                index_frame=prepared.index_frame,
                positions=positions,
                left_inner_label_col=left_inner_label_col,
                left_outer_label_col=left_outer_label_col,
                right_inner_label_col=right_inner_label_col,
                right_outer_label_col=right_outer_label_col,
            )
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            self._apply_limits(
                ax=ax,
                axis="x",
                df=prepared.data,
                axis_limits=xlim,
                mirror_limits=mirror_limits,
                signed=prepared.signed,
            )
            if ylim is not None:
                ax.set_ylim(*ylim)

            self._style_horizontal_axis(
                ax=ax,
                grid=grid,
                grid_color=grid_color,
                grid_linestyle=grid_linestyle,
                grid_linewidth=grid_linewidth,
                x_major_step=x_major_step,
                x_minor_step=x_minor_step,
            )
        else:
            self._draw_vertical_labels(
                ax=ax,
                index_frame=prepared.index_frame,
                positions=positions,
                bottom_inner_label_col=bottom_inner_label_col,
                bottom_outer_label_col=bottom_outer_label_col,
                top_inner_label_col=top_inner_label_col,
                top_outer_label_col=top_outer_label_col,
            )
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            self._apply_limits(
                ax=ax,
                axis="y",
                df=prepared.data,
                axis_limits=ylim,
                mirror_limits=mirror_limits,
                signed=prepared.signed,
            )
            if xlim is not None:
                ax.set_xlim(*xlim)

            self._style_vertical_axis(
                ax=ax,
                grid=grid,
                grid_color=grid_color,
                grid_linestyle=grid_linestyle,
                grid_linewidth=grid_linewidth,
                y_major_step=y_major_step,
                y_minor_step=y_minor_step,
            )

        self._invert_if_requested(ax, orientation=orientation, invert_axis=invert_axis)

        if title:
            ax.set_title(title)

        if show_legend:
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(
                    handles,
                    labels,
                    loc=legend_cfg.get("loc", "best"),
                    frameon=legend_cfg.get("frameon", False),
                    ncol=legend_cfg.get("ncol", 1),
                )

        if orientation == "horizontal":
            left_margin = 0.30 if (left_inner_label_col or left_outer_label_col) else 0.10
            right_margin = 0.9 if (right_inner_label_col or right_outer_label_col or show_legend) else 0.96
            fig.subplots_adjust(left=left_margin, right=right_margin)
        else:
            bottom_margin = 0.20 if (bottom_inner_label_col or bottom_outer_label_col) else 0.12
            top_margin = 0.85 if (top_inner_label_col or top_outer_label_col or title) else 0.94
            right_margin = 0.82 if show_legend else 0.96
            fig.subplots_adjust(bottom=bottom_margin, top=top_margin, right=right_margin)

        return fig, ax

    def _plot_faceted(
        self,
        *,
        prepared: PreparedBarData,
        orientation: str,
        facet_col: str,
        facet_title_col: str | None,
        show_facet_ylabels: str,
        group_col: str | None,
        left_inner_label_col: str | None,
        left_outer_label_col: str | None,
        right_inner_label_col: str | None,
        right_outer_label_col: str | None,
        bottom_inner_label_col: str | None,
        bottom_outer_label_col: str | None,
        top_inner_label_col: str | None,
        top_outer_label_col: str | None,
        fig_size: tuple[float, float],
        colors: Mapping[str, str],
        xlabel: str,
        ylabel: str,
        title: str | None,
        xlim: tuple[float, float] | None,
        ylim: tuple[float, float] | None,
        mirror_limits: bool,
        invert_axis: bool,
        group_gap: float,
        bar_size: float,
        show_group_separators: bool,
        show_legend: bool,
        legend_labels: Mapping[str, str] | None,
        legend_cfg: dict,
        grid: bool,
        grid_color: str,
        grid_linestyle: str,
        grid_linewidth: float,
        x_major_step: float,
        x_minor_step: float | None,
        y_major_step: float,
        y_minor_step: float | None,
    ):
        if facet_col not in prepared.index_frame.columns:
            raise ValueError(f"facet_col '{facet_col}' is not present in group_cols")

        facet_values = prepared.index_frame[facet_col].dropna().drop_duplicates().tolist()
        if len(facet_values) == 0:
            raise ValueError(
                f"No facet values found for facet_col='{facet_col}' in variable "
            )

        n = len(facet_values)
        fig, axes = plt.subplots(1, n, figsize=fig_size, sharex=False, sharey=True, squeeze=False)
        axes_arr = axes[0]

        legend_handles = None
        legend_texts = None

        for i, facet_value in enumerate(facet_values):
            ax = axes_arr[i]
            mask = (prepared.index_frame[facet_col] == facet_value).to_numpy()

            df_sub = prepared.data.iloc[mask]
            idx_sub = prepared.index_frame.iloc[mask].reset_index(drop=True)

            positions = self._build_grouped_positions(
                idx_sub,
                gap_by=group_col,
                gap_size=group_gap,
            )

            self._plot_stacked(
                ax=ax,
                df=df_sub,
                positions=positions,
                stacks=prepared.stack_order,
                colors=colors,
                signed=prepared.signed,
                orientation=orientation,
                bar_size=bar_size,
                legend_labels=legend_labels,
            )

            self._draw_group_separators(
                ax=ax,
                index_frame=idx_sub,
                positions=positions,
                group_col=group_col,
                orientation=orientation,
                enabled=show_group_separators,
            )

            self._trim_bar_axis_padding(
                ax=ax,
                positions=positions,
                orientation=orientation,
                bar_size=bar_size,
                edge_padding=0.35,
            )

            if facet_title_col and facet_title_col in idx_sub.columns and len(idx_sub) > 0:
                facet_title = idx_sub[facet_title_col].iloc[0]
            else:
                facet_title = facet_value
            ax.set_title(str(facet_title), fontsize=11)

            show_labels_this_axis = (
                show_facet_ylabels == "all"
                or (show_facet_ylabels == "first_only" and i == 0)
            )
            if orientation == "horizontal":
                self._draw_horizontal_labels(
                    ax=ax,
                    index_frame=idx_sub,
                    positions=positions,
                    left_inner_label_col=left_inner_label_col if show_labels_this_axis else None,
                    left_outer_label_col=left_outer_label_col if show_labels_this_axis else None,
                    right_inner_label_col=right_inner_label_col if show_labels_this_axis else None,
                    right_outer_label_col=right_outer_label_col if show_labels_this_axis else None,
                )
                ax.set_xlabel(xlabel)
                if i == 0:
                    ax.set_ylabel(ylabel)

                self._apply_limits(
                    ax=ax,
                    axis="x",
                    df=df_sub,
                    axis_limits=xlim,
                    mirror_limits=mirror_limits,
                    signed=prepared.signed,
                )
                if ylim is not None:
                    ax.set_ylim(*ylim)

                self._style_horizontal_axis(
                    ax=ax,
                    grid=grid,
                    grid_color=grid_color,
                    grid_linestyle=grid_linestyle,
                    grid_linewidth=grid_linewidth,
                    x_major_step=x_major_step,
                    x_minor_step=x_minor_step,
                )
            else:
                self._draw_vertical_labels(
                    ax=ax,
                    index_frame=idx_sub,
                    positions=positions,
                    bottom_inner_label_col=bottom_inner_label_col,
                    bottom_outer_label_col=bottom_outer_label_col,
                    top_inner_label_col=top_inner_label_col,
                    top_outer_label_col=top_outer_label_col,
                )
                ax.set_xlabel(xlabel)
                if i == 0:
                    ax.set_ylabel(ylabel)

                self._apply_limits(
                    ax=ax,
                    axis="y",
                    df=df_sub,
                    axis_limits=ylim,
                    mirror_limits=mirror_limits,
                    signed=prepared.signed,
                )
                if xlim is not None:
                    ax.set_xlim(*xlim)

                self._style_vertical_axis(
                    ax=ax,
                    grid=grid,
                    grid_color=grid_color,
                    grid_linestyle=grid_linestyle,
                    grid_linewidth=grid_linewidth,
                    y_major_step=y_major_step,
                    y_minor_step=y_minor_step,
                )

            self._invert_if_requested(ax, orientation=orientation, invert_axis=invert_axis)

            if legend_handles is None:
                legend_handles, legend_texts = ax.get_legend_handles_labels()

            if ax.get_legend() is not None:
                ax.get_legend().remove()

        if title:
            fig.suptitle(title)

        if show_legend and legend_handles:
            fig.legend(
                legend_handles,
                legend_texts,
                loc=legend_cfg.get("loc", "center left"),
                bbox_to_anchor=tuple(legend_cfg.get("bbox_to_anchor", (1.02, 0.5))),
                frameon=legend_cfg.get("frameon", False),
                ncol=legend_cfg.get("ncol", 1),
            )

        if orientation == "horizontal":
            left_margin = 0.18 if (left_inner_label_col or left_outer_label_col) else 0.08
            right_margin = 0.84 if (show_legend or right_inner_label_col or right_outer_label_col) else 0.96
            fig.subplots_adjust(
                left=left_margin,
                right=right_margin,
                wspace=0.18,
                top=0.88 if (title or facet_title_col) else 0.94,
            )
        else:
            bottom_margin = 0.20 if (bottom_inner_label_col or bottom_outer_label_col) else 0.12
            top_margin = 0.85 if (top_inner_label_col or top_outer_label_col or title or facet_title_col) else 0.94
            right_margin = 0.84 if show_legend else 0.96
            fig.subplots_adjust(
                bottom=bottom_margin,
                top=top_margin,
                right=right_margin,
                wspace=0.18,
            )

        return fig, axes_arr