
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:04:11 2024

@author: JDMonster
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import glob
from scipy.stats import linregress
from scipy.interpolate import interp1d

#%%Importing the data
location = ('C:/Users/jossd/195 Lab/Lab 2')
full = str(location) + '/'+ '*.csv'
files = glob.glob(full)
raw_data = []
files = sorted(files)
for n in files:
    raw_data.append(pd.read_csv(str(n), skiprows = 6))
    #print(str(n))
    


#%% Cleaning the data
# Sticking everying in a dictionary with Name Area, height
# keeps things tidier instead of having variables all over the place

samples = { 
    'Specimen 1': (3.26/1000 * 13.19/1000, 65/1000),
    'Specimen 2 cycle': (3.24/1000 * 13.18/1000,65/1000), 
    'Specimen 2 failure': (3.14/1000 * 12.87/1000, 72.66/1000), 
    'Specimen 3 cycle': (3.23/1000 * 13.27/1000, 72.66/1000),
    'Specimen 3 failure': (3.03/1000 * 12.36/1000, 70.42/1000)
    }



#%% Converting raw_data to stress_strain dataframe

# Key is the sample name
# value is strain - stress tuple

processed_data = {}

for index, data in enumerate(raw_data):
    
    new_row = {samples[index]:}




#%% Plotting all together

plt.figure()

for index, data in enumerate(raw_data):
    # Converting raw data into Stress/Strain
    strain = data.iloc[:,1]#/61
    stress = data.iloc[:,2]#/((9.83/1E3)*(3.19/1E3))/1E6
    
    plt.plot(strain, stress, label = names[index])
    plt.xlabel('Displacement (mm)')
    plt.ylabel('Force (N)')
    plt.legend()
    
    

plt.show()




    

