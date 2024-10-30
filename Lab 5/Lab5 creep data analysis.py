# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:10:52 2024

@author: JDMonster
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from scipy.stats import linregress
import Tensile_Test_Functions as TTF
from pathlib import Path


#%%Importing the data
location = ('C:/Users/jossd/195 Lab/Lab 5/Clean data')
full = str(location) + '/'+ '*.csv'
files = glob.glob(full)
files = sorted(files)

dataframe = pd.DataFrame(columns=['Name', 'Area', 'Length'
                                  , 'Time','Extension','Load'])



area_HDPE = 3.25E-3 * 13.05E-3
length_HDPE = 66.12
area_fiber = 13.09E-3 * 3.35E-3
length_fiber = 66
area_PVC = 13.34E-3 * 3.32E-3
length_PVC = 66.5

for index, value in enumerate(files):
    rdata = pd.read_csv(str(value))
    name = Path(str(value)).stem
    time = rdata['Time'].iloc[1:].to_numpy()
    extension = rdata['Extension'].iloc[1:].to_numpy()
    load = rdata['Load'].iloc[1:].to_numpy()
    
    row = [name, 'Null', 'Null', time, extension, load]
    dataframe.loc[len(dataframe)] = row

    
# assigning the areas/lengths

dataframe.loc[0, 'Area'] = area_fiber
dataframe.loc[0, 'Length'] = length_fiber
dataframe.loc[1, 'Area'] = area_HDPE
dataframe.loc[2, 'Area'] = area_HDPE
dataframe.loc[3, 'Area'] = area_HDPE
dataframe.loc[1, 'Length'] = length_HDPE
dataframe.loc[2, 'Length'] = length_HDPE
dataframe.loc[3, 'Length'] = length_HDPE
dataframe.loc[4, 'Area'] = area_PVC
dataframe.loc[4, 'Length'] = length_PVC



    
    #print(str(n))



    




