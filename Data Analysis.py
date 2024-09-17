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
    #print(str(n))

#%% Untempered  data

# first column is time, second is extension [mm], third is load [N] 

n = data[0]
# Converting raw data into Stress/Strain
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress, label = 'Curve')



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
# Linear regression of selected region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected) 
x_fit = np.linspace(0, 0.8* Strain.max(), 100)  # 100 points between 0 and max of strain
y_fit = slope*x_fit + intercept
# Plotting the linear fit
plt.plot(x_fit, y_fit, 'r', label=f'Linear fit (E = {slope/1E3:.2f} GPa)')


# .2% offset method
# calculating the offset required to add .002
intercept_offset = -(0.002 * slope)
# adding that offset to the current intercept to generate .002 offset
y_offset = slope*x_fit + intercept_offset + intercept
# Plotting the offset curve
plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')
# Calculating the .2% offset yield strength

# General graph stuff
plt.xlim(0)
plt.ylim(0)
plt.title('Quenched 4130 Steel')
ax.set_xlabel('Engineering Strain')
ax.set_ylabel('Engineering Stress (MPa)')
plt.legend()

print(f"Young's modulus: {slope/1E3:.2f} GPa")

#%% Calculating 210 data

n = data[1]
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress, label = 'Curve')

# Ultimate tensile strength
Ultimate_Tensile = np.max(Stress)


# Selecting linear area of stress strain curve
Strain_min = 0.02
Strain_max = 0.05
# Creating a mask of indexes where Max>Strain>Min = True
Mask = (Strain >= Strain_min) & (Strain <= Strain_max)
# Applying mask to data to select linear region
Strain_selected = Strain[Mask]
Stress_selected = Stress[Mask]
# Linear regression of selected region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected)
# 
x_fit = np.linspace(0, 0.6* Strain.max(), 100)  # 100 points between 0 and max of strain
y_fit = slope*x_fit + intercept
plt.plot(x_fit, y_fit, 'r', label=f'Linear fit (E = {slope/1E3:.2f} GPa)')

# .2% offset method
# calculating the offset required to add .002
intercept_offset = -(0.002 * slope)
# adding that offset to the current intercept to generate .002 offset
y_offset = slope*x_fit + intercept_offset + intercept
# Plotting the offset curve
plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')


# General graph stuff
plt.xlim(0)
plt.ylim(0)
plt.title('210 C tempered 4130 Steel')
ax.set_xlabel('Engineering Strain')
ax.set_ylabel('Engineering Stress (MPa)')
plt.legend()

print(f"Young's modulus: {slope/1E3:.2f} GPa")


#%% Calculating 370 C

n = data[2]
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress, label = 'Curve')

# Ultimate tensile strength
Ultimate_Tensile = np.max(Stress)


# Selecting linear area of stress strain curve
Strain_min = 0.01
Strain_max = 0.045
# Creating a mask of indexes where Max>Strain>Min = True
Mask = (Strain >= Strain_min) & (Strain <= Strain_max)
# Applying mask to data to select linear region
Strain_selected = Strain[Mask]
Stress_selected = Stress[Mask]
# Linear regression of selected region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected)
# 
x_fit = np.linspace(0, 0.6* Strain.max(), 100)  # 100 points between 0 and max of strain
y_fit = slope*x_fit + intercept
plt.plot(x_fit, y_fit, 'r', label=f'Linear fit (E = {slope/1E3:.2f} GPa)')

# .2% offset method
# calculating the offset required to add .002
intercept_offset = -(0.002 * slope)
# adding that offset to the current intercept to generate .002 offset
y_offset = slope*x_fit + intercept_offset + intercept
# Plotting the offset curve
plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')

# General graph stuff
plt.xlim(0)
plt.ylim(0)
plt.title('370 C tempered 4130 Steel')
ax.set_xlabel('Engineering Strain')
ax.set_ylabel('Engineering Stress (MPa)')
plt.legend()

