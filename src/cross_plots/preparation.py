from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

import pandas as pd
from crosscontract.registry import CrossDataVariable


@dataclass(frozen=True)
class PreparedBarData:
    data: pd.DataFrame
    stack_order: list[str]
    group_cols: list[str]
    signed: bool
    index_frame: pd.DataFrame


def fetch_variable_data(
    *,
    variable: CrossDataVariable,
    stack_col: str,
    include_columns: list[str],
    aggregation: dict | None = None,
    models: dict[str, dict[str, str]] | None = None,
    scenario_names: dict[tuple[str, str], str] | None = None,
    scenario_groups: dict[str, dict[str, list[str]]] | None = None,
    years: list[int] | None = None,
    extra_filters: dict | None = None,
    use_titles: bool = False,
) -> pd.DataFrame:
    filters = dict(extra_filters or {})

    if models is not None:
        filters["model"] = list(models.keys())

    if scenario_names is not None:
        scenarios = list({k[0] for k in scenario_names.keys()})
        variants = list({k[1] for k in scenario_names.keys()})
        filters["scenario_name"] = scenarios
        filters["scenario_variant"] = variants

    if years is not None:
        filters["year"] = years

    columns = [*include_columns]
    if stack_col not in columns:
        columns.append(stack_col)

    df = variable.get_data(
        filters=filters,
        aggregation=aggregation,
        use_titles=use_titles,
        columns=columns,
    ).rename(columns={stack_col: "stack_col"})

    if models is not None:
        id_to_name = {k: v["name"] for k, v in models.items()}
        df["model"] = df["model"].map(id_to_name).fillna(df["model"])

    if scenario_names is not None:
        df["scenario_label"] = (
            df.set_index(["scenario_name", "scenario_variant"])
            .index.map(scenario_names)
            .to_series(index=df.index)
        )
    
    if scenario_groups is not None:
        for group_name in scenario_groups:
            df = apply_scenario_grouping(
                df,
                grouping_name=group_name,
                scenario_groups=scenario_groups,
                source_col="scenario_label",
            )

    return df

def apply_scenario_grouping(
    df: pd.DataFrame,
    *,
    grouping_name: str,
    scenario_groups: dict,
    source_col: str = "scenario_label",
) -> pd.DataFrame:
    """
    Adds:
        - grouping column (e.g. by_climate)
        - label column (e.g. sce_label_by_climate)

    based on SCENARIO_GROUPS definition.
    """

    if grouping_name not in scenario_groups:
        raise ValueError(f"Unknown grouping: {grouping_name}")

    group_def = scenario_groups[grouping_name]

    group_map = {}
    label_map = {}

    for group_value, mapping in group_def.items():
        for original, new_label in mapping.items():
            group_map[original] = group_value
            label_map[original] = new_label

    group_col = grouping_name
    label_col = f"sce_label_{grouping_name}"

    df[group_col] = df[source_col].map(group_map)
    df[label_col] = df[source_col].map(label_map)

    # safety check
    if df[group_col].isna().any() or df[label_col].isna().any():
        missing = df.loc[df[group_col].isna(), source_col].unique()
        raise ValueError(
            f"Some scenarios not covered in '{grouping_name}': {missing}"
        )

    return df

def prepare_bar_data(
    df: pd.DataFrame,
    group_cols: list[str],
    stack_col: str = "stack_col",
    value_col: str = "value",
    stack_order: list[str] | None = None,
    signed: bool = False,
    group_orders: dict[str, list[Any]] | None = None,
    group_dependencies: dict[str, str] | None = None,
    drop_empty_bars: bool = False,
) -> PreparedBarData:
    required = set(group_cols + [stack_col, value_col])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    grouped = (
        df.groupby(group_cols + [stack_col], dropna=False)[value_col]
        .sum()
        .reset_index()
    )

    pivot = grouped.pivot_table(
        index=group_cols,
        columns=stack_col,
        values=value_col,
        aggfunc="sum",
        fill_value=0,
    )

    if stack_order is not None:
        ordered_existing = [c for c in stack_order if c in pivot.columns]
        remaining = [c for c in pivot.columns if c not in ordered_existing]
        pivot = pivot[ordered_existing + remaining]

    # Keep full group combinations when drop_empty_bars=False
    if not drop_empty_bars:
        full_index = _build_full_index(
            df=df,
            group_cols=group_cols,
            group_orders=group_orders,
            group_dependencies=group_dependencies,
        )
        pivot = pivot.reindex(full_index, fill_value=0)

    if drop_empty_bars:
        pivot = pivot.loc[(pivot.abs().sum(axis=1) > 0)]

    if group_orders:
        pivot = _sort_multiindex(
            pivot,
            group_cols=group_cols,
            group_orders=group_orders,
        )

    index_frame = pivot.index.to_frame(index=False)

    return PreparedBarData(
        data=pivot,
        stack_order=list(pivot.columns),
        group_cols=list(group_cols),
        signed=signed,
        index_frame=index_frame,
    )


def _build_full_index(
    df: pd.DataFrame,
    group_cols: list[str],
    group_orders: dict[str, list[Any]] | None = None,
    group_dependencies: dict[str, str] | None = None,
) -> pd.MultiIndex:
    """
    Build a full index.

    - Independent columns are expanded as a Cartesian product.
    - Dependent columns only use values valid for their declared parent.

    Example:
        group_dependencies = {"scenario_label": "scenario_family"}
    means scenario_label values are only expanded within the matching scenario_family.
    """
    group_dependencies = group_dependencies or {}

    if len(group_cols) == 1:
        col = group_cols[0]
        values = _ordered_unique_values(df, col, group_orders)
        return pd.MultiIndex.from_arrays([values], names=group_cols)

    rows = [dict()]

    for col in group_cols:
        parent = group_dependencies.get(col)

        new_rows = []
        for row in rows:
            if parent is not None and parent in row:
                valid_df = df[df[parent] == row[parent]]
                values = _ordered_unique_values(valid_df, col, group_orders)
            else:
                values = _ordered_unique_values(df, col, group_orders)

            for value in values:
                new_row = dict(row)
                new_row[col] = value
                new_rows.append(new_row)

        rows = new_rows

    full_frame = pd.DataFrame(rows, columns=group_cols).drop_duplicates()
    return pd.MultiIndex.from_frame(full_frame, names=group_cols)


def _ordered_unique_values(
    df: pd.DataFrame,
    col: str,
    group_orders: dict[str, list[Any]] | None = None,
) -> list[Any]:
    observed = df[col].drop_duplicates().tolist()

    if group_orders and col in group_orders and group_orders[col] is not None:
        ordered = [v for v in group_orders[col] if v in set(observed)]
        remaining = [v for v in observed if v not in ordered]
        return ordered + remaining

    return observed


def _sort_multiindex(
    df: pd.DataFrame,
    group_cols: list[str],
    group_orders: dict[str, list[Any]],
) -> pd.DataFrame:
    if len(df) == 0:
        return df

    frame = df.index.to_frame(index=False).copy()

    order_cols: list[str] = []
    for col in group_cols:
        order_col = f"__order__{col}"
        if col in group_orders and group_orders[col] is not None:
            order_map = {value: i for i, value in enumerate(group_orders[col])}
            frame[order_col] = frame[col].map(lambda x: order_map.get(x, len(order_map)))
        else:
            frame[order_col] = frame[col].astype(str)
        order_cols.append(order_col)

    frame["__row__"] = range(len(frame))
    frame = frame.sort_values(order_cols, kind="stable")

    return df.iloc[frame["__row__"].tolist()]