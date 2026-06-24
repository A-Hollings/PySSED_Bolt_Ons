# Import modules

import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

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

def filter_and_convert(df, filter_cols, numeric_cols):

    # Remove rows where filter_cols have zero or invalid entries.
    # Convert numeric_cols to float.

    for col in filter_cols:
        df = df[df[col].astype(str) != '0']
        df = df[df[col].astype(str) != '0.0']
    for col in numeric_cols:
        df[col] = df[col].astype(float)
    return df

if __name__ == "__main__":
    # Load and clean data
    columns_mapping = {
        'Object': '#Object', 'RA': 'RA', 'Dec': 'Dec', 'Distance': 'Distance',
        'Teff': 'Teff', 'Luminosity': 'Lum', 'log(g)': 'logg', 'E(B-V)': 'E(B-V)'
    }
    df = load_and_clean_data('Data/60Filters_r-0.85306_pl-0.2/output.dat', columns_mapping=columns_mapping)
    df = filter_and_convert(df, filter_cols=['Distance', 'Luminosity'], numeric_cols=['Teff', 'Luminosity', 'Distance'])

    df['Distance'] = df['Distance'].astype(float)
    df['RA'] = df['RA'].astype(float)
    df['Dec'] = df['Dec'].astype(float)
    df['Teff'] = df['Teff'].astype(float)

    fig = px.scatter_3d(df, x='RA', y='Dec', z='Distance', color='Teff', title= 'Location in Space')

    fig.update_traces(
        hovertemplate=(
            "Right Ascension: %{x:.2f}°<br>"
            "Declination: %{y:.2f}°<br>"
            "Distance: %{z:.0f}pc<br>"
            "Temperature: %{marker.color:.0f}K<br>"
            "<extra></extra>"),marker_size=1)
    fig.update_scenes(xaxis_showspikes=False, yaxis_showspikes=False, zaxis_showspikes=False)
    fig.update_layout(title_x=0.5)

    fig.show()