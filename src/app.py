import dash

from dash import html, dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
import numpy as np
import pandas as pd
import os
from .graphs import graph__3_circuit




import ast
from .preprocessing.preprocessing_3 import get_data, get_max_speed

from .hover_template import hover_template_3_circuit

from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import graphs.graph_1_classement as graph_1_classement

from .graphs.graph_2_scatterplot_pneu import create_scatter_plot
from .graphs.graph_idriss import graph_idriss  # Assurez-vous que graph_idriss est le fichier correct

from .preprocessing.preprocessing_2b import get_combined_pitstop_data
from .graphs.graph_2b import create_pitstop_plot

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'F1 visualiation'
server = app.server

path_max = os.path.join("src","assets", "data", "telemetry_spain_2021_VER.csv")
telemetry_df_max = get_data(path_max)
path_ham = os.path.join("src","assets", "data", "telemetry_spain_2021_HAM.csv")
telemetry_df_ham = get_data(path_ham)

path_classement = os.path.join("src","assets", "data", "classement_2021.csv")
classement_df = pd.read_csv(path_classement, sep=';')


time_str = telemetry_df_max["Time"]   # c'est une chaîne de caractères qui ressemble à une liste
x_length = len(telemetry_df_max['X'])

index_initial = 0
circuit_figure_max_initial = graph__3_circuit.get_circuit(telemetry_df_max, index_initial, "Max",False)
bars_figure_max_initial = graph__3_circuit.get_bars(telemetry_df_max, index_initial, "Max",False)

# Génération initiale des figures pour telemetry_df_ham
circuit_figure_ham_initial = graph__3_circuit.get_circuit(telemetry_df_ham, index_initial, "Ham",True)
bars_figure_ham_initial = graph__3_circuit.get_bars(telemetry_df_ham, index_initial, "Ham",True)

# Génération de la figure évolution du classement au championnat du monde
evol_classement_1 = graph_1_classement.get_evol_classement(classement_df)

# Créez le tracé scatter initial pour un pilote

path_scatter_max = os.path.join("src","assets", "data", "driver_laps_2021_VER.csv")
path_scatter_ham = os.path.join("src","assets", "data", "driver_laps_2021_HAM.csv")
scatter_plot_initial = create_scatter_plot("HAM", path_scatter_max, path_scatter_ham)

# Récupération données pitstops
path_pit = os.path.join("src","assets", "data", "pitstops.csv")
pitstop_data = get_combined_pitstop_data(path_pit)

# Généré la figure Pitstop
pitstops_graph = create_pitstop_plot(pitstop_data)

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
    # 'padding': '20px',
    'borderRadius': '5px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    # 'textAlign': 'center',  # Centre le texte de la légende
}

dropdown_style = {
    'width': '80%',  # Ajustez la largeur à 100% de son conteneur
    'margin': '10px auto',  # Centre le dropdown avec une marge en haut et en bas
    'font-size': '16px',  # Ajustez ceci selon vos préférences et la longueur du texte
}
# legend_style = {
#     'textAlign': 'center',  # Centre le texte de la légende
#     'padding': '10px',
#     'margin': '0 auto',  # Centre la légende
#     'width': '100%',  # La légende prend toute la largeur disponible
# }
graph_container_style = {
    'display': 'flex',
    'flexDirection': 'column',
    # 'alignItems': 'center',  # Centre le graphique scatter plot horizontalement
    'margin': '0 auto',  # Centre le conteneur sur la page
}


