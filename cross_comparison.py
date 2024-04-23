
from distributions import plots 

# Scenario names
sce = ['abroad-together','domestic-together','abroad-alone','domestic-alone']

#  List of files with:
# name: name to be displayed in the plots
# file:  csv file name
# summer: name of the summer day reported by the model
# winter: name of the winter day reported by the model
# color: color to be used for the model in scatter plots
files =  [
          {'name': 'Calliope', 'file': 'resultsCross_Calliope','summer':'Jul 20','winter':'Feb 08','color':'#D57CBE'},
          {'name': 'Expanse', 'file': 'resultsCross_Expanse','summer':'Jul 02','winter':'Jan 01','color':'#FF7D0D'},
          {'name': 'FlexEco', 'file': 'resultsCross_flexeco','summer':'min resudial\nload','winter':'max resudial\nload','color':'#FF0D7D'},
          {'name': 'Nexus-e+\nEP2050+', 'file': 'resultsCross_Nexuse-EP','summer':'Jul 02','winter':'Feb 08','color':'#BCBD21'},
          {'name': 'SecMod', 'file': 'resultsCross_Secmod','summer':'Typical day','winter':'Typical day','color':'#9565BD'},
          {'name': 'SES', 'file': 'resultsCross_SES-epfl','summer':'Typical day','winter':'Typical day','color':'#1E75B3'},
          {'name': 'SES-ETH', 'file': 'resultsCross_SES','summer':'Typical day','winter':'Typical day','color':'#2A9E2A'},
          {'name': 'STEM', 'file': 'resultsCross_STEM','summer':'Week day','winter':'Week day','color':'#D52426'},
          {'name': 'Empa', 'file': 'Data_ehubli_final','summer':'Jul 11','winter':'Feb 15','color':'#8B5349'},
          {'name': 'EP2050+\nZero Basis', 'file': 'resultsCross_EP','summer':'avg. Aug. 13-19','winter':'avg. Feb. 7-13','color':'#7F7F7F'}
          ]

cross_plots = plots.Plots(files,sce,'results','plots') 

#Calculate net imports and exports
cross_plots.calculateNetImports()

