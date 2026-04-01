from __future__ import annotations

from copy import deepcopy
from typing import Any


PLOT_LAYOUTS = {
    "horizontal_grouped": {
        "orientation": "horizontal",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
    "vertical_grouped": {
        "orientation": "vertical",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
    "horizontal_faceted": {
        "orientation": "horizontal",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
    "horizontal_faceted_grouped": {
        "orientation": "horizontal",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
    "vertical_faceted_grouped": {
        "orientation": "vertical",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
    "horizontal_signed_grouped": {
        "orientation": "horizontal",
        "facet_col": None,
        "facet_title_col": None,
        "group_col": None,
        "left_inner_label_col": None,
        "left_outer_label_col": None,
        "right_inner_label_col": None,
        "right_outer_label_col": None,
        "bottom_inner_label_col": None,
        "bottom_outer_label_col": None,
        "top_inner_label_col": None,
        "top_outer_label_col": None,
    },
}


PLOT_VARIANTS = {
    "horizontal_grouped": {
        "layout_template": "horizontal_grouped",
        "figsize_cm": (18, 24),
        "legend_right": False,
        "legend_show": True,
        "signed": False,
    },
    "vertical_grouped": {
        "layout_template": "vertical_grouped",
        "figsize_cm": (28, 14),
        "legend_right": False,
        "legend_show": True,
        "signed": False,
    },
    "horizontal_faceted": {
        "layout_template": "horizontal_faceted",
        "figsize_cm": (32, 18),
        "legend_right": True,
        "legend_show": True,
        "signed": False,
    },
    "horizontal_faceted_grouped": {
        "layout_template": "horizontal_faceted_grouped",
        "figsize_cm": (34, 18),
        "legend_right": True,
        "legend_show": True,
        "signed": False,
    },
    "vertical_faceted_grouped": {
        "layout_template": "vertical_faceted_grouped",
        "figsize_cm": (34, 16),
        "legend_right": True,
        "legend_show": True,
        "signed": False,
    },
    "signed_supply_vs_demand": {
        "layout_template": "horizontal_signed_grouped",
        "figsize_cm": (18, 24),
        "legend_right": False,
        "legend_show": True,
        "signed": True,
    },
}


def _base_style(
    *,
    orientation: str,
    axis_title: str,
    lim: tuple[float, float] | None,
    signed: bool,
    figsize_cm: tuple[float, float],
) -> dict[str, Any]:
    style = {
        "figsize_cm": figsize_cm,
        "xlabel": axis_title if orientation == "horizontal" else "",
        "ylabel": axis_title if orientation == "vertical" else "",
        "title": None,
        "xlim": lim if orientation == "horizontal" else None,
        "ylim": lim if orientation == "vertical" else None,
        "mirror_limits": signed,
        "invert_axis": False,
        "group_gap": 0.8,
        "bar_size": 0.75,
        "show_group_separators": True,
        "grid": True,
        "grid_color": "gray",
        "grid_linestyle": "dashed",
        "grid_linewidth": 0.8,
        "x_major_step": 10,
        "x_minor_step": None,
        "y_major_step": 10,
        "y_minor_step": None,
    }
    return style


def _legend_block(*, legend_right: bool, legend_show: bool) -> dict[str, Any]:
    legend = {
        "show": legend_show,
        "loc": "center left" if legend_right else "best",
        "frameon": False,
        "ncol": 1,
    }
    if legend_right:
        legend["bbox_to_anchor"] = (1.02, 0.5)
    return legend


def make_plot_spec(
    *,
    source_variable: str,
    axis_title: str,
    lim: tuple[float, float] | None,
    filename: str,
    variant_name: str,
    group_cols: list[str],
    group_orders: dict[str, list[Any]] | None = None,
    group_dependencies: dict[str, str] | None = None,
    layout_overrides: dict[str, Any] | None = None,
    style_overrides: dict[str, Any] | None = None,
    legend_overrides: dict[str, Any] | None = None,
    drop_empty_bars: bool = False,
) -> dict[str, Any]:
    variant = PLOT_VARIANTS[variant_name]
    layout = deepcopy(PLOT_LAYOUTS[variant["layout_template"]])
    layout.update(layout_overrides or {})

    signed = bool(variant.get("signed", False))
    style = _base_style(
        orientation=layout["orientation"],
        axis_title=axis_title,
        lim=lim,
        signed=signed,
        figsize_cm=variant["figsize_cm"],
    )
    style.update(style_overrides or {})

    legend = _legend_block(
        legend_right=bool(variant.get("legend_right", False)),
        legend_show=bool(variant.get("legend_show", True)),
    )
    legend.update(legend_overrides or {})

    return {
        "sources": [{"variable": source_variable, "sign": 1}],
        "group_cols": group_cols,
        "group_orders": group_orders or {},
        "group_dependencies": group_dependencies,
        "signed": signed,
        "drop_empty_bars": drop_empty_bars,
        "layout": layout,
        "style": style,
        "legend": legend,
        "filename": filename,
    }


def make_signed_plot_spec(
    *,
    positive_variable: str,
    negative_variable: str,
    axis_title: str,
    lim: tuple[float, float] | None,
    filename: str,
    group_cols: list[str],
    group_orders: dict[str, list[Any]] | None = None,
    group_dependencies: dict[str, str] | None = None,
    layout_overrides: dict[str, Any] | None = None,
    style_overrides: dict[str, Any] | None = None,
    legend_overrides: dict[str, Any] | None = None,
    drop_empty_bars: bool = False,
) -> dict[str, Any]:
    variant = PLOT_VARIANTS["signed_supply_vs_demand"]
    layout = deepcopy(PLOT_LAYOUTS[variant["layout_template"]])
    layout.update(layout_overrides or {})

    style = _base_style(
        orientation=layout["orientation"],
        axis_title=axis_title,
        lim=lim,
        signed=True,
        figsize_cm=variant["figsize_cm"],
    )
    style.update(style_overrides or {})

    legend = _legend_block(
        legend_right=bool(variant.get("legend_right", False)),
        legend_show=bool(variant.get("legend_show", True)),
    )
    legend.update(legend_overrides or {})

    return {
        "sources": [
            {"variable": positive_variable, "sign": 1},
            {"variable": negative_variable, "sign": -1},
        ],
        "group_cols": group_cols,
        "group_orders": group_orders or {},
        "group_dependencies": group_dependencies,
        "signed": True,
        "drop_empty_bars": drop_empty_bars,
        "layout": layout,
        "style": style,
        "legend": legend,
        "filename": filename,
    }


def build_bar_specs(
    *,
    variables: dict[str, dict[str, Any]],
    variable_plot_plans: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}

    for var_key, var_cfg in variables.items():
        supply = var_cfg["supply"]
        consumption = var_cfg.get("consumption")
        axis_title = var_cfg["axis_title"]
        lim = var_cfg["lim"]
        signed_lim = var_cfg.get("signed_lim")

        plans = variable_plot_plans[var_key]

        for plot_name, plan in plans.items():
            if plot_name == "signed_supply_vs_demand":
                if consumption is None:
                    continue
                specs[f"{var_key}_{plot_name}"] = make_signed_plot_spec(
                    positive_variable=supply,
                    negative_variable=consumption,
                    axis_title=axis_title,
                    lim=signed_lim,
                    filename=f"{var_key}_{plot_name}",
                    group_cols=plan["group_cols"],
                    group_orders=plan.get("group_orders"),
                    group_dependencies=plan.get("group_dependencies"),
                    layout_overrides=plan.get("layout_overrides"),
                    style_overrides=plan.get("style_overrides"),
                    legend_overrides=plan.get("legend_overrides"),
                    drop_empty_bars=plan.get("drop_empty_bars", False),
                )
            else:
                specs[f"{var_key}_{plot_name}"] = make_plot_spec(
                    source_variable=supply,
                    axis_title=axis_title,
                    lim=lim,
                    filename=f"{var_key}_{plot_name}",
                    variant_name=plot_name,
                    group_cols=plan["group_cols"],
                    group_orders=plan.get("group_orders"),
                    group_dependencies=plan.get("group_dependencies"),
                    layout_overrides=plan.get("layout_overrides"),
                    style_overrides=plan.get("style_overrides"),
                    legend_overrides=plan.get("legend_overrides"),
                    drop_empty_bars=plan.get("drop_empty_bars", False),
                )

    return specs