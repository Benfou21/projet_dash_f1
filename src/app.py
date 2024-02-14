
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import dy_plot


# dist = {'year': [2018, 2019, 2020, 2021, 2022, 2023], 'distance': [36.12083333333333, 50.6111111111111, 33.585, 33.58333333333333, 35.918055555555554, 40.144444444444446]}
# df = pd.DataFrame(dist)

app = dash.Dash(__name__)

app.title = 'F1 visualiation'


telemetry_df = pd.read_csv("./assets/data/telemetry.csv")
telemetry_df['x'] = telemetry_df['x'].apply(lambda x: np.fromstring(x[1:-1], sep=','))
telemetry_df['y'] = telemetry_df['y'].apply(lambda y: np.fromstring(y[1:-1], sep=','))
telemetry_df['speed'] = telemetry_df['speed'].apply(lambda s: np.fromstring(s[1:-1], sep=','))

data = telemetry_df.iloc[0]

app.layout = html.Div([
    html.H1('F1 Telemetry Animation'),
    dcc.Graph(id='graph', figure=dy_plot.get_circuit(data)),
    dcc.Graph(id='speed-graph', figure=dy_plot.get_bars(data))
])