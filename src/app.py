
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import dy_plot
import ast
from preprocessing import get_data
from preprocessing import get_max_speed
import hover_template
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

app.title = 'F1 visualiation'

path_max = "assets\\data\\telemetry_spain_2021_VER.csv"
telemetry_df_max = get_data(path_max)

path_ham = "assets\\data\\telemetry_spain_2021_HAM.csv"
telemetry_df_ham = get_data(path_ham)


time_str = telemetry_df_max["Time"]   # c'est une chaîne de caractères qui ressemble à une liste
x_length = len(telemetry_df_max['X'])

index_initial = 0
circuit_figure_max_initial = dy_plot.get_circuit(telemetry_df_max, index_initial, "Max")
bars_figure_max_initial = dy_plot.get_bars(telemetry_df_max, index_initial, "Max")

# Génération initiale des figures pour telemetry_df_ham
circuit_figure_ham_initial = dy_plot.get_circuit(telemetry_df_ham, index_initial, "Ham")
bars_figure_ham_initial = dy_plot.get_bars(telemetry_df_ham, index_initial, "Ham")


app.layout = html.Div(
    [
        dcc.Markdown('''
        # Welcome to F1 Telemetry Visualization
        
        Scroll down to see the live telemetry graphs.
        '''),

        html.Div([
            dcc.Graph(id='circuit-graph-1',figure=circuit_figure_max_initial),
            dcc.Graph(id='circuit-graph-2',figure=circuit_figure_ham_initial),
        ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques du circuit côte à côte
        
        html.Div([
            dcc.Graph(id='speed-graph-1',figure=bars_figure_max_initial),
            dcc.Graph(id='speed-graph-2',figure=bars_figure_ham_initial),
        ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques de vitesse côte à côte
        
    ],
    style={'textAlign': 'center'}
)


@app.callback(
    [Output('circuit-graph-1', 'figure'), Output('speed-graph-1', 'figure'), 
     Output('circuit-graph-2', 'figure'), Output('speed-graph-2', 'figure')],
    [Input('circuit-graph-1', 'clickData'), Input('circuit-graph-2', 'clickData')],
    [State('circuit-graph-1', 'figure'), State('circuit-graph-2', 'figure')]
)
def update_graph(clickData1, clickData2, fig1, fig2):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'circuit-graph-1' and clickData1:
        
        x = clickData1['points'][0]['x']
        y = clickData1['points'][0]['y']
        index = find_closest_index(x, y, telemetry_df_max)
        new_fig1 = dy_plot.get_circuit(telemetry_df_max, index, "Max")
        new_fig1_bars = dy_plot.get_bars(telemetry_df_max, index, "Max")
        return new_fig1, new_fig1_bars, dash.no_update, dash.no_update

    elif trigger_id == 'circuit-graph-2' and clickData2:
        x = clickData1['points'][0]['x']
        y = clickData1['points'][0]['y']
        index = find_closest_index(x, y, telemetry_df_max)
        new_fig2 = dy_plot.get_circuit(telemetry_df_ham, index, "Ham")
        new_fig2_bars = dy_plot.get_bars(telemetry_df_ham, index, "Ham")
        return dash.no_update, dash.no_update, new_fig2, new_fig2_bars
    
    

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update

def find_closest_index(x, y, dataframe):
   
    distances = np.sqrt((dataframe['X'] - x)**2 + (dataframe['Y'] - y)**2)
    
    return distances.idxmin()