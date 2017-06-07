import numpy as np
import pandas as pd
from sortData import sorting


def grouping(df = None, numGroup = 3, indexGroup = None, groupName = 'Section', cr = None):

    '''
    This function will divide the data into different groups
    by assigning integer index to each data
    --- input parameters ---
    df is input data frame
    numGroup is how many groups gonna divide into
    indexGroup is specified when subgrouping in an already divided group
    groupName = the name of the group is going generate
    cr = diversity criteria, eg. gender, nationality, etc.
    --- end ---
    '''
    #If dataframe is not assigned, call sorting() to get sample data
    if df is None:      
        df = sorting()
    
    #List out the unique numbers in indexGroup
    if indexGroup != None:
        unq = df[indexGroup].unique()

    else:
        unq = 0
        
    #If there's no 2 and above group in indexGroup, then do the grouping directly
    if (indexGroup == None or len(unq) == 1):
        l = list(np.arange(1,numGroup+1,1))
        df[groupName] = ctile(l, len(df))
        return df
    
    #If there's indexGroup, do grouping under each indexGroup
    else:
        df2 = pd.DataFrame()
        for i in unq:
            ddf = df[df[indexGroup]==i]
            ddf = sorting(ddf, cr)
            df2 = df2.append(grouping(ddf, numGroup, None, groupName)) 
        return df2
    
'''
ctile(l,length) will generate a repeated series of number l to an assigned length.

--- input parameters ---
l is a sequence of number
length of the out put series
--- end ---
'''
def ctile(l,length):
    rint = int(length/len(l))
    rest = length%len(l)
    result = list(np.tile(l,rint)) + l[:rest]
    return result