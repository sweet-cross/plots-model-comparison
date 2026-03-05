"""Code to produce plots for the CROSS model result comparison using the format for CROSSHub"""

# Copyright (c) 2025, ETH Zurich, Energy Science Center, Adriana Marcucci
# Distributed under the terms of the Apache License, Version 2.0.

from cross_tools import plots 
import pandas as pd

#  List of files with:
# name: name to be displayed in the plots
# id:  model_id in CROSSHubhttps://www.dropbox.com/scl/fo/shc5n6517j6v1hklws1x4/AKYZjNrliYD7ChaX8HMa6gE?rlkey=31odqrp28kb7xx0h4a2quukhw&dl=0
# summer: name of the summer day reported by the model
# summerDay: data of the summer typical day in the format dd.mm.yyyy
# winter: name of the winter day reported by the model
# winterDay: data of the winter typical day in the format dd.mm.yyyy
# color: color used for the scatter plots in hex

# color: color to be used for the model in scatter plots
model_list =  [
          #{'name': 'Expanse', 'file': 'resultsCross_Expanse','summer':'Jul 02','winter':'Jan 01','color':'#FF7D0D'},
           #{'name': 'Nexus-e+\nEP2050+', 'file': 'resultsCross_Nexuse-EP','summer':'Jul 02','winter':'Feb 08','color':'#BCBD21'},
          {'name': 'EhubX', 'id':'ehub', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#8B5349'},
          #{'name': 'PowerCheck', 'id': 'powercheck','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#D57CBE'},
          {'name': 'SecMod', 'id': 'secmod','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#9565BD'},
          {'name': 'SES', 'id': 'ses','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#1E75B3'},
          {'name': 'SES-ETH', 'id': 'seseth','summer':'Typical day','summerDay':'01.07.2050','winter':'Typical day','winterDay':'01.02.2050','color':'#2A9E2A'},
          {'name': 'STEM', 'id': 'stem','summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#D52426'},
          {'name': 'ZEN-Garden','id':'zengarden', 'summer':'Week day','summerDay':'01.07.2050','winter':'Week day','winterDay':'01.02.2050','color':'#00BFC4'},
          #{'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

# Create the object that produces the plots and processes the data
# Name of the csv file with the results 
fileResults = "results/results_cross_2026_03_04"
# Scenario names and corresponding colors 
sce = [
       {'name': 'abroad-res-full', 'id': 'abroad-res-full','color':'#9FBA3D'},
       {'name': 'domestic-res-full', 'id': 'domestic-res-full','color':'#E9442E'},
       {'name': 'abroad-res-lim', 'id': 'domestic-res-full','color':'#E9442E'},
       {'name': 'domestic-res-lim', 'id': 'domestic-res-full','color':'#EC9235'},
       {'name': 'abroad-nores-full', 'id': 'abroad-res-full','color':'#3F89BD'},
       {'name': 'domestic-nores-full', 'id': 'domestic-res-full','color':'#8E44AD'},
       {'name': 'abroad-nores-lim', 'id': 'domestic-res-full','color':'#F1C40F'},
       {'name': 'domestic-nores-lim', 'id': 'domestic-res-full','color':'#34495E'},
   ]   
scenario_groups = {
#    "RES target": [("abroad-res-full","reference"), ("abroad-res-lim","reference"),("domestic-res-full","reference"), ("domestic-res-lim","reference")],
#    "No-RES target": [("abroad-nores-full","reference"),("abroad-nores-lim","reference"),("domestic-nores-full","reference"),("domestic-nores-lim","reference")],
    "All": [("abroad-res-full","reference"), ("abroad-res-lim","reference"),("domestic-res-full","reference"), ("domestic-res-lim","reference"),("abroad-nores-full","reference"),("abroad-nores-lim","reference"),("domestic-nores-full","reference"),("domestic-nores-lim","reference")],
}     

# Folders where the plots will be created
folder_plots='presentation_workshop2026'



cross_plots = plots.Plots(fileResults,model_list,sce,folder_plots) 
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


# Effect of renewable target

scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-res-full','reference'):'Target',
        ('abroad-nores-full','reference'):'No-target',
    }


# Annual electricity supply with net imports 

# name: name of the technology or group of technologies (valid names: https://sweet-cross.github.io/instructions-data/docs/sets/tech_generation/)
# data: list with the technologies that correspond to this category
# color: color to use for this category
varList_supply_net = [
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Wood','data':['wood_pp'],'color':'#a9807c'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Hydro','data':['hydro_dam','hydro_ror'],'color':'#0377CA'},
    {'name':'Nuclear','data':['nuclear'],'color':'#FF007F'},
    {'name':'Methane','data':["methane_pp",'fuel_cell_methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['hydrogen_pp','fuel_cell_h2'],'color':'#03CBA0'},
    {'name':'Liquids','data':['liquids_pp'],'color':'#4B4EFC'},
    {'name':'Waste','data':['waste_pp'],'color':'#b82222'},
    {'name':'Storage','data':['net_storage_out'],'color':'#939CAC'},
    {'name':'Net-imports','data':['net_imports'],'color':'#CCCCCC'}
    #     {'name':'Storage','data':['battery_out','phs_out'],'color':'#939CAC'},
    #     {'name':'Imports','data':['imports'],'color':'#CCCCCC'}
    ]

varName = 'electricity_supply'
listModels = cross_plots.modelsid
xlabel = 'Electricity (TWh)'
xmax = 100
fileName = 'elecSupply_tech_net_res'
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
    invert=False, legend=False, 
    pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },#"upper right",
    width=8, height=12,
    #width=12, height=5,
    group_by="model", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


renewables = [{'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Wood','data':['wood_pp'],'color':'#a9807c'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
]



list_renewables = [v["name"] for v in renewables]+['total']
scenario_name = [s for s,variant in scenarios]
renewable_data = pd.DataFrame(index=listModels,columns= pd.MultiIndex.from_product([scenario_name,list_renewables],names=('sce', 'tech')))


for m in listModels:
    for s, variant in scenarios:
        total = 0
        for var in renewables:
            total_v=0
            for v in var['data']:
                try:
                    total_v+=cross_plots.annualData.loc[(s,variant,m,varName,v,'annual',2050),'value']
                except:
                    total_v=total_v
            renewable_data.loc[m,(s,var['name'])]=total_v
            total += total_v
        renewable_data.loc[m,(s,'total')]=total

renewable_data.stack(level=0).to_clipboard()



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
xmax = 100
fileName = 'elecUse_net_resTarget'

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
    invert=False, legend=False, 
    pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.6, 0.5),
                },#"upper right",
   
    width=8, height=12,
    #width=20, height=8,
    group_by="model", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


uses = [
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Road transport','data':['road_public','road_private','truck','ldv'],'color':'#09c5c9'},
    {'name':'Space heating','data':['space_heating_boiler_electrode','space_heating_heater_elec','space_heating_heat_pump'],'color':'#F2960E'},
    {'name':'Process heat','data':['process_heat_boiler_electrode','process_heat_heater_elec','process_heat_heat_pump'],'color':'#CF4832'},
    {'name':'Power to liquids','data':['power_to_liquid'],'color':'#4B4EFC'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'},
    {'name':'CCS','data':['dac'],'color':'#9751CB'},
    {'name':'Storage','data':['net_storage_in'],'color':'#939CAC'},
    {'name':'Net-exports','data':['net_exports'],'color':'#CCCCCC'},
    {'name':'Losses','data':['grid_losses','storage_losses'],'color':'#8B5A2B'}
    ]

list_uses = [v["name"] for v in uses]+['total']
scenario_name = [s for s,variant in scenarios]
uses_data = pd.DataFrame(index=listModels,columns= pd.MultiIndex.from_product([scenario_name,list_uses],names=('sce', 'use')))

for m in listModels:
    for s, variant in scenarios:
        total = 0
        for var in uses:
            total_v=0
            for v in var['data']:
                try:
                    total_v+=cross_plots.annualData.loc[(s,variant,m,varName,v,'annual',2050),'value']
                except:
                    total_v=total_v
            uses_data.loc[m,(s,var['name'])]=total_v
            total += total_v
        uses_data.loc[m,(s,'total')]=total
uses_data.stack(level=0).to_clipboard()




# Hourly plots


listModels = cross_plots.modelsid
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


seasons = {
    'winter': {
    "ehub": None,
    "powercheck": "01.02.2050",
    "stem": "01.02.2050",
    "secmod": "01.02.2050",
    "ses": None,
    "zengarden": "01.02.2050",
    "seseth": "01.02.2050",
    },
    'summer': {
    "ehub": None,
    "powercheck": "01.07.2050",
    "stem": "01.07.2050",
    "secmod": "01.07.2050",
    "ses": None,
    "zengarden": "01.07.2050",
    "seseth": "01.07.2050",
    },
    }

for scenario, name in scenarios.items():
    for season, day_by_model in seasons.items(): 
        cross_plots.plotHourlySignedProfile(
            listModelsid=listModels,
            listSce=[ scenario],   # exactly one scenario/variant
            signedVarList=signedVarList_supply_use,
            day_by_model=day_by_model,
            time_resolution="typical-day",               
            scale=1,
            ylabel="Electricity (GW)",
            fileName="electricity_hourly_signed"+"_"+name+"_"+season,
            width=18,
            height=8,
            ymin=-30, ymax=30,                           # <- asymmetric limits
            legend=False,
            pos_legend={"loc":"lower center","bbox_to_anchor":(0.5,-0.12),"ncol":4},
        )

# Effect of reduced electrification




# Transport supply by technology
scenarios={
        # ('scenario-id','variant'): 'label'
        ('abroad-nores-full','reference'):'Full',
        ('abroad-nores-lim','reference'):'Lim',
    }


varList_transport = [
    {'name':'Electricity','data':['electricity'],'color':'#0377CA'},
    {'name':'Liquids','data':['oil','liquids'],'color':'#b82222'},
    {'name':'Methane','data':['methane'],'color':'#1f6228'},
    {'name':'Hydrogen','data':['h2'],'color':'#03CBA0'},
    ]


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
    invert=False, legend=True, pos_legend="lower right",
    width=8, height=12,
    #width=12, height=5,
    group_by="model", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)




# Liquids supply by technology https://sweet-cross.github.io/instructions-data/docs/sets/tech_liquids/
varList_liquids_supply = [
        {'name':'Power-to-liquids','data':['power_to_liquid'],'color':'#9751CB'},
        {'name':'Liquefaction','data':['wood_liquefaction','waste_liquefaction'],'color':'#a9807c'},
        {'name':'Imports','data':['imports_diesel','imports_biodiesel'],'color':'#CCCCCC'}
        ]
    
varName = 'liquids_supply'
xlabel = 'Liquid fuels (TWh)'
xmax = 50
fileName = 'liquidsSupply_tech_ev'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=cross_plots.modelsid, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_liquids_supply, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=False, pos_legend="upper right",
    width=5, height=12,
    #width=12, height=5,
    group_by="model", # 'scenario' or 'model'
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
xlabel = 'Hydrogen (TWh)'
xmax = 30
fileName = 'h2Supply_tech_ev'
cross_plots.plotBarHorizontal(
#cross_plots.plotBarVertical(

    listModelsid=cross_plots.modelsid, 
    listSce=scenarios,
    varName = varName, 
    varList=varList_h2_supply, 
    year=year, 
    scale=1,
    label=xlabel, 
    figmax = xmax,
    fileName = fileName,
    invert=False, legend=True, pos_legend="lower right",
    width=5, height=12,
    #width=12, height=5,
    group_by="model", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)


varName = 'electricity_supply'
listModels = cross_plots.modelsid
xlabel = 'Electricity (TWh)'
xmax = 100
fileName = 'elecSupply_tech_net_ev'
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
    invert=False, legend=False, 
    pos_legend={# This puts the legend outside-right for vertical plots
                "loc": "center left",
                "bbox_to_anchor": (1.02, 0.5),
                },#"upper right",
    width=8, height=12,
    #width=12, height=5,
    group_by="model", # 'scenario' or 'model'
    multi=False,          # <--- one plot
)

#
            