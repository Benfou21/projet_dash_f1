
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
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
        dcc.Graph(id='circuit-graph'),
        dcc.Graph(id='speed-graph'),
        
        html.Div([
            dcc.Slider(
                id='time-slider',
                min=0,
                max=x_length - 1,
                value=0,
                step=2,
                marks={i: {'label': time_list[i]} for i in range(0, x_length, 50)} 
            ),
        ], style={'padding-left': '50px', 'padding-right': '50px'}),  # Ajustez les valeurs de padding comme nécessaire
        
    ],
    )


@app.callback(
    [Output('circuit-graph', 'figure'),
     Output('speed-graph', 'figure')],
    [Input('time-slider', 'value')]
)
def update_graphs(index):
    # Mettre à jour le graphique du circuit pour montrer la position à l'index sélectionné
    circuit_figure = dy_plot.get_circuit(data, index)
    
    # Mettre à jour le graphique à barres pour montrer la vitesse à l'index sélectionné
    bars_figure = dy_plot.get_bars(data, index)
    
    return circuit_figure, bars_figure