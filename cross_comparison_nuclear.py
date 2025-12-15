"""Code to produce plots for the CROSS model result comparison using the format for CROSSHub"""

# Copyright (c) 2025, ETH Zurich, Energy Science Center, Adriana Marcucci
# Distributed under the terms of the Apache License, Version 2.0.

from cross_tools import plots 


#  List of files with:
# name: name to be displayed in the plots
# id:  model_id in CROSSHub
# summer: name of the summer day reported by the model
# summerDay: data of the summer typical day in the format dd.mm.yyyy
# winter: name of the winter day reported by the model
# winterDay: data of the winter typical day in the format dd.mm.yyyy
# color: color used for the scatter plots in hex

# color: color to be used for the model in scatter plots
model_list =  [
          #{'name': 'Calliope', 'file': 'resultsCross_Calliope','summer':'Jul 20','winter':'Feb 08','color':'#D57CBE'},
          #{'name': 'Expanse', 'file': 'resultsCross_Expanse','summer':'Jul 02','winter':'Jan 01','color':'#FF7D0D'},
          {'name': 'Nexus-e', 'id':'nexuse','summer':'Typical day','summerDay':'02.07.2050','winter':'Typical day','winterDay':'08.02.2050','color':'#BCBD21'},
          #{'name': 'SecMod', 'id': 'secmod','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#9565BD'},
          {'name': 'SES', 'id':'ses','summer':'Typical day','summerDay':'01.08.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#1E75B3'},
          {'name': 'SES-ETH', 'id': 'seseth','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#2A9E2A'},
          {'name': 'STEM', 'id': 'stem','summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#D52426'},
          # {'name': 'ZEN-Garden','id':'zengarden', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#00BFC4'},
         #{'name': 'Empa', 'file': 'resultsCross_VSE','summer':'Jul 11','winter':'Feb 15','color':'#8B5349'},
          #{'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

# Create the object that produces the plots and processes the data
# Name of the csv file with the results 
fileResults = "results/nuclear_results_20251211"
# Scenario names and corresponding colors 
sce = ['abroad-resnuc-high','abroad-resnuc-medium','abroad-resnuc-low','abroad-resnuc-phaseout','abroad-res-high','abroad-res-medium','abroad-res-low','abroad-res-phaseout','abroad-nores-high','abroad-nores-medium','abroad-nores-low','abroad-nores-phaseout']
sceColors = ['#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E','#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E']
# Folders where the plots will be created
folder_plots='presentation_latex_nuc/figures_2025_12_02'


cross_plots = plots.Plots(fileResults,model_list,sce,sceColors,folder_plots) 


# Annual electricity supply with net imports 

# name: name of the technology or group of technologies (valid names: https://sweet-cross.github.io/instructions-data/docs/sets/tech_generation/)
# data: list with the technologies that correspond to this category
# color: color to use for this category
varList_supply_net = [
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Nuclear','data':['nuclear'],'color':'#FF007F'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Methane','data':["methane_pp",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['hydrogen_pp','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_pp'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_pp'],'color':'#b82222'},
    {'name':'Wood','data':['wood_pp'],'color':'#a9807c'},
    {'name':'Storage','data':['net_storage_out'],'color':'#939CAC'},
    {'name':'Net-imports','data':['net_imports'],'color':'#CCCCCC'}
    #     {'name':'Storage','data':['battery_out','phs_out'],'color':'#939CAC'},
    #     {'name':'Imports','data':['imports'],'color':'#CCCCCC'}
   ]

varName = 'electricity_supply'
listModels = cross_plots.modelsid
xlabel = 'Electricity (TWh)'
xmax = 101
fileName = 'elecSupply_tech_net'
year = 2050

scenario_list={
    'nores': {
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-phaseout','wacc_5'):'Phase-out',
        ('abroad-nores-high','wacc_5'):'High cost',
        ('abroad-nores-medium','wacc_5'):'Medium cost',
        ('abroad-nores-low','wacc_5'):'Low cost',
    },
    'res': {
        # ('scenario-id','variant'): 'label'
        ('abroad-res-phaseout','wacc_5'):'Phase-out',
        ('abroad-res-high','wacc_5'):'High cost',
        ('abroad-res-medium','wacc_5'):'Medium cost',
        ('abroad-res-low','wacc_5'):'Low cost',
    },
    'resnuc': {
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','wacc_5'):'Phase-out',
        ('abroad-resnuc-high','wacc_5'):'High cost',
        ('abroad-resnuc-medium','wacc_5'):'Medium cost',
        ('abroad-resnuc-low','wacc_5'):'Low cost',
    },
    }

for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_supply_net, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=False, legend=True,
   #     pos_legend={# This puts the legend outside-right for horizontal plots
   #              "loc": "lower center",
   #              "bbox_to_anchor": (0.5, 1.05),
   #              "ncol": 4,
   #             },
        pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },
   #    pos_legend={ # This puts the legend outside-bottom 
   #     "loc": "upper center",
   #     "bbox_to_anchor": (0.5, -0.15),  #(0.5, -0.15) for vertical plots, this is the shift of the legend 
   #     "ncol": 4,#number of columns of the legend
   #     },
    #    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )


