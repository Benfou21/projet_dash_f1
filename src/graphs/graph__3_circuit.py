import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from preprocessing.preprocessing_3 import resample_based_on_speed
from preprocessing.preprocessing_3 import resample_based_on_time
import hover_template.hover_template_3_circuit as hover_template_3_circuit
import ast

def get_circuit(data,index,pilote):
    
    fig = make_subplots(rows=1, cols=1)
    x = data['X']
    y = data['Y']
    speed = data['Speed']
    
    colors = create_colors(speed)
    
    for i in range(len(x) - 1):
        text = [str(speed.iloc[i]) + ' km/h'] * 2
        fig.add_trace(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=colors[i], width=2),
            showlegend=False,
            text=text,  # Utiliser le texte de survol
            hoverinfo='text'
        ))
    
    # Marquer le point actuel avec un marker
    text_index = [str(speed.iloc[index]) + ' km/h'] * 2
    fig.add_trace(
        go.Scatter(x=[x.iloc[index]], y=[y.iloc[index]], mode='markers', marker=dict(size=10, color='purple'), name='Car',text =text_index,hoverinfo='text')
    )
    
    # Set up the layout of the figure
    fig.update_layout(
        
        title=f'Vitesse selon la position du circuit de {pilote}',
        
        showlegend=False,
        
        xaxis=dict(
            range=[min(x), max(x)], 
            autorange=False,
            showgrid=False,
            zeroline = False,
            tickvals=[],  
            ticktext=[] 
        ),
        
        yaxis=dict(
            range=[min(y), max(y)], 
            autorange=False,
            showgrid=False,
            zeroline = False,
            tickvals=[],  
            ticktext=[] 
        ),
        # plot_bgcolor='white',  
        #paper_bgcolor='white',
    )
   
    fig.update_traces(hovertemplate=hover_template_3_circuit.get_speed_circuit_hover_template())
    
    
    return fig

def get_color_2(speed_value, min_speed, max_speed):
    
    relative_speed = (speed_value - min_speed) / (max_speed - min_speed)
    saturation = 50 + 50 * (relative_speed)  # Saturation varie à hauteur de 40%
    
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


def get_bars(data,index,pilote):
    
    speed = data["Speed"]
    elapsed_time = data["Elapsed"]
    


    colors = create_colors(speed)
    
    colors[index] = "purple"
    
    
    fig = go.Figure(data=[go.Bar(
        x=elapsed_time,
        y=speed,
        marker_color=colors,
        width=0.4
    )])
    
    speed_index = [speed[index]]
    elapsed_time_index = [elapsed_time[index]]
    colors_index = ["purple"]  # ou toute autre couleur distincte pour la barre d'index

    fig.add_trace(go.Bar(x=elapsed_time_index, y=speed_index, marker_color=colors_index, width=0.6))


    # Personnaliser le layout si nécessaire
    fig.update_layout(
        title=f'Vitesse sur différentes plages horaires de {pilote}', 
        xaxis_title='Temps en seconde', 
        yaxis_title='Vitesse en km/h', 
        showlegend = False
        
    )
    fig.update_traces(hovertemplate=hover_template_3_circuit.get_speed_bar_hover_template())
    
   
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
            


