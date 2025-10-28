"""Code to produce plots for the CROSS model result comparison using the format for CROSSHub"""

# Copyright (c) 2025, ETH Zurich, Energy Science Center, Adriana Marcucci
# Distributed under the terms of the Apache License, Version 2.0.

from distributions import plots 

# Scenario names
sce = ['abroad-res-full','abroad-res-lim','domestic-res-full','domestic-res-lim','abroad-nores-full','abroad-nores-lim','domestic-nores-full','domestic-nores-lim',]


#  List of files with:
# name: name to be displayed in the plots
# file:  csv file name
# summer: name of the summer day reported by the model
# winter: name of the winter day reported by the model
# color: color to be used for the model in scatter plots
model_list =  [
          #{'name': 'Calliope', 'file': 'resultsCross_Calliope','summer':'Jul 20','winter':'Feb 08','color':'#D57CBE'},
          #{'name': 'Expanse', 'file': 'resultsCross_Expanse','summer':'Jul 02','winter':'Jan 01','color':'#FF7D0D'},
           #{'name': 'Nexus-e+\nEP2050+', 'file': 'resultsCross_Nexuse-EP','summer':'Jul 02','winter':'Feb 08','color':'#BCBD21'},
          {'name': 'SecMod', 'id': 'secmod','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#9565BD'},
          #{'name': 'SES', 'file': 'resultsCross_SES-epfl','summer':'Typical day','winter':'Typical day','color':'#1E75B3'},
          {'name': 'SES-ETH', 'id': 'seseth','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#2A9E2A'},
          {'name': 'STEM', 'id': 'stem','summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#D52426'},
          {'name': 'ZEN-Garden','id':'zengarden', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#00BFC4'},
         #{'name': 'Empa', 'file': 'resultsCross_VSE','summer':'Jul 11','winter':'Feb 15','color':'#8B5349'},
          #{'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

fileResults = "results_20251116"
cross_plots = plots.Plots(fileResults,model_list,sce,'results','plots') 





# Annual electricity supply with total imports and exports

# name: name of the technology or group of technologies
# data: list with the technologies that correspond to this category
# color: color to use for this category
varList_supply = [
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Methane','data':["methane_chp_ccs","methane_chp_woccs","methane_oc_woccs","methane_oc_ccs","methane_cc_woccs","methane_cc_ccs",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['hydrogen_chp','hydrogen_cc','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_chp_woccs','liquids_chp_ccs','liquids_oc_woccs','liquids_oc_ccs','liquids_cc_woccs','liquids_cc_ccs'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_chp_woccs','waste_chp_ccs','waste_cc_woccs','waste_cc_ccs'],'color':'#b82222'},
    {'name':'Wood','data':['wood_chp_woccs','wood_chp_ccs','wood_cc_woccs','wood_cc_ccs'],'color':'#a9807c'},
    {'name':'Storage','data':['battery_out','phs_out'],'color':'#939CAC'},
    {'name':'Imports','data':['imports'],'color':'#CCCCCC'}
   ]

varList_consumption =['battery_in','phs_in','exports']
# Calculate net supply = sum(varList_supply)-sum(varList_consumption)
cross_plots.calculateTotalSupply(varList_supply,varList_consumption)

# Scatter plot with net supply
listModels = cross_plots.modelsid #any model can be excluded, the list should include the model ids
varName = 'electricity_supply'
use_technology_fuel = 'total'
sceColors = ['#9FBA3D','#E9442E','#EC9235','#3F89BD','#8E44AD','#1ABC9C','#F1C40F','#34495E']
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 180
fileName = 'elecSupply.pdf'
year = '2050'

cross_plots.plotScatter(listModels,varName ,use_technology_fuel,year,sceColors,scale,xlabel,xmax,fileName)


# Electricity supply bar plot
varName = 'electricity_supply'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 160
fileName = 'elecSupply_tech.pdf'
right = False #True if model names have to go on the right
legend = False # True if legend has to be displayed
pos_legend = 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_supply,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Annual electricity supply with net imports 

# name: name of the technology or group of technologies
# data: list with the technologies that correspond to this category
# color: color to use for this category
varList_supply_net = [
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Methane','data':["methane_chp_ccs","methane_chp_woccs","methane_oc_woccs","methane_oc_ccs","methane_cc_woccs","methane_cc_ccs",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['hydrogen_chp','hydrogen_cc','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_chp_woccs','liquids_chp_ccs','liquids_oc_woccs','liquids_oc_ccs','liquids_cc_woccs','liquids_cc_ccs'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_chp_woccs','waste_chp_ccs','waste_cc_woccs','waste_cc_ccs'],'color':'#b82222'},
    {'name':'Wood','data':['wood_chp_woccs','wood_chp_ccs','wood_cc_woccs','wood_cc_ccs'],'color':'#a9807c'},
    {'name':'Storage','data':['net_storage_out'],'color':'#939CAC'},
    {'name':'Net-imports','data':['net_imports'],'color':'#CCCCCC'}
   ]

