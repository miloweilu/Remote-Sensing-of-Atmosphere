#!/usr/bin/env python
# coding: utf-8

# # Image Enhancement

# - Enhancement scheme: https://www.ospo.noaa.gov/Organization/FAQ/enhancements.html
# - data: https://ds.data.jma.go.jp/mscweb/data/himawari/sat_img.php?area=se1

# In[4]:


# Image

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

fileorg = 'se1_b03_0410'
img_org = Image.open(fileorg+'.jpg')

nx,ny = np.size(img_org)
pic_org = img_org.load()
r2pix = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        r2pix[ix,iy] = pic_org[ix,iy][1]


# In[2]:


# Fonction to estimate the coefficient of a linear line

def linear_reg(x1,x2,y1,y2):
    a = (y2-y1)/float(x2-x1)
    b = y1 - a*x1
    return a,b


# ## 1/ Linear shifting

# ### Linear scheme

# In[3]:


x = np.arange(0,256)
y = x
y_up = np.minimum(x+50, 255)
y_dn = np.maximum(x-50, 0)

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,y,'k')
plt.plot(x,y_up,'r',label='shifting up')
plt.plot(x,y_dn,'b',label='shifting down')
plt.legend()
plt.title('Linear shifting scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# ### Image

# In[4]:


ln_up = np.zeros([nx,ny],'uint8')
    # uint8: Unsigned integer (0 to 255)
for ix in range(nx):
    for iy in range(ny):
        ln_up[ix,iy] = min(255,r2pix[ix,iy]+50)
ln_up = np.rollaxis(ln_up,0,2)
img_up = Image.fromarray(ln_up)
img_up.save(fileorg+'_ln_up.jpg')

photo = plt.imread(fileorg+'_ln_up.jpg')
plt.imshow(photo, cmap='gray', vmin = 0, vmax = 255)


# ## 2/ Enhancing contrast

# ### Contrast scheme

# In[5]:


x = np.arange(0,256)
y = x
# more contrast
a,b = linear_reg(75,100,0,255)
# less contrast
a1,b1 = linear_reg(0,255,75,100)
y_more = np.maximum(np.minimum(a*x+b,255),0)
y_less = np.maximum(np.minimum(a1*x+b1,255),0)

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,y,'k')
plt.plot(x,y_more,'r',label='more contrast')
plt.plot(x,y_less,'b',label='less contrast')
plt.legend()
plt.title('Contrast scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# ### Image

# In[6]:


# More contrast

a,b = linear_reg(75,100,0,255)
img_plus = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        img_plus_tmp = int(a*r2pix[ix,iy]+b)
        img_plus[ix,iy] = min(255,max(0,img_plus_tmp))
        
img_plus = np.rollaxis(img_plus,0,2)
img_out_plus = Image.fromarray(img_plus)
img_out_plus.save(fileorg+'_more_contrast.jpg')

photo = plt.imread(fileorg+'_more_contrast.jpg')
plt.imshow(photo, cmap='gray', vmin = 0, vmax = 255)


# In[7]:


# Less contrast

a1,b1 = linear_reg(0,255,75,100)
img_plus = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        img_plus_tmp = int(a1*r2pix[ix,iy]+b1)
        img_plus[ix,iy] = min(255,max(0,img_plus_tmp))
        
img_plus = np.rollaxis(img_plus,0,2)
img_out_plus = Image.fromarray(img_plus)
img_out_plus.save(fileorg+'_less_contrast.jpg')

photo = plt.imread(fileorg+'_less_contrast.jpg')
plt.imshow(photo, cmap='gray', vmin = 0, vmax = 255)


# ## 3/ User-defined Enhancement: ZA

# ### ZA scheme

# In[8]:


x = [0,50,100,200,225,255]
y = [0,0,100,200,255,255]

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,x,'k')
plt.plot(x,y,'b',label='ZA')
plt.legend()
plt.title('ZA scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# ### Image

# In[9]:


img_za = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        i=0
        while (r2pix[ix,iy] >= x[i]) and (i < len(x)-1):
            i = i+1
        a,b = linear_reg(x[i-1],x[i],y[i-1],y[i])
        img_za[ix,iy] = min(max(int(a*r2pix[ix,iy]+b),0),255)
img_za = np.rollaxis(img_za,0,2)
img_out = Image.fromarray(img_za)
img_out.save(fileorg+'_ZA.jpg')
photo = plt.imread(fileorg+'_ZA.jpg')
plt.imshow(photo, cmap='gray', vmin=0, vmax=255)


# ## 5/ User-defined Enhancement: MB

# ### MB scheme

# In[10]:


x = [0,50,100,170,170,185,185,200,200,205,210,225,255]
y = [0,0,100,170,120,120,160,160,75,75,0,255,255]

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,x,'k')
plt.plot(x,y,'b',label='MB')
plt.legend()
plt.title('MB scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# ### Image

# In[11]:


img_mb = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        i=0
        while (r2pix[ix,iy] >= x[i]) and (i < len(x)-1):
            i = i+1
        a,b = linear_reg(x[i-1],x[i],y[i-1],y[i])
        img_mb[ix,iy] = min(max(int(a*r2pix[ix,iy]+b),0),255)
img_mb = np.rollaxis(img_mb,0,2)
img_out = Image.fromarray(img_mb)
img_out.save(fileorg+'_MB.jpg')
photo = plt.imread(fileorg+'_MB.jpg')
plt.imshow(photo, cmap='gray', vmin=0, vmax=255)


# ## 5/ User-defined Enhancement: Dvorak

# ### BD scheme

# In[ ]:


# Read enhancement scheme from text file
x1 = []
x2 = []
yb1 = []
yb2 = []
yg1 = []
yg2 = []
yr1 = []
yr2 = []
schemename = 'BD.txt'
f = open(schemename,'r')
lines = f.readlines()
nline = 0
for line in lines:
    nline+=1
    if nline<=0:
        continue
    else:
        temp = line.split()
        x1 = np.append(x1,int(temp[0]))
        x2 = np.append(x2,int(temp[1]))
        yb1 = np.append(yb1,int(temp[2]))
        yb2 = np.append(yb2,int(temp[3]))
        yg1 = np.append(yg1,int(temp[4]))
        yg2 = np.append(yg2,int(temp[5]))
        yr1 = np.append(yr1,int(temp[6]))
        yr2 = np.append(yr2,int(temp[7]))
x = []
yb = []
for i in range(b,len(x1)):
    x = np.append(x,x1[i])
    x = np.append(x,x2[i])
    yb = np.append(yb,yb1[i])
    yb = np.append(yb,yb2[i])

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,x,'k')
plt.plot(x,yb,'b')
plt.title('BD scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# In[30]:


import pandas as pd
BD = pd.read_csv('BD.csv',sep=';')
x1 = BD['x1']
x2 = BD['x2']
yb1 = BD['yb1']
yb2 = BD['yb2']
yg1 = BD['yg1']
yg2 = BD['yg2']
yr1 = BD['yr1']
yr2 = BD['yr2']


x = []
yb = []
for i in range(0, len(x1)):
    x = np.append(x,x1[i])
    x = np.append(x,x2[i])
    yb = np.append(yb,yb1[i])
    yb = np.append(yb,yb2[i])

fig, ax = plt.subplots(figsize=(5,5))
plt.plot(x,x,'k')
plt.plot(x,yb,'b')
plt.title('BD scheme',fontsize=16)
plt.ylabel('Out',fontsize=14)
plt.xlabel('In',fontsize=14)
plt.grid(True,dashes=(1,2,1,2))
plt.show()


# ### Image

# In[31]:


# BLUE Channel

mat_b = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        for i in range(0,len(x1)):
            if r2pix[ix,iy] <= x2[i]:
                a,b = linear_reg(x1[i],x2[i],yb1[i],yb2[i])
                break
        tmp = int(a*pic_org[ix,iy][2]+b)
        mat_b[ix,iy] = min(255, max(0,tmp))
        
# GREEN Channel
mat_g = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        for i in range(0,len(x1)):
            if r2pix[ix,iy] <= x2[i]:
                a,b = linear_reg(x1[i],x2[i],yg1[i],yg2[i])
                break
        tmp = int(a*pic_org[ix,iy][1]+b)
        mat_g[ix,iy] = min(255, max(0,tmp))
        
# RED Channel
mat_r = np.zeros([nx,ny],'uint8')
for ix in range(nx):
    for iy in range(ny):
        for i in range(0,len(x1)):
            if r2pix[ix,iy] <= x2[i]:
                a,b = linear_reg(x1[i],x2[i],yr1[i],yr2[i])
                break
        tmp = int(a*pic_org[ix,iy][0]+b)
        mat_r[ix,iy] = min(255, max(0,tmp))
        
# COMPOSITE
mat = np.zeros([nx,ny,3],'uint8')
mat[...,0] = mat_r
mat[...,1] = mat_g
mat[...,2] = mat_b

mat = np.rollaxis(mat,0,2)
img_out = Image.fromarray(mat)
img_out.save(fileorg+'_BD.jpg')
photo = plt.imread(fileorg+'_BD.jpg')
plt.imshow(photo)


# In[ ]:




