
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import graphs.graph__3_circuit as graph__3_circuit
import ast
from preprocessing.preprocessing_3 import get_data
from preprocessing.preprocessing_3 import get_max_speed
import hover_template.hover_template_3_circuit as hover_template_3_circuit
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
circuit_figure_max_initial = graph__3_circuit.get_circuit(telemetry_df_max, index_initial, "Max")
bars_figure_max_initial = graph__3_circuit.get_bars(telemetry_df_max, index_initial, "Max")

# Génération initiale des figures pour telemetry_df_ham
circuit_figure_ham_initial = graph__3_circuit.get_circuit(telemetry_df_ham, index_initial, "Ham")
bars_figure_ham_initial = graph__3_circuit.get_bars(telemetry_df_ham, index_initial, "Ham")


# app.layout = html.Div(
#     [
#         dcc.Markdown('''
#         # Welcome to F1 Telemetry Visualization
        
#         Scroll down to see the live telemetry graphs.
#         '''),

#         html.Div([
#             dcc.Graph(id='circuit-graph-1',figure=circuit_figure_max_initial),
#             dcc.Graph(id='circuit-graph-2',figure=circuit_figure_ham_initial),
#         ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques du circuit côte à côte
        
#         html.Div([
#             html.Div(id='speed-display-1', children='', style={'fontSize': 24, 'margin': '10px'}),
#             html.Div(id='speed-display-2', children='', style={'fontSize': 24, 'margin': '10px'}),
#         ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques du circuit côte à côte
        
        
#         html.Div([
#             dcc.Graph(id='speed-graph-1',figure=bars_figure_max_initial),
#             dcc.Graph(id='speed-graph-2',figure=bars_figure_ham_initial),
#         ], style={'display': 'flex','justifyContent': 'center'}),  # Div contenant les graphiques de vitesse côte à côte
        
#     ],
#     style={'textAlign': 'center'}
# )

app.layout = html.Div(
    [
        html.H1(children='Scrollable Story pour la Formule 1'),

        # Horizontal block for Max
        html.Div([
            # Vertical sub-block for Max's circuit graph
            html.Div([
                dcc.Graph(id='circuit-graph-1', figure=circuit_figure_max_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
            html.Div([
                dcc.Graph(id='circuit-graph-2', figure=circuit_figure_ham_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}), # This ensures that the sub-blocks for Max are in one line
        
        html.Div([
            # Vertical sub-block for Max's speed display
            html.Div(
                id='speed-display-1', 
                children='', 
                style={
                    'fontSize': '24px',
                    'display': 'inline-block',
                    'width': '20%',
                    'textAlign': 'center',
                    'border': '2px solid #4CAF50',  # Green border
                    'borderRadius': '10px',  # Rounded corners
                    'backgroundColor': '#f9f9f9',  # Light grey background
                    'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow
                    'padding': '10px'
                }
            ),
            html.Div(
                id='speed-display-2', 
                children='', 
                style={
                    
                    'fontSize': '24px',
                    'display': 'inline-block',
                    'width': '20%',
                    'textAlign': 'center',
                    'border': '2px solid #4CAF50',  # Green border
                    'borderRadius': '10px',  # Rounded corners
                    'backgroundColor': '#f9f9f9',  # Light grey background
                    'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow
                    'padding': '10px'
                }
            ),
          
        ],style={'display': 'inline-block', 'width': '34%', 'textAlign': 'center'}),
        
        # Horizontal block for Ham
        html.Div([
             # Vertical sub-block for Max's bar graph
            html.Div([
                dcc.Graph(id='speed-graph-1', figure=bars_figure_max_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
            # Vertical sub-block for Ham's bar graph
            html.Div([
                dcc.Graph(id='speed-graph-2', figure=bars_figure_ham_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}), # This ensures that the sub-blocks for Ham are in one line
    ],
    style={'textAlign': 'center'}
)



@app.callback(
    [Output('circuit-graph-1', 'figure'), Output('speed-graph-1', 'figure'), 
     Output('circuit-graph-2', 'figure'), Output('speed-graph-2', 'figure'),
     Output('speed-display-1', 'children'),Output('speed-display-2', 'children')],
    [Input('circuit-graph-1', 'clickData'), Input('circuit-graph-2', 'clickData')],
    [State('circuit-graph-1', 'figure'), State('circuit-graph-2', 'figure')]
)
def update_graph(clickData1, clickData2, fig1, fig2):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(trigger_id)
    if trigger_id == 'circuit-graph-1' and clickData1:
        
        x = clickData1['points'][0]['x']
        y = clickData1['points'][0]['y']
        index = find_closest_index(x, y, telemetry_df_max)
        new_fig1 = graph__3_circuit.get_circuit(telemetry_df_max, index, "Max")
        new_fig1_bars = graph__3_circuit.get_bars(telemetry_df_max, index, "Max")
        speed_value_max = telemetry_df_max.loc[index, 'Speed']
        speed_display_max = f"Current Speed: {speed_value_max} km/h"

        return new_fig1, new_fig1_bars, dash.no_update, dash.no_update, speed_display_max, dash.no_update


    elif trigger_id == 'circuit-graph-2' and clickData2:
        
        x = clickData2['points'][0]['x']
        y = clickData2['points'][0]['y']
        index = find_closest_index(x, y, telemetry_df_max)
        new_fig2 = graph__3_circuit.get_circuit(telemetry_df_ham, index, "Ham")
        new_fig2_bars = graph__3_circuit.get_bars(telemetry_df_ham, index, "Ham")
        speed_value_ham = telemetry_df_ham.loc[index, 'Speed']
        speed_display_ham = f"Current Speed: {speed_value_ham} km/h"

        return dash.no_update, dash.no_update, new_fig2, new_fig2_bars, dash.no_update, speed_display_ham
    
    
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

def find_closest_index(x, y, dataframe):
   
    distances = np.sqrt((dataframe['X'] - x)**2 + (dataframe['Y'] - y)**2)
    
    return distances.idxmin()