varName = 'electricity_supply'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 120
fileName = 'elecSupply_tech_net.pdf'
right = False #True if model names have to go on the right
legend = False # True if legend has to be displayed
pos_legend = 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''# 'total'
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_supply_net,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Distribution of annual electricity supply by technology

# name: name of the technology or group of technologies
# data: list with the technologies that correspond to this category
varList_wopot = [
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geoth.','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Gas','data':["methane_chp_ccs","methane_chp_woccs","methane_oc_woccs","methane_oc_ccs","methane_cc_woccs","methane_cc_ccs",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'H2','data':['hydrogen_chp','hydrogen_cc','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_chp_woccs','liquids_chp_ccs','liquids_oc_woccs','liquids_oc_ccs','liquids_cc_woccs','liquids_cc_ccs'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_chp_woccs','waste_chp_ccs','waste_cc_woccs','waste_cc_ccs'],'color':'#b82222'},
    {'name':'Wood','data':['wood_chp_woccs','wood_chp_ccs','wood_cc_woccs','wood_cc_ccs'],'color':'#a9807c'},
    ]

varName = 'electricity_supply'
listModels = cross_plots.modelsid
order = ["Hydro",'Solar','Wind','Waste','Gas','Wood','Geoth.','H2','Liquids']
ylabel = 'Electricity (TWh)'
ymax = 50
fileName = 'elecDist_tech.pdf'
year = '2050'
legend = False

cross_plots.plotTechDist(listModels,varName,varList_wopot,year,order,ylabel,ymax,fileName,legend)


# Electricity consumption by use with exports

varList_use = [
#    {'name':'Total','data':['Electricity-consumption|Total demand'],'color':'#8E8900'},
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Trains','data':['passenger_rail','freight_rail'],'color':'#066256'},
    {'name':'Road transport','data':['road_public','road_private','truck','ldv'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'],'color':'#CF4832'},
    {'name':'Power to liquids','data':['power_to_liquid'],'color':'#4B4EFC'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'},
    {'name':'CCS','data':['dac'],'color':'#9751CB'},
    {'name':'Storage','data':['battery_in','phs_in'],'color':'#939CAC'},
    {'name':'Exports','data':['exports'],'color':'#CCCCCC'},
    {'name':'Losses','data':['grid_losses'],'color':'#8B5A2B'}
    ]

varName = 'electricity_consumption'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 160
fileName = 'elecUse.pdf'
right = True #True if model names have to go on the right
legend = False # True if legend has to be displayed
pos_legend = 'lower left' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_use,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Electricity consumption by use with net exports

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
    {'name':'Storage','data':['net_storage_in'],'color':'#939CAC'},
    {'name':'Net-exports','data':['net_exports'],'color':'#CCCCCC'},
    {'name':'Losses','data':['grid_losses'],'color':'#8B5A2B'}
    ]

varName = 'electricity_consumption'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Electricity (TWh)'
xmax = 120
fileName = 'elecUse_net.pdf'
right = True #True if model names have to go on the right
legend = False # True if legend has to be displayed
pos_legend = 'lower left' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_use_net,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)



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
fileName = 'elecUseDist_use.pdf'
year = '2050'
legend = False

cross_plots.plotTechDist(listModels,varName,varList_use_dist,year,order,ylabel,ymax,fileName,legend)

# Hydrogen supply by technology
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
xmax = 30
fileName = 'h2Supply_tech.pdf'
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_h2_supply,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Hydrogen consumption by use

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
xmax = 30
fileName = 'h2Use.pdf'
right = True #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper left' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName,varList_h2_consump,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)



# Methane supply by technology
varList_methane_supply = [
    {'name':'Anaerobic digestion','data':['anaerobic_digestion'],'color':'#1f6228'},
    {'name':'Gasification','data':['wood_gasification_methane','waste_gasification_methane'],'color':'#a9807c'},
    {'name':'Methanation','data':['methanation'],'color':'#2874A6'},
    {'name':'Pyrolysis','data':['methane_pyrolysis'],'color':'#A93226'},
    {'name':'Imports','data':['imports_methane','imports_gas'],'color':'#CCCCCC'}
    ]

varName = 'methane_supply'
listModels = cross_plots.modelsid
xlabel = 'Methane (TWh)'
xmax = 30
fileName = 'methaneSupply_tech.pdf'
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_methane_supply,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Methane consumption by use

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
xmax = 30
fileName = 'methaneUse.pdf'
right = True #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper left' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName,varList_methane_consump,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)



# Liquids supply by technology
varList_liquids_supply = [
    {'name':'Power-to-liquids','data':['power_to_liquid'],'color':'#9751CB'},
    {'name':'Liquefaction','data':['wood_liquefaction','waste_liquefaction'],'color':'#a9807c'},
    {'name':'Imports','data':['imports_diesel','imports_biodiesel'],'color':'#CCCCCC'}
    ]

varName = 'liquids_supply'
listModels = cross_plots.modelsid
xlabel = 'Liquid fuels (TWh)'
xmax = 50
fileName = 'liquidsSupply_tech.pdf'
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName ,varList_liquids_supply,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Liquids consumption by use

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
fileName = 'liquidsUse.pdf'
right = True #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper left' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName,varList_methane_consump,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)



# Space heating supply by technology

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
    {'name':'District Heating','data':['district_heating'],'color':'#CCCCCC'},
    ]


