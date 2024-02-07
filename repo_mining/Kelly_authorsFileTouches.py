# Script that collects the authors & the dates when they
# touched each file in the list of files generated
# by the adapted file CollectFiles.py (only source files)
import ast
import json
import requests
import csv

import os

import pandas as pd

# Example of .csv file
#app/jni/toolChecker.cpp, Scott Alexander-Bown, 2015-06-19T17:21:37Z
#app/jni/toolChecker.cpp, Matthew Rollings, 2015-06-19T11:06:02Z

# Read the CSV file
csvFilePath = r'C:\Users\kellz\Desktop\CS 460\SeniorDesign\repo_mining\data\file_rootbeer.csv'
data = pd.read_csv(csvFilePath)

# Iterate through the first column [Filename]
# Find files that are not a src file and drop them from the data frame
# i.e. .java or .cpp
for index, row in data.iterrows():    
      filename = row['Filename']

      if (".cpp" not in filename) and (".java" not in filename):
            data.drop(index, inplace = True)

print(data.shape)        
print(data.head(20))