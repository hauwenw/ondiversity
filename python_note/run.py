import sys
import os
import numpy as np
import pandas as pd
from sortData import sorting
from cleanData import dataCleanUp
from grouping import grouping


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


for i in range(len(GroupName)):
    if i == 0:
        indexG = None
    else:
        indexG = GroupName[i-1]

    df = grouping(df,NumofGroup[i],indexG,GroupName[i], cr)
    
dir_path = os.path.dirname(os.path.realpath(__file__))
df.to_csv(dir_path + '/../app/data/{0}_output.csv'.format(user_id))
