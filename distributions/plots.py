# Import all the libraries 
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from functools import reduce      
import numpy as np
import pdb 
import seaborn as sb
from scipy import stats


class Plots:

    def __init__(self, data_list,scenarios,folder_results,folder_plots):

        """ 
        Generic class to upload the data and produce the plots for the model comparison

        Attributes:
            data_list: list of dictionary with the data files, the model names and the color to use for each model
            sceanarios: list with the scenario names
            folder_results: path to folder_results

        """

        # Get the models names
        self.models = [ f['name'] for f in data_list ]
        self.model_colors = [ f['color'] for f in data_list ]
        self.typicalDays = {}
        self.typicalDays['summer'] = [f['summer'] for f in data_list ]
        self.typicalDays['winter'] = [f['winter'] for f in data_list ]
        self.sce = scenarios
        
        self.folder_results = folder_results
        self.folder_plots = folder_plots
        
        # Read all the files in data_list
        df_from_each_file = [self.readData(f) for f in data_list]
        # Merge all files
        self.allData = pd.concat(df_from_each_file).unstack(level=1).droplevel(level=0,axis=1).sort_index()
        #Make all index lower case, to avoid capital and lower cases problems
        self.allData.index = self.allData.index.set_levels(self.allData.index.levels[1].str.lower(), level=1)
        #Calculate net imports and exports
        self.calculateNetImports()
        
        
        self.annualData = self.allData.loc[:,:,'annual',:]
        
        # Read the two days of the hourly data
        self.seasons = ["summer","winter"]  
        self.hourlyData = {}
        for s in self.seasons:
            self.hourlyData[s] =  self.allData.loc[:,:,'typical-day-'+s,:]
        
                
        self.posNegData = {}
       
    #  Reads the annual data from the csv files listed in dictFile
    #  returns a dataFrame with all the data
    def readData(self,dictFile):
        
        data = pd.read_csv(self.folder_results+'/'+dictFile['file']+'.csv', index_col=[0,1,5],header=[0])
        data = data.fillna(0)
        # Get the annual values and make them numeric instead of text
        data['value']=pd.to_numeric(data['value'])
        #Remove all rows with hourly data that are not elec
        data.loc[:,'remove'] = data.apply(lambda x: self.remove(x.variable, x.timeResolution), axis=1)
        data = data[data.remove != 1]
        data = data.drop(['remove'], axis=1)
        # Correct the unit
        data['value']=data.apply(lambda x: x.value * self.correctUnit(x.timeResolution,x.unit),axis=1)
        data = data.drop(['unit'], axis=1)
        
        data = data.reset_index().set_index(['scenario','model','variable', 'timeResolution','timestep'])
        return data
    
    
    def remove(self,var_name,time_resolution):
        """ 
        Checks for hourly variables that are not electricity
        """ 
        
        matches = ["Electricity-consumption|", "Electricity-supply|"]
        if time_resolution != "annual":
            if any(x in var_name for x in matches):
                return 0
            else:
                return 1
        else:
            return 0   

    def correctUnit(self,timeResolution,unit):
        annual_factors = {'twh':1,'gwh':1/1000, 'mwh':1/1e6,'gj':1/3.6,'mtco2':1,'gtco2':1000}
        hourly_factors = {'gw':1,'gwh/h':1, 'mw':1/1000,'mwh/h':1/1000}
        if timeResolution == 'annual':
            if unit.lower() in annual_factors.keys():
                return annual_factors[unit.lower()]
            else:
                return 0
        elif timeResolution == 'typical-day-winter' or timeResolution == 'typical-day-summer':
            if unit.lower() in hourly_factors.keys():
                return hourly_factors[unit.lower()]
            else: 
                return 0

    
    def extractPositiveNegative(self,positive_variables,negative_variables):
        
        positive_labels = [d['name'] for d in positive_variables]
        negative_labels=[d['name'] for d in negative_variables]
        
        timesteps = self.hourlyData['summer'].index.get_level_values(level=2)
        
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

            self.posNegData[season] = posNegData
                            
    
    def recalculateTotalSupply(self,varList_supply):
        """ 
        Calculate Net supply = sum(varList_supply)-Electricity-consumption|Exports-Electricity-consumption|Battery-in-Electricity-consumption|PHS-in
        """ 
        for s in self.sce:
            for m in self.models:
                total = np.nan
                for v in varList_supply:
                    subv = v['data']
                    for t in subv:
                        data_t = self.annualData.loc[(s,t.lower(),'2050'),m]  
                        if not np.isnan(data_t):
                            if np.isnan(total):
                                total = data_t
                            else:
                                total = total + data_t
                battery_in = self.annualData.loc[(s,'electricity-consumption|battery-in','2050'),m] if np.isnan(self.annualData.loc[(s,'electricity-consumption|battery-in','2050'),m])==False else 0
                phs_in = self.annualData.loc[(s,'electricity-consumption|phs-in','2050'),m] if np.isnan(self.annualData.loc[(s,'electricity-consumption|phs-in','2050'),m])==False else 0 
                self.annualData.loc[(s,'electricity-supply|total','2050'),m] = total-self.annualData.loc[(s,'electricity-consumption|exports','2050'),m]-battery_in-phs_in
               
    def calculateNetImports(self):
        """ 
        Calculate net imports and exports for all the models
        """ 
        
        
        # This avoids performance warnings
        new_vars = ['electricity-supply|net-imports','electricity-consumption|net-exports']
        df_imports_annual = pd.DataFrame(index=pd.MultiIndex.from_product([self.sce,new_vars,['annual'], ['2050']] ,names=('scenario', 'variable','timeResolution','timestep')),columns=self.models)
        df_imports_annual.loc[:,:]=0
        
        timeResolution_h = ['typical-day-winter','typical-day-summer']
        timeSteps_h = self.allData.loc[(slice(None),slice(None),'typical-day-winter',slice(None))].index.unique(level=2)
        df_imports_h = pd.DataFrame(index=pd.MultiIndex.from_product([self.sce,new_vars,timeResolution_h, timeSteps_h] ,names=('scenario', 'variable','timeResolution','timestep')),columns=self.models)
        
        self.allData = pd.concat([self.allData,df_imports_annual,df_imports_h])
        self.allData.sort_index(inplace=True)
        
        for s in self.sce:
            for m in self.models:
                #Annual net imports
                
                net = self.allData.loc[(s,'electricity-supply|imports','annual','2050'),m] - self.allData.loc[(s,'electricity-consumption|exports','annual','2050'),m] 
                if net>0:
                    self.allData.loc[(s,'electricity-supply|net-imports','annual','2050'),m] = net
                else:
                    self.allData.loc[(s,'electricity-consumption|net-exports','annual','2050'),m]  = -1*net
                    
                # Calculate net imports and exports for all the models at hourly levels
                for season in timeResolution_h:
                    for h in timeSteps_h:
                        net_h = self.allData.loc[(s,'electricity-supply|imports',season,h),m] - self.allData.loc[(s,'electricity-consumption|exports',season,h),m] 
                        if net_h>0:
                            self.allData.loc[(s,'electricity-supply|net-imports',season,h),m] = net_h
                        else:
                            self.allData.loc[(s,'electricity-consumption|net-exports',season,h),m]  = -1*net_h
                    

    def plotScatter(self,listModels, varName,sceColors,scale,xlabel,xmax,fileName):
        """ 
        Plot scatter of variable by model and scenario. 
        A great part of the function is only to make sure the labels are in the right place

        Parameters:
        ----------
        listModels: list of models to plot
        varName: str, variable name in the data template
        sceColors: list of HEX colors to use for each scenario
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
        

        for index, m in enumerate(listModels):
            y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
            ypos_grid.append(y_ini)
            ypos_cols.append(y_ini-numSce/4-0.25)
            for i in np.arange(numSce):
                y = y_ini - i * 0.5 - 0.5
                plt.scatter(self.annualData.loc[(self.sce[i],varName.lower(),'2050'),m]/scale,y,c=sceColors[i])

        # y axis. Minor ticks are the lines and major ticks the model names

        ax.yaxis.set_major_locator(ticker.FixedLocator(ypos_cols))
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
        plt.show()
        

    def plotBar(self,listModels,varList,scale,xlabel,xmax,fileName,right,legend,pos_legend,onTopVarName):
        """ 
        Bar plot by model and scenario. 
        Parameters:
        ----------
        listModels: list of models to plot
        varList: list of dictionaries with 
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        scale: numeric, if needed, plot will plot var*scale, for unit changes, for example
        xlabel: str, label for x-axis
        xmax: int, maximum level x-axis
        fileName: str, file name for the plot
        right: True if model names have to go on the right
        legend: True if legend has to be displayed
        pos_legend: str: 'lower right' # Options are 'upper left', 'upper right', 'lower left', 'lower right' 
        onTopVarName: str: name of variable to plot on top of the bar plot, '' if none
        """

        numSce= len(self.sce)
        nmodels = len(listModels)

        # Get data
        dataPlot={}
        colors = {}
        names = []


        for v in varList:
            datav = [0]*numSce*nmodels
            colors[v['name']] = v['color']
            names.append(v['name'])
            for index, m in enumerate(listModels):
                for i in np.arange(numSce):
                    for subv in v['data']:
                        try:
                            datasubv = self.annualData.loc[(self.sce[i],subv.lower(),'2050'),m] 
                        except KeyError:
                            datasubv = 0
                        if not np.isnan(datasubv):
                            datav[index*(numSce) + i] = datav[index*(numSce) + i] + datasubv/scale 
            dataPlot[v['name']]= datav  

        # Calculate position of bars, labels and grids
        ypos_grid = []
        ypos_cols = []
        ypos_bar  = []

        for index, m in enumerate(listModels):
            y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
            ypos_grid.append(y_ini)
            ypos_cols.append(y_ini-numSce/4-0.25)
            for i in np.arange(numSce):
                y = y_ini - i * 0.5 - 0.5
                ypos_bar.append(y)

        # figure and axis

        sb.set_style("white")
        fig, (ax)= plt.subplots(1, figsize=(5, 6))


        # Initialize the horizontal-offset for the stacked bar chart.
        x_offset = np.zeros(numSce*nmodels)
        bar_width = 0.3
        for index in colors.keys():
            row = dataPlot[index]
            plt.barh(ypos_bar,row, bar_width, left=x_offset,color=colors[index],zorder=1, edgecolor='none')
            x_offset = x_offset + row

        # Invert axis if the plot is oriented to the right
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
            if legend=='True':
                plt.legend(names, loc=pos_legend, ncol = 1)


        if len(onTopVarName)!=0:
            for index, m in enumerate(listModels):
                y_ini = nmodels*numSce/2 - index*numSce*0.5 + 0.5*(nmodels-index)
                for i in np.arange(numSce):
                    y = y_ini - i * 0.5 - 0.5
                    ax.autoscale(False) # To avoid that the scatter changes limits
                    ax.scatter(self.annualData.loc[(self.sce[i],onTopVarName.lower(),'2050'),m]/scale,y,
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
        plt.show()
        
         
    def plotTechDist(self,listModels,varList,order,ylabel,ymax,fileName):
        """ 
        Plots the distribution by technology
        Parameters:
        ----------
        listModels: list of models to plot
        varList: list of dictionaries with 
            name: name of the technology or group of technologies,
            data: list with the technologies that correspond to this category
            color: color to use for this category
        order: list with the technology order 
        ylabel: str, label for y-axis
        ymax: int, maximum level y-axis
        fileName: str, file name for the plot
        """
    
        variables =[v['name'] for v in varList]
        dataNew =pd.DataFrame (index=pd.MultiIndex.from_product([self.sce,variables] ,names=('scenario','index')), columns=self.annualData.columns)

        for v in varList:
            var =  v['name']
            for s in self.sce:
                for m in listModels:
                    dataNew.loc[(s,var),m] = np. nan
                    for subv in v['data']:
                        datasubv = self.annualData.loc[(s,subv.lower(),'2050'),m]
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
        colors = [ self.model_colors[self.models.index(m)] for m in listModels ]
        
        g1 = sb.catplot(x="index", y="value",hue='Model',hue_order=listModels,palette=sb.color_palette(colors), alpha=.8, data=dataPlot, 
                         order=order);
                         #,height=3.5,aspect=1.5
        g1.set(xlabel='', ylabel=ylabel )
        g1.set(ylim=(0, ymax))

        g2 = sb.boxplot(x="index", y="value", data=dataPlot, order=order,
                    showfliers=False,
                    linewidth=0.75,
                    **PROPS);
        g2.set(xlabel='', ylabel=ylabel )
        g2.set(ylim=(0, ymax))

        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
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

        if season == "summer":
            col_name = "sd-" 
        else:
            col_name = "wd-" 
    

        # Add the typical day info to the model names
        dic_names = {m:m+'\n'+self.typicalDays[season][self.models.index(m)] for m in listModels }
        order_col = [m+'\n'+self.typicalDays[season][self.models.index(m)] for m in listModels ]    

        positive_data = self.posNegData[season].loc[(slice(None),listModels,labels_pos),:]
        negative_data = abs(self.posNegData[season].loc[(slice(None),listModels,labels_neg),:])

        # Melt the dataFrame so it can be plotted with seaborn
        positive_Melted = positive_data.reset_index().melt(id_vars=["scenario","model","index"])
        # Change the names of the columns to the name of the axes in the plot
        positive_Melted.rename(columns={'variable':'hour','value':'Electricity (GW)'}, inplace=True)
        # Remove text from hour
        positive_Melted['hour'] = positive_Melted['hour'].str.replace(col_name, '')
        # Make all columns numeric
        positive_Melted =  positive_Melted.astype({'hour': 'int32','Electricity (GW)': 'float64'})
        positive_Melted['model'] = positive_Melted['model'].replace(dic_names)


         # Melt the dataFrame so it can be plotted with seaborn
        negative_Melted = negative_data.reset_index().melt(id_vars=["scenario","model","index"])
        # Change the names of the columns to the name of the axes in the plot
        negative_Melted.rename(columns={'variable':'hour','value':'Electricity (GW)'}, inplace=True)
        # Remove text from hour
        negative_Melted['hour'] = negative_Melted['hour'].str.replace(col_name, '')
        # Make all columns numeric
        negative_Melted =  negative_Melted.astype({'hour': 'int32','Electricity (GW)': 'float64'})
        negative_Melted['model'] = negative_Melted['model'].replace(dic_names)


   
        positive_Melted['type'] = ylabel_pos 
        negative_Melted['type'] = ylabel_neg 
        
        all_data = pd.concat([positive_Melted, negative_Melted], ignore_index=True, axis=0)
        colors_tech= colors_pos+colors_neg
    
        for s in self.sce:
            data_sce = all_data.loc[all_data['scenario'] == s]
            
            g = sb.displot(kind='hist', 
                           data=data_sce, 
                           x='hour', 
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

        dataNew=abs(self.posNegData[season].loc[(scenario,listModels,varList),:])

        dataNew = dataNew.stack(dropna=False)
        dataNew.index.rename(level=3,names="hour",inplace=True)

        dataPlot = dataNew.reset_index()

        dataPlot.rename(columns={0:'value'},inplace=True)

        sb.set_style("whitegrid")

        g = sb.FacetGrid(dataPlot,  col="index",hue="model",hue_kws={'color': model_colors},col_order=varList
                         ,col_wrap=ncols
                         ,height=2.5,aspect=0.8)
        g = (g.map(plt.plot, "hour", "value")).set(xlim=(0, 24),ylim=(0, ymax),xticks=[0, 6, 12, 18, 24]).set_titles("{col_name}").set_xlabels("")

        if ncols==1:
            for axis in g.axes:
                for subplot in axis:
                    if subplot.get_ylabel()=="value":
                        subplot.set_ylabel(ylabel)

        else:
            for subplot in g.axes:
                if subplot.get_ylabel()=="value":
                    subplot.set_ylabel(ylabel)
        
        
        plt.savefig(self.folder_plots+'/'+fileName,bbox_inches='tight')
        plt.show()
