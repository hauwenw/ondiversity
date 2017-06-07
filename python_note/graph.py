#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 23:50:52 2017

@author: Robin
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def calc(df, cr, groupName):
    
   '''
   df is a dataframe
   cr is a list of criteria, eg. ['gender', 'nat', 'profession']
   groupName is a list with 1 or 2 elements, eg. ['section', 'group'],
   the first element is main group, the second is subgroup
   '''
   
   
   maingroup = df[groupName[0]].unique()
       
    #Get unique numbers of the subgroup
   if len(groupName) > 1:
       subgroup = df[groupName[1]].unique()
   else:
       subgroup = None
       subResult = None
    
   #Calcualte the Richness of each main group and subgroup
   #Build empty dataFrame for each main group and subgroup calculation
   calculations = ['Richness', 'IER']
   mainResult = pd.DataFrame(columns = [groupName[0], 'cr', 
                                        calculations[0], calculations[1]])
   subResult = pd.DataFrame(columns = [groupName[0], groupName[1],'cr', 
                                       calculations[0], calculations[1]])
    
   #Iterate through criteria
   for c in cr:
       #Iterate through maingroup
        for i in maingroup:
            r = richness(df[df[groupName[0]] == i], c)
            IER = simpsonIER(df[df[groupName[0]] == i], c)
            index = len(mainResult)
            mainResult.set_value(index,groupName[0], i)
            mainResult.set_value(index,'cr', c)
            mainResult.set_value(index, calculations[0], r)
            mainResult.set_value(index, calculations[1], IER)
            if subgroup != None:
                #Iterate through subgroup
                for s in subgroup:
                    tempdf = df[(df[groupName[0]]==i) & (df[groupName[1]]==s)]
                    r = richness(tempdf, c)
                    IER = simpsonIER(tempdf, c)
                    index = len(subResult)
                    subResult.set_value(index,groupName[0], i)
                    subResult.set_value(index,groupName[1], s)
                    subResult.set_value(index,'cr', c)
                    subResult.set_value(index, calculations[0], r)
                    subResult.set_value(index, calculations[1], IER)
                index = len(subResult)
                r = richness(df[df[groupName[0]] == i], c)
                IER = simpsonIER(df[df[groupName[0]]==i],c)
                subResult.set_value(index,groupName[0], i)
                subResult.set_value(index,groupName[1], 'ALL')
                subResult.set_value(index, 'cr',c)
                subResult.set_value(index, calculations[0], r)
                subResult.set_value(index, calculations[1], IER)
                
        r = richness(df, c)
        IER = simpsonIER(df, c)
        index = len(mainResult)
        mainResult.set_value(index, groupName[0], 'ALL')
        mainResult.set_value(index, 'cr', c)
        mainResult.set_value(index, calculations[0], r)
        mainResult.set_value(index, calculations[1], IER)
        
   return mainResult, subResult
       

                

def chart(df, cr, groupName, filename):
    
    calculations = ['Richness','IER']
    #set up the plot style
    sns.set_style("darkgrid")
    plt.style.use(plt.style.available[1])
    fig, axes = plt.subplots(len(cr), 2, figsize = (10,8))
   
    #Set ylim to 'IER' result
    lim = lambda x:  (0,1) if x == 1 else None
    #Set title to the first chart in the every column
    ti = lambda x, y: y if x == 0 else None
   
    #Build the subplots
    for i, com in enumerate(calculations):
        for k, c, ax in zip([0,1,2], cr, axes):
            
            ax[i].set_ylabel(c)
            
            df[df['cr'] == c].plot(x=groupName, y = com, 
              legend = False, kind = 'bar', 
              ax= ax[i], sharex = cr[i], 
              ylim = lim(i),title = ti(k, com))
            
            plt.setp( ax[i].xaxis.get_majorticklabels(), rotation=0 )
            
            plt.subplots_adjust(hspace = 0.1)        
   
     #Output the plot
    fig
    plt.savefig(filename, bbox_inches='tight')
       

        
        
        
       
       
    
def richness(df, cr):
# This function returns the richness of the 'kind'    
# df : the data frame
# str : the string for column name (specity 'kind')
    items = df[cr].dropna()
    R = len(np.unique(items)) # richness
    return(R)


def simpsonIER(df, cr):
# This function returns the IER (inter-kind encounter rate) 
# c : the data frame
# str : the string for column name
    items = pd.DataFrame(df[cr].dropna())
    N = len(items)
    p = items.groupby(cr).size()
    IER = (1 - sum((p/N)**2)) * N / (N-1)
    return(IER)