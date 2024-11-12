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

#%% Individual plots
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
    yield_strength, yield_strain , offset = TTS.offset_yield_strength(stress, strain, youngs)
    
    x_elastic = np.linspace(0, 0.3 , 100)
    y_elastic = youngs*x_elastic
    y_yield =  youngs*x_elastic + offset
    b = -youngs*plastic_strain
    y_plastic = youngs*x_elastic + b
    fracture_strain = strain.iloc[-18]
    fracture_stress = stress.iloc[-18]
    # Plotting stuff
    

    sns.lineplot(x=strain[600:], y=stress[600:])
    sns.lineplot(x=x_elastic, y=y_elastic, 
                 label = f'E = {youngs/1000: .1f} GPa')
    sns.lineplot(x=x_elastic, y=y_yield)
    sns.lineplot(x=x_elastic, y=y_plastic)

    ax = plt.gca()
    # offset yield strength arrow
    ax.annotate(f'Offset yield \n={yield_strength: .0f} (MPa)',
                xy=(yield_strain, yield_strength), 
                xytext=(1.1 * yield_strain, 0.6 * yield_strength),
                arrowprops=dict(facecolor='black', arrowstyle="->", lw=2, ec='black'))
    # Fracutre strain arrow
    ax.annotate(f' Fracture Strain \n={fracture_strain: .3f}',
                xy=(fracture_strain, fracture_stress), 
                xytext=(fracture_strain*.7, 1.15 *fracture_stress ),
                arrowprops=dict(facecolor='black', arrowstyle="->", lw=2, ec='black'))
    # plastic strain arrow
    ax.annotate(f' Plastic Strain \n={plastic_strain: .3f}',
                xy=(plastic_strain, 0), 
                xytext=(plastic_strain*.5, 100 ),
                arrowprops=dict(facecolor='black', arrowstyle="->", lw=2, ec='black'))
    plt.xlabel("Strain")
    plt.ylabel("Stress (MPa)")
    plt.legend(loc='lower right')
    plt.title(f'{key} stress strain curve')
    plt.xlim(0, 1.25* max(strain))
    plt.ylim(0, 1.25*max(stress))      
    plt.show()

    pass


#%% combined plots.  Yes this is inefficient.  Deal with it
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
    
    sns.lineplot(x=strain[600:], y=stress[600:], label = key)
    sns.lineplot(x=x_elastic, y=y_elastic)
    plt.xlabel("Strain")
    plt.ylabel("Stress (MPa)")
    plt.legend(loc='lower right')
    plt.title(f'Combined stress strain curve')
    plt.xlim(0)
    plt.ylim(0, 1.1*max(stress))      

    pass
plt.show()