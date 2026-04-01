from __future__ import annotations

from cross_plots import figures_templates

GENERAL_FILTERS = {
    "country": ["CH"],
    "scenario_group": ["cross202506"],
}
YEARS = [2050]

MODELS = {
    "ehub": {"name": "EhubX", "color": "#8B5349"},
    "secmod": {"name": "SecMod", "color": "#9565BD"},
    "ses": {"name": "SES", "color": "#1E75B3"},
    "seseth": {"name": "SES-ETH", "color": "#2A9E2A"},
    "stem": {"name": "STEM", "color": "#D52426"},
    "zengarden": {"name": "ZEN-Garden", "color": "#00BFC4"},
    "powercheck": {"name": "PowerCheck", "color": "#D57CBE"},
}
MODEL_ORDER = ["EhubX", "PowerCheck", "SecMod", "SES", "SES-ETH", "STEM", "ZEN-Garden"]

SCENARIOS = {
    ("abroad-res-full", "reference"): "abroad-res-full",
    ("abroad-res-lim", "reference"): "abroad-res-lim",
    ("abroad-nores-full", "reference"): "abroad-nores-full",
    ("abroad-nores-lim", "reference"): "abroad-nores-lim",
    ("domestic-res-full", "reference"): "domestic-res-full",
    ("domestic-res-lim", "reference"): "domestic-res-lim",
    ("domestic-nores-full", "reference"): "domestic-nores-full",
    ("domestic-nores-lim", "reference"): "domestic-nores-lim",
}
SCENARIOS_ORDER = [
    "abroad-res-full",
    "abroad-res-lim",
    "abroad-nores-full",
    "abroad-nores-lim",
    "domestic-res-full",
    "domestic-res-lim",
    "domestic-nores-full",
    "domestic-nores-lim",
]

SCENARIO_GROUPS = {
    "by_climate": {
        "abroad": {
            "abroad-res-full": "res-full",
            "abroad-res-lim": "res-lim",
            "abroad-nores-full": "nores-full",
            "abroad-nores-lim": "nores-lim",
        },
        "domestic": {
            "domestic-res-full": "res-full",
            "domestic-res-lim": "res-lim",
            "domestic-nores-full": "nores-full",
            "domestic-nores-lim": "nores-lim",
        },
    },
    "by_target": {
        "res": {
            "abroad-res-full": "abroad-full",
            "abroad-res-lim": "abroad-lim",
            "domestic-res-full": "domestic-full",
            "domestic-res-lim": "domestic-lim",
        },
        "nores": {
            "abroad-nores-full": "abroad-full",
            "abroad-nores-lim": "abroad-lim",
            "domestic-nores-full": "domestic-full",
            "domestic-nores-lim": "domestic-lim",
        },
    },
    "by_electrification": {
        "full": {
            "abroad-res-full": "abroad-res",
            "abroad-nores-full": "abroad-nores",
            "domestic-res-full": "domestic-res",
            "domestic-nores-full": "domestic-nores",
        },
        "lim": {
            "abroad-res-lim": "abroad-res",
            "abroad-nores-lim": "abroad-nores",
            "domestic-res-lim": "domestic-res",
            "domestic-nores-lim": "domestic-nores",
        },
    },
}

DEFAULT_COLUMNS = ["model", "scenario_name", "scenario_variant", "year", "value"]

