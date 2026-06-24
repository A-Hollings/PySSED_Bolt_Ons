# Import modules

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.colors as mcolors

hrd_df = pd.read_csv('Data/60Filters_r-0.85306_pl-0.2/hrd.dat', sep = '\t', header = 1)
anc_df = pd.read_csv('Data/60Filters_r-0.85306_pl-0.2/anc.dat', sep = '\t', header = 0)

dist = anc_df['Distance']

dist = dist.replace('--',np.nan)

dist = dist.astype(float)

dist_min = np.nanmin(dist)
dist_max = np.nanmax(dist)

# Removing any problematic or miscalculated values (e.g 0 or NaN). You might want to up the limits for yours seeing as I think you said your stars are ~24kpc away

if dist_min < 200:
    dist_min = 200
if dist_max > 7000:
    dist_max = 7000

# Set variables for axes and find min/max in datasets

lumin = hrd_df['Solar luminosities']
temp = hrd_df['Kelvin']
temp_min = np.min(temp)
temp_max = np.max(temp)
lumin_min = np.min(lumin)
lumin_max = np.max(lumin)

# Removing any problematic or miscalculated values (e.g 0 or NaN)

if temp_min < 2000:
    temp_min = 2000
if temp_max > 12000:
    temp_max = 12000
if lumin_min < 0.00001:
    lumin_min = 0.00001
if lumin_max > 10000:
    lumin_max = 10000

# Find isocrone folder
# For me, I've kept all my isochrones in one folder, and only them, much easier for me to read them in that way.

isochrone_dir = 'Data/Isochrones'

if not os.path.isdir(isochrone_dir):
    raise FileNotFoundError(f"Isochrones directory not found: '{isochrone_dir}'. "
                            f"Check the path is correct relative to your working directory.")

_, _, files = next(os.walk(isochrone_dir))
files = [f for f in files if f.endswith('.dat')]

# Label columns <-- It didn't like reading in headers normally so I had to do it manually.

colnames = ['Zini', 'MH', 'logAge', 'Mini', 'int_IMF', 'Mass', 'logL', 'logTe', 'logg', 'label', 'McoreTP', 'C_0',
            'period0', 'period1', 'period2', 'period3', 'period4', 'pmode', 'Mloss', 'tau1m', 'X', 'Y', 'Xc', 'Xn',
            'Xo', 'Cexcess', 'Z', 'mbolmag', 'Umag', 'Bmag', 'Vmag', 'Rmag', 'Imag', 'Jmag', 'Hmag', 'Kmag']

# Append isochrones to the list

isochrones_list = []
for filename in files:
    temp_df = pd.read_csv(os.path.join(isochrone_dir, filename), sep=r'\s+',
                          header=13, names=colnames, index_col=False)
    isochrones_list.append(temp_df)

# Drop the terminated end line from all isochrones
# Also define the cut-point for get rid of messy part of isochrones (via decimal) <-- Gets rid of that horrific looking swiggle when it starts the horizontal
# giant branch and then down into the white dwarfs.

cut_fraction = 0.55
for isochrone in isochrones_list:
    isochrone.drop(isochrone.tail(round(len(isochrone) * cut_fraction)).index, inplace=True)
    # print(isochrone)

# Iterate over the filenames and strip the ".dat" extension
# I'm assuming you're also using the PARSEC isocrones? In which case, they'll be the same as mine.
# When naming the files, I simply called them the parameters I changed, as that - '.dat' will be the name on the legend.

clean_files = []

for file in files:
    basename, extension = os.path.splitext(file)
    clean_files.append(basename)

# Plot H-R diagram

plt.figure(figsize=(18,9))
ax = plt.axes()

points = ax.scatter(temp, lumin, c=dist, cmap='jet', norm=mcolors.LogNorm(vmin=dist_min, vmax=dist_max), s=0.01)

for i, isochrone in enumerate(isochrones_list):
    temp_iso = 10**isochrone['logTe']
    lumin_iso = 10**isochrone['logL']
    ax.plot(temp_iso, lumin_iso, label=clean_files[i], lw=0.6)

ax.set_xlabel('Effective Temperature (K)')
ax.set_ylabel('Luminosity (Solar Luminosities)')
ax.set_xlim(temp_min, temp_max)
ax.set_ylim(lumin_min, lumin_max)
ax.legend(title='Isochrones')
plt.title('MiniJPAS First 20 Filter Set')
plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().invert_xaxis()
plt.colorbar(points, label ='Distance (pc)')

#plt.savefig('H-R Diagram_Isocroned.png', dpi=300)
plt.show()