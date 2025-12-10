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
           #{'name': 'Nexus-e+\nEP2050+', 'file': 'resultsCross_Nexuse-EP','summer':'Jul 02','winter':'Feb 08','color':'#BCBD21'},
           #{'name': 'SecMod', 'id': 'secmod','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#9565BD'},
          {'name': 'SES', 'id':'ses','summer':'Typical day','summerDay':'01.08.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#1E75B3'},
          {'name': 'SES-ETH', 'id': 'seseth','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#2A9E2A'}
          #{'name': 'STEM', 'id': 'stem','summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#D52426'},
          # {'name': 'ZEN-Garden','id':'zengarden', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#00BFC4'},
         #{'name': 'Empa', 'file': 'resultsCross_VSE','summer':'Jul 11','winter':'Feb 15','color':'#8B5349'},
          #{'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

# Create the object that produces the plots and processes the data
# Name of the csv file with the results 
fileResults = "results/nuclear_results_20251201_2050_sesfixed"
# Scenario names and corresponding colors 
sce = ['abroad-resnuc-high','abroad-resnuc-medium','abroad-resnuc-low','abroad-resnuc-phaseout','abroad-res-high','abroad-res-medium','abroad-res-low','abroad-res-phaseout','abroad-nores-high','abroad-nores-medium','abroad-nores-low','abroad-nores-phaseout']
sceColors = ['#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E','#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E']
# Folders where the plots will be created
folder_plots='presentation_latex_nuc/figures_2025_12_02'


cross_plots = plots.Plots(fileResults,model_list,sce,sceColors,folder_plots) 





# # Annual electricity supply with total imports and exports

# Scatter plot with net supply
listModels = cross_plots.modelsid #any model can be excluded, the list should include the model ids
varName = 'electricity_supply'
use_technology_fuel = 'total'
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 101
fileName = 'elecSupply'
year = '2050'
scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','reference'):'Phase-out',
        ('abroad-resnuc-high','reference'):'High cost',
        ('abroad-resnuc-medium','reference'):'Medium cost',
        ('abroad-resnuc-low','reference'):'Low cost',
    }


cross_plots.plotScatter(
    listModelsid=listModels,
    listSce=scenarios,
    varName=varName,
    use_technology_fuel=use_technology_fuel,
    year=year,
    scale=1,
    label="Electricity (TWh)",
    figmax=xmax,
    fileName=fileName,
    width=5, height=12,
    orientation="horizontal",
    group_by="model",
)

cross_plots.plotScatter(
    listModelsid=listModels,
    listSce=scenarios,
    varName=varName,
    use_technology_fuel=use_technology_fuel,
    year=year,
    scale=1,
    label="Electricity (TWh)",
    figmax=xmax,
    fileName=fileName,
    width=12, height=5,
    orientation="vertical",
    group_by="model",
)





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
year = '2050'
scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','reference'):'Phase-out',
        ('abroad-resnuc-high','reference'):'High cost',
        ('abroad-resnuc-medium','reference'):'Medium cost',
        ('abroad-resnuc-low','reference'):'Low cost',
    }


cross_plots.plotBarHorizontal(
    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_supply_net, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=5, height=12,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


cross_plots.plotBarVertical(
    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_supply_net, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
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
year = '2050'
scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-phaseout','reference'):'Phase-out',
        ('abroad-resnuc-high','reference'):'High cost',
        ('abroad-resnuc-medium','reference'):'Medium cost',
        ('abroad-resnuc-low','reference'):'Low cost',
    }


cross_plots.plotBarHorizontal(
    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_use_net, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=5, height=12,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


cross_plots.plotBarVertical(
    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_use_net, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=True,          # <--- one plot
)


map_sce_xaxis ={
        # ('scenario-id','variant'): 'label'
        ('abroad-resnuc-high','reference'):('resnuc',12000),
        ('abroad-resnuc-medium','reference'):('resnuc',8000),
        ('abroad-resnuc-low','reference'):('resnuc',5000),
        ('abroad-res-high','reference'):('res',12000),
        ('abroad-res-medium','reference'):('res',8000),
        ('abroad-res-low','reference'):('res',5000),
    }

listModels = cross_plots.modelsid #any model can be excluded, the list should include the model ids
varName = 'installed_capacity'
use_technology_fuel = 'nuclear'
xlabel = 'Overnight capital cost (EUR/kW)'
ylabel = 'Nuclear capacity (GW)'
fileName = 'nucCap_occ'
year = '2050'



cross_plots.plotLineByScenario(
    listModelsid = listModels,
    map_sce_xaxis = map_sce_xaxis,
    varName = varName,
    use_technology_fuel = use_technology_fuel,
    year = year,
    scale = 1,  # if values are MW → GW, etc.
    xlabel = xlabel,
    ylabel = ylabel,
    fileName = fileName,
    width = 18,
    height = 10,
)
