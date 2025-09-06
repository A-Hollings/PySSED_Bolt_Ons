# Import modules

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d
import matplotlib.colors as mcolors

# Toggle interactive rotation
# %matplotlib qt

# Import data

foldername = 'Actual_MiniJPAS_r-5_pl-0.1'
hrd_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/PySSED Outputs/'+str(foldername)+'/hrd.dat', sep = '\t', header = 1)
anc_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/PySSED Outputs/'+str(foldername)+'/anc1.txt', sep = '\t', header = 0)

# 'Jury-rigging' the distance variable from the incorrectly read table

dist = anc_df['Distance_err']
dist = dist.replace('--', )
dist = dist.astype(float)

dist_min = np.min(dist)
dist_max = np.max(dist)

if dist_min < 200:
    dist_min = 200
if dist_max > 7000:
    dist_max = 7000

# 'Jury-rigging' the RA variable from the incorrectly read table

ra = anc_df['RA_err']
ra = ra.replace('--', )
ra = ra.astype(float)

ra_min = np.min(ra)
ra_max = np.max(ra)

if ra_min < 205:
    ra_min = 205
if ra_max > 218:
    ra_max = 218

# 'Jury-rigging' the dec variable from the incorrectly read table

dec = anc_df['Dec_err']
dec = dec.replace('--', )
dec = dec.astype(float)

dec_min = np.min(dec)
dec_max = np.max(dec)

if dec_min < 47.5:
    dec_min = 47.5
if dec_max > 54:
    dec_max = 54

# Reading in temperature data and setting limits

temp = hrd_df['Kelvin']
temp_min = np.min(temp)
temp_max = np.max(temp)

if temp_min < 2000:
    temp_min = 2000
if temp_max > 10000:
    temp_max = 10000

# Creating figure
fig = plt.figure(figsize=(15, 12))
ax = plt.axes(projection='3d')

# Creating plot
sctt = ax.scatter3D(ra, dist, dec, c=temp, cmap='jet', norm=mcolors.LogNorm(vmin=temp_min, vmax=temp_max), s=0.01)
ax.set_xlim(ra_min, ra_max)
ax.set_ylim(dist_min, dist_max)
ax.set_zlim(dec_min, dec_max)
plt.title('3d Star Map of Survey Area')
ax.set_xlabel('Right Ascension (deg)')
ax.set_ylabel('Distance (pc)')
ax.set_zlabel('Declination (deg)')
fig.colorbar(sctt, ax=ax, label='Temperature (K)')

# plt.savefig('C:/Users/alexh/Documents/UoM/Research Project/Output Images/'+ str(foldername) + ' 3d_map.png')

# show plot

plt.show()