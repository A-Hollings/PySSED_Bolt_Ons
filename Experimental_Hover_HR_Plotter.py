# --------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, no_update
import plotly.express as px
import os
import base64

# --------------------------------------------------------------------
# Data Loading & Cleaning
# --------------------------------------------------------------------
def load_and_clean_data(filepath, drop_rows=5, columns_mapping=None):

    # Load a CSV file and prepare a cleaned DataFrame.

    # columns_mapping: dict mapping new column names -> original column names

    df = pd.read_csv(filepath, sep='\t', header=3, low_memory=False)
    df = df.drop(df.index[:drop_rows], axis=0)

    if columns_mapping:
        cleaned_df = pd.DataFrame()
        for new_col, orig_col in columns_mapping.items():
            cleaned_df[new_col] = df[orig_col]
        return cleaned_df
    return df


# --------------------------------------------------------------------
# Filtering & Conversion
# --------------------------------------------------------------------
def filter_and_convert(df, filter_cols, numeric_cols):

    # Remove rows where filter_cols have zero or invalid entries.
    # Convert numeric_cols to float.

    for col in filter_cols:
        df = df[df[col].astype(str) != '0']
        df = df[df[col].astype(str) != '0.0']
    for col in numeric_cols:
        df[col] = df[col].astype(float)
    return df


# --------------------------------------------------------------------
# Split by Evolution Stage
# --------------------------------------------------------------------
def split_stars_by_stage(df):

    # Categorize stars into white dwarfs, red giants, main-sequence.

    wd_df = df.loc[(df['Teff'] > 5300) & (df['Teff'] < 30000) & (df['Luminosity'] < 0.1)]
    rg_df = df.loc[(df['Teff'] < 5500) & (df['Luminosity'] > 2)]
    ms_df = df[~df.index.isin(wd_df.index) & ~df.index.isin(rg_df.index)]
    return wd_df, rg_df, ms_df


# --------------------------------------------------------------------
# Image Handling
# --------------------------------------------------------------------
def encode_image(path):

    # Encode a local image file to base64 for Dash display.

    if not os.path.exists(path):
        return None  # Could add a fallback image here
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower().replace(".", "") or "png"
    return f"data:image/{ext};base64,{encoded}"


def assign_images(df, object_col, image_dir, extension='.png'):

    # Build file paths and assign base64 encoded images to a DataFrame column. Allows for usage of local images with Dash WebApp

    df['Object_Path'] = df[object_col].apply(lambda x: os.path.join(image_dir, str(x) + extension))
    df['IMG_URL'] = df['Object_Path'].apply(encode_image)
    return df


# --------------------------------------------------------------------
# Plot Creation
# --------------------------------------------------------------------
def make_hr_diagram(df, x='Teff', y='Luminosity', color='Distance', log_scale=True,
                    title='H-R Diagram', width=1000, height=700):
    fig = px.scatter(df, x=x, y=y, color=color, width=width, height=height,
                     labels=dict(x='Temperature (K)', y='Luminosity (Solar)', color='Distance (pc)'))
    if log_scale:
        fig.update_xaxes(type='log')
        fig.update_yaxes(type='log')
    fig['layout']['xaxis']['autorange'] = 'reversed'
    fig.update_traces(marker_size=4, hoverinfo='none', hovertemplate=None)
    fig.update_layout(title_text=title, title_x=0.5)
    fig.update_layout(coloraxis_colorbar=dict(
        tickvals=[np.log(100), np.log(1000), np.log(10000)],
        ticktext=[100, 1000, 10000],
        title='Distance (pc)'
    ))
    fig.update_xaxes(title_text='Effective Temperature (K)')
    fig.update_yaxes(title_text='Luminosity (☉)')
    return fig


# --------------------------------------------------------------------
# Dash Hover Callback
# --------------------------------------------------------------------
def make_hover_callback(df, img_col='IMG_URL', name_col='Object', teff_col='Teff',
                        lum_col='Luminosity', dist_col='Distance'):

    # Returns a callback function for Dash to display hover tooltips with images.


    def callback(hoverdata):
        if hoverdata is None:
            return False, no_update, no_update
        pt = hoverdata["points"][0]
        bbox = pt["bbox"]
        num = pt["pointNumber"]
        row = df.iloc[num]
        children = [
            html.Div([
                html.Img(src=row[img_col], style={"width": "100%"}),
                html.P(f"{row[name_col]}", style={"color": "darkblue"}),
                html.P(f"T={row[teff_col]:.0f}K"),
                html.P(f"L={row[lum_col]:.4f} L☉"),
                html.P(f"d={row[dist_col]:.0f}pc"),
            ], style={'width': '250px', 'white-space': 'normal'})
        ]
        return True, bbox, children

    return callback


# --------------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Load and clean data
    columns_mapping = {
        'Object': '#Object', 'RA': 'RA', 'Dec': 'Dec', 'Distance': 'Distance',
        'Teff': 'Teff', 'Luminosity': 'Lum', 'log(g)': 'logg', 'E(B-V)': 'E(B-V)'
    }
    df = load_and_clean_data('Data/60Filters_r-0.85306_pl-0.2/output.dat', columns_mapping=columns_mapping)

    # Filter and convert
    df = filter_and_convert(df, filter_cols=['Distance', 'Luminosity'], numeric_cols=['Teff', 'Luminosity', 'Distance'])
    df['Distance'] = np.log(df['Distance'])  # log-distance for plotting

    # Split by evolution stage (optional)
    wd_df, rg_df, ms_df = split_stars_by_stage(df)

    # Assign images
    image_dir = 'Data/60Filters_r-0.85306_pl-0.2/Only MiniJPAS SEDs/png/'
    df = assign_images(df, 'Object', image_dir)

    # Make plot
    fig = make_hr_diagram(df)

    # Dash app
    app = Dash(__name__)
    app.layout = html.Div([
        dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
        dcc.Tooltip(id="graph-tooltip"),
    ])

    # Register hover callback
    app.callback(
        Output("graph-tooltip", "show"),
        Output("graph-tooltip", "bbox"),
        Output("graph-tooltip", "children"),
        Input("graph-basic-2", "hoverData")
    )(make_hover_callback(df))

    app.run(debug=True, host='0.0.0.0', port=8050)