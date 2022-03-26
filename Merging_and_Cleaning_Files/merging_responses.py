# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 18:32:14 2021

@author: katri
"""

## GOAL: Merge all of csv files in Data/Responses for each week 
## into everything_merged.csv
   
import os
import pandas as pd

# looping through csv files and merging them all together
# Note: not all questions/variables are present every week - when it's not present
# it should have null values in the final csv
dir = "../Data/Responses" 
for i, filename in enumerate(os.listdir(dir)):
    filepath = os.path.join(dir, filename)
    if i == 0:  
         pass #skips first file (description)
    else:
        print("Now loading " + filename)
        current_data = pd.read_csv(filepath, sep=",")
        if i == 1: # inputs the first csv
            everything_merged = current_data.copy()
        else: # concatenates all the following csv files to the first
            everything_merged = pd.concat([everything_merged, current_data], ignore_index=True)
        
        
# code below creates final csv if it doesn not exist yet
# if the csv already exists, it replaces the file with the one we just created
if not os.path.isfile("everything_merged.csv"):
    everything_merged.to_csv("everything_merged.csv")
    print("finished merging files to everything_merged.csv") 
else:
    os.remove("everything_merged.csv")
    everything_merged.to_csv("everything_merged.csv") 
    print("successfully updated merged files to everything_merged.csv") 
    
# file ends up being over 3 GB with the first 37 weeks
# this code should also work if more weeks of data are added to the
# Data/Responses folder