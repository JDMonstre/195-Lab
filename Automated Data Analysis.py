# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:18:19 2024

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
location = ('C:/Users/jossd/195 Lab')
full = str(location) + '/'+ '*.csv'
files = glob.glob(full)
data = []
files = sorted(files)
for n in files:
    data.append(pd.read_csv(str(n), skiprows = 6))
    #print(str(n))
names = ['Quenched', '210 C Temper', '370 C Temper','440 C Temper', '677 C Temper']


#%% Individual plots
# Example stress-strain data (you can load your data from a file)
# stress_strain = pd.read_csv("stress_strain_data.csv")
for index, value in enumerate(data):
    n = value
    # Converting raw data into Stress/Strain
    strain = n.iloc[:,1]/61
    stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
        
    
    # Select roughly half the maximum stress to select elastic region
    elastic = np.abs(stress - round(1/2*max(stress))).argmin()
        
    # Fit a linear regression over this region to confirm
    # Select region to be plus minus 250 datapoints from 1/2 max
    start, end = elastic-200, elastic+200
    # linear regression
    slope, intercept, r_value, p_value, std_err = linregress(strain[start:end], stress[start:end])
    # Generating points along linear regression corresponding to the length of strain
    x_fit = np.linspace(0, strain.max(), len(strain))
    y_fit = slope*x_fit + intercept
    
    # .2% offset method
    # calculating the offset required to add .002
    intercept_offset = -(0.002 * slope)
    # adding that offset to the current intercept to generate .002 offset
    y_offset = slope*x_fit + intercept_offset + intercept
    
    
    
    # calculating the intersection of .2% and Stress/Strain curve
    # have to interpolate to get intersection
    #line_interp = interp1d(x_fit, y_offset, kind='linear', fill_value="extrapolate")
    # Interpolate y_line values at the x_curve points
    #y_line_interp = line_interp(strain)

    # Step 3: Find the differences between the .2% line and the curve
    difference = y_offset - stress

    # Step 4: Find the points where they intersect (or differenc)
    indices = []
    indices.append(np.argmin(abs(difference)))
    
    #Plot the stress-strain curve and highlight the elastic region
    # General plotting stuff
    plt.plot(strain, stress, label='Stress-Strain Curve')
    plt.scatter(strain[indices[-1]], stress[indices[-1]], color='red', zorder=5, label='Intersections')
    plt.plot(x_fit, y_fit, 'r', label=f'Youngs Modulus E = {slope/1E3:.2f} GPa \n R-squared : {r_value**2:.3f}')
    plt.plot(x_fit, y_offset, 'y', label = '.2% Offset ')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title(names[index])
    plt.xlim(0)
    plt.ylim(0, 1.1*stress.max())
    plt.legend()
    plt.show()

#%% Combined Plot