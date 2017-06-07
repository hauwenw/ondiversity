import sys
import os
import numpy as np
import pandas as pd
from sortData import sorting
from cleanData import dataCleanUp
from grouping import grouping
from graph import *

#Parameters input by the user
file_name = input('Please enter file name or press enter to continue:\n')
cr = ['Primary Nat', 'Gender', 'Last Job Title 1']
groupName = ['Section', 'Study Group']
numofGroup = [3, 15]

file_name, cr, GroupName, NumofGroup, user_id = sys.argv[1:]

# file_name = input('Please enter file name or press enter to continue')
# cr = None
# GroupName = ['Section', 'Study Group']
# NumofGroup = [3, 15]
# if file_name == '':
#     file_name = "~/version-control/ondiversity/Data/data_public1.csv"
cr = cr.split(',')
GroupName = GroupName.split(',')
NumofGroup = NumofGroup.split(',')
temp = []
for i in NumofGroup:
    temp.append(int(i))
NumofGroup = temp


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
chart(mainResult, cr, groupName[0], 'main.png')

#Plot the subgroup result
##get the unique element of maingroup 
mainGroupElm = subResult[groupName[0]].unique()

##Iterate through each maingroup
for m in mainGroupElm:
    filename = 'sub_main'+str(m)+'.png'
    sdf = subResult[subResult[groupName[0]] == m]
    chart(sdf, cr, groupName[1], filename)
