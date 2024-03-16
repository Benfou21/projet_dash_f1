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
    
    
    
    # Générer la couleur pour le segment actuel
  
    colors = create_colors(speed)
    for i in range(len(x) - 1):
        
        fig.add_trace(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=colors[i], width=4),
            showlegend=False))

    
    fig.add_trace(
        go.Scatter(x=[x[index]], y=[y[index]], mode='markers', marker=dict(size=15, color='purple'), name='Car'),
        row=1, col=1
    )
    
    
    # Set up the layout of the figure
    fig.update_layout(
        title='Vitesse selon la position du circuit',
        showlegend=False,
        xaxis=dict(range=[min(x), max(x)], autorange=False,showgrid=False,zeroline = False),
        yaxis=dict(range=[min(y), max(y)], autorange=False,showgrid=False,zeroline = False),
        # plot_bgcolor='white',  
        #paper_bgcolor='white',
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

def get_color_2(speed_value, min_speed, max_speed):
    
    relative_speed = (speed_value - min_speed) / (max_speed - min_speed)
    saturation = 60 + 40 * relative_speed  # Saturation varie à hauteur de 40%
    
    if speed_value < 100:
        return f"hsl(0, {saturation}%, 50%)"  # Rouge avec saturation variable
    elif 100 <= speed_value < 250:
        return f"hsl(39, {saturation}%, 50%)"  # Orange avec saturation variable
    else:
        return f"hsl(120, {saturation}%, 50%)"  # Vert avec saturation variable


def get_color(speed_value):
    if speed_value < 100:
        return 'red'
    elif 100 <= speed_value < 250:
        return 'orange'
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

    colors = create_colors(speed)
    
    colors[index] = "purple"
    
    fig = go.Figure(data=[go.Bar(
        y=speed,
        marker_color=colors  # Affecter les couleurs aux barres
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



def create_colors(speed):
    min_red_speed, max_red_speed = 0, 100
    min_orange_speed, max_orange_speed = 100, 250
    min_green_speed, max_green_speed = 250, max(speed)
    
    colors = []
    for s in speed:
        if s < 100:
            colors.append(get_color_2(s, min_red_speed, max_red_speed))
        elif 100 <= s < 250:
            colors.append(get_color_2(s, min_orange_speed, max_orange_speed))
        else:
            colors.append(get_color_2(s, min_green_speed, max_green_speed))
    return colors
            


# f"rgb( {int(255 * (1 - v))},{int(255 * v)}, 0)"