
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
    del n

del location, full, files
    


#%% Cleaning the data and creating a dataframe
# Sticking everying in a dictionary with Name Area, height
# keeps things tidier instead of having variables all over the place

samples = { 
    'Specimen 1': (3.26/1000 * 13.19/1000, 65/1000),
    'Specimen 2 cycle': (3.24/1000 * 13.18/1000,65/1000), 
    'Specimen 2 failure': (3.14/1000 * 12.87/1000, 72.66/1000), 
    'Specimen 3 cycle': (3.23/1000 * 13.27/1000, 72.66/1000),
    'Specimen 3 failure': (3.03/1000 * 12.36/1000, 70.42/1000)
    }


# initializing the dataframe with the following column names
dataframe = pd.DataFrame(columns=['Name', 'Area', 'Length'
                                  , 'Stress (MPa)','Strain'])


for index, value in enumerate(samples):
    name = value
    dimensions = samples[value]
    area = dimensions[0]
    length = dimensions[1]
    data = raw_data[index]
    strain = (data['(mm)']/1000)/length
    stress = (data['(N)']/area)/1E6
    
    
    # combining all the data into a single row
    dank = [name, area, length, stress, strain]
    # adding the data to the dataframe
    dataframe.loc[len(dataframe)] = dank
    
    # clearing variables so they don't appear in my IDE
    del name, dimensions, area, length, data, strain, stress, dank
    del index, value

# Dataframe is the pandas dataframe with all the data

del raw_data, samples

#%% Youngs modulus, ultimate tensile strength

# adding youngs modulus, intercept, and ultimate tensile to the dataframe
dataframe['Youngs'] = 'Unknown'
dataframe['Intercepts'] = 'Unknown'
dataframe['Ultimate'] = 'Unkown'
# iterating through the rows
for index, row in dataframe.iterrows():
    stress = row['Stress (MPa)']
    strain = row['Strain']
    # ultimate = maximum of the stress
    ultimate = max(stress)
    # finding the index nearest to half the maximum
    elastic_mid = np.abs(stress - round(1/2*ultimate)).argmin()
    # selecting the 200 points to the right and left of the elastic mid
    start, end = elastic_mid-200, elastic_mid+200
    # doing a linear regression
    # slope is the youngs modulus
    slope, intercept, r_value, p_value, std_err = linregress(strain[start:end],
                                                             stress[start:end])
    # adding the slope and intercept back to the original dataframe
    dataframe.at[index, 'Youngs'] = slope
    dataframe.at[index, 'Intercepts'] = intercept
    dataframe.at[index, 'Ultimate'] = ultimate
    
    # clearing variables to clean up IDE
    del stress, strain, ultimate, elastic_mid, start, end, slope, intercept,
    del r_value, p_value, std_err, row, index
    
    
    pass




#%% plotting combined

plt.figure()

for index, row in dataframe.iterrows():
    x = row['Strain']
    y = row['Stress (MPa)']
    sample = row['Name']
    plt.plot(x, y, label=sample)
    
    pass

plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.title('Combined Stress Strain Curves')
plt.legend()
plt.xlim(0)
plt.ylim(0)
plt.show()
    

