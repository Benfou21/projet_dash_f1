
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
import graphs.graph_1_classement as graph_1_classement
from graphs.graph_2_scatterplot_pneu import create_scatter_plot
from graphs.graph_idriss import graph_idriss  # Assurez-vous que graph_idriss est le fichier correct



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'F1 visualiation'

path_max = "assets\\data\\telemetry_spain_2021_VER.csv"
telemetry_df_max = get_data(path_max)

path_ham = "assets\\data\\telemetry_spain_2021_HAM.csv"
telemetry_df_ham = get_data(path_ham)

path_classement = 'assets\\data\\classement_2021.csv'
classement_df = pd.read_csv(path_classement, sep=';')


time_str = telemetry_df_max["Time"]   # c'est une chaîne de caractères qui ressemble à une liste
x_length = len(telemetry_df_max['X'])

index_initial = 0
circuit_figure_max_initial = graph__3_circuit.get_circuit(telemetry_df_max, index_initial, "Max")
bars_figure_max_initial = graph__3_circuit.get_bars(telemetry_df_max, index_initial, "Max")

# Génération initiale des figures pour telemetry_df_ham
circuit_figure_ham_initial = graph__3_circuit.get_circuit(telemetry_df_ham, index_initial, "Ham")
bars_figure_ham_initial = graph__3_circuit.get_bars(telemetry_df_ham, index_initial, "Ham")

# Génération de la figure évolution du classement au championnat du monde
evol_classement_1 = graph_1_classement.get_evol_classement(classement_df)

# Créez le tracé scatter initial pour un pilote
scatter_plot_initial = create_scatter_plot("HAM", "assets/data/driver_laps_2021_VER.csv", "assets/data/driver_laps_2021_HAM.csv")



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

app.layout = html.Div([
         html.H1(children=["Comprendre une course de Formule 1,la bataille",
                        html.Br(),
                        "Verstappen-Hamilton lors du GP d'Espagne 2021"]),
        html.P(children=[
            "Une course de Formule 1 dure deux heures, et les pilotes parcourent le circuit près de 60 fois à plus de 300 km/h. Ils se battent tous pour dépasser leurs adversaires et",
            html.Br(),
            "franchir la ligne d'arrivée en premier, mais un seul gagne! Le spectacle d'une course est captivant, mais pour un amateur, il est compliqué de comprendre les stratégies et",
            html.Br(),
            "les idées que suivent les équipes et les pilotes pour parvenir à la victoire.La bataille pour remporter le Grand Prix d'Espagne 2021 servira d'exemple pour",
            html.Br(),
            "comprendre certains de ces principes de course."
        ]),
        html.Div(style={'margin-top': '100px'}),        
        html.Table([
                html.Tr([
                    html.Td([
                        html.Div(children = 'Red Bull', style={'text-align': 'right'}),
                        html.Div(children='23 ans', style={'text-align': 'right'}),
                        html.Div(children='7e saison en F1', style={'text-align': 'right'}),
                        html.Div(children='10 Grand Prix remportés', style={'text-align': 'right'})
                        ]),
                    html.Td([
                        html.Img(src='assets/data/verstappen.png'),
                        ]),
                    html.Td([
                        html.Img(src='assets/data/Hamilton.png')
                        ]),
                    html.Td([
                        html.Div(children = 'Mercedes', style={'text-align': 'left'}),
                        html.Div(children = '36 ans', style={'text-align': 'left'}),
                        html.Div(children = '15e saison en F1', style={'text-align': 'left'}),
                        html.Div(children = '95 Grand Prix remportés', style={'text-align': 'left'}),
                        html.Div(children = '7 fois champion du monde', style={'text-align': 'left'}),
                        ])
                    ])       
            ]),
        
        html.Div(style={'margin-top': '30px'}),  
        
        html.P(children=[
            " La saison 2021 est l'une des plus disputée des 10 dernières années. L'expérience du champion en titre Lexis ",
            html.Br(),
            "Hamilton et le talent brut de Max Verstappen s'affronte tout au long de l'année 2021. Les 2 pilotes se livrent ",
            html.Br(),
            "d'incroyables duels pour remporter le championnat du monde. Le GP d'Espagne se déroule au début de la saison, ",
            html.Br(),
            "alors que Hamilton est déjà 1er au classement. Verstappen se bat pour ne pas prendre trop de retard."
        ]),   
        html.Div(style={'margin-top': '200px'}), 
        
        html.H1(children = "Le Grand Prix d'Espagne 2021 "),
        
        html.P(children=[
            "Le GP d'Espagne 2021 prend place le dimanche 9 mai à Barcelone, sur le circuit de Barcelona-Catalunya, utilisé depuis 1991. La",
            html.Br(),
            "caractéristique principale du circuit est sa longue ligne droite des stands d'environ 1,05km où les pilotes peuvent atteindre des ",
            html.Br(),
            "vitesses supérieures à 310 km/h. C'est la plus longue ligne droite dite « des stands » du championnat du monde de Formule 1.",
            html.Br(),
            "Le reste du circuit est composé de successions de virages rapides, de quelques gros freinages et d'une ligne droite opposée."
        ]),   
        
        html.Div(style={'margin-top': '200px'}),
        # Évolution classement championnat du monde
        html.Div([
            html.Div([
                dcc.Graph(id='graph_evol_classement', figure=evol_classement_1,config=dict(
                      showTips=False,
                      showAxisDragHandles=False,
                      displayModeBar=False))
                ])
        ]),
        html.Div(style={'margin-top': '200px'}),
        
        html.H2(children = "La vitesse et la conduite en F1"),
        html.Div(style={'margin-top': '100px'}),
        html.H3(children = "Observation de la vitesse"),
        html.Div(style={'margin-top': '50px'}),
        html.P(children=[
            "Ces graphiques vous montrent la vitesse des deux pilotes sur leurs meilleurs tours.",
            html.Br(),
            "Vous pouvez cliquer sur une position du circuit pour vous y déplacer et observer la vitesse.",
            html.Br(),
            "Vous pouvez cocher la case de synchronisation pour interargir avec les deux graphs en même temps."
        ]),   
        html.Div(style={'margin-top': '50px'}),
        
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
    ], style={'textAlign': 'center', 'margin': '5px'}),
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
    
    ## section youyou
    html.Div(style={'margin-top': '200px'}),
    
    html.Div([
        # Votre graphique ici
        dcc.Graph(id='delta-scatter-plot', figure=scatter_plot_initial),

        # Le Dropdown juste en dessous du graphique
        html.Div([
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
    ], style={'textAlign': 'center'}),  # Centre tout le contenu de la page
    
    html.Div(style={'margin-top': '200px'}),
    
    # idriss plot
    html.Div([
        dcc.Graph(id='speed-difference-plot')  # Nouvel ID pour le graphique de différence de vitesse
    ], style={'padding': '20px', 'display': 'flex', 'justifyContent': 'center'}),
  
    ],
    style={'textAlign': 'center'},  
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
    Output('delta-scatter-plot', 'figure'),
    [Input('pilote-dropdown', 'value')]
)

def update_scatter_plot(selected_pilote):
    # Mettez à jour le scatter plot basé sur le pilote sélectionné
    return create_scatter_plot(selected_pilote, "assets/data/driver_laps_2021_VER.csv", "assets/data/driver_laps_2021_HAM.csv")


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