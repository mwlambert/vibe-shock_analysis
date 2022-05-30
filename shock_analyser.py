# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 18:32:46 2021

@author: m.lambert
"""

import idelib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from srs_engine.srs_engine import SRS
from srs_engine.srs_engine import build_freq_array
from dataprocessing.plotting import select_points
from scipy import signal

# plt.style.use('classic')

# DOWNSAMPLE = False
# DOWNSAMPLE_FACTOR = 100
# WINDOW = 10

# file = r'C:\Users\m.lambert\Michael\Git\vibe_shock_analysis\Test Data\Shock and Vibration Inside Mining Drill Head\1o7f8rqcjhty.ide'
# file = r'C:\Users\m.lambert\Michael\Git\vibe_shock_analysis\Test Data\Shock and Vibration Inside Mining Drill Head\p3x0bqam2dpb.ide'
file = r'C:\Users\m.lambert\Michael\Git\vibe_shock_analysis\Test Data\enDAQ-Shock-Data-Share-SRS-Blog\motorcycle-crash.IDE'

ds = idelib.importFile(file)#, updater=idelib.importer.SimpleUpdater())

def remove_sensor_bias(input_accel):
    input_accel = input_accel - input_accel.mean()
    return input_accel

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

T = np.mean(np.diff(df['time_s']))
fs = 1/T
fc = 160
Wn = fc/(fs/2)

plt.figure(figsize=(18,9))
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)') 
plt.title('Shock and Vibration for Car-Motorcycle Crash')
plt.plot(df['time_s'], df['x_data'], label='X Main Accel')
plt.plot(df['time_s'], df['y_data'], label='Y Main Accel')
plt.plot(df['time_s'], df['z_data'], label='Z Main Accel')
# plt.plot(df['time_s'], x_filt, label='X Main Accel Filtered')
plt.legend()
plt.show()

indices = select_points(df['time_s'])
plt.close()

pulse = df[indices[0]:indices[1]].set_index('time_s')
pulse.plot()

pulse = pd.DataFrame(pulse['z_data'] - pulse['z_data'].mean())

srs = SRS(pulse)
srs.calc_smallwood_srs(build_freq_array(start=1, end=100))
srs.plot_results()