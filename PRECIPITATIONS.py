#!/usr/bin/env python
# coding: utf-8

# # Precipitations

# - weather radar in Vietnam: http://amo.gov.vn/radar/
# - **Himawari**: 10min temporal resolution and 2.5min in Japan & 500m pixel resolution

# ### Threshold Arkin Method

# $$ Precipitation (mm) = FRAC * RATE * TIME $$
# 
# - *FRAC*: fractional coverage of IR pixels < 235K over a large domaine (> 50km x 50km)
# - *RATE*: 3mm/h
# - *TIME*: number of hours over which *FRAC* was compiled
# 
# http://tao.atmos.washington.edu/data_sets/gpi/
# 
# $$ GPI = \frac{T_{b}<235K}{\sum T_{b}}\frac{3mm}{1hr} $$

# ### Cloud Indexing Method

# $$ R_{r} = \sum_{i} r_{i}f_{i} $$
# 
# is the amount of rain where $r_{i}$ is the rainfall rate assigned to a cloud type $i$ and $f_{i}$ is the fraction of time that the point is covered with cloud $i$.

# ### NAW Method

# ### Autoestimator Method

# $$ R = A \exp(-bT^{c}) $$
# 
# where R is the rainfall in mm/h, T is the cloud temperatire in K and A, b, c are empirical constant.

# ## Rainfall algorithm: GMSRA
# 
# GOES Multi-Spectral Rainfall Algorithm

# ## Multi-Satellite Algorithms for TRMM and GPM
# 
# http://pmm.nasa.gov/science/precipitation-algorithms

# # Practice

# **1/ Plot the animation pictures to see the development of the Haiyan typhoon for the 3 channels: VIS, Water Vapor & IR.**

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import netCDF4
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import xarray as xr


# In[ ]:


# Variable selection (water vapor, VIS or IR)
var = 'ir'
# Read file
filename = '/Users/macbookairdemilo/Desktop/GRIDSAT-B1.2013.11.07.12.v02r01'
ifile = filename + '.nc'
ofile = var + filename + '.jpg'
ds = xr.open_dataset(ifile)
print(ds)


# In[ ]:


# Region of Interest
latbounds = [0,30]
lonbounds = [100,140]
latmin = min(latbounds)
latmax = max(latbounds)
lonmin = min(lonbounds)
lonmax = max(lonbounds)

# Select data of the input file
lons = ds.lon.sel(lon=slice(lonmin,lonmax)).values
lats = ds.lat.sel(lat=slice(latmin,latmax)).values
if var == 'vis':
    dat = ds.vschn.sel(lat=lats, lon=lons)
elif var == 'ir':
    dat = ds.irwin_cdr.sel(lat=lats, lon=lons)
else:
    dat = ds.irwvp.sel(lat=lats, lon=lons)

# Plot figure
plt.figure(figsize=(10,8))
lonsmesh, latsmesh = np.meshgrid(lons,lats)
m = Basemap(projection='merc', llcrnrlat=latmin, urcrnrlat=latmax, llcrnrlon=lonmin,
           urcrnrlon=lonmax, lat_ts=latmin+(latmax-latmin)/float(2), resolution='i')

# Draw parrallels and meridians
m.drawparallels(np.arange(latmin,latmax,3), labels=[1,0,0,0], fontsize=14)
m.drawparallels(np.arange(lonmin,lonmax,3), labels=[0,0,0,1], fontsize=14)
m.drawcoastlines(linewidth=1)
m.drawcountries(linewidth=1)

x,y = m(lonsmesh, latsmesh)
m.pcolormesh(x,y,np.squeeze(dat), cmap='rainbow')
m.colorbar()
plt.title(filename)
plt.show()


# In[ ]:


# We plot the animation (GIF format)
import PIL

# Variable selection (water vapor, VIS or IR)
var = 'ir' # here we take IR

date = ['09','12','15','18','21']

