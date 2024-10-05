
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
# this ended up being a bad idea but whatever  Should have just put everyting
# in a pandas array to begin with

samples = { 
    'Specimen 1': (3.26/1000 * 13.19/1000, 65/1000),
    'Specimen 2 cycle': (3.24/1000 * 13.18/1000,65/1000), 
    'Specimen 2 failure': (3.24/1000 * 13.18/1000,65/1000), 
    'Specimen 3 cycle': (3.23/1000 * 13.27/1000, 72.66/1000),
    'Specimen 3 failure': (3.23/1000 * 13.27/1000, 72.66/1000)
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

dataframe['%'] = [0, 15, 15, 30, 30]


#%% Youngs modulus, ultimate tensile strength

# adding youngs modulus, intercept, and ultimate tensile to the dataframe
dataframe['Youngs'] = 'Unknown'
dataframe['Ultimate'] = 'Unkown'
dataframe['Ultimate Strain'] = 'Unknown'
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
    
    # gives me the location of the ultimate yield strength etc
    strain_index = stress.idxmax() if stress.eq(ultimate).any() else None
    ultimate_strain = strain.iloc[strain_index]
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
    # everything should go through 0,0, the offset of the graph is strain[0]
    dataframe.at[index, 'Ultimate'] = ultimate
    dataframe.at[index, 'Strain'] = strain
    dataframe.at[index, 'Ultimate Strain'] = ultimate_strain
    
    
    # clearing variables to clean up IDE
del stress, strain, ultimate, elastic_mid, start, end, slope, intercept,
del r_value, p_value, std_err, row, index, strain_index, ultimate_strain
del offset
    
    
    

#%% 0.02 offset calculations

# initializing the yield strength and the offset intercept for future plotting
dataframe['Yield Strength'] = 'Unknown'
dataframe['Yield Strain'] = 'Unknown'
dataframe['Offset intercept'] = 'Unknown'

for index, row in dataframe.iterrows():
    youngs = row['Youngs']
    offset = -(0.002*youngs)
    strain = row['Strain']
    stress = row['Stress (MPa)']
    # creating y values to find where the lines intersect
    x_area = np.linspace(min(strain), max(strain), len(strain))
    y_line = youngs*x_area + offset
    
    # finding the index of the last place where the signs change
    data = (y_line - stress)
    # making sure that it's the right data type because I am going insane
    data = data.to_numpy()
    # returns an array where all the sign changes
    intercept = np.where(np.diff(np.sign(data)))[-1]
    # yield strength is the last spot where they change signs thus the [-1]
    # Finding it from the offset graph because taking it from the data gives
    # me wrong stuff???
    yield_strength = y_line[intercept[-1]]
    yield_strain = x_area[intercept[-1]]
    
    dataframe.at[index,'Yield Strength'] = yield_strength
    dataframe.at[index,'Offset intercept'] = offset
    dataframe.at[index,'Yield Strain'] = yield_strain
    pass


del youngs, offset, strain, stress, y_line, data, yield_strength, index
del yield_strain, x_area, intercept, row
#%% plastic deformation strain

# calculating the plastic fracture strain (kinda).  I do this for the cycled 
# samples so that it gives me the offset that I need to add to the fractured
# samples.  

dataframe['Plastic Strain'] = 'Unknown'
dataframe['Fracture Stress'] = 'Unknown'
dataframe['Fracture Strain'] = 'Unknown'
dataframe['Plastic Offset'] = 'Unknown'

for index, row in dataframe.iterrows():
    youngs = row['Youngs']
    stress = row['Stress (MPa)']
    strain = row['Strain']
    # the second to last value (avoids the drop off for failure)
    fracture_stress = stress.iloc[-2]
    fracture_strain = strain.iloc[-2]
    # calculating the b of y=mx+b so that it goes through the failure point
    offset = fracture_stress - youngs*fracture_strain
    # calculating the x intercept of this new youngs line
    # 0 = mx + b -> -b/m = x
    plastic_strain = -offset/youngs
    dataframe.at[index, 'Plastic Strain'] = plastic_strain
    dataframe.at[index, 'Fracture Stress'] = fracture_stress
    dataframe.at[index, 'Fracture Strain'] = fracture_strain
    dataframe.at[index, 'Plastic Offset'] = offset
    
    pass


del fracture_strain, fracture_stress, index, offset, plastic_strain
del row, strain, stress, youngs


#%% Specimen 1 zoomed in for offset

row = dataframe.iloc[0]
name = row['Name']
stress = row['Stress (MPa)']
strain = row['Strain']
youngs = row['Youngs']
ultimate_stress = row['Ultimate']
ultimate_strain = row['Ultimate Strain']
yield_strength = row['Yield Strength']
yield_strain = row['Yield Strain']
offset_intercept = row['Offset intercept']
plastic_strain = row['Plastic Strain']
plastic_offset = row['Plastic Offset']
work = row['%']

plt.figure()
# only plotting from the first 400 points to remove any wacky behavior
plt.plot(strain.iloc[225:], stress.iloc[225:])
# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs, label = f'Modulus = {youngs:.0f} (MPa)')
# using the same x values but now to calculate the offset values
y_offset = x_youngs*youngs+offset_intercept
# plotting the 0.2% offset line
plt.plot(x_youngs, y_offset)
# plotting the 0.2% dot
plt.scatter(yield_strain, yield_strength)
plt.annotate(f"0.2% yield strength \n {yield_strength:.0f} MPa",
             (yield_strain, yield_strength),
             xytext=(yield_strain + 0.005*ultimate_strain, 
                     yield_strength-0.15*ultimate_stress),
             arrowprops=dict(facecolor='black', shrink=0.01, width= .5))






plt.title(f'{name} at {work}% reduction')
plt.xlim(0, yield_strain*1.5)
# setting the upper bounds as a percentage of the tensile stress
plt.ylim(0, 1.25*yield_strength)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.legend()

plt.show()


del row, name, stress, strain, youngs, ultimate_strain, ultimate_stress
del yield_strain, yield_strength, offset_intercept, plastic_offset
del plastic_strain, work, x_youngs, y_offset, y_youngs
#%% Specimen 2 zoomed in

row = dataframe.iloc[1]
name = row['Name']
stress = row['Stress (MPa)']
strain = row['Strain']
youngs = row['Youngs']
ultimate_stress = row['Ultimate']
ultimate_strain = row['Ultimate Strain']
yield_strength = row['Yield Strength']
yield_strain = row['Yield Strain']
offset_intercept = row['Offset intercept']
plastic_strain = row['Plastic Strain']
plastic_offset = row['Plastic Offset']
work = row['%']

plt.figure()
# only plotting from the first 400 points to remove any wacky behavior
plt.plot(strain.iloc[225:], stress.iloc[225:])
# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs, label = f'Modulus = {youngs:.0f} (MPa)')
# using the same x values but now to calculate the offset values
y_offset = x_youngs*youngs+offset_intercept
# plotting the 0.2% offset line
plt.plot(x_youngs, y_offset)
# plotting the 0.2% dot
plt.scatter(yield_strain, yield_strength)
plt.annotate(f"0.2% yield strength \n {yield_strength:.0f} MPa",
             (yield_strain, yield_strength),
             xytext=(yield_strain + 0.005*ultimate_strain, 
                     yield_strength-0.15*ultimate_stress),
             arrowprops=dict(facecolor='black', shrink=0.01, width= .5))






plt.title(f'{name} at {work}% reduction')
plt.xlim(0, yield_strain*1.5)
# setting the upper bounds as a percentage of the tensile stress
plt.ylim(0, 1.25*yield_strength)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.legend()

plt.show()

del row, name, stress, strain, youngs, ultimate_strain, ultimate_stress
del yield_strain, yield_strength, offset_intercept, plastic_offset
del plastic_strain, work, x_youngs, y_offset, y_youngs

#%% Specimen 3 zoomed in


row = dataframe.iloc[3]
name = row['Name']
stress = row['Stress (MPa)']
strain = row['Strain']
youngs = row['Youngs']
ultimate_stress = row['Ultimate']
ultimate_strain = row['Ultimate Strain']
yield_strength = row['Yield Strength']
yield_strain = row['Yield Strain']
offset_intercept = row['Offset intercept']
plastic_strain = row['Plastic Strain']
plastic_offset = row['Plastic Offset']
work = row['%']

plt.figure()
# only plotting from the first 400 points to remove any wacky behavior
plt.plot(strain.iloc[225:], stress.iloc[225:])
# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs, label = f'Modulus = {youngs:.0f} (MPa)')
# using the same x values but now to calculate the offset values
y_offset = x_youngs*youngs+offset_intercept
# plotting the 0.2% offset line
plt.plot(x_youngs, y_offset)
# plotting the 0.2% dot
plt.scatter(yield_strain, yield_strength)
plt.annotate(f"0.2% yield strength \n {yield_strength:.0f} MPa",
             (yield_strain, yield_strength),
             xytext=(yield_strain + 0.005*ultimate_strain, 
                     yield_strength-0.15*ultimate_stress),
             arrowprops=dict(facecolor='black', shrink=0.01, width= .5))






plt.title(f'{name} at {work}% reduction')
plt.xlim(0, yield_strain*1.5)
# setting the upper bounds as a percentage of the tensile stress
plt.ylim(0, 1.25*yield_strength)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.legend()

plt.show()

del row, name, stress, strain, youngs, ultimate_strain, ultimate_stress
del yield_strain, yield_strength, offset_intercept, plastic_offset
del plastic_strain, work, x_youngs, y_offset, y_youngs

#%% zoomed out specimen 1 graph

row = dataframe.iloc[0]
name = row['Name']
stress = row['Stress (MPa)']
strain = row['Strain']
youngs = row['Youngs']
ultimate_stress = row['Ultimate']
ultimate_strain = row['Ultimate Strain']
yield_strength = row['Yield Strength']
yield_strain = row['Yield Strain']
offset_intercept = row['Offset intercept']
plastic_strain = row['Plastic Strain']
plastic_offset = row['Plastic Offset']

plt.figure()
# only plotting from the first 400 points to remove any wacky behavior
plt.plot(strain.iloc[400:], stress.iloc[400:])
# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs, label = f'Modulus = {youngs:.0f} (MPa)')

plt.scatter(ultimate_strain, ultimate_stress)

plt.annotate(f"Ultimate tensile stress \n {yield_strength:.0f} MPa",
             (ultimate_strain, ultimate_stress),
             xytext=(ultimate_strain - 0.1*ultimate_strain, 
                     ultimate_stress-.2*ultimate_stress),
             ha='center',
             arrowprops=dict(facecolor='black', shrink=0.01, width= .5))





plt.ylabel('Stress (MPa)')
plt.xlabel('Strain')
plt.title(name)
plt.xlim(0)
# setting the upper bounds as a percentage of the tensile stress
plt.ylim(0, 1.1*ultimate_stress)
plt.legend(loc = 'lower right')

plt.show()

del row, name, stress, strain, youngs, ultimate_strain, ultimate_stress
del yield_strain, yield_strength, offset_intercept, plastic_offset
del plastic_strain, x_youngs, y_youngs


#%% Specimen 2 combined

cycle = dataframe.iloc[1]
fail = dataframe.iloc[2]

cycle_stress = cycle['Stress (MPa)']
cycle_strain = cycle['Strain']
fail_stress = fail['Stress (MPa)']
fail_strain = fail['Strain']
youngs = cycle['Youngs']
plastic_strain = cycle['Plastic Strain']
ultimate_stress = fail['Ultimate']


plt.figure()
#plotting only past the first 400 points of the cycle for the youngs modulus
plt.plot(cycle_strain[400:], cycle_stress[400:])
plt.plot(fail_strain+plastic_strain, fail_stress)

# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs)


plt.title('Specimen 2 15% reduction')
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.xlim(0)
plt.ylim(0 , 1.1*ultimate_stress)
plt.show()

del cycle, cycle_strain, cycle_stress, fail, fail_strain, fail_stress
del plastic_strain, ultimate_stress, x_youngs, y_youngs, youngs

#%% Specimen 3 combined

cycle = dataframe.iloc[3]
fail = dataframe.iloc[4]

cycle_stress = cycle['Stress (MPa)']
cycle_strain = cycle['Strain']
fail_stress = fail['Stress (MPa)']
fail_strain = fail['Strain']
youngs = cycle['Youngs']
plastic_strain = cycle['Plastic Strain']
ultimate_stress = fail['Ultimate']

plt.figure()
#plotting only past the first 400 points of the cycle for the youngs modulus
plt.plot(cycle_strain[400:], cycle_stress[400:])
plt.plot(fail_strain+plastic_strain, fail_stress)

# generating 100 points from 0 to 0.1 for the x values of the youngs modulus
x_youngs = np.linspace(0, 0.1 , 100)
# generating the y values of the youngs modulus line
y_youngs = youngs * x_youngs
# plotting the youngs modulus, rounding to nearest whole number
plt.plot(x_youngs, y_youngs)


plt.title('Sample 3 30% reduction ')
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.xlim(0)
plt.ylim(0 , 1.1*ultimate_stress)
plt.show()

del cycle, cycle_strain, cycle_stress, fail, fail_strain, fail_stress
del plastic_strain, ultimate_stress, x_youngs, y_youngs, youngs
#%% plotting combined

plt.figure()

for index, row in dataframe.iterrows():
    x_curve = row['Strain']
    y_curve = row['Stress (MPa)']
    sample = row['Name']
    youngs = row['Youngs']
    
    x_line = np.linspace(0, 0.5, 100)
    y_line = youngs*x_line
    
    plt.plot(x_curve, y_curve, label=sample)
    plt.plot(x_line, y_line, label = f' Youngs modulus of {sample} is {youngs} MPa')
    pass

plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.title('Combined Stress Strain Curves')
#plt.legend()
plt.xlim(0, 0.5)
plt.ylim(0, 500)
plt.show()
    


del x_curve, y_curve, sample, youngs, x_line, y_line, row, index

