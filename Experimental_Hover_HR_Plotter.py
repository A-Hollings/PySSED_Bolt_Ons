# IMPORT ALL NECESSARY PACKAGES AND DATA SOURCES

import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, no_update
import plotly.express as px
import os
import base64

output_df = pd.read_csv('60Filters_r-0.85306_pl-0.2/output.dat',
                        sep = '\t', header = 3, low_memory=False)
#----------------------------------------------------------------------------------------------
# OLD CODE FOR READING IN DIFFERENT DATA SOURCES

#hrd_df = pd.read_csv('60Filters_r-0.85306_pl-0.2/Only MiniJPAS SEDs/hrd.dat', sep = '\t', header = 1)
#anc_df = pd.read_csv('60Filters_r-0.85306_pl-0.2/Only MiniJPAS SEDs/anc1.txt', sep = '\s+', header = 0)

#trimmed_df['Object'] = hrd_df['#Name']
#trimmed_df['Distance'] = anc_df['Distance']
#trimmed_df['Teff'] = hrd_df['Kelvin']
#trimmed_df['Luminosity'] = hrd_df['Solar luminosities']

#true_distance_df = trimmed_df

#----------------------------------------------------------------------------------------------
# SETTING UP OPERATING DATAFRAME AND NAMING COLUMNS

trimmed_df = pd.DataFrame()
trimmed_df['Object'] = output_df['#Object']
trimmed_df['RA'] = output_df['RA']
trimmed_df['Dec'] = output_df['Dec']
trimmed_df['Distance'] = output_df['Distance']
trimmed_df['Teff'] = output_df['Teff']
trimmed_df['Luminosity'] = output_df['Lum']
trimmed_df['log(g)'] = output_df['logg']
trimmed_df['E(B-V)'] = output_df['E(B-V)']
trimmed_df = trimmed_df.drop(trimmed_df.index[:5], axis=0)

true_distance_df = trimmed_df[trimmed_df['Distance'] != '0.0']
true_distance_df = true_distance_df[true_distance_df['Distance'] != '0']
true_distance_df = true_distance_df[true_distance_df['Luminosity'] != '0.0']
true_distance_df = true_distance_df[true_distance_df['Luminosity'] != '0']


true_distance_df['Teff'] = true_distance_df['Teff'].astype(float)
true_distance_df['Luminosity'] = true_distance_df['Luminosity'].astype(float)
# MOVED LOGGING TRUE_DISTANCE_DF['DISTANCE'] TO BEFORE EVOLTUION TYPE SPLIT - ISSUES LATER?
true_distance_df['Distance'] = true_distance_df['Distance'].astype(float)
true_distance_df['Distance'] = np.log(true_distance_df['Distance'])

#----------------------------------------------------------------------------------------------
# SPLITTING INTO DATAFRAMES BY EVOLUTION STAGE IF IT IS WANTED TO SHOW ONLY CERTAIN TYPES OF STELLAR OBJECTS

wd_df = true_distance_df.loc[(true_distance_df['Teff'] > 5300) & (true_distance_df['Teff'] < 30000) & (true_distance_df['Luminosity'] < 0.1)]
rg_df = true_distance_df.loc[(true_distance_df['Teff'] < 5500) & (true_distance_df['Luminosity'] > 2)]
ms_df = true_distance_df[~true_distance_df.index.isin(wd_df.index) & ~true_distance_df.index.isin(rg_df.index)]

#----------------------------------------------------------------------------------------------
# ALLOWING LOCAL IMAGE FILES TO BE USED BY DASH WEBAPP INSTEAD OF ONLINE SOURCES

def encode_image(path):
    if not os.path.exists(path):
        return None  # Or point to a fallback image later
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower().replace(".", "") or "png"
    return f"data:image/{ext};base64,{encoded}"

# Path to your PNGs
image_directory = "60Filters_r-0.85306_pl-0.2/Only MiniJPAS SEDs/png/"
file_extension = ".png"

# Build the full file path for each Object
true_distance_df["Object_Path"] = true_distance_df["Object"].apply(
    lambda name: os.path.join(image_directory, str(name) + file_extension))

# Encode images to base64 and store in IMG_URL
true_distance_df["IMG_URL"] = true_distance_df["Object_Path"].apply(encode_image)

#----------------------------------------------------------------------------------------------
# SETTING UP THE PLOT IN PLOTLY

fig = px.scatter(true_distance_df, x='Teff', y='Luminosity', color='Distance',
                 labels=dict(x='Temperature (K)', y='Luminosity (Solar)', color='Distance (pc)'),
                 width=1000, height=700,
                 log_y=True, log_x=True)

fig['layout']['xaxis']['autorange'] = 'reversed'

# UPDATE AXIS LABELS, COLOURBAR AND TITLES

fig.update_xaxes(title_text='Effective Temperature (K)')
fig.update_yaxes(title_text='Luminosity (☉)')
fig.update_layout(
    coloraxis_colorbar=dict(tickvals=[np.log(100), np.log(1000), np.log(10000)], ticktext=[100, 1000, 10000],
                            title='Distance (pc)'))
fig.update_layout(title_text='H-R Diagram for Gaia & miniJPAS Data produced by PySSED', title_x=0.5, title_y=0.96)

# turn off native plotly.js hover effects - make sure to use
# hoverinfo="none" rather than "skip" which also halts events.
fig.update_traces(hoverinfo="none", hovertemplate=None, marker_size=4)

#----------------------------------------------------------------------------------------------
# VOODOO DASH-MAGIC

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
    dcc.Tooltip(id="graph-tooltip"),
])

@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # Will only show the first point, but other points may also be available if highly stacked
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = true_distance_df.iloc[num]
    img_src = df_row['IMG_URL']
    name = df_row['Object']
    temperature = df_row['Teff']
    luminosity = df_row['Luminosity']
    distance = df_row['Distance']

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.P(f"Gaia DR3 {name}", style={"color": "darkblue"}),
            html.P(f"{temperature:.0f}K"),
            html.P(f"{luminosity:.4f} L☉"),
            html.P(f"{distance:.0f}pc"),
        ], style={'width': '250px', 'white-space': 'normal'})
    ]

    return True, bbox, children


if __name__ == "__main__":
    app.run(debug=True)