# Hydrogen supply by technology https://sweet-cross.github.io/instructions-data/docs/sets/tech_hydrogen/
varList_h2_supply = [
    {'name':'Electrolysis','data':['electrolyser'],'color':'#FAC748'},
    {'name':'Steam reforming','data':['steam_reforming'],'color':'#1f6228'},
    {'name':'Gasification','data':['wood_gasification_h2','waste_gasification_h2'],'color':'#a9807c'},
    {'name':'Pyrolysis','data':['methane_pyrolysis'],'color':'#A93226'},
    {'name':'Imports','data':['imports'],'color':'#CCCCCC'}
    ]

varName = 'h2_supply'
listModels = cross_plots.modelsid
xlabel = 'Hydrogen (TWh)'
xmax = 40
fileName = 'h2Supply_tech'
year = 2050

for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_h2_supply, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=False, legend=True, 
        pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },
 #    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )


varList_h2_consump = [
    {'name':'Electricity','data':['hydrogen_pp','fuel_cell_h2'],'color':'#9751CB'},
    {'name':'Freight','data':['truck','ldv'],'color':'#8B5349'},
    {'name':'Passengers','data':['passenger_road_public','passenger_road_private'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat'],'color':'#CF4832'},
    {'name':'Fuel synthesis','data':['fuel_synthesis'],'color':'#1F4E79'},
     {'name':'Storage','data':['storage'],'color':'#939CAC'},
    {'name':'Exports','data':['exports'],'color':'#CCCCCC'}
    ]

varName = 'h2_fec'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Hydrogen (TWh)'
xmax = 40
fileName = 'h2Use'
year = 2050
for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_h2_consump, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=False, legend=True, 
        pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },
#    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )


# Electricity consumption by use with net exports
# Available variables: https://sweet-cross.github.io/instructions-data/docs/sets/use_elec/
varList_use_net = [
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Trains','data':['passenger_rail','freight_rail'],'color':'#066256'},
    {'name':'Road transport','data':['road_public','road_private','truck','ldv'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'],'color':'#CF4832'},
    {'name':'Power to liquids','data':['power_to_liquid'],'color':'#4B4EFC'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'},
    {'name': 'Data centers', 'data': ['data_centers'], 'color': '#4A90E2'},
    {'name':'Others','data':['dac','data_centers'],'color':'#9751CB'},
 #  {'name':'Storage','data':['battery_in','phs_in'],'color':'#939CAC'},
 #  {'name':'Exports','data':['exports'],'color':'#CCCCCC'},
    {'name':'Storage','data':['net_storage_in'],'color':'#939CAC'},
    {'name':'Net-exports','data':['net_exports'],'color':'#CCCCCC'},
    {'name':'Losses','data':['grid_losses','storage_losses'],'color':'#8B5A2B'}
    ]

varName = 'electricity_consumption'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 101
fileName = 'elecUse_net'
year = 2050

scenario_list={
    'nores': {
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-phaseout','wacc_5'):'Phase-out',
        ('abroad-nores-high','wacc_5'):'High cost',
        ('abroad-nores-medium','wacc_5'):'Medium cost',
        ('abroad-nores-low','wacc_5'):'Low cost',
    },
    'res': {
        # ('scenario-id','variant'): 'label'
        ('abroad-res-phaseout','wacc_5'):'Phase-out',
        ('abroad-res-high','wacc_5'):'High cost',
        ('abroad-res-medium','wacc_5'):'Medium cost',
        ('abroad-res-low','wacc_5'):'Low cost',
    },
    'resnuc': {
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','wacc_5'):'Phase-out',
        ('abroad-resnuc-high','wacc_5'):'High cost',
        ('abroad-resnuc-medium','wacc_5'):'Medium cost',
        ('abroad-resnuc-low','wacc_5'):'Low cost',
    },
    }


for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_use_net, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=True, legend=True, 
        pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },
#    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )


# Total System Costs
varList_cost = [
    {'name':'Total','data':[''],'color':'#A6A6A6'},
    ]

varName = 'total_system_costs'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Total system costs (Billion CHF)'
xmax = 50
fileName = 'total_system_costs'
year = 2050

scenario_list={
    'nores': {
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-phaseout','wacc_5'):'Phase-out',
        ('abroad-nores-high','wacc_5'):'High cost',
        ('abroad-nores-medium','wacc_5'):'Medium cost',
        ('abroad-nores-low','wacc_5'):'Low cost',
    },
    'res': {
        # ('scenario-id','variant'): 'label'
        ('abroad-res-phaseout','wacc_5'):'Phase-out',
        ('abroad-res-high','wacc_5'):'High cost',
        ('abroad-res-medium','wacc_5'):'Medium cost',
        ('abroad-res-low','wacc_5'):'Low cost',
    },
    'resnuc': {
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','wacc_5'):'Phase-out',
        ('abroad-resnuc-high','wacc_5'):'High cost',
        ('abroad-resnuc-medium','wacc_5'):'Medium cost',
        ('abroad-resnuc-low','wacc_5'):'Low cost',
    },
    }


for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_cost, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=False, legend=False, pos_legend="upper right",
    #    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )

for name, scenarios in scenario_list.items():
    cross_plots.plotScatter(
        listModelsid=listModels,
        listSce=scenarios,
        varName=varName,
        use_technology_fuel='',
        year=year,
        scale=1,
        label=xlabel,
        figmax=xmax,
        fileName = fileName+'_'+name,
        width=12, height=5,
        orientation="vertical",
        group_by="scenario",
    )

# Carbon price
varList_cost = [
    {'name':'Total','data':[''],'color':'#A6A6A6'},
    ]

varName = 'carbon_price'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Carbon price (CHF/tCO2)'
xmax = 500
fileName = 'carbon_price'
year = 2050

scenario_list={
    'nores': {
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-phaseout','wacc_5'):'Phase-out',
        ('abroad-nores-high','wacc_5'):'High cost',
        ('abroad-nores-medium','wacc_5'):'Medium cost',
        ('abroad-nores-low','wacc_5'):'Low cost',
    },
    'res': {
        # ('scenario-id','variant'): 'label'
        ('abroad-res-phaseout','wacc_5'):'Phase-out',
        ('abroad-res-high','wacc_5'):'High cost',
        ('abroad-res-medium','wacc_5'):'Medium cost',
        ('abroad-res-low','wacc_5'):'Low cost',
    },
    'resnuc': {
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','wacc_5'):'Phase-out',
        ('abroad-resnuc-high','wacc_5'):'High cost',
        ('abroad-resnuc-medium','wacc_5'):'Medium cost',
        ('abroad-resnuc-low','wacc_5'):'Low cost',
    },
    }


for name, scenarios in scenario_list.items():
    #cross_plots.plotBarHorizontal(
    cross_plots.plotBarVertical(   
        listModelsid=listModels, 
        listSce=scenarios,
        varName = varName, 
        varList=varList_cost, 
        year=year, 
        scale=1,
        label=xlabel, 
        figmax = xmax,
        fileName = fileName+'_'+name,
        invert=False, legend=False, pos_legend="upper right",
    #    width=5, height=12,
        width=12, height=5,
        group_by="scenario", # 'scenario' or 'model'
        multi=False,          # <--- one plot
    )

#### Capacity vs. cost plot


scenario_groups = {
    "resnuc": {
        "map_sce_xaxis": {
                # ('scenario-id','variant'): 'label'
                ('abroad-resnuc-high','wacc_5'):('wacc_5',12000),
                ('abroad-resnuc-medium','wacc_5'):('wacc_5',8000),
                ('abroad-resnuc-low','wacc_5'):('wacc_5',5000),
                ('abroad-resnuc-high','wacc_8'):('wacc_8',12000),
                ('abroad-resnuc-medium','wacc_8'):('wacc_8',8000),
                ('abroad-resnuc-low','wacc_8'):('wacc_8',5000),
            },
        "extra_values": {
            ('abroad-resnuc-high',   'wacc_8', 'nexuse'): 0.0,
            ('abroad-resnuc-medium', 'wacc_8', 'nexuse'): 0.4,
            ('abroad-resnuc-low',    'wacc_8', 'nexuse'): 1.63,
            ('abroad-resnuc-high',   'wacc_8', 'stem'): 0.4,
            ('abroad-resnuc-medium', 'wacc_8', 'stem'): 1.7,
            ('abroad-resnuc-low',    'wacc_8', 'stem'): 2.8,
            ('abroad-resnuc-high',   'wacc_5', 'stem'): 1.4,
            ('abroad-resnuc-medium', 'wacc_5', 'stem'): 2.3,
            ('abroad-resnuc-low',    'wacc_5', 'stem'): 3.6,
        },
    },
    "nores": {
        "map_sce_xaxis": {
                # ('scenario-id','variant'): 'label'
                ('abroad-nores-high','wacc_5'):('wacc_5',12000),
                ('abroad-nores-medium','wacc_5'):('wacc_5',8000),
                ('abroad-nores-low','wacc_5'):('wacc_5',5000),
                ('abroad-nores-high','wacc_8'):('wacc_8',12000),
                ('abroad-nores-medium','wacc_8'):('wacc_8',8000),
                ('abroad-nores-low','wacc_8'):('wacc_8',5000),

            },
        "extra_values": {
            ('abroad-nores-high',   'wacc_8', 'nexuse'): 0.0,
            ('abroad-nores-medium', 'wacc_8', 'nexuse'): 0.0,
            ('abroad-nores-low',    'wacc_8', 'nexuse'): 0.0,
              ('abroad-nores-high',   'wacc_8', 'stem'): 0.8,
              ('abroad-nores-medium', 'wacc_8', 'stem'): 1.7,
              ('abroad-nores-low',    'wacc_8', 'stem'): 3.3,
              ('abroad-nores-high',   'wacc_5', 'stem'): 1.5,
              ('abroad-nores-medium', 'wacc_5', 'stem'): 3.3,
              ('abroad-nores-low',    'wacc_5', 'stem'): 3.6,
        },
    },
    "res": {
        "map_sce_xaxis": {
                # ('scenario-id','variant'): 'label'
                ('abroad-res-high','wacc_5'):('wacc_5',12000),
                ('abroad-res-medium','wacc_5'):('wacc_5',8000),
                ('abroad-res-low','wacc_5'):('wacc_5',5000),
                ('abroad-res-high','wacc_8'):('wacc_8',12000),
                ('abroad-res-medium','wacc_8'):('wacc_8',8000),
                ('abroad-res-low','wacc_8'):('wacc_8',5000),

            },
        "extra_values": {
            ('abroad-res-high',   'wacc_8', 'nexuse'): 0.0,
            ('abroad-res-medium', 'wacc_8', 'nexuse'): 0.0,
            ('abroad-res-low',    'wacc_8', 'nexuse'): 0.0,
              ('abroad-res-high',   'wacc_8', 'stem'): 0.4,
              ('abroad-res-medium', 'wacc_8', 'stem'): 1.1,
              ('abroad-res-low',    'wacc_8', 'stem'): 1.4,
              ('abroad-res-high',   'wacc_5', 'stem'): 0.7,
              ('abroad-res-medium', 'wacc_5', 'stem'): 1.4,
              ('abroad-res-low',    'wacc_5', 'stem'): 2.4,
        },
    },
}


listModels = cross_plots.modelsid #any model can be excluded, the list should include the model ids
varName = 'installed_capacity'
use_technology_fuel = 'nuclear'
xlabel = 'Overnight capital cost (EUR/kW)'
ylabel = 'Nuclear capacity (GW)'
fileName = 'nucCap_occ'
year = 2050

for group_name, cfg in scenario_groups.items():

    cross_plots.plotLineByScenario(
        listModelsid = listModels,
        map_sce_xaxis = cfg["map_sce_xaxis"],
        varName = varName,
        use_technology_fuel = use_technology_fuel,
        year = year,
        scale = 1,  # if values are MW → GW, etc.
        xlabel = xlabel,
        ylabel = ylabel,
        fileName = fileName+'_'+group_name,
        width = 18,
        height = 10,
        ylim = (0,5),
        extra_values        = cfg["extra_values"], 
    )




#### Imports and exports
fileName = 'elec_imports'
year = 2050

signedVarList = [
    {
        "name": "Imports",
        "varName": "electricity_supply",
        "techs": ["imports"],
        "sign": +1,
        "color": "#cccccc",
    },
    {
        "name": "Exports",
        "varName": "electricity_consumption",
        "techs": ["exports"],
        "sign": -1,
        "color": "#CF4832",
    },
]

scenario_list={
    'nores': {
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-phaseout','wacc_5'):'Phase-out',
        ('abroad-nores-high','wacc_5'):'High cost',
        ('abroad-nores-medium','wacc_5'):'Medium cost',
        ('abroad-nores-low','wacc_5'):'Low cost',
    },
    'res': {
        # ('scenario-id','variant'): 'label'
        ('abroad-res-phaseout','wacc_5'):'Phase-out',
        ('abroad-res-high','wacc_5'):'High cost',
        ('abroad-res-medium','wacc_5'):'Medium cost',
        ('abroad-res-low','wacc_5'):'Low cost',
    },
    'resnuc': {
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','wacc_5'):'Phase-out',
        ('abroad-resnuc-high','wacc_5'):'High cost',
        ('abroad-resnuc-medium','wacc_5'):'Medium cost',
        ('abroad-resnuc-low','wacc_5'):'Low cost',
    },
    }

for name, scenarios in scenario_list.items():
    print(name)
    cross_plots.plotBarVerticalSigned(
        listModelsid=listModels,
        listSce=scenarios,
        signedVarList=signedVarList,
        year=year,
        scale=1,
        label="Electricity (TWh)",
        figmax=100,
        fileName=fileName+"_"+name,
        invert=False,
        legend=True,
        #pos_legend="upper right",
        pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },
        width=12,
        height=5,
        group_by="scenario",  # or "model"
        multi=False,
    )
