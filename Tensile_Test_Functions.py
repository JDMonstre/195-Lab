# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:47:29 2024

@author: JDMonster
"""

import numpy as np
from scipy.stats import linregress


def stress_strain(extension, load, area, length):
    strain = (extension - length)/length
    stress = load/area
    
    return stress, strain

def youngs_and_strain_correction(stress, strain):
    ultimate = max(stress)
    # finding the index nearest to half the maximum
    elastic_mid = np.abs(stress - round(1/2*ultimate)).argmin()
    # selecting the 200 points to the right and left of the elastic mid
    start, end = elastic_mid-200, elastic_mid+200
    # doing a linear regression
    # slope is the youngs modulus
    array = [strain[start:end].tolist(), stress[start:end].tolist()]
    slope, intercept, r_value, p_value, std_err = linregress(array)
    
    # - intercept/slope = x
    offset = -intercept/slope
    # adding the offset to the strain to set to (0,0)
    strain = strain - offset
    
    return slope, strain

def offset_yield_strength(stress, strain, youngs):
    offset = -(0.002*youngs)
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
    return yield_strength, yield_strain
  
def plastic_strain(youngs, stress, strain):

    # the second to last value (avoids the drop off for failure)
    fracture_stress = stress.iloc[-4]
    fracture_strain = strain.iloc[-4]
    # calculating the b of y=mx+b so that it goes through the failure point
    offset = fracture_stress - youngs*fracture_strain
    # calculating the x intercept of this new youngs line
    # 0 = mx + b -> -b/m = x
    plastic_strain = -offset/youngs

    return plastic_strain

    