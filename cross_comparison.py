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
          {'name': 'SecMod', 'id': 'secmod','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#9565BD'},
          {'name': 'SES', 'id': 'ses','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#1E75B3'},
          {'name': 'SES-ETH', 'id': 'seseth','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#2A9E2A'},
          {'name': 'STEM', 'id': 'stem','summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#D52426'},
          {'name': 'ZEN-Garden','id':'zengarden', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#00BFC4'},
         #{'name': 'Empa', 'file': 'resultsCross_VSE','summer':'Jul 11','winter':'Feb 15','color':'#8B5349'},
          #{'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

# Create the object that produces the plots and processes the data
# Name of the csv file with the results 
fileResults = "results/results_cross_2025_12_17"
# Scenario names and corresponding colors 
sce = ['abroad-res-full','abroad-res-lim','domestic-res-full','domestic-res-lim','abroad-nores-full','abroad-nores-lim','domestic-nores-full','domestic-nores-lim',]
sceColors = ['#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E']
# Folders where the plots will be created
folder_plots='presentation_latex/figures_2025_10_25'



cross_plots = plots.Plots(fileResults,model_list,sce,sceColors,folder_plots) 
year = 2050
scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-res-full','reference'):'abroad-res-full',
        ('abroad-res-lim','reference'):'abroad-res-lim',
        ('abroad-nores-full','reference'):'abroad-nores-full',
        ('abroad-nores-lim','reference'):'abroad-nores-lim',
        ('domestic-res-full','reference'):'domestic-res-full',
        ('domestic-res-lim','reference'):'domestic-res-lim',
        ('domestic-nores-full','reference'):'domestic-nores-full',
        ('domestic-nores-lim','reference'):'domestic-nores-lim',
    }

# # Annual electricity supply with total imports and exports

# Scatter plot with net supply
listModels = cross_plots.modelsid #any model can be excluded, the list should include the model ids
varName = 'electricity_supply'
use_technology_fuel = 'total'
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 120
fileName = 'elecSupply'
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
    width=8, height=20,
    orientation="horizontal",
    # width=20, height=8,
    # orientation="vertical",
    group_by="scenario",
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
xmax = 120
fileName = 'elecSupply_tech_net'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

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
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


# Electricity consumption by use with total exports
# Available variables: https://sweet-cross.github.io/instructions-data/docs/sets/use_elec/