varName = 'space_heat_useful_energy_supply'
listModels = cross_plots.modelsid
scale = 1
xlabel = 'Space heating (TWh)'
xmax = 120
fileName = 'spaceHeating.pdf'
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'upper right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName,varList_spaceHeat,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


# Space heating distribution by technology
varList_dist_spaceheat = [
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

varName = 'space_heat_useful_energy_supply'
listModels = cross_plots.modelsid
order = ["Heat\npumps",'Wood','Waste','Solar','Geoth.','Gas','H2','Heaters','Liquid']
ylabel = 'Space heating (TWh)'
ymax = 120
fileName = 'spaceHeating_dist.pdf'
legend = False
year = '2050'

cross_plots.plotTechDist(listModels,varName,varList_dist_spaceheat,year,order,ylabel,ymax,fileName,legend)


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
fileName = 'processHeating.pdf'
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'

cross_plots.plotBar(listModels,varName,varList_indHeat,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


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
ymax = 14
fileName = 'processHeating_dist.pdf'
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
scale = 1
right = False #True if model names have to go on the right, it invers the axis
legend = True # True if legend has to be displayed
pos_legend = 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
onTopVarName = ''
year = '2050'


varName = 'passenger_road_private_fec'
xlabel = 'Passenger road private transport (TWh)'
xmax = 40
fileName = 'passenger_road_private_fec.pdf'
cross_plots.plotBar(listModels,varName,varList_transport,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)


varName = 'passenger_road_public_fec'
xlabel = 'Passenger road public transport (TWh)'
xmax = 40
fileName = 'passenger_road_public_fec.pdf'
cross_plots.plotBar(listModels,varName,varList_transport,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)

varName = 'freight_road_fec'
xlabel = 'Freight road transport (TWh)'
xmax = 40
fileName = 'freight_road_fec.pdf'
cross_plots.plotBar(listModels,varName,varList_transport,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName)



# Transport distribution by technology
order = ["Electricity",'Liquids','Hydrogen','Methane']
legend = False
year = '2050'

varName = 'passenger_road_private_fec'
ylabel = 'Passenger road private transport (TWh)'
ymax = 20
fileName = 'passenger_road_private_fec_dist.pdf'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)

varName = 'passenger_road_public_fec'
ylabel = 'Passenger road public transport (TWh)'
ymax = 20
fileName = 'passenger_road_public_fec_dist.pdf'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)

varName = 'freight_road_fec'
ylabel = 'Freight road transport (TWh)'
ymax = 20
fileName = 'freight_road_fec_dist.pdf'

cross_plots.plotTechDist(listModels,varName,varList_transport,year,order,ylabel,ymax,fileName,legend)


