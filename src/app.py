
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
import numpy as np
import pandas as pd
import graphs.graph__3_circuit as graph__3_circuit
import ast
from preprocessing.preprocessing_3 import get_data
from preprocessing.preprocessing_3 import get_max_speed
import hover_template.hover_template_3_circuit as hover_template_3_circuit
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

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



app.layout = html.Div(
    [
        html.H1(children='Scrollable Story pour la Formule 1'),
        
        dbc.Button("Ouvrir l'explication", id="open-modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Explication des graphes de vitesses")),
                dbc.ModalBody("Ces graphes vous permet d'explorer la vitesses des deux pilotes et de les comparer"),
                dbc.ModalFooter(
                    dbc.Button("Fermer", id="close-modal", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            is_open=False,  # Commence avec le modal fermé
        ),
        # Horizontal block for Max
        html.Div([
            # Vertical sub-block for Max's circuit graph
            html.Div(
                id='speed-display-1', 
                children=f'Current Speed: {telemetry_df_max["Speed"][0]} km/h', 
                style={
                    'fontSize': '18px',
                    'display': 'inline-block',
                    'width': '15%',
                    'textAlign': 'center',
                    'border': '2px solid #344feb',  # color border
                    'borderRadius': '10px',  # Rounded corners
                    'backgroundColor': '#f9f9f9',  # Light grey background
                    'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow
                    'padding': '10px'
                }
            ),
            html.Div([
                dcc.Graph(id='circuit-graph-1', figure=circuit_figure_max_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
            
            html.Div([
                dcc.Graph(id='circuit-graph-2', figure=circuit_figure_ham_initial)
            ], style={'display': 'inline-block', 'width': '33%'}),
            html.Div(
                id='speed-display-2', 
                children=f'Current Speed: {telemetry_df_ham["Speed"][0]} km/h',  
                style={
                    
                    'fontSize': '18px',
                    'display': 'inline-block',
                    'width': '15%',
                    'textAlign': 'center',
                    'border': '2px solid #344feb',  # color border
                    'borderRadius': '10px',  # Rounded corners
                    'backgroundColor': '#f9f9f9',  # Light grey background
                    'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow
                    'padding': '10px'
                }
            ),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}), # This ensures that the sub-blocks for Max are in one line
        
        html.Div([
            dcc.Checklist(
                id='toggle-sync',
                options=[{'label': ' Synchroniser les graphes ', 'value': 'sync'}],
                value=[],
                labelStyle={'display': 'block'}
            )
    ], style={'textAlign': 'center', 'margin': '20px'}),
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
    [Input('circuit-graph-1', 'clickData'), Input('circuit-graph-2', 'clickData'),Input('toggle-sync', 'value')],
    [State('circuit-graph-1', 'figure'), State('circuit-graph-2', 'figure')]
)
def update_graph(clickData1, clickData2,sync_value, fig1, fig2):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if 'sync' in sync_value:  # Si le toggle est activé
        if trigger_id in ['circuit-graph-1', 'circuit-graph-2']:
            clickData = clickData1 if trigger_id == 'circuit-graph-1' else clickData2
            if clickData:
                x = clickData['points'][0]['x']
                y = clickData['points'][0]['y']
                index_max = find_closest_index(x, y, telemetry_df_max)
                index_ham = find_closest_index(x, y, telemetry_df_ham)

                new_fig1 = graph__3_circuit.get_circuit(telemetry_df_max, index_max, "Max")
                new_fig1_bars = graph__3_circuit.get_bars(telemetry_df_max, index_max, "Max")
                speed_value_max = telemetry_df_max.loc[index_max, 'Speed']
                speed_display_max = f"Current Speed: {speed_value_max} km/h"

                new_fig2 = graph__3_circuit.get_circuit(telemetry_df_ham, index_ham, "Ham")
                new_fig2_bars = graph__3_circuit.get_bars(telemetry_df_ham, index_ham, "Ham")
                speed_value_ham = telemetry_df_ham.loc[index_ham, 'Speed']
                speed_display_ham = f"Current Speed: {speed_value_ham} km/h"

                return new_fig1, new_fig1_bars, new_fig2, new_fig2_bars, speed_display_max, speed_display_ham
    else :
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


@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open