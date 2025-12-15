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
        self.sceVariants= self.getReportedSceVariants()
        
        
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
        
        variables = ['total_system_costs','carbon_price']
        self.__checkVariablesNoSub(variables)
        
        self.annualData = self.allData.loc[(slice(None),slice(None),slice(None),slice(None),slice(None),'annual',slice(None)),'value'].to_frame()
        
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
        data.drop(columns=['scenario_group','uploaded_by','uploaded_at','country'],inplace=True)
                        
        # Get the annual values and make them numeric instead of text
        data['value']=pd.to_numeric(data['value'])
        
        # Correct the unit
        data['value']=data.apply(lambda x: x.value * self.__correctUnit(x.time_resolution,x.unit),axis=1)
        data = data.drop(['unit'], axis=1)
        
        data = data.set_index(['scenario_name','scenario_variant','model','variable','use_technology_fuel', 'time_resolution','timestamp'])
        # Models to columns
        #data = data.unstack(level=1)
        #data.columns = data.columns.droplevel()
        data = data.fillna(0)
        return data
    
    def __correctUnit(self,timeResolution,unit):
        annual_factors = {'twh':1,'gwh':1/1000, 'mwh':1/1e6,'gj':1/3.6,'mtco2':1,'gtco2':1000,'gw':1,'mw':1/1000,'bchf':1,'mchf':1/1000,'chf/tco2':1}
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
            data_annual_m = self.allData.loc[(slice(None),slice(None),m,slice(None),slice(None),'annual',slice(None)),:].reset_index(level=[6])
            years_m = data_annual_m.timestamp.unique().tolist()
            years[m]=years_m
            
        return years
    
    
    def getReportedScenariosByModel(self):
        sceModel =  {}
        for m in self.modelsid:
           data_annual_m = self.allData.loc[(slice(None),slice(None),m,slice(None),slice(None),'annual',slice(None)),:]
            # Bring scenario_name and scenario_variant back as columns
           data_annual_m = data_annual_m.reset_index(level=['scenario_name', 'scenario_variant'])
    
           # Unique (scenario_name, scenario_variant) combinations
           combos = (
               data_annual_m[['scenario_name', 'scenario_variant']]
               .drop_duplicates()
               .apply(tuple, axis=1)
               .tolist()
           )

           sceModel[m] = combos
            
        return sceModel
    
    def getReportedSceVariants(self):
        seen = set()
        union_list = []
        
        for pairs in self.sceModel.values():
            for combo in pairs:
                if combo not in seen:
                    seen.add(combo)
                    union_list.append(combo)
        return union_list
                        
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
                            totalCat = self.allData.loc[(s[0],s[1],m,v['varName'],v['cat'],v['time_resolution'],t),'value']
                        except:
                            totalCat = 0
                            flag = 0
                            # Check if the subvariables exist
                            for subv in v['subcats']:
                                try:
                                    totalCat = totalCat + self.allData.loc[(s[0],s[1],m,v['varName'],subv,v['time_resolution'],t),'value']
                                    flag +=1
                                except:
                                    totalCat = totalCat 
                            
                            if flag>0:
                                self.allData.loc[(s[0],s[1],m,v['varName'],v['cat'],'annual',t),'value']  = totalCat
                                
    def __checkVariablesNoSub(self,variables):
        """ 
        Remove any text that was reported in use_technology_fuel for variables without subcategories 
        """ 
        # Convert index to DataFrame
        idx_df = self.allData.index.to_frame(index=False)
        
        # Create mask on the 'variable' index level
        mask = idx_df['variable'].isin(variables)
        
        # Set use_technology_fuel to '' where condition holds
        idx_df.loc[mask, 'use_technology_fuel'] = ''
        
        # Rebuild MultiIndex
        self.allData.index = pd.MultiIndex.from_frame(idx_df)
      
                                
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
                                net = net + self.allData.loc[(s[0],s[1],m,v['varSupply']+sufix,subv,resolution,t),'value']
                            for subv in v['use']:
                                net = net - self.allData.loc[(s[0],s[1],m,v['varDemand']+sufix,subv,resolution,t),'value']
                            if net>0:
                                self.allData.loc[(s[0],s[1],m,v['varSupply']+sufix,v['netPositive'],resolution,t),'value'] = net
                                self.allData.loc[(s[0],s[1],m,v['varDemand']+sufix,v['netNegative'],resolution,t),'value'] = 0
                                
                            else:
                                self.allData.loc[(s[0],s[1],m,v['varSupply']+sufix,v['netPositive'],resolution,t),'value'] = 0
                                self.allData.loc[(s[0],s[1],m,v['varDemand']+sufix,v['netNegative'],resolution,t),'value'] = -1*net

                   
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
                            data_v = self.annualData.loc[(s[0],s[1],m,'electricity_supply',v,'annual',y),'value']
                        except:
                            data_v = np.nan
                            
                        if not np.isnan(data_v):
                            if np.isnan(total):
                                total = data_v
                            else:
                                total = total + data_v
                    
                    self.annualData.loc[(s[0],s[1],m,'electricity_supply','total','annual',y),'value']   = total
                     
    
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
            
     
    def plotScatter(
        self,
        listModelsid,
        listSce,
        varName,
        use_technology_fuel,
        year,
        scale,
        label,          # label of value axis (x or y)
        figmax,         # max of value axis (x or y)
        fileName,
        width,
        height,
        orientation="horizontal",   # 'horizontal' or 'vertical'
        group_by="model",           # 'model' or 'scenario'
    ):
        """
        Scatter plot of a variable by model and scenario/variant.
    
        Geometry and grouping follow the same logic as:
          - plotBarHorizontal (for orientation='horizontal')
          - plotBarVertical   (for orientation='vertical', multi=False)
    
        Behaviour:
          - group_by='model':
                groups   = models
                within   = scenarios
                primary ticks = scenarios (repeated per model)
                group labels  = models (outside: right for horizontal, top for vertical)
          - group_by='scenario':
                groups   = scenarios
                within   = models
                primary ticks = models (repeated per scenario)
                group labels  = scenarios (outside)
        """
        
        # ----- Styling -----
        sb.reset_defaults()
        matplotlib.rcParams["font.family"] = "sans-serif"
        matplotlib.rcParams["font.sans-serif"] = "Arial"
    
        # ===============================
        # 1. Scenario selection + labels
        # ===============================
        if listSce is None:
            # Expect self.sceVariants to be list of (scenario, variant)
            sce_names = list(self.sceVariants)
            sce_labels = [f"{s} ({v})" for s, v in sce_names]
        elif isinstance(listSce, dict):
            sce_names = list(listSce.keys())      # tuples (scenario, variant)
            sce_labels = list(listSce.values())   # pretty labels
        else:
            # list-like; accept tuples or simple scenario IDs
            sce_names = []
            sce_labels = []
            for item in listSce:
                if isinstance(item, tuple) and len(item) == 2:
                    s, v = item
                else:
                    s, v = item, "reference"
                sce_names.append((s, v))
                sce_labels.append(f"{s} ({v})")
    
        numSce   = len(sce_names)
        nmodels  = len(listModelsid)
        listModels = [self.models[k] for k in listModelsid if k in self.models]
    
        if group_by not in ("model", "scenario"):
            raise ValueError("group_by must be 'model' or 'scenario'")
    
        is_horizontal = (orientation == "horizontal")
    
        # ====================================
        # 2. Build values matrix [model, sce]
        # ====================================
        values = np.full((nmodels, numSce), np.nan)
    
        for im, m in enumerate(listModelsid):
            for isce, (sce_id, variant) in enumerate(sce_names):
                try:
                    val = self.annualData.loc[
                        (sce_id, variant, m, varName, use_technology_fuel, "annual", year),
                        "value",
                    ]
                except KeyError:
                    val = np.nan
                if not np.isnan(val):
                    values[im, isce] = val / scale
    
        # ============================================================
        # 3. Grouping logic (same as bars)
        # ============================================================
        if group_by == "model":
            nGroups = nmodels
            nWithin = numSce
            group_labels  = listModels        # printed outside
            within_labels = sce_labels        # used for ticks
    
            def index_for(g, w):
                # g = model index, w = scenario index
                return g, w
    
        else:  # group_by == "scenario"
            nGroups = numSce
            nWithin = nmodels
            group_labels  = sce_labels        # printed outside
            within_labels = listModels        # used for ticks
    
            def index_for(g, w):
                # g = scenario index, w = model index
                return w, g
    
        # ============================================================
        # 4. Geometry for category axis
        #    (copy of horizontal / vertical bar logic)
        # ============================================================
        pos_grid = []  # group separators
        pos_cols = []  # group centers
        pos_bar  = []  # one per (group, within) point
        
        for g in range(nGroups):
            ini = nGroups * nWithin / 2 - g * nWithin * 0.5 + 0.5 * (nGroups - g)
            pos_grid.append(ini)
            pos_cols.append(ini - nWithin / 4 - 0.25)
            for w in range(nWithin):
                # use the SAME formula for horizontal and vertical
                pos = ini - w * 0.5 - 0.5
                pos_bar.append(pos)
        
        pos_bar = np.array(pos_bar)
    
        # For vertical orientation, flip so first group is LEFT-most,
        # mirroring your final plotBarVertical behaviour.
        if not is_horizontal:
            max_pos = pos_grid[0]
            pos_grid = [max_pos - x for x in pos_grid]
            pos_cols = [max_pos - x for x in pos_cols]
            pos_bar  = max_pos - pos_bar
        else:
            max_pos = pos_grid[0]
    
        # ============================================================
        # 5. Prepare figure & axis
        # ============================================================
        sb.set_style("white")
        cm = 1 / 2.54
        fig, ax = plt.subplots(1, figsize=(width * cm, height * cm))
    
        set_val_lim   = ax.set_xlim if is_horizontal else ax.set_ylim
        set_cat_lim   = ax.set_ylim if is_horizontal else ax.set_xlim
        val_grid      = ax.xaxis.grid if is_horizontal else ax.yaxis.grid
        cat_minor_loc = ax.yaxis.set_minor_locator if is_horizontal else ax.xaxis.set_minor_locator
        cat_minor_grid= ax.yaxis.grid if is_horizontal else ax.xaxis.grid
        set_val_label = ax.set_xlabel if is_horizontal else ax.set_ylabel
    
        # ============================================================
        # 6. Plot all points
        # ============================================================
        tick_pos = []      # within positions (for primary ticks)
        tick_lab = []      # within labels repeated in group order
    
        k = 0
        for g in range(nGroups):
            for w in range(nWithin):
                im, isce = index_for(g, w)
                v = values[im, isce]
                pos = pos_bar[k]
                k += 1
    
                if not np.isnan(v):
                    if is_horizontal:
                        x, y = v, pos
                    else:
                        x, y = pos, v
                    if group_by == "model":
                        ax.scatter(x, y, c=self.sceColors[isce], s=20, zorder=2)
                    else:  # group_by == "scenario"    
                        ax.scatter(x, y, c=self.model_colors[im], s=20, zorder=2)
    
                tick_pos.append(pos)
                tick_lab.append(within_labels[w])
    
        # ============================================================
        # 7. Axes labels, ticks, grids
        # ============================================================
        # Value axis
        set_val_lim(0, figmax)
        val_grid(color="gray", linestyle="dashed")
    
        # Category axis range
        set_cat_lim(0, max_pos)
    
        # Primary ticks = within labels (scenarios or models)
        if is_horizontal:
            ax.yaxis.set_major_locator(ticker.FixedLocator(tick_pos))
            ax.set_yticklabels(tick_lab)
            ax.tick_params(axis="y", which="major", length=0)
        else:
            ax.xaxis.set_major_locator(ticker.FixedLocator(tick_pos))
            ax.set_xticklabels(tick_lab, rotation=90)
            ax.tick_params(axis="x", which="major", length=0)
    
        # Group labels printed outside at group centers
        if is_horizontal:
            # text on the right
            xmin, xmax = ax.get_xlim()
            span = xmax - xmin
            x_text = xmax + 0.02 * span
            for y, lab in zip(pos_cols, group_labels):
                ax.text(x_text, y, lab, va="center", ha="left")
        else:
            # text at the top
            ymin, ymax = ax.get_ylim()
            span = ymax - ymin
            y_text = ymax + 0.02 * span
            for x, lab in zip(pos_cols, group_labels):
                ax.text(x, y_text, lab, va="bottom", ha="center")
    
        # Dotted group separators
        cat_minor_loc(ticker.FixedLocator(pos_grid))
        cat_minor_grid(color="gray", linestyle="dashed", which="minor")
    
        # Value label
        set_val_label(label)
    
        # Spines & grid style (match bars)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if is_horizontal:
            ax.spines["left"].set_visible(False)
        else:
            ax.spines["bottom"].set_visible(False)
    
        # ============================================================
        # 8. Save & show
        # ============================================================
        plt.savefig(self.folder_plots + "/" + fileName+ ".pdf", bbox_inches="tight")
        plt.savefig(
            self.folder_plots + "/" + fileName + ".png",
            bbox_inches="tight",
            dpi=300,
        )
        plt.show()



    
    def plotBarHorizontal(
        self,
        listModelsid,
        listSce,
        varName,
        varList,
        year,
        scale,
        label,
        figmax,
        fileName,
        invert,
        legend,
        pos_legend,
        width,
        height,
        group_by="model",   # 'model' or 'scenario'
        multi=False,        # False = one plot; True = subplots per group
    ):
        """
        Horizontal stacked bar plot by model and scenario.
    
        Parameters
        ----------
        listModelsid : list
            List of model ids to plot.
        listSce : None, list[str], or dict[tuple, str]
            Which scenarios to include and how to label them.
        
            - None  → use all scenarios in self.sceVariants (labels = scenario IDs)
            - list  → subset of scenarios (labels = the same list elements)
            - dict  → keys = (scenario IDs in the data, variant)
                        values = alternative display labels for axis ticks
        
                Example:
                    listSce = {
                        ('abroad-resnuc-high','reference'): 'High cost',
                        ('abroad-resnuc-low','reference'): 'Low cost'
                    }
        varName : str
            Variable name in the data template.
        varList : list of dict
            Each dict with:
                - 'name': name of the technology or group of technologies,
                - 'data': list with the technologies in this category,
                - 'color': color used for this category.
        year : int
            Year for the plot.
        scale : float
            Factor to divide the data (e.g. unit changes).
        label : str
            Label for the x-axis (value axis).
        figmax : float
            Maximum of the x-axis (value axis).
        fileName : str
            File name (without extension) for the plot.
        invert : bool
            True if the x-axis should be inverted.
        legend : bool
            If True, show legend.
        pos_legend : str
            Legend position: 'upper left', 'upper right', 'lower left', 'lower right'.
        width : float
            Width of the plot in cm.
        height : float
            Height of the plot in cm.
        group_by : {'model', 'scenario'}
            Whether groups are models (bars inside are scenarios)
            or groups are scenarios (bars inside are models).
        multi : bool
            If False, all groups in one axis (with separators).
            If True, one subplot per group, shared xlim.
        """
    
        # ----- Scenario selection -----
        if listSce is None:
            sce_names = self.sceVariants
            sce_labels = sce_names[:]  # Default labels equal IDs
        elif isinstance(listSce, dict):
            sce_names = list(listSce.keys())      # For retrieving data
            sce_labels = list(listSce.values())   # For display
        else:
            sce_names = list(listSce)
            sce_labels = sce_names[:]             # Labels equal IDs
    
        numSce   = len(sce_names)
        nmodels  = len(listModelsid)
        listModels = [self.models[k] for k in listModelsid if k in self.models]
    
        if group_by not in ("model", "scenario"):
            raise ValueError("group_by must be 'model' or 'scenario'")
    
        # ---------- Get data as 2D matrices: [model, scenario] ----------
        dataMat = {}   # name -> (nmodels, numSce)
        colors  = {}
        names   = []
    
        for v in varList:
            mat = np.zeros((nmodels, numSce))
            colors[v["name"]] = v["color"]
            names.append(v["name"])
    
            for im, m in enumerate(listModelsid):
                for isce, sce_name in enumerate(sce_names):
                    for subv in v["data"]:
                        try:
                            datasubv = self.annualData.loc[
                                (sce_name[0],sce_name[1], m, varName, subv, "annual", year),
                                "value",
                            ]
                        except KeyError:
                            datasubv = 0
                        if not np.isnan(datasubv):
                            mat[im, isce] += datasubv / scale
            dataMat[v["name"]] = mat
    
        # ---------- Grouping logic ----------
        if group_by == "model":
            nGroups = nmodels
            nWithin = numSce
            group_labels  = listModels         # one per model
            within_labels = sce_labels           # one per scenario
    
            def flatten_for_plot(mat):
                # order: model-major, then scenario (axis 0 -> groups)
                return mat.reshape(-1)
    
        else:  # group_by == "scenario"
            nGroups = numSce
            nWithin = nmodels
            group_labels  = sce_labels           # one per scenario
            within_labels = listModels        # one per model
            print(group_labels)
            def flatten_for_plot(mat):
                # order: scenario-major, then model (axis 1 -> groups)
                return mat.T.reshape(-1)
    
        # ============================================================
        #                MODE 1: SINGLE AXIS (multi=False)
        # ============================================================
        if not multi:
            # ---------- Positions of bars and group separators ----------
            pos_grid = []  # separator / grid positions between groups
            pos_cols = []  # center of each group block (for group labels)
            pos_bar  = []  # one per (group, within) bar
    
            for g in range(nGroups):
                ini = nGroups * nWithin / 2 - g * nWithin * 0.5 + 0.5 * (nGroups - g)
                pos_grid.append(ini)
                pos_cols.append(ini - nWithin / 4 - 0.25)
                for w in range(nWithin):
                    pos = ini - w * 0.5 - 0.5
                    pos_bar.append(pos)
    
            pos_bar = np.array(pos_bar)
    
            # ---------- Figure and axis ----------
            sb.set_style("white")
            cm = 1 / 2.54
            fig, ax = plt.subplots(1, figsize=(width * cm, height * cm))
    
            barfunc         = ax.barh
            stack_key       = "left"
            set_mainlim     = ax.set_xlim
            set_seclim      = ax.set_ylim
            set_value_label = ax.set_xlabel
            main_grid       = ax.xaxis.grid
            cat_minor_loc   = ax.yaxis.set_minor_locator
            cat_minor_grid  = ax.yaxis.grid
    
            # ---------- Plot stacked bars ----------
            offset = np.zeros(nGroups * nWithin)
            bar_width = 0.3
    
            for name in names:
                row_flat = flatten_for_plot(dataMat[name])
                kwargs = {stack_key: offset}
                barfunc(
                    pos_bar,
                    row_flat,
                    bar_width,
                    color=colors[name],
                    edgecolor="none",
                    zorder=1,
                    **kwargs,
                )
                offset += row_flat
    
            # ---------- Invert x-axis if needed ----------
            if invert:
                ax.invert_xaxis()
                set_mainlim(figmax, 0)
            else:
                set_mainlim(0, figmax)
    
            # ---------- "Within" labels (one per bar) ----------
            within_labels_flat = []
            if group_by == "model":
                for _m in listModels:
                    within_labels_flat.extend(within_labels)
            else:
                for _s in sce_names:
                    within_labels_flat.extend(within_labels)
    
            ax.set_yticks(pos_bar)
            ax.set_yticklabels(within_labels_flat)
            ax.tick_params(axis="x", which="major", length=0)
    
            # ---------- Group labels (outside the bar block) ----------
            x_min, x_max = ax.get_xlim()
            span = x_max - x_min
            if not invert:
                x_text = x_max + 0.02 * span
                ha = "left"
            else:
                x_text = x_min - 0.02 * span
                ha = "right"
    
            for y, group_label in zip(pos_cols, group_labels):
                ax.text(x_text, y, group_label, va="center", ha=ha)
    
            # ---------- Secondary axis (categorical) limits ----------
            set_seclim(0, pos_grid[0])
    
            # ---------- Dotted lines separating groups ----------
            cat_minor_loc(ticker.FixedLocator(pos_grid))
            cat_minor_grid(color="gray", linestyle="dashed", which="minor")
    
            # ---------- Main grid on value axis ----------
            main_grid(color="gray", linestyle="dashed")
    
            # ---------- Axis labels & spines ----------
            set_value_label(label)
    
            if invert:
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                
            else:
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
    
            # ---------- Legend ----------
            if legend:
                ax.legend(names, loc=pos_legend, ncol=1)
    
            # ---------- Save & show ----------
            plt.savefig(self.folder_plots + "/" + fileName, bbox_inches="tight")
            plt.savefig(
                self.folder_plots + "/" + fileName + ".png",
                bbox_inches="tight",
                dpi=300,
            )
            plt.show()
            return
    
        # ============================================================
        #                MODE 2: MULTI-SUBPLOT (multi=True)
        # ============================================================
    
        # One subplot per group, side by side, with shared xlim
        sb.set_style("white")
        cm = 1 / 2.54
    
        fig, axes = plt.subplots(
            1,
            nGroups,
            figsize=(width * cm, height * cm),
            sharex=True,    # share value axis (x) across all
            sharey=False,
        )
    
        if nGroups == 1:
            axes = [axes]
    
        bar_width = 0.3
    
        for g in range(nGroups):
            ax = axes[g]
    
            # --- Use the SAME spacing logic as single-axis, but with nGroups=1 ---
            # This removes the weird extra gap between bars.
            local_pos_bar = []
            local_pos_grid = []
            local_pos_cols = []
    
            # pretend we have just 1 "group" with nWithin bars
            ini = 1 * nWithin / 2 - 0 * nWithin * 0.5 + 0.5 * (1 - 0)
            local_pos_grid.append(ini)
            local_pos_cols.append(ini - nWithin / 4 - 0.25)
            for w in range(nWithin):
                pos = ini - w * 0.5 - 0.5
                local_pos_bar.append(pos)
    
            local_pos_bar = np.array(local_pos_bar)
            offset_local = np.zeros(nWithin)
    
            barfunc         = ax.barh
            stack_key       = "left"
            set_mainlim     = ax.set_xlim
            set_seclim      = ax.set_ylim
            set_value_label = ax.set_xlabel
    
            # stack bars in this group
            for name in names:
                mat = dataMat[name]
                if group_by == "model":
                    row_vals = mat[g, :]            # scenarios
                else:
                    row_vals = mat[:, g]            # models
    
                kwargs = {stack_key: offset_local}
                barfunc(
                    local_pos_bar,
                    row_vals,
                    bar_width,
                    color=colors[name],
                    edgecolor="none",
                    zorder=1,
                    **kwargs,
                )
                offset_local += row_vals
    
            # shared value limit
            if invert:
                ax.invert_xaxis()
                set_mainlim(figmax, 0)
            else:
                set_mainlim(0, figmax)
    
            # within labels
            if group_by == "model":
                wt_labels = within_labels    # scenarios
            else:
                wt_labels = within_labels    # models
    
            ax.set_yticks(local_pos_bar)
            ax.set_yticklabels(wt_labels)
            ax.tick_params(axis="x", which="major", length=0)
    
            # local y-limits (categorical) – match our single-axis style
            set_seclim(0, local_pos_grid[0])
    
            # group label as title
            ax.set_title(group_labels[g], fontsize=ax.xaxis.get_ticklabels()[0].get_fontsize())

    
            # grid on value axis
            ax.xaxis.grid(color="gray", linestyle="dashed")
    
            set_value_label(label)
    
            # clean spines a bit
            if invert:
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                
            else:
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
        
            if g != 0:
                ax.set_yticklabels([])
                ax.tick_params(axis="y", which="major", length=0)
        
        # Legend: one for the whole figure
        if legend:
            handles, labels_legend = axes[0].get_legend_handles_labels()
            if handles:
                fig.legend(handles, labels_legend, loc=pos_legend, ncol=1)
    
        fig.tight_layout()
        plt.savefig(self.folder_plots + "/" + fileName+ ".pdf", bbox_inches="tight")
        plt.savefig(
            self.folder_plots + "/" + fileName + ".png",
            bbox_inches="tight",
            dpi=300,
        )
        plt.show()


    def plotBarVertical(
        self,
        listModelsid,
        listSce,
        varName,
        varList,
        year,
        scale,
        label,
        figmax,
        fileName,
        invert,
        legend,
        pos_legend,
        width,
        height,
        group_by="model",   # 'model' or 'scenario'
        multi=False,        # False = one plot; True = subplots per group
    ):
        """
        Vertical stacked bar plot by model and scenario.
    
        Parameters
        ----------
        listModelsid : list
            List of model ids to plot.
        listSce : None, list[str], or dict[tuple, str]
            Which scenarios to include and how to label them.
        
            - None  → use all scenarios in self.sceVariants (labels = scenario IDs)
            - list  → subset of scenarios (labels = the same list elements)
            - dict  → keys = (scenario IDs in the data, variant)
                        values = alternative display labels for axis ticks
        
                Example:
                    listSce = {
                        ('abroad-resnuc-high','reference'): 'High cost',
                        ('abroad-resnuc-low','reference'): 'Low cost'
                    }
        varName : str
            Variable name in the data template.
        varList : list of dict
            Each dict with:
                - 'name': name of the technology or group of technologies,
                - 'data': list with the technologies in this category,
                - 'color': color used for this category.
        year : int
            Year for the plot.
        scale : float
            Factor to divide the data (e.g. unit changes).
        label : str
            Label for the y-axis (value axis).
        figmax : float
            Maximum of the y-axis (value axis).
        fileName : str
            File name (without extension) for the plot.
        invert : bool
            True if the y-axis should be inverted.
        legend : bool
            If True, show legend.
        pos_legend : str
            Legend position: 'upper left', 'upper right', 'lower left', 'lower right'.
        width : float
            Width of the plot in cm.
        height : float
            Height of the plot in cm.
        group_by : {'model', 'scenario'}
            Whether groups are models (bars inside are scenarios)
            or groups are scenarios (bars inside are models).
        multi : bool
            If False, all groups in one axis (with separators).
            If True, one subplot per group, shared ylim.
        """
    
   
        # ----- Scenario selection -----
        if listSce is None:
            sce_names = self.sceVariants
            sce_labels = sce_names[:]  # Default labels equal IDs
        elif isinstance(listSce, dict):
            sce_names = list(listSce.keys())      # For retrieving data
            sce_labels = list(listSce.values())   # For display
        else:
            sce_names = list(listSce)
            sce_labels = sce_names[:]             # Labels equal IDs
            
        numSce   = len(sce_names)
        nmodels  = len(listModelsid)
        listModels = [self.models[k] for k in listModelsid if k in self.models]
    
        if group_by not in ("model", "scenario"):
            raise ValueError("group_by must be 'model' or 'scenario'")
    
        # ---------- Get data as 2D matrices: [model, scenario] ----------
        dataMat = {}   # name -> (nmodels, numSce)
        colors  = {}
        names   = []
    
        for v in varList:
            mat = np.zeros((nmodels, numSce))
            colors[v["name"]] = v["color"]
            names.append(v["name"])
    
            for im, m in enumerate(listModelsid):
                for isce, sce_name in enumerate(sce_names):
                    for subv in v["data"]:
                        try:
                            datasubv = self.annualData.loc[
                                (sce_name[0],sce_name[1], m, varName, subv, "annual", year),
                                "value",
                            ]
                        except KeyError:
                            datasubv = 0
                        if not np.isnan(datasubv):
                            mat[im, isce] += datasubv / scale
            dataMat[v["name"]] = mat
    
            
        # ---------- Grouping logic ----------
        if group_by == "model":
            nGroups = nmodels
            nWithin = numSce
            group_labels  = listModels         # one per model
            within_labels = sce_labels           # one per scenario
    
            def flatten_for_plot(mat):
                # order: model-major, then scenario
                return mat.reshape(-1)
    
        else:  # group_by == "scenario"
            nGroups = numSce
            nWithin = nmodels
            group_labels  = sce_labels           # one per scenario
            within_labels = listModels        # one per model
    
            def flatten_for_plot(mat):
                # order: scenario-major, then model
                return mat.T.reshape(-1)
    
        # ============================================================
        #                MODE 1: SINGLE AXIS (multi=False)
        # ============================================================
        if not multi:
            # ---------- Positions of bars and group separators ----------
            pos_grid = []
            pos_cols = []
            pos_bar  = []
    
            for g in range(nGroups):
                ini = nGroups * nWithin / 2 - g * nWithin * 0.5 + 0.5 * (nGroups - g)
                pos_grid.append(ini)
                pos_cols.append(ini - nWithin / 4 - 0.25)
                for w in range(nWithin):
                    pos = ini - (nWithin - 1 - w) * 0.5 - 0.5
                    pos_bar.append(pos)
    
            pos_bar = np.array(pos_bar)
            
            # --- Flip groups so the first one is on the LEFT ---
            max_grid = pos_grid[0]              # largest x used as total span
            pos_grid = [max_grid - x for x in pos_grid]
            pos_cols = [max_grid - x for x in pos_cols]
            pos_bar  = max_grid - pos_bar


    
            # ---------- Figure and axis ----------
            sb.set_style("white")
            cm = 1 / 2.54
            fig, ax = plt.subplots(1, figsize=(width * cm, height * cm))
    
            barfunc         = ax.bar
            stack_key       = "bottom"
            set_mainlim     = ax.set_ylim
            set_seclim      = ax.set_xlim
            set_value_label = ax.set_ylabel
            main_grid       = ax.yaxis.grid
            cat_minor_loc   = ax.xaxis.set_minor_locator
            cat_minor_grid  = ax.xaxis.grid
    
            # ---------- Plot stacked bars ----------
            offset = np.zeros(nGroups * nWithin)
            bar_width = 0.3
    
            for name in names:
                row_flat = flatten_for_plot(dataMat[name])
                kwargs = {stack_key: offset}
                barfunc(
                    pos_bar,
                    row_flat,
                    bar_width,
                    color=colors[name],
                    edgecolor="none",
                    zorder=1,
                    **kwargs,
                )
                offset += row_flat
    
            # ---------- Invert y-axis if needed ----------
            if invert:
                ax.invert_yaxis()
                set_mainlim(figmax, 0)
            else:
                set_mainlim(0, figmax)
    
            # ---------- "Within" labels (one per bar) ----------
            within_labels_flat = []
            if group_by == "model":
                for _m in listModels:
                    within_labels_flat.extend(within_labels)
            else:
                for _s in sce_names:
                    within_labels_flat.extend(within_labels)
    
            ax.set_xticks(pos_bar)
            ax.set_xticklabels(within_labels_flat, rotation=90)
            ax.tick_params(axis="y", which="major", length=0)
    
            # ---------- Group labels (outside the bar block) ----------
            y_min, y_max = ax.get_ylim()
            span = y_max - y_min
            if not invert:
                y_text = y_max + 0.02 * span
                va = "bottom"
            else:
                y_text = y_min - 0.02 * span
                va = "top"
    
            for x, group_label in zip(pos_cols, group_labels):
                ax.text(x, y_text, group_label, ha="center", va=va)
    
            # ---------- Secondary axis (categorical) limits ----------
            set_seclim(0, max_grid)

            # ---------- Dotted lines separating groups ----------
            cat_minor_loc(ticker.FixedLocator(pos_grid))
            cat_minor_grid(color="gray", linestyle="dashed", which="minor")
    
            # ---------- Main grid on value axis ----------
            main_grid(color="gray", linestyle="dashed")
    
            # ---------- Axis labels & spines ----------
            set_value_label(label)
    
            if invert:
               ax.spines['right'].set_visible(False)
               ax.spines['bottom'].set_visible(False)
            else:
               ax.spines['right'].set_visible(False)
               ax.spines['top'].set_visible(False)
    
            # ---------- Legend ----------
            if legend:
                ax.legend(names, loc=pos_legend, ncol=1)
    
            plt.savefig(self.folder_plots + "/" + fileName, bbox_inches="tight")
            plt.savefig(
                self.folder_plots + "/" + fileName + ".png",
                bbox_inches="tight",
                dpi=300,
            )
            plt.show()
            return
    
        # ============================================================
        #                MODE 2: MULTI-SUBPLOT (multi=True)
        # ============================================================
    
        sb.set_style("white")
        cm = 1 / 2.54
    
        fig, axes = plt.subplots(
            1,
            nGroups,
            figsize=(width * cm, height * cm),
            sharex=False,
            sharey=True,    # shared value axis (y)
        )
    
        if nGroups == 1:
            axes = [axes]
    
        bar_width = 0.3
    
        for g in range(nGroups):
            ax = axes[g]
    
            # local positions using same spacing logic as single-axis
            local_pos_bar = []
            local_pos_grid = []
            local_pos_cols = []
    
            ini = 1 * nWithin / 2 - 0 * nWithin * 0.5 + 0.5 * (1 - 0)
            local_pos_grid.append(ini)
            local_pos_cols.append(ini - nWithin / 4 - 0.25)
            for w in range(nWithin):
                pos = ini - (nWithin - 1 - w) * 0.5 - 0.5
                local_pos_bar.append(pos)
    
            local_pos_bar = np.array(local_pos_bar)
            offset_local = np.zeros(nWithin)
    
            barfunc         = ax.bar
            stack_key       = "bottom"
            set_mainlim     = ax.set_ylim
            set_seclim      = ax.set_xlim
            set_value_label = ax.set_ylabel
    
            # stack bars in this group
            for name in names:
                mat = dataMat[name]
                if group_by == "model":
                    row_vals = mat[g, :]
                else:
                    row_vals = mat[:, g]
    
                kwargs = {stack_key: offset_local}
                barfunc(
                    local_pos_bar,
                    row_vals,
                    bar_width,
                    color=colors[name],
                    edgecolor="none",
                    zorder=1,
                    **kwargs,
                )
                offset_local += row_vals
    
            # shared value limit
            if invert:
                ax.invert_yaxis()
                set_mainlim(figmax, 0)
            else:
                set_mainlim(0, figmax)
    
            # within labels
            ax.set_xticks(local_pos_bar)
            ax.set_xticklabels(within_labels, rotation=90)
            ax.tick_params(axis="y", which="major", length=0)
    
            # x-limits (categorical)
            set_seclim(0, local_pos_grid[0])
    
            # group label as title
            ax.set_title(group_labels[g], fontsize=ax.xaxis.get_ticklabels()[0].get_fontsize())

            # grid on value axis
            ax.yaxis.grid(color="gray", linestyle="dashed")
    
            # Only show y-axis label on the first subplot
            if g == 0:
                set_value_label(label)
            else:
                ax.set_ylabel("")
                ax.tick_params(axis="y", labelleft=False)
    
            if invert:
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
            else:
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
    
        if legend:
            handles, labels_legend = axes[0].get_legend_handles_labels()
            if handles:
                fig.legend(handles, labels_legend, loc=pos_legend, ncol=1)
    
        fig.tight_layout()
        plt.savefig(self.folder_plots + "/" + fileName+ ".pdf", bbox_inches="tight")
        plt.savefig(
            self.folder_plots + "/" + fileName + ".png",
            bbox_inches="tight",
            dpi=300,
        )
        plt.show()
        
    def plotLineByScenario(
        self,
        listModelsid,
        map_sce_xaxis,
        varName,
        use_technology_fuel,
        year,
        scale,
        xlabel,
        ylabel,
        fileName,
        width,
        height,
        ylim=None,
        extra_values=None, 
    ):
        """
        Line plot of a variable by scenario/variant, with custom x-positions.
    
        Parameters
        ----------
        listModelsid : list[str]
            Model IDs to plot (keys in self.models).
    
        map_sce_xaxis : dict[(str, str), (str, float)]
            Mapping from (scenario_id, variant) -> (line_id, x_value).
            line_id    : arbitrary string used to group points into lines
                         (e.g. 'resnuc', 'res', or '5% WACC', '10% WACC').
            x_value    : numeric value for the x-axis (e.g. OCC).
    
            Example:
                map_sce_xaxis = {
                    ('abroad-resnuc-high','reference'):   ('resnuc', 12000),
                    ('abroad-resnuc-medium','reference'): ('resnuc', 8000),
                    ('abroad-resnuc-low','reference'):    ('resnuc', 5000),
                    ('abroad-res-high','reference'):      ('res',    12000),
                    ('abroad-res-medium','reference'):    ('res',    8000),
                    ('abroad-res-low','reference'):       ('res',    5000),
                }
    
        varName : str
            Variable name in the data template.
    
        use_technology_fuel : str
            Name of the use / technology / fuel.
    
        year : int
            Year for the plot.
    
        scale : float
            Factor dividing the raw value (e.g. PJ → TWh).
    
        xlabel, ylabel : str
            Axis labels.
    
        fileName : str
            Base name for saved figure files.
    
        width, height : float
            Figure size in centimeters.
            
        ylim : (float, float) or None, optional
            If not None, fixed y-axis limits (ymin, ymax).
        
        """
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sb
        import matplotlib
    
        # ---- Styling ----
        sb.reset_defaults()
        matplotlib.rcParams["font.family"] = "sans-serif"
        matplotlib.rcParams["font.sans-serif"] = "Arial"
    
        # Collect all line_ids (e.g. 'resnuc', 'res', ...)
        line_ids = sorted({v[0] for v in map_sce_xaxis.values()})
    
        # Container: values[model_id][line_id] = list of (x,y)
        values = {
            m: {line_id: [] for line_id in line_ids}
            for m in listModelsid
        }
    
                        
         # ---- Read data ----
        for (sce_id, variant), (line_id, x_val) in map_sce_xaxis.items():
            for m in listModelsid:
                # 1) try to read from self.annualData
                try:
                    val = self.annualData.loc[
                        (sce_id, variant, m, varName, use_technology_fuel, "annual", year),
                        "value",
                    ]
                except KeyError:
                    val = np.nan
    
                # 2) if missing, try extra_values
                if (np.isnan(val) or val is None) and extra_values is not None:
                    key = (sce_id, variant, m)
                    if key in extra_values:
                        val = extra_values[key]
    
                # 3) if still NaN, skip
                if not np.isnan(val):
                    y_val = val / scale
                    values[m][line_id].append((x_val, y_val))
    
        # ---- Figure ----
        cm = 1 / 2.54
        fig, ax = plt.subplots(1, figsize=(width * cm, height * cm))
    
        # Simple color mapping for models
        # If you already have self.modelColors, you can replace this.
        color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        model_colors = {}
        for i, m in enumerate(listModelsid):
            if hasattr(self, "modelColors") and m in self.modelColors:
                model_colors[m] = self.modelColors[m]
            else:
                model_colors[m] = color_cycle[i % len(color_cycle)]
    
        # Some markers for different line_ids so they are distinguishable
        marker_cycle = ["o", "s", "^", "D", "v", "P", "X"]
        line_styles = ["-", "--", "-.", ":"]
    
        # For legend management
        model_handles = {}
        line_handles  = {}
    
        # ---- Plot each model & line ----
        for im, m in enumerate(listModelsid):
            for il, line_id in enumerate(line_ids):
                pts = values[m][line_id]
                if not pts:
                    continue
    
                # sort by x
                pts = sorted(pts, key=lambda t: t[0])
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
    
                color = model_colors[m]
                marker = marker_cycle[il % len(marker_cycle)]
                ls = line_styles[il % len(line_styles)]
    
                # line + markers
                h = ax.plot(
                    xs,
                    ys,
                    linestyle=ls,
                    marker=marker,
                    color=color,
                    label=self.models.get(m, m),
                )[0]
    
                # store handles for potential legends
                model_handles.setdefault(m, h)
                line_handles.setdefault(line_id, h)
    
                # annotate each point: "x: y GW"
                for x_val, y_val in zip(xs, ys):
                    text = f"{int(x_val)}: {y_val:.1f} GW"
                    ax.text(
                        x_val,
                        y_val,
                        text,
                        fontsize=8,
                        va="bottom",
                        ha="center",
                        bbox=dict(
                            boxstyle="round,pad=0.2",
                            edgecolor=color,
                            facecolor="white",
                            linewidth=1,
                        ),
                    )
    
        # ---- Axes, grid, labels ----
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.5)
    
        # Optional: small padding around x
        all_x = [x for m_dict in values.values() for line_pts in m_dict.values() for (x, _) in line_pts]
        if all_x:
            xmin, xmax = min(all_x), max(all_x)
            span = xmax - xmin if xmax > xmin else 1.0
            ax.set_xlim(xmin - 0.05 * span, xmax + 0.05 * span)
            
        # <<< Optional fixed y-limits
        if ylim is not None:
            ax.set_ylim(ylim)
    
        # ---- Legends ----
        from matplotlib.lines import Line2D

        # ---- Build final legend with custom handles ----
        combined_handles = []
        combined_labels  = []
        
        # 1. Model entries  (colored lines, NO markers)
        for m in listModelsid:
            if m in model_handles:
                # get color from the actual plotted handle
                color = model_handles[m].get_color()
                h = Line2D(
                    [], [], 
                    linestyle='-',
                    color=color,
                    marker='None',
                    linewidth=2,
                )
                combined_handles.append(h)
                combined_labels.append(self.models.get(m, m))
        
        # 2. Line-group entries  (black line + marker + linestyle)
        for il, lid in enumerate(line_ids):
            marker = marker_cycle[il % len(marker_cycle)]
            ls     = line_styles[il % len(line_styles)]
        
            h = Line2D(
                [], [],
                linestyle=ls,
                color='DARKGREY',
                marker='None',
                markersize=8,
                linewidth=1.5,
            )
        
            combined_handles.append(h)
            combined_labels.append(lid)
        
        # ---- Draw combined legend ----
        ax.legend(
            combined_handles,
            combined_labels,
            loc="upper right",
            frameon=True,
        )



    
        plt.tight_layout()
        plt.savefig(self.folder_plots + "/" + fileName+ ".pdf", bbox_inches="tight")
        plt.savefig(
            self.folder_plots + "/" + fileName + ".png",
            bbox_inches="tight",
            dpi=300,
        )
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
                            datasubv = self.annualData.loc[(s,m,varName,subv,'annual',year),'value']
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
