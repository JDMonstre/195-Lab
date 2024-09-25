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
# creating the figure


#%% Data Analysis+plotting individual
# Example stress-strain data (you can load your data from a file)
# stress_strain = pd.read_csv("stress_strain_data.csv")

combined_strain = []
combined_stress = []
combined_youngs = []
youngs_xy_intercepts=[]
offset_x_intercepts = []
offset_yield_xy = []
ultimate_yield_xy = []
fracture = []

for index, value in enumerate(data):
    n = value
    # Converting raw data into Stress/Strain
    strain = n.iloc[:,1]/61
    stress = n.iloc[:,2]/((9.83/1E3)*(3.19/1E3))/1E6
    # removing the last two datapoints to clean things up
    strain = strain[:-2]
    stress = stress[:-2]
    
    combined_strain.append(strain)
    combined_stress.append(stress)
        
    
    # Select roughly half the maximum stress to select elastic region
    elastic = np.abs(stress - round(1/2*max(stress))).argmin()
        
    # Fit a linear regression over this region to confirm
    # Select region to be plus minus 250 datapoints from 1/2 max
    start, end = elastic-200, elastic+200
    # linear regression
    slope, intercept, r_value, p_value, std_err = linregress(strain[start:end],
                                                             stress[start:end])
    combined_youngs.append(slope)
    
    # Generating points along linear regression corresponding to the length of strain
    x_fit = np.linspace(0, strain.max(), len(strain))
    y_fit = slope*x_fit + intercept
    x_intercept = (-intercept/slope)
    youngs_xy_intercepts.append((x_intercept,intercept))

    
    # .2% offset method
    # calculating the offset required to add .002
    intercept_offset = -(0.002 * slope)
    offset_x_intercepts.append(intercept_offset)
    # adding that offset to the current intercept to generate .002 offset
    y_offset = slope*x_fit + intercept_offset + intercept
    
    # Step 3: Find the differences between the .2% line and the curve
    difference = y_offset - stress

    # Step 4: Find the points where they intersect (or differenc)
    indices = []
    indices.append(np.argmin(abs(difference)))
    offset_yield_xy.append((strain[indices[-1]],stress[indices[-1]]))
    ult_yield = np.max(stress)
    ult_yield_strain = strain[np.argmax(stress)]
    ultimate_yield_xy.append((ult_yield_strain,ult_yield))
    fracture_xy = (strain.iloc[-1],stress.iloc[-1])
    fracture.append(fracture_xy)
    
    #Plot the stress-strain curve and highlight the elastic region
    # General plotting stuff
    # Subtracting x-intercept of youngs from everything to shift graphs
    # also not plotting the first 200 points to composite it
    plt.plot(strain[500:] - x_intercept, stress[500:], label='Stress-Strain Curve')
    plt.scatter(strain[indices[-1]]-x_intercept, stress[indices[-1]], color='red', zorder=5)
    plt.annotate(f"0.2% yield \n {stress[indices[-1]]:.2f} MPa",
                 (strain[indices[-1]]-x_intercept, stress[indices[-1]]),
                 xytext=(strain[indices[-1]] - x_intercept, stress[indices[-1]]-0.18*stress.max()),
                 arrowprops=dict(facecolor='black', shrink=0.01, width= .5))
    plt.plot(x_fit - x_intercept, y_fit, 'r', label=f'Youngs Modulus E = {slope/1E3:.2f} MPa \n R-squared : {r_value**2:.3f}')
    plt.plot(x_fit - x_intercept, y_offset, 'y', label = '.2% Offset ')
    plt.scatter(ult_yield_strain-x_intercept, ult_yield, color='green', zorder=5)
    plt.annotate(f"Ultimate yield \n {ult_yield:.2f} MPa",
                 (ult_yield_strain-x_intercept, ult_yield),
                 xytext=(ult_yield_strain - 0.02 - x_intercept, ult_yield-0.18*stress.max()),
                 arrowprops=dict(facecolor='black', shrink=0.01, width= .5))
    # fracture_xy = fracture[index]
    # plt.scatter(fracture_xy[0] - x_intercept,fracture_xy[1],color='purple', zorder=5 )
    # plt.annotate(f"Fracture \n {ult_yield:.2f} MPa",
    #              (fracture_xy[0]-x_intercept, fracture_xy[1]),
    #              xytext=(fracture_xy[0] - 0.02 - x_intercept, fracture_xy[1]-0.18*stress.max()),
    #              arrowprops=dict(facecolor='black', shrink=0.01, width= .5))
    plt.xlabel('Strain')
    plt.ylabel('Stress (MPa)')
    plt.title(names[index])
    plt.xlim(0, 1.1*strain.max())
    plt.ylim(0, 1.1*stress.max())
    plt.legend()
    plt.show()
    

    
    



#%% Plotting combined

plt.figure()
labels = ['Quenched','210 C', '310 C', '440 C', '677 C']
colors = ['red', 'blue', 'green', 'orange', 'purple']
# Dimensions of test = 9.83 mm x 3.19 mm x 61-83mm (depends on where it is)
for index, value in enumerate(combined_strain):
    strain = value
    stress = combined_stress[index]
    slope = combined_youngs[index]
    x_fit = np.linspace(0, strain[450], 100)
    xy_intercepts = youngs_xy_intercepts[index]
    x_intercept, y_intercept = xy_intercepts[0], xy_intercepts[1]
    y_fit = slope*x_fit + y_intercept
    
    plt.plot(strain[450:] - x_intercept, stress[450:], label=labels[index]
             , color = colors[index])
    
    plt.plot(x_fit - x_intercept, y_fit, color = colors[index])

    # integrating below the curve in order to calculate toughness
    integral_trapz = round(np.trapz(stress, strain),2)
    print(f"Toughness of {labels[index]} using the trapezoidal rule: {integral_trapz}")

plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.title('Combined Stress Strain Curve')
plt.legend()
plt.xlim(0)
plt.ylim(0)
plt.show()

#%% Plotting the temperature vs 0.2 yield

offset_yield = [1042.14, 769.25, 806.46, 510.05, 1216.05]
temperatures = [210, 370, 440, 677, 0]

plt.scatter(temperatures, offset_yield)
plt.xlabel('Temperature (C)')
plt.ylabel('0.2 offset yield strength (MPa)')
plt.title('0.2 offset yield strength vs temper temperature')
plt.annotate("Quenched @ 810 C but not tempered",
             (temperatures[-1]+10, offset_yield[-1]),
             xytext=(temperatures[-1]+100, offset_yield[-1]-10),
             arrowprops=dict(facecolor='black', shrink=0.01, width= .5))
plt.show()

