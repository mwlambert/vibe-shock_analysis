# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 18:32:46 2021

@author: m.lambert
"""

import idelib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataprocessing import plotting_tools as plotting_tools
from srsengine.srs_engine import SRS

plt.style.use('default')

# DOWNSAMPLE = False
# DOWNSAMPLE_FACTOR = 100
# WINDOW = 10

# file = r'C:\Users\m.lambert\Michael\Git\vibeshockanalysis\Test Data\Shock and Vibration Inside Mining Drill Head\1o7f8rqcjhty.ide'
file = r'C:\Users\m.lambert\Michael\Git\vibeshockanalysis\Test Data\Shock and Vibration Inside Mining Drill Head\p3x0bqam2dpb.ide'

ds = idelib.importFile(file)#, updater=idelib.importer.SimpleUpdater())

print("file: {0}\n".format(ds.name))

for chID in ds.channels:
    chObj = ds.channels[chID]
    print("    Channel: {0}".format(chObj))
    for schId, schObj in enumerate(chObj.subchannels):
        print("        SubChannel: {0}".format(schObj))
        print("            Data Type: {0}, units: {1}".format(*schObj.units))



#Channel 8 is the accelerometer data, so we'll start with that.
# First, we get the EventArray
ch8_eventarray = ds.channels[8].getSession()

# The EventArray object has several methods to access data, but the simplest is
# EventArray.arraySlice, which returns a numpy ndarray where the first row is
# the time in microseconds, and the following rows are the subchannels in order
ch8_data = ch8_eventarray.arraySlice()

df = pd.DataFrame({
    'time_s':ch8_data[0, :]/1e6,
    'x_data':ch8_data[1, :],
    'y_data':ch8_data[2, :],
    'z_data':ch8_data[3, :],
    })

# if DOWNSAMPLE:
#     df = df.set_index('time_s')
#     df = df.rolling(window=WINDOW).mean()[::DOWNSAMPLE_FACTOR]
    
#     plt.figure()
#     plt.xlabel('Time (s)')
#     plt.ylabel('Acceleration (g)') 
#     plt.title('Shock and Vibration inside Mining Drill Head')
#     df.plot()

plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)') 
plt.title('Shock and Vibration inside Mining Drill Head')
plt.plot(df['time_s'], df['x_data'], label='X Main Accel')
plt.plot(df['time_s'], df['y_data'], label='Y Main Accel')
plt.plot(df['time_s'], df['z_data'], label='Z Main Accel')
plt.legend()

indices = plotting_tools.select_inputs(df['time_s'])

shock_pulse = df[indices[0]:indices[1]]

plt.close()

srs = SRS(shock_pulse)



