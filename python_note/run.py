import sys
import os
import numpy as np
import pandas as pd
from sortData import sorting
from cleanData import dataCleanUp
from grouping import grouping
import matplotlib
matplotlib.use('Agg')
from graph import *

file_name, cr, groupName, numofGroup, user_id = sys.argv[1:]

cr = cr.split(',')
groupName = groupName.split(',')
numofGroup = numofGroup.split(',')
temp = []
for i in numofGroup:
    temp.append(int(i))
numofGroup = temp

df = pd.read_csv(file_name)
df = dataCleanUp(df)
df = sorting(df, cr)

#Divide the list according to the Group
for i in range(len(groupName)):
    if i == 0:
        indexG = None
    else:
        indexG = groupName[i-1]

    df = grouping(df,numofGroup[i],indexG,groupName[i], cr)

df = df.sort_values(by = groupName)    
dir_path = os.path.dirname(os.path.realpath(__file__))
df.to_csv(dir_path + '/../app/data/{0}_output.csv'.format(user_id))

#Calculate the result
mainResult, subResult = calc(df, cr, groupName)

#Plot the main group result
chart(mainResult, cr, groupName[0], dir_path + '/../app/data/{0}_main.png'.format(user_id))

#Plot the subgroup result
##get the unique element of maingroup 
mainGroupElm = subResult[groupName[0]].unique()

##Iterate through each maingroup
for m in mainGroupElm:
    filename = dir_path + '/../app/data/{0}_sub_main{1}.png'.format(user_id, str(m))
    sdf = subResult[subResult[groupName[0]] == m]
    chart(sdf, cr, groupName[1], filename)
