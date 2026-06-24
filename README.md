# PySSED Bolt-Ons

A collection of standalone visualisation scripts designed to be run against the output files of [PySSED](https://github.com/iain-mcdonald/PySSED) (Python Stellar Spectral Energy Distributions), a stellar modelling tool developed by Iain McDonald et al. PySSED is not my work — I contributed to a later stage of its development and the sample data included here was produced by running PySSED on the MiniJPAS dataset. These scripts were developed for various needs as they arose throughout the research project.

> **Note:** This repository represents the original standalone/post-processing stage of this work. The visualisation tools have since been integrated directly into an unofficial PySSED pipeline. See [PySSED_Interactive](https://github.com/A-Hollings/PySSED_Interactive) for the current version.

---

## Scripts

### `Functional_HR_Plotter.py`
Produces a static H-R diagram using matplotlib, plotting effective temperature against luminosity for stars in the PySSED output. Supports overlay of PARSEC isochrones and colours datapoints by distance using a logarithmic colour scale. The primary starting point for visualisation of PySSED results.

### `Experimental_Hover_HR_Plotter.py`
An interactive H-R diagram built with Plotly and Dash. Hovering over a datapoint displays a tooltip showing the star's SED image (where available), GaiaDR3 ID, effective temperature, luminosity, and distance. This was the prototype for the interactive visualisation approach that has since been fully integrated into PySSED — see [PySSED_Interactive](https://github.com/A-Hollings/PySSED_Interactive).

### `Altered_SED_Plotter.py`
Overlays individual Spectral Energy Distributions (SEDs) directly onto H-R diagram datapoints, making it easier to inspect individual stars for features such as potential dust extinction. Useful for identifying anomalous results during analysis. Tweaked from the original function in PySSED to allow for wider ranges of plotting.

### `3d_Location_Plotter.py`
Plots the 3D spatial distribution of stars in the dataset using Plotly, allowing inspection of the survey volume and identification of any spatial biases in the sample.

### `Artificial_Pop_Probability_Distributions.py`
Generates probability distribution functions (PDFs) for simulated Gaia-detected stellar populations using kernel density estimation (KDE). Separates the population into main sequence, white dwarf, and red giant branch (RGB) components and plots their distributions on an H-R diagram. Uses a Besançon-model artificial population as input.

### `Besancan_Artificial_Pop_HR.py`
Plots an H-R diagram for an artificial stellar population generated from the Besançon Galaxy model, for comparison against observed PySSED results.

---

## Data

The sample data directory (`60Filters_r-0.85306_pl-0.2/`) contains output produced by running PySSED on the MiniJPAS survey using a 60-filter configuration.

---

## Dependencies

```
numpy
pandas
matplotlib
scipy
plotly
dash
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Usage

Each script is self-contained and can be run directly from the repo root, provided the `Data/` directory structure is in place:

```bash
python Functional_HR_Plotter.py
python Experimental_Hover_HR_Plotter.py
# etc.
```

For `Experimental_Hover_HR_Plotter.py`, once running, open your browser and navigate to `http://127.0.0.1:8050`.

---

## Changelog

- **v0.1** (`v0.1-bolt-on`) — Original standalone post-processing scripts, run against PySSED output files
- **v0.2** — Scripts cleaned up, hardcoded paths removed, requirements.txt added
- For the fully integrated version, see [PySSED_Interactive](https://github.com/A-Hollings/PySSED_Interactive)
