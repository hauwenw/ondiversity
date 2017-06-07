'''
This function sorts data with ascending order based on the parameters
'''
import pandas as pd
from cleanData import dataCleanUp

def sorting(df = None, cr1=None):
# Set default data if parameters are not asigned    
    if df is None:
        df = dataCleanUp()
    
    if cr1 == None:
        cr1 = ["Primary Nat", "Gender", "Last Job Domain Description", "Last Job Title 1"]
    
    if not set(cr1).issubset(set(list(df))):
        print("Warning: the sorting criteria can't be found in the headers of data")
        print("System has assigned the first 3 headers as new criteria")
        cr1 = list(df)[1:3]

    new_df = df.sort_values(by = cr1)
    return new_df