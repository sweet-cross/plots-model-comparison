#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 21:34:03 2025

@author: madriana
"""

#Get the hourly data for the variables of interest
varList_supply_h = [
    {'name':'Net-imports','data':['net_imports'],'color':'#CCCCCC'},
    {'name':'Storage out','data':['net_storage_out'],'color':'#939CAC'},
    {'name':'Solar','data':['spv'],'color':'#FAC748'},
    {'name':'Hydro Dams','data':['hydro_dam'],'color':'#ADD8E6'},
    {'name':'Wind','data':['wind'],'color':'#F2960E'},
    {'name':'Geothermal','data':['geothermal_pp'],'color':'#ac79c4'},
    {'name':'Thermal','data':['methane_pp','fuel_cell_methane','hydrogen_pp','fuel_cell_h2','waste_pp','wood_pp','liquids_pp'],'color':'#b82222'},
    {'name':'Hydro RoR','data':['hydro_ror'],'color':'#0377CA'},
    ]


varList_use_h = [
    {'name':'Net-exports','data':['net_exports'],'color':'#CCCCCC'},
    {'name':'Storage in','data':['net_storage_in'],'color':'#939CAC'},
    {'name':'EVs','data':['road_public','road_private','truck','ldv'],'color':'#09c5c9'},
    {'name':'Heat pumps','data':['space_heating_heat_pump','process_heat_heat_pump'],'color':'#F2960E'},
    {'name':'Heaters','data':['space_heating_heater_elec','process_heat_heater_elec','space_heating_boiler_electrode','process_heat_boiler_electrode'],'color':'#CF4832'},
    {'name':'Electrolysis','data':['electrolysis'],'color':'#F5DD1B'},
    {'name':'Others','data':['power_to_liquid','dac','data_centers'],'color':'#9751CB'},
    {'name':'Trains','data':['passenger_rail','freight_rail'],'color':'#000000'},
    {'name':'Base','data':['elec_appliances'],'color':'#097F6D'},
    {'name':'Losses','data':['grid_losses','storage_losses'],'color':'#8B5A2B'}
#    {'name':'Total','data':['Electricity-consumption|Total demand'],'color':'#8E8900'}
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