app.layout = html.Div(
[
    
    html.Div(style={'margin-top': '100px'}), 
    html.H1(children=["Comprendre une course de Formule 1, la bataille",
            html.Br(),
            "Verstappen-Hamilton lors du GP d'Espagne 2021"]),
    html.Div(style={'margin-top': '100px'}), 
    html.P(children=
            '''Une course de Formule 1 dure deux heures, et les pilotes parcourent le circuit près de 60 fois à plus 
            de 300 km/h. Ils se battent tous pour dépasser leurs adversaires et
            franchir la ligne d'arrivée en premier, mais un seul gagne! Le spectacle d'une course est captivant, 
            mais pour un amateur, il est compliqué de comprendre les stratégies et
            les idées que suivent les équipes et les pilotes pour parvenir à la victoire.La bataille pour remporter 
            le Grand Prix d'Espagne 2021 servira d'exemple pour comprendre certains de ces principes de course.'''
    ),
    html.Div(style={'margin-top': '80px'}),        
    html.Table([
        html.Tr([
            html.Td([
                html.Div(children = 'Red Bull', style={'text-align': 'right'}),
                html.Div(children='23 ans', style={'text-align': 'right'}),
                html.Div(children='7e saison en F1', style={'text-align': 'right'}),
                html.Div(children='10 Grand Prix remportés', style={'text-align': 'right'})
                 ]),
             html.Td([
                html.Div('Max Verstappen', style={'text-align': 'center', 'font-weight': 'bold'}),
                html.Img(src='assets/data/verstappen.png'),
                ]),
            html.Td([
                html.Div('Lewis Hamilton', style={'text-align': 'center', 'font-weight': 'bold'}),
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
        
    html.Div(style={'margin-top': '100px'}),  
        
    html.P(children=
        '''La saison 2021 est l'une des plus disputée des 10 dernières années. L'expérience du
        champion en titre Lexis Hamilton et le talent brut de Max Verstappen s'affrontent tout
        au long de l'année. Les deux pilotes livrent d'incroyables duels pour remporter
        le championnat du monde. Le Grand Prix d'Espagne se déroule au début de la saison, alors que
        Lewis Hamilton a pris la tête du classement. Verstappen, qui finira par remporter le titre,
        se bat pour ne pas prendre trop de retard.'''
    ), 
        
    # Évolution classement championnat du monde
    html.Div(style={'margin-top': '50px'}), 
    html.Div(className='centered-div', children= [
        html.Div([
            dcc.Graph(id='graph_evol_classement', figure=evol_classement_1,config=dict(
                  showTips=False,
                  showAxisDragHandles=False,
                  displayModeBar=False),
                      style={
                          "width": "80%",
                          "height": "500px",
                          "display": "inline-block",
                          "top": "25%",
                          "left": "25%",
            })
        ])
    ]),
          
    html.Div(style={'margin-top': '200px'}), 
        
    html.H1(children = "Le Grand Prix d'Espagne 2021 "),
    
    html.Div(style={'margin-top': '50px'}), 
        
    html.P(children=
           '''Le Grand Prix d'Espagne 2021 prend place le dimanche 9 mai à Barcelone, sur le circuit de Barcelona-Catalunya.
           Utilisé depuis 1991, la caractéristique principale du circuit
           est la longue ligne droite des stands, d'environ 1050 mètres, où les pilotes peuvent
           atteindre des vitesses supérieures à 310 km/h. C'est la plus longue ligne droite
           « des stands » du championnat du monde de Formule 1. Le reste du circuit est
           composé de successions de virages rapides, de quelques gros freinages et d'une ligne droite opposée.'''
    ),
    html.Div(style={'margin-top': '80px'}), 
    html.Div(className='centered-div', children=
        [html.Img(src='assets/data/circuit-catalogne.png',
            style={
                'height': '100%',
                'width' : 'auto',
                "display": 'inline-block', 
                'max-width': '1000px'
            }
            
        )],style={'height': '300px'}
    ),
    
    html.Div(className='centered-div', children= [html.Span('Track Map Circuit de Catalunya - '),
        dcc.Link("Grand Prix d'Espagne 2021", href="https://fr.wikipedia.org/wiki/Grand_Prix_automobile_d%27Espagne_2021")
    ]),
                 
        
        
    #Partie 2  
    #Titre 2 eme section
    html.Div(style={'margin-top': '200px'}),
    html.H1(children = "Stratégie des Pneus"),        
    #1er partie 2 eme section
    html.Div(style={'margin-top': '100px'}),
    html.H3(children = "Stratégie des Pneus et leurs impacts sur le temps au tour"),
    html.Div(style={'margin-top': '50px'}),
    html.P(children=[
    
        '''Ce graphique met en evidence les delta de temps entre Verstappen et Hamilton en fonction des tours en mettant en évidence les changments de pneus.
        Nous permettant ainsi d'observer les stratégies réalisées par les écuries.
        En vert nous avons un delta positif et en rouge le delta est négatif.  La liste déroulantes en bas du graphique permet de changer de pilote. '''
    ]),      
    html.Div(style={'margin-top': '30px'}), 
    html.Div([
        html.P(children=[
            html.Br(),
            "Changement de pilote dans cette liste déroulante.",
        ],style={'textAlign': 'center'}),
        html.Div(style={'margin-top': '20px'}), 
        html.Div([
            dcc.Dropdown(
                id='pilote-dropdown',
                options=[
                    {'label': 'Max Verstappen', 'value': 'VER'},
                    {'label': 'Lewis Hamilton', 'value': 'HAM'}
                ],
                value='VER',  # Valeur par défaut
                clearable=False,
                style=dropdown_style
            )
        ], style=graph_container_style),
        dcc.Graph(id='delta-scatter-plot', figure=scatter_plot_initial,className='graph-small'),
    ]),
    html.Div(style={'margin-top': '60px'}), 
    html.P(children=[
            '''On remarque que Hamilton a opté pour des relais plus courts sur ses pneus comparativement à Verstappen. 
            En procédant à un premier changement de pneus anticipé, Hamilton avec des pneus neufs a pu rattraper son retard sur Verstappen entre le tour 30 et 42.
            Il recidive avec un changement surprise de pneus au tour 42, alors que Verstappen réalise son deuxième changement au tour 60.
            Cette manœuvre a permis à Hamilton de se retrouver sur des pneus plus frais, lui donnant l'opportunité de réduire l'écart de manière significative à partir du 56e tour 
            Finalement, après son deuxième arrêt, Verstappen se retrouve surclassé avec des pneus neufs mais non encore à leur pleine efficacité thermique, ce qui a facilité son dépassement par Hamilton''',
           
    ]),  
    
    html.Div(style={'margin-top': '100px'}),
    html.H3(children = "Les temps de pit stops des pilotes"),
    html.Div(style={'margin-top': '50px'}),
    html.P(children=[
        '''Ce graphique permet d'observer les temps que passes les deux pilotes lors des arrêts aux 
            stands. Les points bleu corresponds aux pit stops antérieurs au GP d'Espagne.Les points
            orange corresponds aux pit stops du GP d'Espagne.Vous pouvez affichez uniquement les
            points bleu ou orange en cliquant sur la légende'''
    ]),  
    html.Div(style={'margin-top': '100px'}),
    # Graphes Pitstops
    html.Div([
        dcc.Graph(id='pitstop-graph', figure=pitstops_graph)
    ], style={
        # 'display': 'flex', 
        'justifyContent': 'center', 
        'width': '100%',  
        # 'height': 'auto'  
    }),
    html.Div(style={'margin-top': '10px'}),
    html.P(children=[

        '''On remarque que l'équipe de Verstappen a été plus consitant sur la course que celle de Hamilton lors du GP d'Espagne
        On note cependant que Hamilton possède le temps le plus rapide.
        Sur ce point Max Verstappen possède l'avantage.'''
        
    ]),  
        #Partie 3 
    html.Div(style={'margin-top': '200px'}),
        
    html.H1(children = "La vitesse et la conduite en F1"),
    html.Div(style={'margin-top': '80px'}),
    html.H3(children = "Observation de la vitesse"),
    html.Div(style={'margin-top': '50px'}),
    html.P(children=[
        '''Ces graphiques vous montrent la vitesse des deux pilotes sur leurs meilleurs tours.
        Vous pouvez cliquer sur une position du circuit pour vous y déplacer et observer la vitesse. 
        Vous pouvez cocher la case de synchronisation pour interargir avec les deux graphiques en même temps.'''
    ]),   
    html.Div(style={'margin-top': '100px'}),
        
        
    html.Div([
            
        html.Div([
            dcc.Graph(id='circuit-graph-1', figure=circuit_figure_max_initial)
        ], style={'display': 'inline-block','flex' : '1','margin':'0px'}),
            
        html.Div([
            dcc.Graph(id='circuit-graph-2', figure=circuit_figure_ham_initial)
                
    ], style={'display': 'inline-block','flex' : '1','margin':'0px'}),
            
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},), # This ensures that the sub-blocks for Max are in one line
        
    html.Div([
        
        html.Div(
            id='speed-display-1', 
            children=f'Vitesse actuelle: {telemetry_df_max["Speed"][0]} km/h', 
            style={
                'flex': '1',
                'fontSize': '16px',
                'display': 'inline-block',
                'textAlign': 'center',
                'border': '2px solid #344feb',  # color border
                'borderRadius': '10px',  # Rounded corners
                'backgroundColor': '#f9f9f9',  # Light grey background
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow
                'padding': '5px',
                'margin': '0 200px',
            }
        ),
        
        html.Div(
            id='speed-display-2', 
            children=f'Vitesse actuelle: {telemetry_df_ham["Speed"][0]} km/h',  
            style={
                'flex': '1',
                'fontSize': '16px',
                'display': 'inline-block',
                'textAlign': 'center',
                'border': '2px solid #344feb', 
                'borderRadius': '10px',  
                'backgroundColor': '#f9f9f9', 
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                'padding': '5px',
                'margin': '0 200px',      
            }
            ),
    ], style={'justifyContent': 'space-between', 'alignItems': 'center', 'display': 'flex',}),
        
    html.Div(style={'margin-top': '20px'}),
    html.P(children="En cochant la case synchronisation, lorsque vous allez modifier la position sur un graphe cela synchronise l'autre.", style={'fontSize': '12px','textAlign': 'center'}),
    html.Div([
        dcc.Checklist(
            id='toggle-sync',
            options=[{'label': 'Synchronisation ', 'value': 'sync'}],
            value=[],
            labelStyle={'display': 'block'}
        )
    ], style={'textAlign': 'center', 'margin': '5px'}),
    # Horizontal block for Ham
    html.Div([
         # Vertical sub-block for Max's bar graph
        html.Div([
            dcc.Graph(id='speed-graph-1', figure=bars_figure_max_initial)
        ], style={'display': 'inline-block','flex' : '1'}),
            # Vertical sub-block for Ham's bar graph
        html.Div([
            dcc.Graph(id='speed-graph-2', figure=bars_figure_ham_initial)
        ], style={'display': 'inline-block','flex' : '1'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
        
        
    html.Div(style={'margin-top': '100px'}),
    
    html.H3(children = "Observation de la vitesse relatives sur les section de circuit "),
    
    html.Div(style={'margin-top': '50px'}),
    
    html.P(children=[
        '''Ce graphique montre les section de circuit ou Max Verstappen est plus rapide que Lewis
        Hamilton. En rouge sont les protions de circuit ou Verstappen avait une vistesse inférieur
        à Hamilton. En vert sont les protions de circuit ou Verstappen avait une vistesse
        supérieur à Hamilton.'''
    ]),
    
    html.Div(style={'margin-top': '80px'}),
    
    html.Div([
        dcc.Graph(id='speed-difference-plot')  # Nouvel ID pour le graphique de différence de vitesse
    ], style={'paddingLeft': '15%', 'paddingRight': '15%', 'alignItems': 'center', 'justifyContent': 'center',}),
      
    html.Div(style={'margin-top': '100px'}),
    
    html.P(children=[
        '''On remarque que Max Verstappen est plus rapide en sortie de virage. Il est cependant plus lent que Lewis dans les virages.
        Enfin la grande ligne droite du circuit est à l'avantage de Lewis.
        On ne peut faire ressortir l'un des pilotes comme celui ayant la conduite la plus rapide. '''
    ]),  
    
    html.Div(style={'margin-top': '90px'}),
    
    html.H1("Conlusion"),
    html.Div(style={'margin-top': '40px'}),
    html.P(children=
        '''Le vainqueur de le course est Lewis Hamilton, Max Verstappen finissant deuxième.
        Ces graphiques nous ont montrés une bataille très sérrée entre les deux pilotes, les deux possèdants des conduites performantes.
        C'est la stratégie des pneus de Hamilton qui lui a donné sa victoire.''',
    ), 
    
    html.Div(style={'margin-top': '200px'}),
    
    html.H1("Annexe"),
    html.Div(style={'margin-top': '40px'}),
    html.P([
    "L’ensemble des données présentées sur ce site provient de l'API ",
    html.A("Fast F1", href="https://github.com/theOehrly/Fast-F1", target="_blank"),
    ", une ressource de premier plan pour les statistiques et informations détaillées sur la Formule 1. ",
    "Fast F1 est reconnu pour son approche exhaustive et précise, offrant des données fiables et à jour qui comprennent les temps au tour, ",
    "les positions, les états des pneus et bien plus encore.",
    html.Br(),
    "Cette API tire profit des dernières avancées en matière de traitement de données pour fournir des informations en temps quasi réel, ",
    "ce qui permet aux amateurs de course ainsi qu'aux professionnels d’analyser en profondeur chaque Grand Prix. ",
    "La rigueur de la collecte des données et l'attention portée à la mise à jour continue font de Fast F1 une source incontournable ",
    "pour tous ceux qui cherchent à comprendre les nuances et la dynamique de ce sport de haute voltige.",
    html.Br(),
    "Nous nous engageons à respecter l'intégrité des informations et à créditer Fast F1 comme source principale des données utilisées ",
    "pour les analyses et visualisations disponibles sur notre site. Pour plus d'informations sur l'API Fast F1 et pour accéder à leur documentation complète, ",
    "veuillez visiter leur ",
    html.A("site officiel", href="https://github.com/theOehrly/Fast-F1", target="_blank"),
    "."
]), 
    
    
], style={ 'padding' : '80px',  'textAlign': 'center'},)



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

                new_fig1 = graph__3_circuit.get_circuit(telemetry_df_max, index_max, "Max",False)
                new_fig1_bars = graph__3_circuit.get_bars(telemetry_df_max, index_max, "Max",False)
                speed_value_max = telemetry_df_max.loc[index_max, 'Speed']
                speed_display_max = f"Vitesse actuelle: {speed_value_max} km/h"

                new_fig2 = graph__3_circuit.get_circuit(telemetry_df_ham, index_ham, "Ham",True)
                new_fig2_bars = graph__3_circuit.get_bars(telemetry_df_ham, index_ham, "Ham",True)
                speed_value_ham = telemetry_df_ham.loc[index_ham, 'Speed']
                speed_display_ham = f"Vitesse actuelle: {speed_value_ham} km/h"

                return new_fig1, new_fig1_bars, new_fig2, new_fig2_bars, speed_display_max, speed_display_ham
    else :
        if trigger_id == 'circuit-graph-1' and clickData1:
            
            x = clickData1['points'][0]['x']
            y = clickData1['points'][0]['y']
            index = find_closest_index(x, y, telemetry_df_max)
            new_fig1 = graph__3_circuit.get_circuit(telemetry_df_max, index, "Max",False)
            new_fig1_bars = graph__3_circuit.get_bars(telemetry_df_max, index, "Max",False)
            speed_value_max = telemetry_df_max.loc[index, 'Speed']
            speed_display_max = f"Vitesse actuelle: {speed_value_max} km/h"

            return new_fig1, new_fig1_bars, dash.no_update, dash.no_update, speed_display_max, dash.no_update


        elif trigger_id == 'circuit-graph-2' and clickData2:
            
            x = clickData2['points'][0]['x']
            y = clickData2['points'][0]['y']
            index = find_closest_index(x, y, telemetry_df_max)
            new_fig2 = graph__3_circuit.get_circuit(telemetry_df_ham, index, "Ham",True)
            new_fig2_bars = graph__3_circuit.get_bars(telemetry_df_ham, index, "Ham",True)
            speed_value_ham = telemetry_df_ham.loc[index, 'Speed']
            speed_display_ham = f"Vitesse actuelle: {speed_value_ham} km/h"

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
    return create_scatter_plot(selected_pilote, "src/assets/data/driver_laps_2021_VER.csv", "src/assets/data/driver_laps_2021_HAM.csv")



@app.callback(
    Output('speed-difference-plot', 'figure'),
    [Input('pilote-dropdown', 'value')]  # Vous pouvez utiliser le même dropdown pour déclencher ce callback
)
def update_speed_difference_plot(selected_pilote):
    # Vous pouvez ajouter la logique ici pour choisir le chemin en fonction du pilote sélectionné
    # Pour l'instant, je vais utiliser les chemins en dur que vous avez fournis
    path_max = os.path.join("src","assets", "data", "telemetry_spain_2021_VER.csv")
    path_ham = os.path.join("src","assets", "data", "telemetry_spain_2021_HAM.csv")
   
    # Appel à votre fonction de graphique ici
    return graph_idriss(path_max, path_ham)



if __name__ == '__main__':
    app.run_server(debug=True)