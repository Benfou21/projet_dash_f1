
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import dy_plot
import ast


app = dash.Dash(__name__)

app.title = 'F1 visualiation'


telemetry_df = pd.read_csv("./assets/data/telemetry.csv")
telemetry_df['x'] = telemetry_df['x'].apply(lambda x: np.fromstring(x[1:-1], sep=','))
telemetry_df['y'] = telemetry_df['y'].apply(lambda y: np.fromstring(y[1:-1], sep=','))
telemetry_df['speed'] = telemetry_df['speed'].apply(lambda s: np.fromstring(s[1:-1], sep=','))


data = telemetry_df.iloc[0]
time_str = data["time"]   # c'est une chaîne de caractères qui ressemble à une liste
time_list = ast.literal_eval(time_str)


x_length = len(data['x'])

app.layout = html.Div(
    [
        html.H1('F1 Telemetry Animation'),
        
        html.Div([
            dcc.Graph(id='circuit-graph-1'),
            dcc.Graph(id='circuit-graph-2'),
        ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques du circuit côte à côte
        
        html.Div([
            dcc.Graph(id='speed-graph-1'),
            dcc.Graph(id='speed-graph-2'),
        ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques de vitesse côte à côte
        
        html.Div([
            dcc.Slider(
                id='time-slider',
                min=0,
                max=x_length - 1,
                value=0,
                step=2,
                marks={i: {'label': time_list[i]} for i in range(0, x_length, 50)} 
            ),
        ],style={'padding-left': '50px', 'padding-right': '50px', 'width': '50%', 'margin': '0 auto'} ),
       
    ],
    style={'textAlign': 'center'}
)

@app.callback(
    [Output('circuit-graph-1', 'figure'),
     Output('circuit-graph-2', 'figure'),
     Output('speed-graph-1', 'figure'),
     Output('speed-graph-2', 'figure')],
    [Input('time-slider', 'value')]
)
def update_graphs(index):
    w = 1100
    circuit_figure = dy_plot.get_circuit(data, index)
    bars_figure = dy_plot.get_bars(data, index)
    circuit_figure.update_layout(
        height=600,  # hauteur en pixels
        width=w,  # largeur en pixels
    )
    bars_figure.update_layout(
        height=600,  # hauteur en pixels
        width=w,  # largeur en pixels
    )
    
    # Puisque nous doublons simplement les graphiques, nous retournons la même figure pour les graphiques 1 et 2
    return circuit_figure, circuit_figure, bars_figure, bars_figure