varList_use_net = [
#    {'name':'Total','data':['Electricity-consumption|Total demand'],'color':'#8E8900'},
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Trains','data':['passenger_rail','freight_rail'],'color':'#066256'},
    {'name':'Road transport','data':['road_public','road_private','truck','ldv'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'],'color':'#CF4832'},
    {'name':'Power to liquids','data':['power_to_liquid'],'color':'#4B4EFC'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'},
    {'name':'CCS','data':['dac'],'color':'#9751CB'},
    #{'name':'Storage','data':['battery_in','phs_in'],'color':'#939CAC'},
    # {'name':'Exports','data':['exports'],'color':'#CCCCCC'},
    # {'name':'Losses','data':['grid_losses'],'color':'#8B5A2B'}
    {'name':'Storage','data':['net_storage_in'],'color':'#939CAC'},
    {'name':'Net-exports','data':['net_exports'],'color':'#CCCCCC'},
    {'name':'Losses','data':['grid_losses','storage_losses'],'color':'#8B5A2B'}
    ]

varName = 'electricity_consumption'
listModels = cross_plots.modelsid
xlabel = 'Electricity (TWh)'
xmax = 120
fileName = 'elecUse_net'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_use_net, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=True, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=20, height=8,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)





# Hourly plots

signedVarList_supply_use = [
    {'name':'Hydro', "varName":"electricity_supply_typical_day",'techs':['hydro_dam','hydro_ror'], "sign": +1,'color':'#0377CA'},
    {'name':'Nuclear', "varName":"electricity_supply_typical_day",'techs':['nuclear'], "sign": +1,'color':'#FF007F'},
    {'name':'Solar', "varName":"electricity_supply_typical_day",'techs':['spv'], "sign": +1,'color':'#FAC748'},
    {'name':'Wind', "varName":"electricity_supply_typical_day",'techs':['wind'], "sign": +1,'color':'#F2960E'},
    {'name':'Geothermal', "varName":"electricity_supply_typical_day",'techs':['geothermal_pp'], "sign": +1,'color':'#ac79c4'},
    {'name':'Methane', "varName":"electricity_supply_typical_day",'techs':["methane_pp",'fuel_cell_methane'], "sign": +1,'color':'#1f6228'},
    {'name':'Hydrogen', "varName":"electricity_supply_typical_day",'techs':['hydrogen_pp','fuel_cell_h2'], "sign": +1,'color':'#03CBA0'},
    {'name':'Liquids', "varName":"electricity_supply_typical_day",'techs':['liquids_pp'], "sign": +1,'color':'#4B4EFC'},
    {'name':'Waste', "varName":"electricity_supply_typical_day",'techs':['waste_pp'], "sign": +1,'color':'#b82222'},
    {'name':'Wood', "varName":"electricity_supply_typical_day",'techs':['wood_pp'], "sign": +1,'color':'#a9807c'},
    {'name':'Storage', "varName":"electricity_supply_typical_day",'techs':['net_storage_out'], "sign": +1,'color':'#939CAC'},
    {'name':'Net-imports', "varName":"electricity_supply_typical_day",'techs':['net_imports'], "sign": +1,'color':'#CCCCCC'},
    {'name':'Base', "varName":"electricity_consumption_typical_day",'techs':['elec_appliances'], "sign": -1,'color':'#097F6D'},
    {'name':'Trains', "varName":"electricity_consumption_typical_day",'techs':['passenger_rail','freight_rail'], "sign": -1,'color':'#066256'},
    {'name':'Road transport', "varName":"electricity_consumption_typical_day",'techs':['road_public','road_private','truck','ldv'], "sign": -1,'color':'#09c5c9'},
    {'name':'Space heating', "varName":"electricity_consumption_typical_day",'techs':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'], "sign": -1,'color':'#F2960E'},
    {'name':'Process heat', "varName":"electricity_consumption_typical_day",'techs':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'], "sign": -1,'color':'#CF4832'},
    {'name':'Power to liquids', "varName":"electricity_consumption_typical_day",'techs':['power_to_liquid'], "sign": -1,'color':'#4B4EFC'},
    {'name':'Electrolysis', "varName":"electricity_consumption_typical_day",'techs':['electrolysis'], "sign": -1,'color':'#F5DD1B'},
    {'name': 'Data centers', "varName":"electricity_consumption_typical_day" ,'techs': ['data_centers'], "sign": -1, 'color': '#4A90E2'},
    {'name':'Others', "varName":"electricity_consumption_typical_day",'techs':['dac','data_centers'], "sign": -1,'color':'#9751CB'},
    {'name':'Storage', "varName":"electricity_consumption_typical_day",'techs':['net_storage_in'], "sign": -1,'color':'#939CAC'},
    {'name':'Net-exports', "varName":"electricity_consumption_typical_day",'techs':['net_exports'], "sign": -1,'color':'#CCCCCC'},
    {'name':'Losses', "varName":"electricity_consumption_typical_day",'techs':['grid_losses','storage_losses'], "sign": -1,'color':'#8B5A2B'}
]

day_by_model = {
    "stem": "01.02.2050",
    "secmod": "01.02.2050",
}

cross_plots.plotHourlySignedProfile(
    listModelsid=["stem","zen_garden","secmod"],
    listSce=[ ('abroad-res-full','reference')],   # exactly one scenario/variant
    signedVarList=signedVarList_supply_use,
    day_by_model=day_by_model,
    time_resolution="typical-day",                # or "hourly"
    scale=1,
    ylabel="Electricity (GW)",
    fileName="electricity_hourly_signed",
    ymin=-60, ymax=100,                           # <- asymmetric limits
    pos_legend={"loc":"lower center","bbox_to_anchor":(0.5,-0.12),"ncol":4},
)



# Distribution box plot of annual electricity supply by technology


# name: name of the technology or group of technologies (valid names: https://sweet-cross.github.io/instructions-data/docs/sets/tech_generation/)
# data: list with the technologies that correspond to this category
varList_supply = [
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Nuc.','data':['nuclear'],'color':'#FF007F'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geoth.','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Gas','data':["methane_pp",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'H2','data':['hydrogen_pp','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_pp'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_pp'],'color':'#b82222'},
    {'name':'Wood','data':['wood_pp'],'color':'#a9807c'},
    ]

varName = 'electricity_supply'
listModels = cross_plots.modelsid
order = ["Hydro",'Solar','Wind','Nuc.','Waste','Gas','Wood','Geoth.','H2','Liquids']
ylabel = 'Electricity (TWh)'
ymax = 70
fileName = 'elecDist_tech'
year = '2050'
legend = False

cross_plots.plotTechDist(listModels,varName,varList_supply,year,order,ylabel,ymax,fileName,legend)




# Distribution of annual electricity use by use

# name: name of the technology or group of technologies
# data: list with the technologies that correspond to this category
varList_use_dist = [
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Passenger','data':['road_public','road_private'],'color':'#09c5c9'},
    {'name':'Freight','data':['truck','ldv'],'color':'#09c5c9'},
    {'name':'Space\nheating','data':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'],'color':'#F2960E'},
    {'name':'Process\nheat','data':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'],'color':'#CF4832'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'}
  ]

varName = 'electricity_consumption'
listModels = cross_plots.modelsid
order = ["Base",'Passenger','Freight','Space\nheating','Process\nheat','Electrolysis']
ylabel = 'Electricity (TWh)'
ymax =50
fileName = 'elecUseDist_use'
year = '2050'
legend = False

cross_plots.plotTechDist(listModels,varName,varList_use_dist,year,order,ylabel,ymax,fileName,legend)

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
xmax = 15
fileName = 'h2Supply_tech'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_h2_supply, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


 
# Hydrogen consumption by use https://sweet-cross.github.io/instructions-data/docs/sets/use_hydrogen/

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
xmax = 15
fileName = 'h2Use'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_h2_consump, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=True, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=20, height=8,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Methane supply by technology  https://sweet-cross.github.io/instructions-data/docs/sets/tech_methane/
varList_methane_supply = [
    {'name':'Anaerobic digestion','data':['anaerobic_digestion'],'color':'#1f6228'},
    {'name':'Gasification','data':['wood_gasification_methane','waste_gasification_methane'],'color':'#a9807c'},
    {'name':'Methanation','data':['methanation'],'color':'#2874A6'},
    {'name':'Imports','data':['imports_methane','imports_gas'],'color':'#CCCCCC'}
    ]

varName = 'methane_supply'
listModels = cross_plots.modelsid
xlabel = 'Methane (TWh)'
xmax = 20
fileName = 'methaneSupply_tech'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_methane_supply, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Methane consumption by use https://sweet-cross.github.io/instructions-data/docs/sets/use_methane/

varList_methane_consump = [
    {'name':'Electricity','data':['elec_generation'],'color':'#9751CB'},
    {'name':'Freight','data':['truck','ldv'],'color':'#8B5349'},
    {'name':'Passengers','data':['passenger_road_public','passenger_road_private'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat'],'color':'#CF4832'},
    {'name':'Fuel syntheis','data':['fuel_synthesis'],'color':'#1F4E79'},
     {'name':'Storage','data':['storage'],'color':'#939CAC'},
    {'name':'Exports','data':['exports'],'color':'#CCCCCC'}
    ]

varName = 'methane_fec'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Methane (TWh)'
xmax = 20
fileName = 'methaneUse'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_methane_consump, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=True, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=20, height=8,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


# Liquids supply by technology https://sweet-cross.github.io/instructions-data/docs/sets/tech_liquids/
varList_liquids_supply = [
        {'name':'Power-to-liquids','data':['power_to_liquid'],'color':'#9751CB'},
        {'name':'Liquefaction','data':['wood_liquefaction','waste_liquefaction'],'color':'#a9807c'},
        {'name':'Imports','data':['imports_diesel','imports_biodiesel'],'color':'#CCCCCC'}
        ]
    
varName = 'liquids_supply'
listModels = cross_plots.modelsid
xlabel = 'Liquid fuels (TWh)'
xmax = 50
fileName = 'liquidsSupply_tech'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_liquids_supply, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Liquids consumption by use https://sweet-cross.github.io/instructions-data/docs/sets/use_liquids/

varList_liquids_consump = [
    {'name':'Electricity','data':['elec_generation'],'color':'#9751CB'},
    {'name':'Freight','data':['truck','ldv'],'color':'#8B5349'},
    {'name':'Passengers','data':['passenger_road_public','passenger_road_private'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat'],'color':'#CF4832'},
    {'name':'Fuel syntheis','data':['fuel_synthesis'],'color':'#1F4E79'},
     {'name':'Storage','data':['storage'],'color':'#939CAC'},
    {'name':'Exports','data':['exports'],'color':'#CCCCCC'}
    ]

varName = 'liquids_fec'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Liquid fuels (TWh)'
xmax = 50
fileName = 'liquidsUse'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_liquids_consump, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=True, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=20, height=8,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Space heating supply by technology https://sweet-cross.github.io/instructions-data/docs/sets/tech_heat/

varList_spaceHeat = [
    {'name':'Heat pumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geothermal','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Methane','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    {'name':'District Heating','data':['district_heat'],'color':'#CCCCCC'},
    ]


varName = 'space_heat_useful_energy_supply'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Space heating (TWh)'
xmax = 80
fileName = 'spaceHeating'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_spaceHeat, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Space heating distribution by technology
varList_dist_spaceheat = [
    {'name':'Heat\npumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geoth.','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Gas','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'H2','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    ]

varName = 'space_heat_useful_energy_supply'
listModels = cross_plots.modelsid
order = ["Heat\npumps",'Wood','Waste','Solar','Geoth.','Gas','H2','Heaters','Liquids']
ylabel = 'Space heating (TWh)'
ymax = 80
fileName = 'spaceHeating_dist'
legend = False


cross_plots.plotTechDist(listModels,varName,varList_dist_spaceheat,year,order,ylabel,ymax,fileName,legend)


# Distric heating supply by technology https://sweet-cross.github.io/instructions-data/docs/sets/tech_heat/

varList_distHeat = [
    {'name':'Heat pumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geothermal','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Methane','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    ]


varName = 'district_heat_useful_energy_production'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'District heating (TWh)'
xmax = 80
fileName = 'districtHeating'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_distHeat, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# District heating distribution by technology
varList_dist_distheat = [
    {'name':'Heat\npumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geoth.','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Gas','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'H2','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    ]

varName = 'district_heat_useful_energy_production'
listModels = cross_plots.modelsid
order = ["Heat\npumps",'Wood','Waste','Solar','Geoth.','Gas','H2','Heaters','Liquids']
ylabel = 'Space heating (TWh)'
ymax = 60
fileName = 'districtHeating_dist'
legend = False
year = '2050'

cross_plots.plotTechDist(listModels,varName,varList_dist_distheat,year,order,ylabel,ymax,fileName,legend)


# Industrial heat supply by technology

varList_indHeat = [
    {'name':'Heat pumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geothermal','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Methane','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    ]

varName = 'process_heat_useful_energy_production'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Process heat (TWh)'
xmax = 40
fileName = 'processHeating'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_indHeat, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Industrial heat distribution by technology
varList_indHeat_dist = [
    {'name':'Heat\npumps','data':['heat_pump'],'color':'#1290A3'},
    {'name':'Heaters','data':['heater_elec','boiler_electrode'],'color':'#FF6F31'},
    {'name':'Solar','data':['solar_thermal'],'color':'#FAC748'},
    {'name':'Geoth.','data':['geothermal_heat'],'color':'#9467BD'},
    {'name':'Gas','data':['boiler_methane','chp_methane'],'color':'#1f6228'},
    {'name':'H2','data':['boiler_h2','chp_h2'],'color':'#03CBA0'},
    {'name':'Liquid','data':['boiler_liquids','chp_liquids'],'color':'#4B4EFC'},
    {'name':'Waste','data':['boiler_waste','chp_waste'],'color':'#b82222'},
    {'name':'Wood','data':['boiler_wood','chp_wood'],'color':'#a9807c'},
    ]

varName = 'process_heat_useful_energy_production'
listModels = cross_plots.modelsid
order = ["Heat\npumps",'Wood','Waste','Solar','Geoth.','Gas','H2','Heaters','Liquid']
ylabel = 'Industrial heat (TWh)'
ymax = 25
fileName = 'processHeating_dist'
legend = False
year = '2050'

cross_plots.plotTechDist(listModels,varName,varList_indHeat_dist,year,order,ylabel,ymax,fileName,legend)



# Transport supply by technology

varList_transport = [
    {'name':'Electricity','data':['electricity'],'color':'#0377CA'},
    {'name':'Liquids','data':['oil','liquids'],'color':'#b82222'},
    {'name':'Biogas','data':['methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['hydrogen'],'color':'#03CBA0'},
    ]

listModels = cross_plots.modelsid


varName = 'passenger_road_private_fec'
xlabel = 'Passenger road private transport (TWh)'
xmax = 30
fileName = 'passenger_road_private_fec'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_transport, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

varName = 'passenger_road_public_fec'
xlabel = 'Passenger road public transport (TWh)'
xmax = 10
fileName = 'passenger_road_public_fec'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_transport, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)
varName = 'freight_road_fec'
xlabel = 'Freight road transport (TWh)'
xmax = 10
fileName = 'freight_road_fec'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=listModels, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_transport, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=8, height=20,
    #width=12, height=5,
    group_by="scenario", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

# Transport distribution by technology
order = ["Electricity",'Liquids','Hydrogen','Methane']
legend = False


varName = 'passenger_road_private_fec'
ylabel = 'Passenger road private transport (TWh)'
ymax = 20
fileName = 'passenger_road_private_fec_dist'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)

varName = 'passenger_road_public_fec'
ylabel = 'Passenger road public transport (TWh)'
ymax = 5
fileName = 'passenger_road_public_fec_dist'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)

varName = 'freight_road_fec'
ylabel = 'Freight road transport (TWh)'
ymax = 5
fileName = 'freight_road_fec_dist'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)