for i in date:
    filename = '/Users/macbookairdemilo/Desktop/data_GRIDSAT/GRIDSAT-B1.2013.11.07.'+str(i)+'.v02r01'
    ifile = filename + '.nc'
    ofile = var + filename + '.jpg'
    ds = xr.open_dataset(ifile)

    # Region of Interest
    latbounds = [0,30]
    lonbounds = [100,140]
    latmin = min(latbounds)
    latmax = max(latbounds)
    lonmin = min(lonbounds)
    lonmax = max(lonbounds)
    
    lons = ds.lon.sel(lon=slice(lonmin,lonmax)).values
    lats = ds.lat.sel(lat=slice(latmin,latmax)).values
    if var == 'vis':
        dat = ds.vschn.sel(lat=lats, lon=lons)
    elif var == 'ir':
        dat = ds.irwin_cdr.sel(lat=lats, lon=lons)
    else:
        dat = ds.irwvp.sel(lat=lats, lon=lons)

    # Plot figure
    lonsmesh, latsmesh = np.meshgrid(lons,lats)
    m = Basemap(projection='merc', llcrnrlat=latmin, urcrnrlat=latmax, llcrnrlon=lonmin,
                urcrnrlon=lonmax, lat_ts=latmin+(latmax-latmin)/float(2), resolution='i')

    # Draw parrallels and meridians
    m.drawparallels(np.arange(latmin,latmax,3), labels=[1,0,0,0], fontsize=14)
    m.drawparallels(np.arange(lonmin,lonmax,3), labels=[0,0,0,1], fontsize=14)

    x,y = m(lonsmesh, latsmesh)

    m.drawcoastlines(linewidth=1)
    m.drawcountries(linewidth=1)
    
    m.pcolormesh(x,y,np.squeeze(dat), cmap='rainbow')
    m.colorbar()
    plt.title(filename)
    plt.savefig('/Users/macbookairdemilo/Desktop/data_GRIDSAT/Animation/GRIDSAT-B1.2013.11.07.'+str(i)+'.v02r01.jpg')

image_frames = []

for i in date:
    new_frame = PIL.Image.open('/Users/macbookairdemilo/Desktop/data_GRIDSAT/Animation/GRIDSAT-B1.2013.11.07.'+str(i)+'.v02r01.jpg')
    image_frames.append(new_frame)
    
image_frames[0].save('/Users/macbookairdemilo/Desktop/data_GRIDSAT/Animation/haiyan_typhoon_timelapse_'+str(var)+'.gif', format = 'GIF', 
            append_images = image_frames[1: ], 
            save_all = True, duration = 200, 
            loop = 3)


# **2/ Derive rainfall from the IR data using the GPI algorithm**

# In[ ]:


var = 'ir'
# Read file
filename = '/Users/macbookairdemilo/Desktop/GRIDSAT-B1.2013.11.07.12.v02r01'
ifile = filename + '.nc'
ofile = var + filename + '.jpg'
ds = xr.open_dataset(ifile)

# Region of Interest
latbounds = [0,30]
lonbounds = [100,140]
latmin = min(latbounds)
latmax = max(latbounds)
lonmin = min(lonbounds)
lonmax = max(lonbounds)

# Select data of the input file
lons = ds.lon.sel(lon=slice(lonmin,lonmax)).values
lats = ds.lat.sel(lat=slice(latmin,latmax)).values
if var == 'vis':
    dat = ds.vschn.sel(lat=lats, lon=lons)
elif var == 'ir':
    dat = ds.irwin_cdr.sel(lat=lats, lon=lons)
else:
    dat = ds.irwvp.sel(lat=lats, lon=lons)

plt.figure(figsize=(10,8))
plt.title('GPI Precipitations (in m)')
lonsmesh, latsmesh = np.meshgrid(lons,lats)
m = Basemap(projection='merc', llcrnrlat=latmin, urcrnrlat=latmax, llcrnrlon=lonmin,
           urcrnrlon=lonmax, lat_ts=latmin+(latmax-latmin)/float(2), resolution='i')

# Draw parrallels and meridians
m.drawparallels(np.arange(latmin,latmax,3), labels=[1,0,0,0], fontsize=14)
m.drawparallels(np.arange(lonmin,lonmax,3), labels=[0,0,0,1], fontsize=14)
m.drawcoastlines(linewidth=1)
m.drawcountries(linewidth=1)

x,y = m(lonsmesh, latsmesh)
m.pcolormesh(x,y,((np.squeeze(dat)<235)/(np.squeeze(dat)))*3, cmap='rainbow')
m.colorbar()
plt.title(filename)
plt.show()

