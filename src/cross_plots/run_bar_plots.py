from __future__ import annotations

from typing import Any

from .preparation import fetch_variable_data, prepare_bar_data
from .plots import BarPlotter



def default_label_formatter(values: dict[str, Any]) -> str:
    parts = []
    preferred = ["model", "scenario_name", "scenario_variant"]

    for key in preferred:
        value = values.get(key)
        if value not in (None, ""):
            parts.append(str(value))

    for key, value in values.items():
        if key not in preferred and value not in (None, ""):
            parts.append(str(value))

    return "\n".join(parts)






def _resolve_group_orders(
    group_cols: list[str],
    group_orders: dict[str, list[Any] | None] | None,
    MODELS: dict[str, Any],
    SCENARIOS: dict[Any, str],
) -> dict[str, list[Any]]:
    resolved: dict[str, list[Any]] = {}
    group_orders = group_orders or {}

    for col in group_cols:
        explicit = group_orders.get(col)
        if explicit is not None:
            resolved[col] = list(explicit)
        elif col == "model":
            resolved[col] = list(MODELS.keys())
        elif col == "scenario_name":
            resolved[col] = list(SCENARIOS.values())

    return resolved



def make_bar_plots(
    my_registry,
    contracts_specs,
    MODELS,
    SCENARIOS,
    *,
    output_dir: str,
    selected_variables: list[str] | None = None,
    year: int | None = None,
) -> dict[str, object]:
    raw_data = fetch_variable_data(
        my_registry=my_registry,
        contracts_specs=contracts_specs,
        models=MODELS,
        scenarios=SCENARIOS,
        selected_variables=selected_variables,
    )

    plotter = BarPlotter(output_dir=output_dir)
    figures: dict[str, object] = {}

    for variable_name, df in raw_data.items():
        plot_cfg = BAR_SPECS.get(variable_name, {})
        group_cols = plot_cfg.get("group_cols", ["model", "scenario_name"])
        group_orders = _resolve_group_orders(
            group_cols=group_cols,
            group_orders=plot_cfg.get("group_orders"),
            MODELS=MODELS,
            SCENARIOS=SCENARIOS,
        )

        prepared = prepare_bar_data(
            df,
            variable_name,
            group_cols=group_cols,
            group_orders=group_orders,
            stack_order=plot_cfg.get("stack_order"),
            year=year,
            label_formatter=plot_cfg.get("label_formatter", default_label_formatter),
            drop_empty_bars=plot_cfg.get("drop_empty_bars", False),
            signed=plot_cfg.get("signed", False),
            positive_stacks=plot_cfg.get("positive_stacks"),
            negative_stacks=plot_cfg.get("negative_stacks"),
            scale=plot_cfg.get("scale", 1.0),
        )

        orientation = plot_cfg.get("orientation", "horizontal")
        common_kwargs = {
            "colors": plot_cfg.get("colors"),
            "title": plot_cfg.get("title"),
            "filename": plot_cfg.get("filename", variable_name),
            "figsize": plot_cfg.get("figsize", (9, 12)),
            "show_legend": plot_cfg.get("show_legend", True),
            "legend_kwargs": plot_cfg.get("legend_kwargs"),
            "invert_axis": plot_cfg.get("invert_axis", False),
            "mirror_limits": plot_cfg.get("mirror_limits", False),
        }

        if orientation == "vertical":
            fig, _ = plotter.plot_bar_vertical(
                prepared,
                ylabel=plot_cfg.get("ylabel", plot_cfg.get("xlabel", variable_name)),
                ylim=plot_cfg.get("ylim"),
                **common_kwargs,
            )
        else:
            fig, _ = plotter.plot_bar_horizontal(
                prepared,
                xlabel=plot_cfg.get("xlabel", variable_name),
                xlim=plot_cfg.get("xlim"),
                **common_kwargs,
            )

        figures[variable_name] = fig

    return figures


if __name__ == "__main__":
    raise SystemExit(
        "Import make_bar_plots(...) into your project and pass my_registry, "
        "contracts_specs, MODELS, and SCENARIOS from your runtime."
    )
