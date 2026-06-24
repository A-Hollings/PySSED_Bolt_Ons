import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from scipy.stats import gaussian_kde

full_v_df = pd.read_csv('Data/Artificial_Populations/V.txt', sep=r'\s+')

trim_v_df = pd.DataFrame()
trim_v_df['RA'] = full_v_df['RAJ2000']
trim_v_df['Dec'] = full_v_df['DECJ2000']
trim_v_df['V Mag'] = full_v_df['V']
trim_v_df['B-V'] = full_v_df['B-V']
trim_v_df['B Mag'] = full_v_df['Mbol']
trim_v_df['Teff'] = full_v_df['Teff']
trim_v_df['Distance'] = full_v_df['Dist']*1000

ms_df = trim_v_df.loc[(trim_v_df['B Mag'] > 3.8) & (trim_v_df['B Mag'] < 12)]
wd_df = trim_v_df.loc[(trim_v_df['B Mag'] > 12)]
rgb_df = trim_v_df.loc[(trim_v_df['B Mag'] < 3.8)]

# Plot distance distribution
title = 'Distance Distribution for Simulated Gaia-Detected Stars'
x = trim_v_df['Teff']
y = trim_v_df['B Mag']

temp_min = 3000
temp_max = 7000

plt.figure(figsize=(18,9))
ax = plt.axes()

points = ax.scatter(x, y, color='r', s=0.1)

plt.gca().set_xlim(temp_min, temp_max)
ax.set_xlabel('Temperature (K)')
ax.set_ylabel('Bolometric Magnitude')

plt.title(str(title))
#plt.gca().set_xscale('log')
#plt.gca().set_yscale('log')
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()

plt.show()

# Main Sequence Probability Distribution

ms_temp = ms_df['Teff']
ms_bmag = ms_df['B Mag']

ms_kde = stats.gaussian_kde([ms_temp, ms_bmag])

ms_temperature_grid = np.linspace(min(ms_temp), max(ms_temp), 100)
ms_bmag_grid = np.linspace(min(ms_bmag), max(ms_bmag), 100)
ms_temperature_mesh, ms_bmag_mesh = np.meshgrid(ms_temperature_grid, ms_bmag_grid)
ms_positions = np.vstack([ms_temperature_mesh.ravel(), ms_bmag_mesh.ravel()])

ms_pdf_values = ms_kde(ms_positions)
ms_pdf_values = ms_pdf_values.reshape(ms_temperature_mesh.shape)

# White Dwarf Probability Distribution

wd_temp = wd_df['Teff']
wd_bmag = wd_df['B Mag']

wd_kde = stats.gaussian_kde([wd_temp, wd_bmag])

wd_temperature_grid = np.linspace(min(wd_temp), max(wd_temp), 100)
wd_bmag_grid = np.linspace(min(wd_bmag), max(wd_bmag), 100)
wd_temperature_mesh, wd_bmag_mesh = np.meshgrid(wd_temperature_grid, wd_bmag_grid)
wd_positions = np.vstack([wd_temperature_mesh.ravel(), wd_bmag_mesh.ravel()])
wd_pdf_values = wd_kde(wd_positions)
wd_pdf_values = wd_pdf_values.reshape(wd_temperature_mesh.shape)

# Red Giant Branch Probability Distribution

rgb_temp = rgb_df['Teff']
rgb_bmag = rgb_df['B Mag']

rgb_kde = stats.gaussian_kde([rgb_temp, rgb_bmag])

rgb_temperature_grid = np.linspace(min(rgb_temp), max(rgb_temp), 100)
rgb_bmag_grid = np.linspace(min(rgb_bmag), max(rgb_bmag), 100)
rgb_temperature_mesh, rgb_bmag_mesh = np.meshgrid(rgb_temperature_grid, rgb_bmag_grid)
rgb_positions = np.vstack([rgb_temperature_mesh.ravel(), rgb_bmag_mesh.ravel()])
rgb_pdf_values = rgb_kde(rgb_positions)
rgb_pdf_values = rgb_pdf_values.reshape(rgb_temperature_mesh.shape)

# Plots

