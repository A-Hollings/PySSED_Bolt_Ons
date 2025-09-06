# ORIGINAL FUNCTION

def plotsed(sed, modwave, modflux, plotfile):
    # Plot the completed individual SEDs to a file

    fig, ax = plt.subplots(figsize=[10, 7])

    newcmp = colourmap(1.)

    # Set up main axes
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Wavelength (microns)", fontsize=20)
    # plt.xlabel(fontsize=20)
    # plt.tick_params(axis='x', which='both', labelsize=20)
    plt.ylabel("Flux (Jy)", fontsize=20)
    # plt.ylabel(fontsize=20)
    # plt.tick_params(axis='y', which='both', labelsize=20)
    plt.minorticks_on()

    # Plot the model if it exists
    if (len(modwave) > 0):
        x = modwave * 1.e6
        y = modflux
        indx = x.argsort()
        xs = x[indx]
        ys = y[indx]
        xerr = 0
        yerr = 0
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='s', markersize=3, color='#AA33AA80', ecolor='lightgray',
                     elinewidth=1, capsize=0, zorder=5)
        plt.plot(xs, ys, color='#FF00FF20', zorder=0, linewidth=3)

    # Plot the observed (reddened data)
    # Plot all the data
    x = sed[sed['mag'] != 0]['wavel'] / 10000
    y = sed[sed['mag'] != 0]['flux']
    xerr = 0
    yerr = sed[sed['mag'] != 0]['ferr']
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='+', markersize=4, color='lightgray', ecolor='lightgray', elinewidth=1,
                 capsize=0, zorder=10)

    # Clip the plot if data too faint
    maxrange = float(pyssedsetupdata[pyssedsetupdata[:, 0] == "MaxSEDPlotFluxRange", 1])
    maxflux = np.max(y)
    minflux = np.min(y)
    if (minflux * maxrange < maxflux):
        plt.ylim(ymin=maxflux / maxrange)

    # Overplot the unmasked in grey-red
    x = sed[sed['mask'] > 0]['wavel'] / 10000
    y = sed[sed['mask'] > 0]['flux']
    xerr = 0
    yerr = 0
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='+', markersize=4, color='#FFAAAA00', ecolor='#FFAAAA00', elinewidth=1,
                 capsize=0, zorder=10)

    # Decide whether to put the inset on top or bottom,
    # based on whether the left or right quarter of the model points are higher
    lhs = np.average(np.log10(y[:int(len(y) / 4)]))
    rhs = np.average(np.log10(y[-int(len(y) / 4):]))

    # Plot the dereddened data
    # Plot all the data
    x = sed[sed['mag'] != 0]['wavel'] / 10000
    y = sed[sed['mag'] != 0]['dered']
    xerr = sed[sed['mag'] != 0]['dw'] / 2 / 10000
    yerr = sed[sed['mag'] != 0]['derederr']
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', markersize=4, color='lightgray', ecolor='lightgray', elinewidth=1,
                 capsize=0, zorder=10)

    # Overplot the unmasked in colour
    x = sed[sed['mask'] > 0]['wavel'] / 10000
    y = sed[sed['mask'] > 0]['dered']
    xerr = sed[sed['mask'] > 0]['dw'] / 2 / 10000
    yerr = sed[sed['mask'] > 0]['derederr']
    colour = np.log10(x)
    plt.scatter(x, y, c=colour, cmap=newcmp, s=16, zorder=20)

    # Save the file
    plt.savefig(plotfile, dpi=300, bbox_inches='tight')
    plt.close("all")

    return

########################################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap

def colourmap(opacity):
    # Set up colour map
    n = 128
    vals = np.ones((n*2, 4))
    vals[:128, 0] = 0
    vals[:128, 1] = np.linspace(0/256, 256/256, n)
    vals[:128, 2] = np.linspace(256/256, 0/256, n)
    vals[128:, 0] = np.linspace(0/256, 256/256, n)
    vals[128:, 1] = np.linspace(256/256, 0/256, n)
    vals[128:, 2] = 0.
    vals[:, 3] = opacity
    newcmp = ListedColormap(vals)

    return newcmp

# MODIFICATION ATTEMPT

# Load sed file

sed=pd.read_csv('G:/My Drive/Uni Data/Only Gaia/New_Gaia_0.2/sed/1608004247742692608.sed', sep='\t')

# Sort out missing variables

newcmp=colourmap(1.)

modwave = sed['wavel']
modflux = sed['model']


fig, ax = plt.subplots(figsize=[10, 7])

#Set up main axes
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Wavelength (Angstroms)", fontsize=20)
#plt.xlabel(fontsize=20)
#plt.tick_params(axis='x', which='both', labelsize=20)
plt.ylabel("Flux (Jy)", fontsize=20)
#plt.ylabel(fontsize=20)
#plt.tick_params(axis='y', which='both', labelsize=20)
plt.minorticks_on()


# Plot the model if it exists
if (len(modwave)>0):
    x=modwave
    y=modflux
    indx = x.argsort()
    xs = x[indx]
    ys = y[indx]
    xerr=0
    yerr=0
    plt.errorbar(x,y,xerr=xerr,yerr=yerr,fmt='s',markersize=3,color='#AA33AA80',ecolor='lightgray', elinewidth=1, capsize=0, zorder=5)
    plt.plot(xs,ys,color='#FF00FF20',zorder=0,linewidth=3)

# Plot the dereddened data
# Plot all the data
x=sed[sed['mag']!=0]['wavel']
y=sed[sed['mag']!=0]['dered']
xerr=sed[sed['mag']!=0]['dw']/2
yerr=sed[sed['mag']!=0]['derederr']
plt.errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o',markersize=4,color='lightgray',ecolor='lightgray', elinewidth=1, capsize=0, zorder=10)

# Overplot the unmasked in colour
x=sed[sed['mask']>0]['wavel']
y=sed[sed['mask']>0]['dered']
xerr=sed[sed['mask']>0]['dw']/2
yerr=sed[sed['mask']>0]['derederr']
colour=np.log10(x)
plt.scatter(x,y,c=colour,cmap=newcmp,s=16,zorder=20)

# Set minor locator
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10, step=2)))

# Set minor formatter
ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda x, pos: r"$%d \times 10^{%d}$" % (x / 10**np.floor(np.log10(x)), np.floor(np.log10(x)))))

# Show minor tick labels
ax.tick_params(axis='y', which='minor', labelsize='small', labelcolor='0.5')

#plt.savefig('5.1left.png',dpi=300,bbox_inches='tight')

plt.show()
# Save the file
plt.close("all")