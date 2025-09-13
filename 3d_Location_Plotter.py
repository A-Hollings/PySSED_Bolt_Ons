# Import modules

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"


# Import data

hrd_df = pd.read_csv('60Filters_r-0.85306_pl-0.2/hrd.dat', sep = '\t', header = 1)
anc_df = pd.read_csv('60Filters_r-0.85306_pl-0.2/anc1.txt', sep = '\t', header = 0)

# 'Jury-rigging' the distance variable from the incorrectly read table

dist = anc_df['Distance']
dist = dist.astype(float)

dist_min = np.min(dist)
dist_max = np.max(dist)

if dist_min < 200:
    dist_min = 200
if dist_max > 7000:
    dist_max = 7000

# 'Jury-rigging' the RA variable from the incorrectly read table

ra = anc_df['RA']
ra = ra.astype(float)

ra_min = np.min(ra)
ra_max = np.max(ra)

if ra_min < 205:
    ra_min = 205
if ra_max > 218:
    ra_max = 218

# 'Jury-rigging' the dec variable from the incorrectly read table

dec = anc_df['Dec']
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

fig = px.scatter_3d(x=ra, y=dec, z=dist, color=temp, title= 'Location in Space',
                     labels=dict(x='Right Ascension (°)', y='Declination (°)', z='Distance (pc)', color='Temperature (K)'))

fig.update_traces(marker_size=1)
fig.update_layout(title_x=0.5)
fig.show()