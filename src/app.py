
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from preprocessing.preprocessing_3 import get_data
import graphs.graph__3_circuit as graph__3_circuit
from graphs.graph_2_scatterplot_pneu import create_scatter_plot
from graphs.graph_idriss import graph_idriss  # Assurez-vous que graph_idriss est le fichier correct


app = dash.Dash(__name__)
app.title = 'F1 Visualization'

# Obtenez les données nécessaires pour les tracés de télémétrie et les différences de tours
path_max = "assets/data/telemetry_spain_2021_VER.csv"
telemetry_df_max = get_data(path_max)
path_ham = "assets/data/telemetry_spain_2021_HAM.csv"
telemetry_df_ham = get_data(path_ham)

# Générez les figures initiales pour la télémétrie et les barres
index_initial = 0
circuit_figure_max_initial = graph__3_circuit.get_circuit(telemetry_df_max, index_initial, "Max")
bars_figure_max_initial = graph__3_circuit.get_bars(telemetry_df_max, index_initial, "Max")
circuit_figure_ham_initial = graph__3_circuit.get_circuit(telemetry_df_ham, index_initial, "Ham")
bars_figure_ham_initial = graph__3_circuit.get_bars(telemetry_df_ham, index_initial, "Ham")

# Créez le tracé scatter initial pour un pilote
scatter_plot_initial = create_scatter_plot("HAM", "assets/data/driver_laps_2021_VER.csv", "assets/data/driver_laps_2021_HAM.csv")

# Définition de la mise en page de l'application avec les composants nécessaires
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

#stles CSS pr youyou
dropdown = dcc.Dropdown(
    id='pilote-dropdown',
    options=[
        {'label': 'Max Verstappen', 'value': 'VER'},
        {'label': 'Lewis Hamilton', 'value': 'HAM'}
    ],
    value='VER',  # Valeur par défaut
    clearable=False
)
graph_style = {
    'padding': '20px',
    'borderRadius': '5px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
}

dropdown_style = {
    'width': '50%',  # Ajustez en fonction de la taille de votre graphique
    'margin': '10px auto 20px',  # Centre le dropdown avec une marge en haut et en bas
}

legend_style = {
    'textAlign': 'center',  # Centre le texte de la légende
    'padding': '10px',
    'margin': '0 auto',  # Centre la légende
    'width': '100%',  # La légende prend toute la largeur disponible
}
graph_container_style = {
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',  # Centre le graphique scatter plot horizontalement
    'margin': '0 auto',  # Centre le conteneur sur la page
}



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
        
        
        #div graph younes 
        
    html.Div([
            # Le Dropdown juste en dessous du graphique
            html.Div([
            dcc.Graph(id='delta-scatter-plot', figure=scatter_plot_initial),
            dcc.Dropdown(
                id='pilote-dropdown',
                options=[
                    {'label': 'Max Verstappen', 'value': 'VER'},
                    {'label': 'Lewis Hamilton', 'value': 'HAM'}
                ],
                value='VER',  # Valeur par défaut
                clearable=False,
                style=dropdown_style,
            )
        ], style=graph_container_style),
        ], style={'textAlign': 'center'}  # Centre tout le contenu de la page
    ),
       #idriss plot
       html.Div([
        dcc.Graph(id='speed-difference-plot')  # Nouvel ID pour le graphique de différence de vitesse
    ], style={'padding': '20px', 'display': 'flex', 'justifyContent': 'center'}),
            
])



#pour younes 


@app.callback(
    Output('delta-scatter-plot', 'figure'),
    [Input('pilote-dropdown', 'value')]
)

def update_scatter_plot(selected_pilote):
    # Mettez à jour le scatter plot basé sur le pilote sélectionné
    return create_scatter_plot(selected_pilote, "assets/data/driver_laps_2021_VER.csv", "assets/data/driver_laps_2021_HAM.csv")

# @app.callback(
#     [Output('circuit-graph-1', 'figure'), Output('speed-graph-1', 'figure'), 
#      Output('circuit-graph-2', 'figure'), Output('speed-graph-2', 'figure'),
#      Output('speed-display-1', 'children'),Output('speed-display-2', 'children')],
#     [Input('circuit-graph-1', 'clickData'), Input('circuit-graph-2', 'clickData')],
#     [State('circuit-graph-1', 'figure'), State('circuit-graph-2', 'figure')]
# )
# def update_graph(clickData1, clickData2, fig1, fig2):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     print(trigger_id)
#     if trigger_id == 'circuit-graph-1' and clickData1:
        
#         x = clickData1['points'][0]['x']
#         y = clickData1['points'][0]['y']
#         index = find_closest_index(x, y, telemetry_df_max)
#         new_fig1 = graph__3_circuit.get_circuit(telemetry_df_max, index, "Max")
#         new_fig1_bars = graph__3_circuit.get_bars(telemetry_df_max, index, "Max")
#         speed_value_max = telemetry_df_max.loc[index, 'Speed']
#         speed_display_max = f"Current Speed: {speed_value_max} km/h"

#         return new_fig1, new_fig1_bars, dash.no_update, dash.no_update, speed_display_max, dash.no_update


#     elif trigger_id == 'circuit-graph-2' and clickData2:
        
#         x = clickData2['points'][0]['x']
#         y = clickData2['points'][0]['y']
#         index = find_closest_index(x, y, telemetry_df_max)
#         new_fig2 = graph__3_circuit.get_circuit(telemetry_df_ham, index, "Ham")
#         new_fig2_bars = graph__3_circuit.get_bars(telemetry_df_ham, index, "Ham")
#         speed_value_ham = telemetry_df_ham.loc[index, 'Speed']
#         speed_display_ham = f"Current Speed: {speed_value_ham} km/h"

#         return dash.no_update, dash.no_update, new_fig2, new_fig2_bars, dash.no_update, speed_display_ham
    
    
#     return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# def find_closest_index(x, y, dataframe):
   
#     distances = np.sqrt((dataframe['X'] - x)**2 + (dataframe['Y'] - y)**2)
    
#     return distances.idxmin()


@app.callback(
    Output('speed-difference-plot', 'figure'),
    [Input('pilote-dropdown', 'value')]  # Vous pouvez utiliser le même dropdown pour déclencher ce callback
)
def update_speed_difference_plot(selected_pilote):
    # Vous pouvez ajouter la logique ici pour choisir le chemin en fonction du pilote sélectionné
    # Pour l'instant, je vais utiliser les chemins en dur que vous avez fournis
    ver_path = "assets/data/telemetry_spain_2021_VER.csv"
    ham_path = "assets/data/telemetry_spain_2021_HAM.csv"
    # Appel à votre fonction de graphique ici
    return graph_idriss(ver_path, ham_path)


if __name__ == '__main__':
    app.run_server(debug=True)