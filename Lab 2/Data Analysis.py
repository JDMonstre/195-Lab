
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
location = ('Lab 2')
full = str(location) + '/'+ '*.csv'
files = glob.glob(full)
data = []
files = sorted(files)
for n in files:
    data.append(pd.read_csv(str(n), skiprows = 6))
    #print(str(n))
names = ['Specimen 1', 'Specimen 2 Cycled', 'Specimen 2 Failure','Specimen 3 cycle', 'Specimen 3 fail']
# creating the figure


#%% Untempered  data

# first column is time, second is extension [mm], third is load [N] 

n = data[0]
# Converting raw data into Stress/Strain
strain = n.iloc[:,1]/61
stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6

# Step 1: Define a curve (x_curve, y_curve) and a line (x_line, y_line)


x_offset = np.linspace(-8, 8, 30)  # 30 points for the line
m = 16000  # Slope
b = -200  # Intercept
y_offset = m * x_offset + b  # Line: y = mx + b

# Step 2: Interpolate the curve or the line to have a common set of x values
# We'll interpolate the line to match the x values of the curve
line_interp = interp1d(x_offset, y_offset, kind='linear', fill_value="extrapolate")

# Interpolate y_line values at the x_curve points
y_line_interp = line_interp(strain)

# Step 3: Find the differences between the interpolated line and the curve
difference = stress - y_line_interp

# Step 4: Find where the difference changes sign (indicating an intersection)
indices = np.where(np.diff(np.sign(difference)))[0]

# Step 5: For more precise intersection points, you can use interpolation or a numerical solver

# Step 6: Plot for visualization
plt.plot(strain, stress, label="Curve: $y = x^2$")
plt.plot(strain, y_line_interp, label="Interpolated Line: $y = mx + b$")
plt.scatter(strain[indices], stress[indices], color='red', zorder=5, label='Intersections')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Intersection of Line and Curve with Different Sizes')
plt.grid(True)
plt.show()

# Print intersection points
for index in indices:
    print(f"Intersection point: x = {strain[index]:.2f}, y = {stress[index]:.2f}")

    
#%% Plotting all together

plt.figure()

for n in data:
    # Converting raw data into Stress/Strain
    strain = n.iloc[:,1]/61
    stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
    
    plt.plot(strain, stress)

plt.show()
    

