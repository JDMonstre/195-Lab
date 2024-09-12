# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:04:11 2024

@author: JDMonster
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
from scipy.stats import linregress

#Importing the data
location = ('C:/Users/jossd/195 Lab')
full = str(location) + '/'+ '*.csv'
files = glob.glob(full)
data = []
files = sorted(files)
for n in files:
    data.append(pd.read_csv(str(n), skiprows = 6))

#%% Calculating data Untempered  data

# first column is time, second is extension [mm], third is load [N] 

n = data[0]
# Converting raw data into Stress/Strain
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress)
plt.xlim(0)
plt.ylim(0)

# Ultimate tensile strength
Ultimate_Tensile = np.max(Stress)


# Selecting linear area of stress strain curve
Strain_min = 0.04
Strain_max = 0.075
# Creating a mask of indexes where Max>Strain>Min = True
Mask = (Strain >= Strain_min) & (Strain <= Strain_max)
# Applying mask to data to select linear region
Strain_selected = Strain[Mask]
Stress_selected = Stress[Mask]
# Slope + Intercept of region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected)

plt.title('Untempered')
ax.set_xlabel('Strain')
ax.set_ylabel('Stress (MPa)')
plt.plot(Stress, intercept + slope * Stress, 'r', label=f'Linear fit (E = {slope:.2f})')

print(f"Young's modulus: {slope}")

#%% Calculating 370 data

n = data[1]
x = n.iloc[:,1]
y = n.iloc[:,2]
fig, ax = plt.subplots()
ax.scatter(x, y)
plt.title('370 C temper')
ax.set_xlabel('Extension (mm)')
ax.set_ylabel('Load (N)')

#%% Calculating 440 C

n = data[2]
x = n.iloc[:,1]
y = n.iloc[:,2]
fig, ax = plt.subplots()
ax.scatter(x, y)
plt.title('449 C temper')
ax.set_xlabel('Extension (mm)')
ax.set_ylabel('Load (N)')

#%% Calculating 677 C

n = data[3]
x = n.iloc[:,1]
y = n.iloc[:,2]
fig, ax = plt.subplots()
ax.scatter(x, y)
plt.title('677 C temper')
ax.set_xlabel('Extension (mm)')
ax.set_ylabel('Load (N)')

#%% Combined Plot

plt.figure()
test = 0
labels = ['Untempered','677 C', '440 C', '370 C', '210 C']
# Dimensions of test = 9.83 mm x 3.19 mm x 61-83mm (depends on where it is)
for n in data:
    # Extension in mm
    x = n.iloc[:,1]
    # Force divided by crosssectional area in m2 divided by 10E6 for megapascal
    y = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
    plt.plot(x, y , label = labels[test]) 
    # integrating below the curve in order to calculate toughness
    integral_trapz = round(np.trapz(y, x),2)
    print(f"Toughness of {labels[test]} using the trapezoidal rule: {integral_trapz}")
    test +=1

plt.xlabel("Extension (mm)")
plt.ylabel("Load (MPa)")
plt.title('Stress Strain Curve')
plt.legend()
plt.xlim(0)
plt.ylim(0)