print(f"Young's modulus: {slope/1E3:.2f} GPa")

#%% Calculating 440 C

n = data[3]
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress, label = 'Curve')

# Ultimate tensile strength
Ultimate_Tensile = np.max(Stress)


# Selecting linear area of stress strain curve
Strain_min = 0.02
Strain_max = 0.035
# Creating a mask of indexes where Max>Strain>Min = True
Mask = (Strain >= Strain_min) & (Strain <= Strain_max)
# Applying mask to data to select linear region
Strain_selected = Strain[Mask]
Stress_selected = Stress[Mask]
# Linear regression of selected region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected)
# 
x_fit = np.linspace(0, 0.4* Strain.max(), 100)  # 100 points between 0 and max of strain
y_fit = slope*x_fit + intercept
plt.plot(x_fit, y_fit, 'r', label=f'Linear fit (E = {slope/1E3:.2f} GPa)')


# .2% offset method
# calculating the offset required to add .002
intercept_offset = -(0.002 * slope)
# adding that offset to the current intercept to generate .002 offset
y_offset = slope*x_fit + intercept_offset + intercept
# Plotting the offset curve
plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')

# General graph stuff
plt.xlim(0)
plt.ylim(0)
plt.title('440 C tempered 4130 Steel')
ax.set_xlabel('Engineering Strain')
ax.set_ylabel('Engineering Stress (MPa)')
plt.legend()

print(f"Young's modulus: {slope/1E3:.2f} GPa")


#%% Calculating 670 C

n = data[4]
Strain = n.iloc[:,1]/61
Stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
# Plotting Stress Strain curve
fig, ax = plt.subplots()
ax.scatter(Strain, Stress, label = 'Curve')

# Ultimate tensile strength
Ultimate_Tensile = np.max(Stress)


# Selecting linear area of stress strain curve
Strain_min = 0.02
Strain_max = 0.025
# Creating a mask of indexes where Max>Strain>Min = True
Mask = (Strain >= Strain_min) & (Strain <= Strain_max)
# Applying mask to data to select linear region
Strain_selected = Strain[Mask]
Stress_selected = Stress[Mask]
# Linear regression of selected region
slope, intercept, r_value, p_value, std_err = linregress(Strain_selected, Stress_selected)
# 
x_fit = np.linspace(0, 0.2* Strain.max(), 100)  # 100 points between 0 and max of strain
y_fit = slope*x_fit + intercept
plt.plot(x_fit, y_fit, 'r', label=f'Linear fit (E = {slope/1E3:.2f} GPa)')


# .2% offset method
# calculating the offset required to add .002
intercept_offset = -(0.002 * slope)
# adding that offset to the current intercept to generate .002 offset
y_offset = slope*x_fit + intercept_offset + intercept
# Plotting the offset curve
plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')

# General graph stuff
plt.xlim(0)
plt.ylim(0)
plt.title('670 C tempered 4130 Steel')
ax.set_xlabel('Engineering Strain')
ax.set_ylabel('Engineering Stress (MPa)')
plt.legend()

print(f"Young's modulus: {slope/1E3:.2f} GPa")


#%% Combined Plot

plt.figure()
test = 0
labels = ['Untempered','210 C', '310 C', '440 C', '677 C']
# Dimensions of test = 9.83 mm x 3.19 mm x 61-83mm (depends on where it is)
for n in data:
    # Strain
    x = n.iloc[:,1]/61
    # Force divided by crosssectional area in m2 divided by 10E6 for megapascal
    y = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
    plt.plot(x, y , label = labels[test]) 
    # integrating below the curve in order to calculate toughness
    integral_trapz = round(np.trapz(y, x),2)
    # print(f"Toughness of {labels[test]} using the trapezoidal rule: {integral_trapz}")
    test +=1

plt.xlabel("Engineering Strain")
plt.ylabel("Engineering Stress (MPa)")
plt.title('Stress Strain Curve')
plt.legend()
plt.xlim(0)
plt.ylim(0)

