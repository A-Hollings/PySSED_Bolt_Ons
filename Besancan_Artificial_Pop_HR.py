import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from ipywidgets import widgets

# Loading the five individual catalogues

b_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/Catalogues/Artificial Populations/Gaia Mag Sim/B.txt', sep='\s+',
                  usecols=['RAJ2000','Dist','Teff','Mbol'])

i_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/Catalogues/Artificial Populations/Gaia Mag Sim/I.txt', sep='\s+',
                  usecols=['RAJ2000','Dist','Teff','Mbol'])

r_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/Catalogues/Artificial Populations/Gaia Mag Sim/R.txt', sep='\s+',
                  usecols=['RAJ2000','Dist','Teff','Mbol'])

u_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/Catalogues/Artificial Populations/Gaia Mag Sim/U.txt', sep='\s+',
                  usecols=['RAJ2000','Dist','Teff','Mbol'])

v_df = pd.read_csv('C:/Users/alexh/Documents/UoM/Research Project/Data/Catalogues/Artificial Populations/Gaia Mag Sim/V.txt', sep='\s+',
                  usecols=['RAJ2000','Dist','Teff','Mbol'])

merged_df = pd.merge(b_df, i_df, on=['RAJ2000','Teff','Dist','Mbol'], how='outer')

merged_df = pd.merge(merged_df, r_df, on=['RAJ2000','Teff','Dist','Mbol'], how='outer')

merged_df = pd.merge(merged_df, u_df, on=['RAJ2000','Teff','Dist','Mbol'], how='outer')

merged_df = pd.merge(merged_df, v_df, on=['RAJ2000','Teff','Dist','Mbol'], how='outer')

# Sort targets by RA co-ord

merged_df = merged_df.sort_values('RAJ2000')

object_count = 0

# Based on PSF of highest wavelength (1um), should be 0.516 arcseconds, or 0.000143 degrees

coord_err = 0.000143

diff = merged_df['RAJ2000'].diff()

# Assign id based on whether each difference is within tolerance

object_id = (diff.abs() > coord_err).cumsum() + 1

# Add id column to DataFrame

merged_df['OBJECT_ID'] = object_id

filtered_merged_df = merged_df[~merged_df['OBJECT_ID'].duplicated(keep='first')]

filtered_merged_df

#r_df = pd.read_csv('C:/Users/alexh/Downloads/Gaia - R.txt', sep='\s+',
                  #usecols=['RAJ2000','Dist','Teff','Mbol'])
#merged_df= r_df

# Converting from kpc to pc
filtered_merged_df['Dist'] = 1000*filtered_merged_df['Dist']

# Converting bolometric magnitude to luminosity in solar values
solar_lum = 3.828*10**26
lum_zpt = 3.0128*10**28

filtered_merged_df['Luminosity'] = (lum_zpt * 10**(-0.4*filtered_merged_df['Mbol']))/solar_lum

filtered_merged_df

# Dataframes split by evolution stage

wd_df = filtered_merged_df.loc[(filtered_merged_df['Teff'] > 5500) & (filtered_merged_df['Teff'] < 30000) & (filtered_merged_df['Luminosity'] < 0.1)]
rg_df = filtered_merged_df.loc[(filtered_merged_df['Teff'] < 5500) & (filtered_merged_df['Luminosity'] > 2)]
ms_df = filtered_merged_df[~filtered_merged_df.index.isin(wd_df.index) & ~filtered_merged_df.index.isin(rg_df.index)]

rg_df

# true_distance_df['Distance'] = true_distance_df['Distance'].astype(float)
filtered_merged_df['Log Dist'] = np.log(filtered_merged_df['Dist'])

fig = px.scatter(filtered_merged_df, x='Teff', y='Luminosity', color='Log Dist',
                 labels=dict(x='Temperature (K)', y='Luminosity (Solar)', color='Distance (pc)'),
                 width=1000, height=700,
                 log_y=True, log_x=True)

fig['layout']['xaxis']['autorange'] = 'reversed'
fig.update_traces(marker_size=4)
fig.update_layout(
    coloraxis_colorbar=dict(tickvals=[np.log(100), np.log(1000), np.log(10000)], ticktext=[100, 1000, 10000],
                            title='Distance (pc)'))
# Update the title
fig.update_layout(title_text='H-R Diagram for Besancon Galaxy Model (Gaia)', title_x=0.5, title_y=0.96)

# Update the axis labels
fig.update_xaxes(title_text='Effective Temperature (K)')
fig.update_yaxes(title_text='Luminosity (Solar)')

fig.show()