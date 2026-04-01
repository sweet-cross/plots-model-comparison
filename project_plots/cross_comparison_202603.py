"""Run stacked bar plots for the CROSS comparison using the refactored bar pipeline."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from crosscontract import CrossRegistry
from matplotlib import pyplot as plt
from cross_plots import preparation, plots
from .settings_cross2025 import (
    BAR_SPECS,
    DEFAULT_COLUMNS,
    MODELS,
    SCENARIOS,
    SCENARIO_GROUPS,
    YEARS,
    CONTRACT_SPECS,
    GENERAL_FILTERS
)


def main() -> None:
    env_path = Path.cwd() / "dontshare" / "ATT62020.env"
    load_dotenv(env_path)

    my_registry = CrossRegistry(
        username=os.getenv("CROSSUSER"),
        password=os.getenv("PASSWORD"),
    )

    output_dir = Path("./plots/cross_comparison_2025")
    plotter = plots.BarPlotter(output_dir=output_dir)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    selected = list(BAR_SPECS.keys())
    plotter = plots.BarPlotter(output_dir=output_path)

    use_titles=False

    for plot_name in selected:
        spec = BAR_SPECS[plot_name]
        
        dfs = []
        plot_colors = {}
        stack_order = []

        for src in spec["sources"]:
            variable_name = src["variable"]
            variable = my_registry.add_variable(variable_name, overwrite=True)
            contract = CONTRACT_SPECS[variable_name]
            plot_colors.update(contract.get("colors", {}))

            # stack order (append, preserve order)
            for k in contract.get("stack_order", []):
                if k not in stack_order:
                    stack_order.append(k)


            df = preparation.fetch_variable_data(
                variable=variable,
                stack_col=contract["stack_col"],
                include_columns=DEFAULT_COLUMNS,
                aggregation=contract.get("aggregation"),
                models=MODELS,
                scenario_names=SCENARIOS,
                scenario_groups=SCENARIO_GROUPS,
                years=YEARS,
                extra_filters=GENERAL_FILTERS,
                use_titles=use_titles,
            )
            df["value"] = df["value"] * src.get("sign", 1)
            dfs.append(df)

        df_combined = pd.concat(dfs, ignore_index=True)

        prepared = preparation.prepare_bar_data(
            df=df_combined,
            group_cols=spec["group_cols"],
            stack_col="stack_col",
            value_col="value",
            stack_order=stack_order,
            signed=spec.get("signed", False),
            group_orders=spec.get("group_orders"),
            drop_empty_bars=spec.get("drop_empty_bars", False),
        )

        #Merge contract specs into plot specs 
        spec["style"]["colors"] = plot_colors
        
        fig, _ = plotter.plot_bar(prepared, spec)
        fig.tight_layout()
        filename = spec.get("filename", plot_name) + ".pdf"
        fig.savefig(output_path / filename, bbox_inches="tight", dpi=300)
        filename = spec.get("filename", plot_name) + ".png"
        fig.savefig(output_path / filename, bbox_inches="tight", dpi=300)
        
        plt.close(fig)


if __name__ == "__main__":
    main()
