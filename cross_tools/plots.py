"""Code to produce plots for the CROSS model result comparison"""

# Copyright (c) 2024, ETH Zurich, Energy Science Center, Adriana Marcucci
# Distributed under the terms of the Apache License, Version 2.0.


# Import all the libraries 
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sb
from datetime import datetime, timedelta
import inspect
import os


import warnings
warnings.filterwarnings(
    "ignore",
    "indexing past lexsort depth may impact performance.",
    category=pd.errors.PerformanceWarning,
)


class Plots:

    def __init__(self, fileResults,model_list,scenarios,sceColors,folder_plots):

        """ 
        Generic class to upload the data and produce the plots for the model comparison

        Attributes:
            fileResults: Name of the file with the results
            model_list: list of dictionary with model names and the color to use for each model
            scenarios: list with the scenario names
            sceColors: list with the color for the scenarios
            folder_plots: path to folder_plots
        """
        

        # Get the models names
        self.models = {f['id']: f['name'] for f in model_list}
        self.modelsid = [ f['id'] for f in model_list ]
        self.model_colors = [ f['color'] for f in model_list ]
        self.typicalDays = {}
        self.typicalDays['summer'] = {
                                    'name':  {f['id']: f['summer'] for f in model_list},
                                    'value': {f['id']: f['summerDay'] for f in model_list}
                                }
                                
        self.typicalDays['winter'] =  {
                                    'name':  {f['id']: f['winter'] for f in model_list},
                                    'value': {f['id']: f['winterDay'] for f in model_list}
                                }
        
        os.makedirs(folder_plots, exist_ok=True)
        self.folder_plots = folder_plots
        
        # Read the file with the data
        self.allData = self.__readData(fileResults) 
        
        self.yearsModel = self.getReportedYearsByModel()
        self.sce = scenarios
        self.sceColors = sceColors
        self.sceModel = self.getReportedScenariosByModel()
        
        
        #Calculate net imports and exports
        self.__calculateNets()
        
        # For the following variables we do a pre-processing:
        # We make sure that if the var 'cat' wasn't reported, we calculate it from the subcategories
        # The variable '(varName,cat)' will be created and can be used later in the code
        # This guarantees that we can compare even if models report different levels of aggregation 

        subcats = [
            {'varName':'electricity_supply','time_resolution':'annual','cat':'spv','subcats':['spv_rooftop','spv_facade','spv_mountain','spv_agriculture']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'spv','subcats':['spv_rooftop','spv_facade','spv_mountain','spv_agriculture']},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'wind','subcats':['wind_on','wind_off']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'wind','subcats':['wind_on','wind_off']},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'methane_pp','subcats':["methane_chp_ccs","methane_chp_woccs","methane_oc_woccs","methane_oc_ccs","methane_cc_woccs","methane_cc_ccs"]},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'methane_pp','subcats':["methane_chp_ccs","methane_chp_woccs","methane_oc_woccs","methane_oc_ccs","methane_cc_woccs","methane_cc_ccs"]},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'liquids_pp','subcats':['liquids_chp_woccs','liquids_chp_ccs','liquids_oc_woccs','liquids_oc_ccs','liquids_cc_woccs','liquids_cc_ccs']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'liquids_pp','subcats':['liquids_chp_woccs','liquids_chp_ccs','liquids_oc_woccs','liquids_oc_ccs','liquids_cc_woccs','liquids_cc_ccs']},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'waste_pp','subcats':['waste_chp_woccs','waste_chp_ccs','waste_cc_woccs','waste_cc_ccs']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'waste_pp','subcats':['waste_chp_woccs','waste_chp_ccs','waste_cc_woccs','waste_cc_ccs']},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'wood_pp','subcats':['wood_chp_woccs','wood_chp_ccs','wood_cc_woccs','wood_cc_ccs']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'wood_pp','subcats':['wood_chp_woccs','wood_chp_ccs','wood_cc_woccs','wood_cc_ccs']},
            {'varName':'electricity_supply','time_resolution':'annual','cat':'hydrogen_pp','subcats':['hydrogen_chp','hydrogen_cc']},
            {'varName':'electricity_supply_typical_day','time_resolution':'typical-day','cat':'hydrogen_pp','subcats':['hydrogen_chp','hydrogen_cc']},
            {'varName':'space_heat_useful_energy_supply','time_resolution':'annual','cat':'heat_pump','subcats':['air_source','ground_source','water_source']}, 
            {'varName':'district_heat_useful_energy_supply','time_resolution':'annual','cat':'heat_pump','subcats':['air_source','ground_source','water_source']}, 
            {'varName':'process_heat_useful_energy_production','time_resolution':'annual','cat':'heat_pump','subcats':['air_source','ground_source','water_source']}, 
            {'varName':'space_heat_useful_energy_supply','time_resolution':'annual','cat':'boiler_wood','subcats':['boiler_wood_chips','boiler_wood_pellets']}, 
            {'varName':'district_heat_useful_energy_supply','time_resolution':'annual','cat':'boiler_wood','subcats':['boiler_wood_chips','boiler_wood_pellets']}, 
            {'varName':'process_heat_useful_energy_production','time_resolution':'annual','cat':'boiler_wood','subcats':['boiler_wood_chips','boiler_wood_pellets']}, 
           ]


        self.__checkSubcategories(subcats)
        
        self.annualData = self.allData.loc[(slice(None),slice(None),slice(None),slice(None),'annual',slice(None)),'value'].to_frame()
        
        varList_supply_net = ['hydro_dam','hydro_ror','nuclear','spv','wind','geothermal_pp',"methane_pp",'fuel_cell_methane',
                          'hydrogen_pp','fuel_cell_h2','liquids_pp','waste_pp','wood_pp','net_storage_out','net_imports']
        
        self.__calculateTotalSupply(varList_supply_net)
        
        # ---- Print info for the user ----
        print("=== Plots object initialized ===\n")
        
        print("Attributes:")
        for name, value in self.__dict__.items():
            print(f"  {name}: {type(value).__name__}")
        
        print("\nMethods:")
        for name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith("_"):   # skip internal methods
                print(f"  {name}()")
        print("\n================================\n")
        
        
        
        
        # # Hourly data
        # self.seasons = ["summer","winter"]  
        # self.hourlyData = {}
        # for season in self.seasons:
        #     seasondata =[]
        #     for m in self.modelsid:
        #         season_m = self.allData.loc[(slice(None),slice(None),slice(None),slice(None),'typical-day',self.typicalDays[season]['value'][m]),'value']
        #         seasondata.append(season_m)
            
        #     self.hourlyData[season]= pd.concat(seasondata, axis=0, ignore_index=False,sort=True)
                
        # self.posNegData = {}
       
    #  Reads the annual data from the csv file from CROSSHub
    #  returns a dataFrame with all the data
    def __readData(self,fileResults):
        
        data = pd.read_csv(fileResults+'.csv', index_col=[],header=[0])
        
        #  remove columns that are not used 
        data.drop(columns=['scenario_group','scenario_variant','uploaded_by','uploaded_at','country'],inplace=True)
                        
        # Get the annual values and make them numeric instead of text
        data['value']=pd.to_numeric(data['value'])
        
        # Correct the unit
        data['value']=data.apply(lambda x: x.value * self.__correctUnit(x.time_resolution,x.unit),axis=1)
        data = data.drop(['unit'], axis=1)
        
        data = data.set_index(['scenario_name','model','variable','use_technology_fuel', 'time_resolution','timestamp'])
        # Models to columns
        #data = data.unstack(level=1)
        #data.columns = data.columns.droplevel()
        data = data.fillna(0)
        return data
    
    def __correctUnit(self,timeResolution,unit):
        annual_factors = {'twh':1,'gwh':1/1000, 'mwh':1/1e6,'gj':1/3.6,'mtco2':1,'gtco2':1000,'gw':1,'mw':1/1000}
        hourly_factors = {'gw':1,'gwh/h':1, 'mw':1/1000,'mwh/h':1/1000}
        if timeResolution == 'annual':
            if unit.lower() in annual_factors.keys():
                return annual_factors[unit.lower()]
            else:
                return 0
        elif timeResolution == 'typical-day':
            if unit.lower() in hourly_factors.keys():
                return hourly_factors[unit.lower()]
            else: 
                return 0
            
    def getReportedYearsByModel(self):
        years =  {}
        for m in self.modelsid:
            data_annual_m = self.allData.loc[(slice(None),m,slice(None),slice(None),'annual',slice(None)),:].reset_index(level=[5])
            years_m = data_annual_m.timestamp.unique().tolist()
            years[m]=years_m
            
        return years
    
    
    def getReportedScenariosByModel(self):
        sceModel =  {}
        for m in self.modelsid:
            data_annual_m = self.allData.loc[(slice(None),m,slice(None),slice(None),'annual',slice(None)),:].reset_index(level=[0])
            sce_m = data_annual_m.scenario_name.unique().tolist()
            sceModel[m]=sce_m
            
        return sceModel

                        
    def __checkSubcategories(self,subcats):
        """ 
        Calculate cat = sum(subcats)
        """ 
        
        for v in subcats:
            for m in self.modelsid:
                for s in self.sceModel[m]:
                    time = []
                    if  v['time_resolution'] == 'annual':
                        time = self.yearsModel[m]
                    elif v['time_resolution'] == 'typical-day':
                        time = [self.typicalDays['summer']['value'][m]]+[self.typicalDays['winter']['value'][m]]
                        # Annual data
                    for t in time:
                        # Check if the variable exists
                        try:
                            totalCat = self.allData.loc[(s,m,v['varName'],v['cat'],v['time_resolution'],t),'value'].iloc[0]
                        except:
                            totalCat = 0
                            flag = 0
                            # Check if the subvariables exist
                            for subv in v['subcats']:
                                try:
                                    totalCat = totalCat + self.allData.loc[(s,m,v['varName'],subv,v['time_resolution'],t),'value'].iloc[0]
                                    flag +=1
                                except:
                                    totalCat = totalCat 
                            
                            if flag>0:
                                self.allData.loc[(s,m,v['varName'],v['cat'],'annual',t),'value']  = totalCat
                                
                            
    def __calculateNets(self):
        """ 
        Calculate net imports, exports and storage for all the models, scenarios and timesteps
        """ 
        
        variables = [
            {'varSupply': 'electricity_supply','tech':['imports'],
             'varDemand': 'electricity_consumption','use':['exports'], 
             'netPositive':'net_imports',
             'netNegative':'net_exports',
             'time_resolution':['annual']},
            #'time_resolution':['annual','typical-day']}, Since GF doesnt submit typical days, we dont do it for now
            {'varSupply': 'electricity_supply','tech':['battery_out','phs_out'],
             'varDemand': 'electricity_consumption','use':['battery_in','phs_in'],
             'netPositive':'net_storage_out',
             'netNegative':'net_storage_in',
             'time_resolution':['annual']},
            #'time_resolution':['annual','typical-day']}, Since GF doesnt submit typical days, we dont do it for now
            
        ]
        for m in self.modelsid:
            for s in self.sceModel[m]:
                for v in variables:
                    for resolution in v['time_resolution']:
                        time = []
                        sufix = ''
                        if  resolution == 'annual':
                            time = self.yearsModel[m]
                        elif resolution == 'typical-day':
                            
                            timestamps_summer = [datetime.strptime(self.typicalDays['summer']['value'][m], "%d.%m.%Y") + timedelta(hours=i) for i in range(24)]
                            timestamps_winter = [datetime.strptime(self.typicalDays['winter']['value'][m], "%d.%m.%Y") + timedelta(hours=i) for i in range(24)]
                            
                            
                            time = [dt.strftime("%d.%m.%Y %H:%M") for dt in timestamps_summer]+[dt.strftime("%d.%m.%Y %H:%M") for dt in timestamps_winter]
                            sufix = '_typical_day'
                        
                        for t in time:
                            net = 0
                            for subv in v['tech']:
                                net = net + self.allData.loc[(s,m,v['varSupply']+sufix,subv,resolution,t),'value']
                            for subv in v['use']:
                                net = net - self.allData.loc[(s,m,v['varDemand']+sufix,subv,resolution,t),'value']
                            if net>0:
                                self.allData.loc[(s,m,v['varSupply']+sufix,v['netPositive'],resolution,t),'value'] = net
                                self.allData.loc[(s,m,v['varDemand']+sufix,v['netNegative'],resolution,t),'value'] = 0
                                
                            else:
                                self.allData.loc[(s,m,v['varSupply']+sufix,v['netPositive'],resolution,t),'value'] = 0
                                self.allData.loc[(s,m,v['varDemand']+sufix,v['netNegative'],resolution,t),'value'] = -1*net
                                
                   
    def __calculateTotalSupply(self,varList_supply):
        """ 
        Calculate Net supply = sum(varList_supply)
        """ 
        for m in self.modelsid:
            for s in self.sceModel[m]:
                # Annual data
                for y in self.yearsModel[m]:
                    total = np.nan
                    for v in varList_supply:
                        try:
                            data_v = self.annualData.loc[(s,m,'electricity_supply',v,'annual',y),'value'].iloc[0]
                        except:
                            data_v = np.nan
                            
                        if not np.isnan(data_v):
                            if np.isnan(total):
                                total = data_v
                            else:
                                total = total + data_v
                    
                    self.annualData.loc[(s,m,'electricity_supply','total','annual',y),'value']   = total
                     
    
    def __extractPositiveNegative(self,positive_variables,negative_variables):
        
        positive_labels = [d['name'] for d in positive_variables]
        negative_labels=[d['name'] for d in negative_variables]
        
        timesteps = self.hourlyData['summer'].index.get_level_values(level=2).unique()
        
        for season in self.seasons:
            allData_h = self.hourlyData[season].copy()
            
            posNegData=pd.DataFrame(index=pd.MultiIndex.from_product([self.sce,positive_labels+negative_labels,timesteps] ,names=('scenario','index','timestep')),columns=self.models)
            posNegData.sort_index(inplace=True)
            posNegData.loc[(slice(None),slice(None),slice(None)),:] = 0
            
            for v in positive_variables:
                for s in self.sce:
                    for t in timesteps:
                        for subv in v['data']:
                            try:
                                posNegData.loc[(s,v['name'],t),:] += allData_h.loc[(s,subv.lower(),t),:]
                            except KeyError:
                                posNegData.loc[(s,v['name'],t),:] = posNegData.loc[(s,v['name'],t),:] 
            for v in negative_variables:
                for s in self.sce:
                    for t in timesteps:
                        for subv in v['data']:
                            try:
                                posNegData.loc[(s,v['name'],t),:] -= allData_h.loc[(s,subv.lower(),t),:]
                            except KeyError:
                                posNegData.loc[(s,v['name'],t),:] = posNegData.loc[(s,v['name'],t),:] 
            
            posNegData = posNegData.reset_index().melt(id_vars=["scenario",'index','timestep'])
            posNegData.rename(columns={'variable':'model','value':'Electricity (GW)'},inplace=True)
            self.posNegData[season] = posNegData.set_index(["scenario",'index','timestep','model'])
            
                            
    
              

    def plotScatter(self,listModelsid, varName,use_technology_fuel,year,scale,xlabel,xmax,fileName):
        """ 
        Plot scatter of variable by model and scenario. 
        A great part of the function is only to make sure the labels are in the right place

        Parameters:
        ----------
        listModelsid: list of models id to plot
        varName: str, variable name in the data template
        use_technology_fuel: str, name of the use, technology or fuel
        year: year for the plot
        scale: numeric, if needed, plot will plot var*scale, for unit changes, for example
        xlabel: str, label for x-axis
        xmax: int, maximum level x-axis
        fileName: str, file name for the plot
        """
        sb.reset_defaults()
        matplotlib.rcParams["font.family"] = "sans-serif"
        matplotlib.rcParams['font.sans-serif'] = "Arial"

        nmodels = len(self.models)
        ypos_grid = []
        ypos_cols = []

        # figure and axis
        fig, (ax)= plt.subplots(1, figsize=(5, 6))


        numSce= len(self.sce)
        

        for index, m in enumerate(listModelsid):
            y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
            ypos_grid.append(y_ini)
            ypos_cols.append(y_ini-numSce/4-0.25)
            for i in np.arange(numSce):
                y = y_ini - i * 0.5 - 0.5
                try:
                    value = self.annualData.loc[(self.sce[i],m,varName,use_technology_fuel,'annual',year),'value']/scale
                except:
                    value = np.NaN
                plt.scatter(value,y,c=self.sceColors[i])

        # y axis. Minor ticks are the lines and major ticks the model names

        ax.yaxis.set_major_locator(ticker.FixedLocator(ypos_cols))
        
        listModels = [self.models[k] for k in listModelsid if k in self.models]
        plt.yticks(ypos_cols, listModels)

        ax.yaxis.set_minor_locator(ticker.FixedLocator(ypos_grid))
        ax.yaxis.grid(color='gray', linestyle='dashed',which='minor')
        # Remove the tick lines
        ax.tick_params(axis='y', which='major', tick1On=False, tick2On=False)

        # x axis.
        ax.set_axisbelow(True)
        ax.xaxis.grid(color='gray', linestyle='dashed')
        plt.xlabel(xlabel)

        # y and x limits
        plt.ylim(0, ypos_grid[0])
        plt.xlim(0,xmax)

        # remove spines
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)# adjust limits and draw grid lines

        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
        plt.savefig(self.folder_plots+'/'+fileName+'.png',bbox_inches='tight', dpi=300)
        plt.show()
        

    def plotBar(self,listModelsid,varName ,varList,year,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName,width,height):
        """ 
        Bar plot by model and scenario. 
        Parameters:
        ----------
        listModelsid: list of models id to plot
        varName: str, variable name in the data template
        varList: list of dictionaries with 
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        year: year for the plot
        scale: numeric, if needed, plot will plot var*scale, for unit changes, for example
        xlabel: str, label for x-axis
        xmax: int, maximum level x-axis
        fileName: str, file name for the plot
        right: True if model names have to go on the right
        legend: True if legend has to be displayed
        pos_legend: str: 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
        onTopVarName: str: name of variable to plot on top of the bar plot, '' if none
        width: width of the plot in cm
        height: height of the plot in cm
        """

        numSce= len(self.sce)
        nmodels = len(listModelsid)

        # Get data
        dataPlot={}
        colors = {}
        names = []


        for v in varList:
            datav = [0]*numSce*nmodels
            colors[v['name']] = v['color']
            names.append(v['name'])
            for index, m in enumerate(listModelsid):
                for i in np.arange(numSce):
                    for subv in v['data']:
                        try:
                            datasubv = self.annualData.loc[(self.sce[i],m,varName,subv,'annual',year),'value'].iloc[0] 
                        except KeyError:
                            datasubv = 0
                        if not np.isnan(datasubv):
                            datav[index*(numSce) + i] = datav[index*(numSce) + i] + datasubv/scale 
            dataPlot[v['name']]= datav  

        # Calculate position of bars, labels and grids
        ypos_grid = []
        ypos_cols = []
        ypos_bar  = []

        for index, m in enumerate(listModelsid):
            y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
            ypos_grid.append(y_ini)
            ypos_cols.append(y_ini-numSce/4-0.25)
            for i in np.arange(numSce):
                y = y_ini - i * 0.5 - 0.5
                ypos_bar.append(y)

        # figure and axis

        sb.set_style("white")
        cm = 1/2.54  # centimeters in inches
        fig, (ax)= plt.subplots(1, figsize=(width*cm, height*cm))


        # Initialize the horizontal-offset for the stacked bar chart.
        x_offset = np.zeros(numSce*nmodels)
        bar_width = 0.3
        for index in colors.keys():
            row = dataPlot[index]
            plt.barh(ypos_bar,row, bar_width, left=x_offset,color=colors[index],zorder=1, edgecolor='none')
            x_offset = x_offset + row

        # Invert axis if the plot is oriented to the right
        listModels = [self.models[k] for k in listModelsid if k in self.models]
        if right==True:
            ax.invert_xaxis() 
            ax.yaxis.set_major_locator(ticker.FixedLocator(ypos_cols))
            plt.yticks(ypos_cols, [])
            plt.xlim(xmax,0)
            if legend==True:
                plt.legend(names, loc=pos_legend, ncol = 1)

        else:
            # y axis. Minor ticks are the lines and major ticks the model names
            ax.yaxis.set_major_locator(ticker.FixedLocator(ypos_cols))
            plt.yticks(ypos_cols, listModels)
            plt.xlim(0,xmax)
            if legend==True:
                plt.legend(names, loc=pos_legend, ncol = 1)


        if len(onTopVarName)!=0:
            for index, m in enumerate(listModelsid):
                y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
                for i in np.arange(numSce):
                    y = y_ini - i * 0.5 - 0.5
                    ax.autoscale(False) # To avoid that the scatter changes limits
                    ax.scatter(self.annualData.loc[(self.sce[i],m,varName,onTopVarName,'annual',year),'value']/scale,y,
                               c='#000000',marker=r'x',s=12,zorder=2,linewidths=1)


        ax.yaxis.set_minor_locator(ticker.FixedLocator(ypos_grid))
        ax.yaxis.grid(color='gray', linestyle='dashed',which='minor')
        # Remove the tick lines
        ax.tick_params(axis='y', which='major', tick1On=False, tick2On=False)

        # x axis.
        ax.set_axisbelow(True)
        ax.xaxis.grid(color='gray', linestyle='dashed')
        plt.xlabel(xlabel)

        # y and x limits
        plt.ylim(0, ypos_grid[0])


        # remove spines
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)# adjust limits and draw grid lines
        
        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
        plt.savefig(self.folder_plots+'/'+fileName+'.png',bbox_inches='tight', dpi=300)
        plt.show()
        
         
    def plotTechDist(self,listModelsid,varName,varList,year,order,ylabel,ymax,fileName,legend):
        """ 
        Plots the distribution by technology
        Parameters:
        ----------
        listModelsid: list of models id to plot
        varName: str, variable name in the data template
        varList: list of dictionaries with 
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        year: year for the plot
        order: list with the technology order 
        ylabel: str, label for y-axis
        ymax: int, maximum level y-axis
        fileName: str, file name for the plot
        legend: True if legend has to be displayed
        """
    
        variables =[v['name'] for v in varList]
        dataNew =pd.DataFrame (index=pd.MultiIndex.from_product([self.sce,variables] ,names=('scenario','index')), columns=listModelsid)

        for v in varList:
            var =  v['name']
            for s in self.sce:
                for m in listModelsid:
                    dataNew.loc[(s,var),m] = np.nan
                    for subv in v['data']:
                        datasubv = np.nan
                        try:
                            datasubv = self.annualData.loc[(s,m,varName,subv,'annual',year),'value'].iloc[0]
                        except:
                            datasubv = np.nan
                        if not np.isnan(datasubv):
                            if not np.isnan(dataNew.loc[(s,var),m]):    
                                dataNew.loc[(s,var),m] = dataNew.loc[(s,var),m] + datasubv
                            else:
                                dataNew.loc[(s,var),m] = datasubv

        dataNew=dataNew.dropna(how='all')
        # Remove scenarios not existent
        dataNew.reset_index(inplace=True)

        dataNew=dataNew.melt(id_vars=["scenario", "index"], 
                var_name="Model", 
                value_name="value")

        # Rename the models using the name instead of the modelid
        dataNew=dataNew.replace({'Model': self.models})
        
        # Remove  non-existent scenarios
        dataNew_unmelted = dataNew.pivot(index=['scenario','Model'], columns='index')
        dataNew_unmelted=dataNew_unmelted.loc[(dataNew_unmelted!=0).any(axis=1)]
        dataNew_unmelted.columns= dataNew_unmelted.columns.droplevel()

        dataNew_unmelted.reset_index(inplace=True)
        
        
        dataPlot=dataNew_unmelted.melt(id_vars=["scenario", "Model"], 
                    var_name="index", 
                    value_name="value")

        sb.set_style("whitegrid")

        PROPS = {
            'boxprops':{'facecolor':'none', 'edgecolor':'grey'},
            'medianprops':{'color':'grey'},
            'whiskerprops':{'color':'grey'},
            'capprops':{'color':'grey'}
        }
        
        #Get the color of the models in the list
        colors = [ self.model_colors[self.  modelsid.index(m)] for m in listModelsid ]
        #Get the names from the ids
        listModels = [self.models[x] for x in listModelsid]

        g1 = sb.catplot(x="index", y="value",hue='Model',hue_order=listModels,palette=sb.color_palette(colors), alpha=.8, data=dataPlot, 
                             order=order);
        if legend==False:
            g1._legend.remove()
        
        g1.set(xlabel='', ylabel=ylabel )
        g1.set(ylim=(0, ymax))
        
        g2 = sb.boxplot(x="index", y="value", data=dataPlot, order=order,
                        showfliers=False,
                        linewidth=0.75,
                        **PROPS);
        g2.set(xlabel='', ylabel=ylabel )
        g2.set(ylim=(0, ymax))
        
        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
        plt.savefig(self.folder_plots+'/'+fileName+'.png',bbox_inches='tight', dpi=300)
        plt.show()
    
        
    def plotHourlyStack(self,listModels,positive_variables,negative_variables,season,ylabel_pos,ylabel_neg,ymax,legend,fileName):
        """ 
        Plots the daily stacked hourly profile by technology: supply positive, use negative
        Parameters:
        ----------
        listModels: list of models to plot
        positive_variables: list of dictionaries with positive data to plot
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        negative_variables: list of dictionaries with negative data to plot
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        season: str ('winter' or 'summer')
        ylabel_pos: str, label for positive y-axis
        ylabel_neg: str, label for negative y-axis
        ymax: int, maximum level y-axis
        legend: True if legend is displayed
        fileName: str, file name for the plot
        """
        sb.set_style("whitegrid", {'grid.linestyle': ':'})

        colors_pos= [d['color'] for d in positive_variables]
        colors_neg= [d['color'] for d in negative_variables]

        labels_pos= [d['name'] for d in positive_variables]
        labels_neg= [d['name'] for d in negative_variables]

        # Add the typical day info to the model names
        dic_names = {m:m+'\n'+self.typicalDays[season][self.models.index(m)] for m in listModels }
        order_col = [m+'\n'+self.typicalDays[season][self.models.index(m)] for m in listModels ]    

                
        positive_data = self.posNegData[season].loc[(slice(None),labels_pos,slice(None),listModels),:].reset_index()
        negative_data = abs(self.posNegData[season].loc[(slice(None),labels_neg,slice(None),listModels),:]).reset_index()

        # Remove text year and :00 from timestep
        positive_data['timestep'] = positive_data['timestep'].apply(lambda x: datetime.strptime(str(x),'%Y %H:%M').strftime('%H'))
        # Make all columns numeric
        positive_data =  positive_data.astype({'timestep': 'int32','Electricity (GW)': 'float64'})
        positive_data['model'] = positive_data['model'].replace(dic_names)


        # Remove text year and :00 from hour
        negative_data['timestep'] = negative_data['timestep'].apply(lambda x: datetime.strptime(str(x),'%Y %H:%M').strftime('%H'))
        # Make all columns numeric
        negative_data =  negative_data.astype({'timestep': 'int32','Electricity (GW)': 'float64'})
        negative_data['model'] = negative_data['model'].replace(dic_names)

   
        positive_data['type'] = ylabel_pos 
        negative_data['type'] = ylabel_neg 
        
        all_data = pd.concat([positive_data, negative_data], ignore_index=True, axis=0)
        colors_tech= colors_pos+colors_neg
    
        for s in self.sce:
            data_sce = all_data.loc[all_data['scenario'] == s]
            
            g = sb.displot(kind='hist', 
                           data=data_sce, 
                           x='timestep', 
                           weights='Electricity (GW)', 
                           hue='index', 
                           col='model', 
                           col_order=order_col,
                           row='type',
                           multiple='stack', 
                           shrink=1,
                           bins=24, #Number of hours, do not change
                           palette=colors_tech,
                           alpha=1,
                           edgecolor='none',
                           height=2.5,aspect=0.7,
                           legend=legend,
                           facet_kws={'sharey': False,'gridspec_kws': {"wspace":0.1,"hspace":0}}
                           ).set(xlim=(0, 24),ylim=(0, 30), xticks=[0, 6, 12, 18, 24]).set_titles("{col_name}").set_xlabels("")
            
            #The first row corresponds to the supply, it is manually modified
            row_pos = g.axes[0]
            for subplot in row_pos:
                subplot.set_ylim([0,ymax])
                if subplot.get_ylabel()=="Count":
                    subplot.set_ylabel(ylabel_pos)
                else:
                    subplot.set_yticklabels([])
            
            
            row_neg = g.axes[1]
            for subplot in row_neg:
                subplot.set_ylim([ymax,0]) #Mirror
                subplot.set_title("") #Remove title
                if subplot.get_ylabel()=="Count":
                    subplot.set_ylabel(ylabel_neg)
                else:
                    subplot.set_yticklabels([])
                
            g.savefig(self.folder_plots+'/'+fileName+"_"+season+"_stacked_"+s+".pdf",bbox_inches='tight')
            print(season+"-"+s)
            plt.show()
            
    def plotHourProfileTech(self,listModels,scenario,varList,season,ylabel,ymax,ncols,fileName):
        """ 
        Plots the hourly profile by technology
        Parameters:
        ----------
        listModels: list of models to plot
        scenario: str, scenario to plot
        varList: list of str with data to plot
        season: str ('winter' or 'summer')
        ylabel: str, label for y-axis
        ymax: int, maximum level y-axis
        ncols: int, number of columns per row
        fileName: str, file name for the plot
        """
        model_colors= [self.model_colors[self.models.index(m)] for m in listModels ]    

        dataNew=abs(self.posNegData[season].loc[(scenario,varList,slice(None),listModels),:])

        dataPlot = dataNew.reset_index()
        # Remove text year and :00 from timestep
        dataPlot['timestep'] = dataPlot['timestep'].apply(lambda x: datetime.strptime(str(x),'%Y %H:%M').strftime('%H'))

        sb.set_style("whitegrid")

        g = sb.FacetGrid(dataPlot,  col="index",hue="model",hue_kws={'color': model_colors},col_order=varList
                         ,col_wrap=ncols
                         ,height=2.5,aspect=0.8)
        g = (g.map(plt.plot, "timestep", "Electricity (GW)")).set(xlim=(0, 24),ylim=(0, ymax),xticks=[0, 6, 12, 18, 24]).set_titles("{col_name}").set_xlabels("")

        if ncols==1:
            for axis in g.axes:
                for subplot in axis:
                    if subplot.get_ylabel()=="Electricity (GW)":
                        subplot.set_ylabel(ylabel)

        else:
            for subplot in g.axes:
                if subplot.get_ylabel()=="Electricity (GW)":
                    subplot.set_ylabel(ylabel)
        
        
        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
        plt.show()
