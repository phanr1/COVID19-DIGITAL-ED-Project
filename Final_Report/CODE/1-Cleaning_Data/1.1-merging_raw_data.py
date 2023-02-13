# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 18:32:14 2021

@author: katri
"""

## GOAL: Merge all of csv files for the survey data for each week into 
# one file --> everything_merged.csv (not included for submission)


# Note: We downloaded all of the survey data online from the U.S. Census from: 
# https://www.census.gov/programs-surveys/household-pulse-survey/datasets.html

# Since we were instructed not to include the full dataset, we are not submitting
# each of the csv files for each week nor the full merged dataset 

# However, you can see all the files we downloaded and merged together in our GitHub Repo:
# https://github.gatech.edu/DVA-group97/our-lovely-repo/tree/master/Data/Responses

# You can also see the full merged dataset (3 GB) in our repo:
# https://github.gatech.edu/DVA-group97/our-lovely-repo/blob/master/Merging_and_Cleaning_Files/everything_merged.csv

# We merged together data from weeks 1-37 because these weeks had information 
# related to the digital divide



# If you were to run this file on your own computer to create the full merged dataset,
# you would need to download all the csv files for each week linked in our repo above
# and update the directory ("dir" variable) below to the location of the weekly data



import os
import pandas as pd

# update this for your computer, assuming you have all the weekly data
dir = "C:/Users/katri/our-lovely-repo/Data/Responses"

# looping through csv files and merging them all together
# Note: not all questions/variables are present every week - when it's not present
# it should have null values in the final csv
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
        
        
# code below creates final csv 
everything_merged.to_csv("everything_merged.csv")
print("finished merging files to everything_merged.csv") 
 
# file ends up being over 3 GB with the first 37 weeks
# this code should also work if more weeks of data are added to the
# Data/Responses folder
