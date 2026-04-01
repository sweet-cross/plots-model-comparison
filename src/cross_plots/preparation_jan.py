import pandas as pd

from crosscontract.registry import CrossDataVariable
from ...project_plots.settings import SCENARIOS_INVERSE


def infer_stack_column(var: CrossDataVariable) -> str:
    """Infers the name of the column to use for stacking in a horizontal bar plot.
    This is done by excluding known columns for model, scenario, and value, and
    checking that exactly one column remains.

    Args:
        var: The CrossDataVariable instance containing the data to be plotted.

    Returns:
        The name of the column to use for stacking.

    Raises:
        ValueError: If there is not exactly one column that can be used for stacking.
    """
    # drop the
    stack_cols = [
        col
        for col in var.data.columns
        if col
        not in [
            "model",
            "scenario_name",
            "value",
            "year",
            "unit",
            "scenario_variant",
            "scenario_group",
            "country",
        ]
    ]
    if len(stack_cols) != 1:
        raise ValueError(
            f"Expected exactly one stack column, but found {len(stack_cols)}: {stack_cols}"
        )
    return stack_cols[0]


def prepare_horizontal_bar_plot_data(
    variable: CrossDataVariable,
    years: list[int],
    models: list[str] | None,
    scenario_names: list[str] | None,
    drop_columns: list[str] | None = None,
    aggregation: dict[str, int] | None = None,
    use_titles: bool = True,
) -> pd.DataFrame:
    """Prepares a DataFrame for plotting by filtering and reshaping it.

    Args:
        variable: The DataVariable to prepare the data from.
        years: The years to filter the data by.
        models: A list of models to include in the plot (optional).
        scenario_names: A list of scenario names to include in the plot (optional).
        drop_columns: A list of columns to drop from the DataFrame (optional).
        aggregation: A dictionary specifying the aggregation level for each column (optional).
        use_titles: Whether to use titles for id given in the referencing columns.

    Returns:
        A DataFrame that has been filtered and reshaped for plotting.
    """

    df_out = (
        variable.get_data(
            filters={
                "year": years,
                "model": models,
                "scenario_name": scenario_names,
            },
            aggregation=aggregation,
            use_titles=use_titles,
        )
        .assign(
            scenario=lambda df: df["scenario_name"].map(SCENARIOS_INVERSE),
        )
        .drop(
            columns=["scenario_name", "scenario_variant", "unit"],
            errors="ignore",
        )
    )
    if drop_columns is not None:
        df_out = df_out.drop(columns=drop_columns, errors="ignore")
    return df_out




