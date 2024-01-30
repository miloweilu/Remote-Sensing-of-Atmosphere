#!/usr/bin/env python
# coding: utf-8

# # Skew-T

# - code: https://unidata.github.io/MetPy/latest/tutorials/upperair_soundings.html#sphx-glr-tutorials-upperair-soundings-py

# We use data of Hanoi (station 48820) from the Wyoming University database, using the Siphon package.

# In[ ]:


from datetime import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from metpy.plots import SkewT
from metpy.units import pandas_dataframe_to_unit_arrays, units
import numpy as np
from siphon.simplewebservice.wyoming import WyomingUpperAir

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import Hodograph, SkewT
from metpy.units import units

dt = datetime(2017, 9, 25)
station = '48820'
# Read remote sounding data based on time (dt) and station
df = WyomingUpperAir.request_data(dt, station)

# Create dictionary of united arrays
data = pandas_dataframe_to_unit_arrays(df)


# In[ ]:


# Isolate united arrays from dictionary to individual variables
p = data['pressure']
T = data['temperature']
Td = data['dewpoint']
u = data['u_wind']
v = data['v_wind']


# - **Lifting Condensation Level (LCL)** - The level at which an air parcel’s relative humidity becomes 100% when lifted along a dry adiabatic path.
# - **Parcel Path** - Path followed by a hypothetical parcel of air, beginning at the surface temperature/pressure and rising dry adiabatically until reaching the LCL, then rising moist adiabatially.

# In[ ]:


# Calculate the LCL
lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])

# print(lcl_pressure, lcl_temperature)

# Calculate the parcel profile.
parcel_prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')


# ### Adding a Hodograph
# 
# A hodograph is a polar representation of the wind profile measured by the rawinsonde. Winds at different levels are plotted as vectors with their tails at the origin, the angle from the vertical axes representing the direction, and the length representing the speed. The line plotted on the hodograph is a line connecting the tips of these vectors, which are not drawn.

# In[ ]:


# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 11))
skew = SkewT(fig, rotation=30)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 40)

# Plot LCL temperature as black dot
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

# Plot the parcel profile as a black line
skew.plot(p, parcel_prof, 'k', linewidth=2, label='Parcel profile')

# Shade areas of CAPE and CIN
skew.shade_cin(p, T, parcel_prof, Td)
skew.shade_cape(p, T, parcel_prof)

# Plot a zero degree isotherm
skew.ax.axvline(0, color='c', linestyle='--', linewidth=2, label='Zero degree isotherm')

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

skew.plot_mixing_lines(pressure=np.arange(1000, 99, -20) * units.hPa,
                       linestyle='dotted', color='tab:blue')

# Show the plot

plt.title('{} Sounding'.format(station), loc='left')
plt.title('Valid Time: {}'.format(dt), loc='right')
plt.legend()

# Create a hodograph
# Create an inset axes object that is 40% width and height of the
# figure and put it in the upper center corner.
ax_hod = inset_axes(skew.ax, '30%', '30%', loc=9)
h = Hodograph(ax_hod, component_range=80.)
h.add_grid(increment=20)
h.plot_colormapped(u, v, u)  # Plot a line colored by wind speed

plt.savefig('25.09.2017.png')
plt.show()