CONTRACT_SPECS = {
    "result_electricity_supply": {
        "aggregation": {"technology": {"level": 1, "keep": ["spv","wind","geothermal_pp"]}},
        "stack_col": "technology",
        "stack_order": [
            "hydro",
            "nuclear",
            "spv",
            "wind",
            "geothermal_pp",
            "methane_pp",
            "hydrogen_pp",
            "liquids_pp",
            "waste_pp",
            "wood_pp",
            "battery_out",
            "vehicle_to_grid",
            "phs_out",
            "imports",

        ],
        "colors": {
            "hydro": "#0377CA",
            "nuclear": "#FF007F",
            "spv": "#FAC748",
            "wind": "#F2960E",
            "geothermal_pp": "#ac79c4",
            "methane_pp": "#1f6228",
            "hydrogen_pp": "#03CBA0",
            "liquids_pp": "#4B4EFC",
            "waste_pp": "#b82222",
            "wood_pp": "#a9807c",
            "battery_out": "#939CAC",
            "vehicle_to_grid": "#09c5c9",
            "phs_out": "#193C78",
            "imports": "#CCCCCC",
        },
    },

    "result_liquids_supply": {
        "aggregation": {"technology": {"level": 1}},
        "stack_col": "technology",
        "stack_order": [
            "imports_biodiesel",
            "imports_diesel",
            "power_to_liquid",
            "waste_liquefaction",
            "wood_liquefaction",
            "liquefaction",
        ],
        "colors": {
            "imports_biodiesel": "#8dd3c7",
            "imports_diesel": "#d9d9d9",
            "power_to_liquid": "#9751CB",
            "waste_liquefaction": "#b82222",
            "wood_liquefaction": "#a9807c",
            "liquefaction": "#2b7bba",
        },
    },
    "result_h2_supply": {
        "aggregation": {"technology": {"level": 1}},
        "stack_col": "technology",
        "stack_order": [
            "electrolyser",
            "steam_reforming",
            "methane_pyrolysis",
            "waste_gasification_h2",
            "wood_gasification_h2",
            "imports",
        ],
        "colors": {
            "electrolyser": "#FAC748",
            "steam_reforming": "#1f6228",
            "methane_pyrolysis": "#2b7bba",
            "waste_gasification_h2": "#b82222",
            "wood_gasification_h2": "#a9807c",
            "imports": "#CCCCCC",
        },
    },

    "result_methane_supply": {
        "aggregation": {"technology": {"level": 1}},
        "stack_col": "technology",
        "stack_order": [
            "anaerobic_digestion",
            "methanation",
            "wood_gasification_methane",
            "waste_gasification_methane",
            "imports_methane",
            "imports_gas",
        ],
        "colors": {
            "anaerobic_digestion": "#1f6228",
            "methanation": "#2874A6",
            "wood_gasification_methane": "#b82222",
            "waste_gasification_methane": "#a9807c",
            "imports_methane": "#8dd3c7",
            "imports_gas": "#d9d9d9",
        },
    },
    "result_electricity_consumption": {
        "aggregation": {"sector": {"level": 0, "keep": ["electrolysis"]}},
        "stack_col": "sector",
        "stack_order": [
            "elec_appliances",
            "rail",
            "passenger",
            "freight_road"
            "space_heating",
            "process_heat",
            "electrolysis",
            "fuel_production",
            "dac",
            "storage",
            "exports",
            "grid_losses",

        ],
        "colors": {
            "elec_appliances": "#097F6D",
            "rail": "#066256",
            "passenger": "#09c5c9",
            "freight_road": "#30B0B2",
            "space_heating": "#F2960E",
            "process_heat": "#CF4832",
            "electrolysis": "#F5DD1B",
            "fuel_production": "#1F4E79",
            "dac": "#9751CB",
            "storage": "#939CAC",
            "exports": "#CCCCCC",
            "grid_losses": "#8B5A2B",
        },
    },
    "result_liquids_consumption": {
        "aggregation": {"sector": {"level": 0}},
        "stack_col": "sector",
        "stack_order": [
            "elec_generation",
            "freight_road",
            "passenger",
            "space_heating",
            "process_heat",
            "fuel_synthesis",
            "storage",
            "exports",
        ],
        "colors": {
            "elec_generation": "#9751CB",
            "freight_road": "#8B5349",
            "passenger": "#09c5c9",
            "space_heating": "#F2960E",
            "process_heat": "#CF4832",
            "fuel_synthesis": "#1F4E79",
            "storage": "#939CAC",
            "exports": "#CCCCCC",
        },
    },
    "result_h2_fec": {
        "aggregation": {"sector": {"level": 0}},
        "stack_col": "sector",
        "stack_order": [
            "elec_generation",
            "freight_road",
            "passenger",
            "space_heating",
            "process_heat",
            "fuel_synthesis",
            "storage",
            "exports",
        ],
        "colors": {
            "elec_generation": "#9751CB",
            "freight_road": "#8B5349",
            "passenger": "#09c5c9",
            "space_heating": "#F2960E",
            "process_heat": "#CF4832",
            "fuel_synthesis": "#1F4E79",
            "storage": "#939CAC",
            "exports": "#CCCCCC",
        },
    },
    "result_methane_consumption": {
        "aggregation": {"sector": {"level": 0}},
        "stack_col": "sector",
        "stack_order": [
            "elec_generation",
            "freight_road",
            "passenger",
            "space_heating",
            "process_heat",
            "fuel_synthesis",
            "storage",
            "exports",
        ],
        "colors": {
            "elec_generation": "#9751CB",
            "freight_road": "#8B5349",
            "passenger": "#09c5c9",
            "space_heating": "#F2960E",
            "process_heat": "#CF4832",
            "fuel_synthesis": "#1F4E79",
            "storage": "#939CAC",
            "exports": "#CCCCCC",
        },
    },
    "result_passenger_road_private_fec": {
        "aggregation": {"sector": ["electricity", "liquids", "h2", "methane"]},
        "stack_col": "sector",
        "stack_order": [
            "electricity",
            "liquids",
            "methane",
            "h2",
        ],
        "colors": {
            "electricity": "#0377CA",
            "liquids": "#b82222",
            "methane": "#1f6228",
            "h2": "#03CBA0",
        },
    },
}

