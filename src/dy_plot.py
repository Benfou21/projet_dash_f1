import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from preprocessing import resample_based_on_speed
from preprocessing import resample_based_on_time
import ast

def get_circuit(data,index):
    
    # fig = go.Figure()
    fig = make_subplots(rows=1, cols=1)
    x = data['x']
    y = data['y']
    speed = data['speed']
    
    # time_str = data["time"]   # c'est une chaîne de caractères qui ressemble à une liste
    # time_list = ast.literal_eval(time_str)
    # x, y, speed = resample_based_on_time(data['x'], data['y'], data['speed'], time_list)
    
    # Add the trace of the circuit
    # fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Track'))
    
    
    
    speed_normalized = (speed - min(speed)) / (max(speed) - min(speed))
    color_scale = [(v, f"rgb( {int(255 * (1 - v))},{int(255 * v)}, 0)") for v in speed_normalized]
    
    for i in range(len(x) - 1):
        fig.add_trace(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=color_scale[i][1], width=2),
            showlegend=False))

    
    fig.add_trace(
        go.Scatter(x=[x[index]], y=[y[index]], mode='markers', marker=dict(size=10, color='red'), name='Car'),
        row=1, col=1
    )
    
    
    # Set up the layout of the figure
    fig.update_layout(
        title='F1 Telemetry Data Animation',
        showlegend=False,
        xaxis=dict(range=[min(x), max(x)], autorange=False),
        yaxis=dict(range=[min(y), max(y)], autorange=False)
    )
    
    # frames = [go.Frame(
    #     data=[
    #         go.Scatter(x=x, y=y, mode='lines', name='Track'),  # include the track in each frame
    #         go.Scatter(x=[x[k]], y=[y[k]], mode='markers', marker=dict(size=10, color='red'))  # car's position
    #     ],
    #     name=str(k)
    # ) for k in range(len(x))]


    # fig.frames = frames
    

    
    
    return fig



def get_color(speed_value):
    if speed_value < 50:
        return 'red'
    elif 50 <= speed_value < 100:
        return 'orange'
    elif 100 <= speed_value < 200 :
        return 'yellow'
    else:
        return 'green'


def get_bars(data,index):
    speed = data["speed"]
    

    # Convertir la chaîne en liste
    time_str = data["time"]   # c'est une chaîne de caractères qui ressemble à une liste
    time_list = ast.literal_eval(time_str)
    # print(time_list)
    
    tickvals = [i for i in range(len(time_list)) if i % 50 == 0]

    # Définir le texte des étiquettes pour correspondre à ces emplacements
    ticktext = [str(time_list[i]) for i in tickvals]

    speed_normalized = (speed - min(speed)) / (max(speed) - min(speed))
    color_scale = [f"rgb({int(255 * (1 - v))}, {int(255 * v)}, 0)" for v in speed_normalized]
    
    colors = [get_color(s) for s in speed]
    colors[index] = 'red'
    fig = go.Figure(data=[go.Bar(
        y=speed,
        marker_color=color_scale  # Affecter les couleurs aux barres
    )])

    # Personnaliser le layout si nécessaire
    fig.update_layout(
        title='Vitesse sur différentes plages horaires', 
        xaxis_title='Temps en seconde', 
        yaxis_title='Vitesse en km/h', 
    )
    # Mettre à jour l'axe des x pour inclure les étiquettes de temps personnalisées
    fig.update_xaxes(tickvals=tickvals, ticktext=ticktext)

    return fig






# f"rgb( {int(255 * (1 - v))},{int(255 * v)}, 0)"