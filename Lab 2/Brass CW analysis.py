# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:22:48 2024

@author: JDMonster
"""

import pandas as pd
import Tensile_Test_Functions as TTS
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



# Importing data
df = pd.read_excel('C:/Users/jossd/195 Lab/Lab 2/Cold Worked Brass_Tensile Data Only_MatE 195-03_2024 10 22.xlsx',
                   sheet_name=None, header=None)


for key, value in df.items():
    length = value.iloc[0,1]
    thickness = value.iloc[1,1]
    width = value.iloc[2,1]
    area = thickness*width
    extension = value.iloc[7:,1]
    load = value.iloc[7:,2]
    
    stress = load/area
    strain = extension/length
    
    youngs, strain = TTS.youngs_and_strain_correction(stress, strain)
    plastic_strain = TTS.plastic_strain(youngs, stress, strain)
    
    x_elastic = np.linspace(0, 0.1 , 100)
    y_elastic = youngs*x_elastic
    
    # Plotting stuff
    sns.lineplot(x=strain[600:], y=stress[600:])
    sns.lineplot(x=x_elastic, y=y_elastic)
    plt.xlabel("Strain")
    plt.ylabel("Stress (MPa)")
    plt.title(f'{key} stress strain curve')
    plt.xlim(0)
    plt.ylim(0, 1.1*max(stress))
    plt.show()

    pass