VARIABLES = {
    "electricity": {
        "supply": "result_electricity_supply",
        "consumption": "result_electricity_consumption",
        "axis_title": "Electricity (TWh)",
        "lim": (0, 150),
        "signed_lim": (-100, 150),
    },
    # "liquids": {
    #     "supply": "result_liquids_supply",
    #     "consumption": "result_liquids_consumption",
    #     "axis_title": "Liquids (TWh)",
    #     "lim": (0, 50),
    #     "signed_lim": (-50, 50),
    # },
    # "h2": {
    #     "supply": "result_h2_supply",
    #     "consumption": "result_h2_fec",
    #     "axis_title": "Hydrogen (TWh)",
    #     "lim": (0, 30),
    #     "signed_lim": (-30, 30),
    # },
    # "methane": {
    #     "supply": "result_methane_supply",
    #     "consumption": "result_methane_consumption",
    #     "axis_title": "Methane (TWh)",
    #     "lim": (0, 20),
    #     "signed_lim": (-20, 20),
    # },
    # "passenger_transport": {
    #     "supply": "result_passenger_road_private_fec",
    #     "axis_title": "Passenger transport (TWh)",
    #     "lim": (0, 30),
    #     # no consumption
    #     # no signed_lim needed
    # },
}
COMMON_STYLE = {
    "grid": True,
    "grid_color": "gray",
    "grid_linestyle": "dashed",
    "grid_linewidth": 0.8,
    "group_gap": 0.8,
    "bar_size": 0.75,
    "show_group_separators": True,
}

NO_LEGEND = {"show": False}
RIGHT_LEGEND = {"show": True, "loc": "center left", "bbox_to_anchor": (1.02, 0.5)}
BEST_LEGEND = {"show": True, "loc": "best"}


VARIABLE_PLOT_PLANS = {
    key: {
        "horizontal_grouped": {
            "group_cols": ["model", "scenario_label"],
            "group_orders": {
                "model": MODEL_ORDER,
                "scenario_label": SCENARIOS_ORDER,
            },
            "layout_overrides": {
                "group_col": "model",
                "left_inner_label_col": "scenario_label",
                "right_outer_label_col": "model",
            },
            "style_overrides": {
                **COMMON_STYLE,
            },
            "legend_overrides": BEST_LEGEND,
            "drop_empty_bars": False,
        },
        "vertical_grouped": {
            "group_cols": ["scenario_label", "model"],
            "group_orders": {
                "scenario_label": SCENARIOS_ORDER,
                "model": MODEL_ORDER,
            },
            "layout_overrides": {
                "group_col": "scenario_label",
                "bottom_inner_label_col": "model",
                "bottom_outer_label_col": "scenario_label",
            },
            "style_overrides": {
                **COMMON_STYLE,
            },
            "legend_overrides": BEST_LEGEND,
            "drop_empty_bars": False,
        },
        "horizontal_faceted": {
            "group_cols": ["model", "scenario_label"],
            "group_orders": {
                "model": MODEL_ORDER,
                "scenario_label": SCENARIOS_ORDER,
            },
            "layout_overrides": {
                "facet_col": "model",
                "facet_title_col": "model",
                "left_inner_label_col": "scenario_label",
            },
            "style_overrides": {
                **COMMON_STYLE,
            },
            "legend_overrides": RIGHT_LEGEND,
            "drop_empty_bars": False,
        },
        "horizontal_faceted_grouped": {
            "group_cols": ["by_climate", "model", "sce_label_by_climate"],
            "group_orders": {
                "by_climate": [
                    "abroad",
                    "domestic",
                ],
                "model": MODEL_ORDER,
                "sce_label_by_climate": [
                    "res-full",
                    "res-lim",
                    "nores-full",
                    "nores-lim",
                ],
            },
            "layout_overrides": {
                "facet_col": "by_climate",
                "facet_title_col": "by_climate",
                "group_col": "model",
                "left_inner_label_col": "sce_label_by_climate",
                "right_outer_label_col": "model",
            },
            "style_overrides": {
                **COMMON_STYLE,
            },
            "legend_overrides": RIGHT_LEGEND,
            "drop_empty_bars": False,
        },
        "vertical_faceted_grouped": {
            "group_cols": ["by_climate", "model", "sce_label_by_climate"],
            "group_orders": {
                "by_climate": [
                    "abroad",
                    "domestic",
                ],
                "model": MODEL_ORDER,
                "sce_label_by_climate": [
                    "res-full",
                    "res-lim",
                    "nores-full",
                    "nores-lim",
                ],
            },
            "layout_overrides": {
                "facet_col": "by_climate",
                "facet_title_col": "by_climate",
                "group_col": "model",
                "bottom_inner_label_col": "sce_label_by_climate",
                "bottom_outer_label_col": "model",
            },
            "style_overrides": {
                **COMMON_STYLE,
            },
            "legend_overrides": RIGHT_LEGEND,
            "drop_empty_bars": False,
        },
        "signed_supply_vs_demand": {
            "group_cols": ["model", "scenario_label"],
            "group_orders": {
                "model": MODEL_ORDER,
                "scenario_label": SCENARIOS_ORDER,
            },
            "layout_overrides": {
                "group_col": "model",
                "left_inner_label_col": "scenario_label",
                "right_outer_label_col": "model",
            },
            "style_overrides": {
                **COMMON_STYLE,
                "mirror_limits": True,
            },
            "legend_overrides": BEST_LEGEND,
            "drop_empty_bars": False,
        },
    }
    for key in VARIABLES.keys()
}

BAR_SPECS = figures_templates.build_bar_specs(
    variables=VARIABLES,
    variable_plot_plans=VARIABLE_PLOT_PLANS,
)