plt.contourf(ms_temperature_mesh, ms_bmag_mesh, ms_pdf_values, cmap='hot')
plt.contourf(wd_temperature_mesh, wd_bmag_mesh, wd_pdf_values, cmap='hot')
plt.contourf(rgb_temperature_mesh, rgb_bmag_mesh, rgb_pdf_values, cmap='hot')
plt.xlabel('Temperature (K)')
plt.ylabel('Bolometric Magnitude')
plt.gca().set_xlim(3000,8000)
plt.gca().set_ylim(1.5,15)
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
plt.colorbar(label='PDF')

#plt.savefig('Three_Separate_PDFs_Combined.png', dpi=300)
plt.show()

# All stars grouped probability distribution

temp = trim_v_df['Teff']
bmag = trim_v_df['B Mag']

kde = stats.gaussian_kde([temp, bmag])

temperature_grid = np.linspace(min(temp), max(temp), 100)
bmag_grid = np.linspace(min(bmag), max(bmag), 100)
temperature_mesh, bmag_mesh = np.meshgrid(temperature_grid, bmag_grid)
positions = np.vstack([temperature_mesh.ravel(), bmag_mesh.ravel()])

pdf_values = kde(positions)
pdf_values = pdf_values.reshape(temperature_mesh.shape)

plt.contourf(temperature_mesh, bmag_mesh, pdf_values, cmap='hot')
plt.xlabel('Temperature (K)')
plt.ylabel('Bolometric Magnitude')
plt.gca().set_xlim(3000,7000)
plt.gca().set_ylim(1.5,15)
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
plt.colorbar(label='PDF')

#plt.savefig('All_Stars.png', dpi=300)
plt.show()


# Only Main Sequence

plt.contourf(ms_temperature_mesh, ms_bmag_mesh, ms_pdf_values, cmap='hot', norm=mcolors.LogNorm(vmin=ms_pdf_values.min(), vmax=ms_pdf_values.max()))
plt.xlabel('Temperature (K)')
plt.ylabel('Bolometric Magnitude')
plt.gca().set_xlim(3000,7000)
plt.gca().set_ylim(3.8, 12)
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
colorbar = plt.colorbar(label='PDF')
#colorbar.set_ticks([10**-3,10**-4,10**-5])

#plt.savefig('Only_Main_Sequence.png', dpi=300)
plt.show()


# Generate random data for demonstration purposes
np.random.seed(0)
luminosity = trim_v_df['B Mag']
temperature = trim_v_df['Teff']

# Create a 2D density estimation
data = np.vstack([luminosity, temperature])
kde = gaussian_kde(data)

# Define the grid of values
luminosity_grid = np.linspace(min(luminosity), max(luminosity), 100)
temperature_grid = np.linspace(min(temperature), max(temperature), 100)
temperature_grid, luminosity_grid  = np.meshgrid(temperature_grid, luminosity_grid)

# Evaluate the density estimation on the grid
density = kde.evaluate(np.vstack([luminosity_grid.ravel(), temperature_grid.ravel()]))
density = density.reshape(luminosity_grid.shape)

# Weight the white dwarfs and red giant branch
wd_density = density.copy()
wd_density[(luminosity_grid >= 2) & (luminosity_grid <= 3) & (temperature_grid >= 5000) & (temperature_grid <= 10000)] *= 10  # Adjust the weight factor as desired

rgb_density = density.copy()
rgb_density[(luminosity_grid >= 3.5) & (luminosity_grid <= 4.5) & (temperature_grid >= 3000) & (temperature_grid <= 4500)] *= 10  # Adjust the weight factor as desired

# Plot the PDF of the H-R diagram
plt.figure(figsize=(8, 6))
plt.imshow(density.T, origin='lower', aspect='auto', cmap='hot', extent=[min(luminosity), max(luminosity), min(temperature), max(temperature)])

# Overlay the white dwarfs and red giant branch with increased density
plt.imshow(wd_density.T, origin='lower', aspect='auto', cmap='Blues', extent=[min(luminosity), max(luminosity), min(temperature), max(temperature)], alpha=0.3)
plt.imshow(rgb_density.T, origin='lower', aspect='auto', cmap='Reds', extent=[min(luminosity), max(luminosity), min(temperature), max(temperature)], alpha=0.3)

plt.colorbar(label='Probability Density')
plt.xlabel('Luminosity')
plt.ylabel('Temperature')
plt.title('Probability Distribution Function of H-R Diagram')

plt.show()