#Get the hourly data for the variables of interest
varList_supply_h = [
    {'name':'Net-imports','data':['Electricity-supply|Net-imports'],'color':'#CCCCCC'},
    {'name':'Storage out','data':['Electricity-supply|PHS-out','Electricity-supply|Battery-out'],'color':'#939CAC'},
    {'name':'SPV-Battery','data':['Electricity-supply|SPV-battery'],'color':'#FEFF54'},
    {'name':'Solar','data':['Electricity-supply|Solar'],'color':'#FAC748'},
    {'name':'Hydro Dams','data':['Electricity-supply|Hydro Dams'],'color':'#ADD8E6'},
    {'name':'Wind','data':['Electricity-supply|Wind'],'color':'#F2960E'},
    {'name':'Geothermal','data':['Electricity-supply|Geothermal'],'color':'#ac79c4'},
    {'name':'Thermal','data':['Electricity-supply|Biogas','Electricity-supply|Gas','Electricity-supply|Hydrogen','Electricity-supply|Waste','Electricity-supply|Wood'],'color':'#b82222'},
    {'name':'Hydro RoR','data':['Electricity-supply|Hydro RoR'],'color':'#0377CA'},
    ]

varList_use_h = [
    {'name':'Net-exports','data':['Electricity-consumption|Net-exports'],'color':'#CCCCCC'},
    {'name':'Storage in','data':['Electricity-consumption|Battery-In','Electricity-consumption|PHS-In'],'color':'#939CAC'},
    {'name':'EVs','data':['Electricity-consumption|Battery-vehicles'],'color':'#09c5c9'},
    {'name':'Heat pumps','data':['Electricity-consumption|Heat pumps'],'color':'#F2960E'},
    {'name':'Heaters','data':['Electricity-consumption|Electric heaters'],'color':'#CF4832'},
    {'name':'Electrolysis','data':['Electricity-consumption|Electrolysis'],'color':'#F5DD1B'},
    {'name':'Others','data':['Electricity-consumption|New processes'],'color':'#9751CB'},
    {'name':'Trains','data':['Electricity-consumption|Trains'],'color':'#000000'},
    {'name':'Base','data':['Electricity-consumption|Base'],'color':'#097F6D'},
    {'name':'Total','data':['Electricity-consumption|Total demand'],'color':'#8E8900'}
    ]

cross_plots.extractPositiveNegative(varList_supply_h,varList_use_h)

#Plot stacked hourly profiles
listModels = cross_plots.models
positive_variables = varList_supply_h
negative_variables = varList_use_h
ylabel_pos = "Electricity supply (GW)"
ylabel_neg = "Electricity use (GW)"
ymax = 30
legend = False
fileName = 'hourlyElec'

season = "summer"
cross_plots.plotHourlyStack(listModels,positive_variables,negative_variables,season,ylabel_pos,ylabel_neg,ymax,legend,fileName)

season = "winter"
cross_plots.plotHourlyStack(listModels,positive_variables,negative_variables,season,ylabel_pos,ylabel_neg,ymax,legend,fileName)

#Plot hourly profiles by technology
listModels = cross_plots.models

ncols = 3
scenario = "abroad-together"
season = "summer"

varList_elec_supply_dist = ['Net-imports','Solar','Wind','Hydro Dams','Hydro RoR','Storage out','Thermal']
ymax = 27
ylabel = "Electricity use (GWh/h)"
fileName = "hourProfileTech_"+season+"_"+scenario+".pdf"
cross_plots.plotHourProfileTech(listModels,scenario,varList_elec_supply_dist,season,ylabel,ymax,ncols,fileName)


varList_elec_use_dist = ['Net-exports','Electrolysis','Storage in','EVs','Heat pumps','Heaters','Base']
ymax = 15
ylabel = "Electricity use (GWh/h)"
fileName = "hourProfileSupply_"+season+"_"+scenario+".pdf"
cross_plots.plotHourProfileTech(listModels,scenario,varList_elec_use_dist,season,ylabel,ymax,ncols,fileName)


#Plot hourly profiles by technology
listModels = cross_plots.models

ncols = 3
scenario = "abroad-together"
season = "summer"

varList_elec_supply_dist = ['Net-imports','Solar','Wind','Hydro Dams','Hydro RoR','Storage out','Thermal']
ymax = 27
ylabel = "Electricity use (GWh/h)"
fileName = "hourProfileTech_"+season+"_"+scenario+".pdf"
cross_plots.plotHourProfileTech(listModels,scenario,varList_elec_supply_dist,season,ylabel,ymax,ncols,fileName)


varList_elec_use_dist = ['Net-exports','Electrolysis','Storage in','EVs','Heat pumps','Heaters','Base']
ymax = 15
ylabel = "Electricity use (GWh/h)"
fileName = "hourProfileSupply_"+season+"_"+scenario+".pdf"
cross_plots.plotHourProfileTech(listModels,scenario,varList_elec_use_dist,season,ylabel,ymax,ncols,fileName)
