#!/usr/bin/env python
# coding: utf-8

# # CYCLONES
# 
# - examples: https://tropycal.github.io/tropycal/examples/index.html
# - digital typhoon (Haiyan): http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/s/201330.html.en
# - enhancement scheme (Dvorak, ...): https://www.ospo.noaa.gov/Organization/FAQ/enhancements.html
# 
# ### Himawari mission:
#     - launch: 7 Oct 2014
#     - service start: 7 July 2015
#     - duration: 8 years
#     - launch mass: 3500kg
#     - longitude: 140.7°E
#     - number of bands: 16
# 
# The **AHI (Advances Himawari Imager)** is a 16-channel multispectral imager with a resolution down to 500m.
# 
# - python script for himawari: https://loneskyimages.blogspot.com/2020/04/python-script-for-himawari-8.html
# - prcessing images: https://github.com/gSasikala/ftp-himawari8-hsd/blob/main/examples/Processing_Satellite_Imagery.ipynb

# In[1]:


import warnings
warnings.filterwarnings('ignore')


# In[2]:


import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from satpy import Scene
import glob


# In[3]:


files = glob.glob(r'/Users/macbookairdemilo/Desktop/data_HIMAWARI/202312170010/*.DAT') 


# ## Create readers and open files.

# In[4]:


from datetime import datetime 
scn = Scene(filenames=files,  reader='ahi_hsd',filter_parameters={'start_time': datetime(2023,12,17,0,00), 'end_time': datetime(2023,12,17,0,10)})


# ## Load datasets from input files.

# In[5]:


scn.load(["B01"])


# In[6]:


# scn.save_dataset('B01', 'B01.png')


# In[7]:

"""
image = plt.imread('B01.png') 
plt.imshow(image)
cbar=plt.colorbar()
cbar.set_label("Kelvin")
plt.show()
"""


# In[8]:


country_borders = cfeature.NaturalEarthFeature(
    category='cultural',
    name='‘admin_0_boundary_lines_land',
    scale='50m',
    facecolor='none')


# ## Resample from Satellite Imagery and save resampled datasets to current directory.
# 

# ### Crop Scene to a specific Area boundary or bounding box.

# #### Cropping Area: South East Asia

# In[9]:

"""
cropped_scn_aus = scn.crop(ll_bbox=(80, 20, 140, 45))
remapped_scn_aus = cropped_scn_aus.resample(resampler='native')

ccrs= remapped_scn_aus["B01"].attrs['area'].to_cartopy_crs()
ax=plt.axes(projection=ccrs)

ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)

ax.gridlines()
ax.set_global()

plt.imshow(remapped_scn_aus["B01"], transform=ccrs, extent=ccrs.bounds, origin='upper',cmap=plt.cm.gist_gray_r )
cbar=plt.colorbar()
cbar.set_label("Kelvin")
plt.show()
"""


# ## Satpy Composites

# Get names of composites that can be generated from the available datasets.

# In[10]:


scn.available_composite_ids()


# All configured composites known to this Scene.

# In[11]:


scn.available_composite_names()


# In[12]:


scn.load(['water_vapors1'])


# In[13]:


scn.save_dataset('water_vapors1', 'water_vapors1.png')


# In[14]:


image = plt.imread('water_vapors1.png') 
plt.imshow(image)
cbar=plt.colorbar()
cbar.set_label("Kelvin")
plt.show()

