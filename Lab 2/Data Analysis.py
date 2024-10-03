
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
dataframe['Y Intercept'] = 'Unknown'
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
    # Subtracting the x intercept of the youngs modulus line so that
    # everything goes through (0,0)
    # Finding x intercept
    # y=mx+b  -> 0 = (slope)*x + intercept
    
    # - intercept/slope = x
    offset = -intercept/slope
    # adding the offset to the strain to set to (0,0)
    strain = strain - offset
    
    # pushing everything to the dataframe
    dataframe.at[index, 'Youngs'] = slope
    # everything should be going through (0,0) so I can hardcode it
    dataframe.at[index, 'Y Intercept'] = 0
    dataframe.at[index, 'Ultimate'] = ultimate
    dataframe.at[index, 'Strain'] = strain
    
    
    # clearing variables to clean up IDE
    del stress, strain, ultimate, elastic_mid, start, end, slope, intercept,
    del r_value, p_value, std_err, row, index
    
    
    pass

#%% 0.02 offset calculations

# initializing the yield strength and the offset intercept for future plotting
dataframe['Yield Strength'] = 'Unknown'
dataframe['Yield Strain'] = 'Unknown'
dataframe['Offset intercept'] = 'Unknown'

for index, row in dataframe.iterrows():
    youngs = row['Youngs']
    offset = -(youngs*0.002)
    strain = row['Strain']
    stress = row['Stress (MPa)']
    # creating y values to find where the lines intersect
    x_area = np.linspace(0, max(strain), len(strain))
    y_line = youngs*x_area + offset
    
    # finding the index of the last place where the signs change
    # subtracting the offset because the data is offset from above
    data = (y_line - (stress-offset))
    # making sure that it's the right data type because I am going insane
    data = data.to_numpy()
    # returns an array where all the sign changes
    intercept = np.where(np.diff(np.sign(data)))[-1]
    # yield strength is the last spot where they change signs thus the [-1]
    yield_strength = (stress.loc[intercept[-1]])
    yield_strain = strain.loc[intercept[-1]]
    
    dataframe.at[index,'Yield Strength'] = yield_strength
    dataframe.at[index,'Offset intercept'] = offset
    dataframe.at[index,'Yield Strain'] = yield_strain
    pass


del youngs, offset, strain, stress, y_line, data, yield_strength, index
del yield_strain, x_area, intercept
#%% yield strength and plastic 

# Now that I have the youngs modulus I can calculate the yield strength


#%% plotting combined

plt.figure()

for index, row in dataframe.iterrows():
    x_curve = row['Strain']
    y_curve = row['Stress (MPa)']
    sample = row['Name']
    youngs = row['Youngs']
    y_intercept = row['Y Intercept']
    
    x_line = np.linspace(0, 0.5, 100)
    y_line = youngs*x_line - y_intercept
    
    plt.plot(x_curve, y_curve, label=sample)
    plt.plot(x_line, y_line, label = f' Youngs modulus of {sample} is {youngs} MPa')
    pass

plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.title('Combined Stress Strain Curves')
#plt.legend()
plt.xlim(0, 0.075)
plt.ylim(0, 500)
plt.show()
    


del x_curve, y_curve, sample, youngs, y_intercept, x_line, y_line, row, index


#%% Individual plots


for index, row in dataframe.iterrows():
    plt.figure()
    x_curve = row['Strain']
    y_curve = row['Stress (MPa)']
    sample = row['Name']
    youngs = row['Youngs']
    y_intercept = row['Y Intercept']
    
    x_line = np.linspace(0, 0.5, 100)
    y_line = youngs*x_line - y_intercept
    
    plt.plot(x_curve, y_curve, label=sample)
    plt.plot(x_line, y_line, label = f' Youngs modulus of {sample} is {youngs} MPa')
    plt.xlabel("Strain")
    plt.ylabel("Stress (MPa)")
    plt.xlim(0, 0.075)
    plt.ylim(0, 500)
    plt.show()
    pass



del x_curve, y_curve, sample, youngs, y_intercept, x_line, y_line, row, index