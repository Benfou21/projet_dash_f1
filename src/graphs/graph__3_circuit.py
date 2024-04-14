import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hover_template import hover_template_3_circuit
import ast

def get_circuit(data,index,pilote,legend):
    
    fig = make_subplots(rows=1, cols=1)
    x = data['X']
    y = data['Y']
    speed = data['Speed']
    max_speed = speed.max()
    min_speed = speed.min()
    colors = create_colors(speed)
    min_line_width = 2
    max_line_width = 10
    
    for i in range(len(x) - 1):
        relative_speed = (speed.iloc[i] - min_speed) / (max_speed - min_speed)
        line_width = min_line_width + (max_line_width - min_line_width) * relative_speed
        text = [str(speed.iloc[i]) + ' km/h'] * 2
        fig.add_trace(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=colors[i], width=5),
            showlegend=False,
            text=text,  # Utiliser le texte de survol
            hoverinfo='text'
        ))
    
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color='rgba(0,0,0,0)', showlegend=True, name="Légende"))
    
    # Marquer le point actuel avec un marker
    text_index = [str(speed.iloc[index]) + ' km/h'] * 2
    fig.add_trace(
        go.Scatter(x=[x.iloc[index]], y=[y.iloc[index]], mode='markers', marker=dict(size=10, color='purple'), name='Point selectionné',text =text_index,hoverinfo='text')
    )
    
    # Set up the layout of the figure
    fig.update_layout(
        
        title=f'Vitesse selon la position du circuit de {pilote}',
        
        showlegend=legend,
        # width = 800,
        # height = 500,
        autosize=True,
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
    
    
    
    fig.add_trace(go.Bar(x=[None], y=[None], marker=dict(
        color=['rgba(0, 255, 0, 0.5)', 'rgba(0, 255, 0, 1)'],
        colorsrc="speed",
    ), showlegend=True, name="Encodage de la vitesse par l'intensité"))

   
    fig.update_traces(hovertemplate=hover_template_3_circuit.get_speed_circuit_hover_template())
    
    fig.update_layout(
        legend=dict(
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=10,
                color='black'
            ),
            bordercolor='#344feb',
            borderwidth=1,
            y=1.3,
            xanchor='right',  
            yanchor='top',  
        )
    )
    
    
    return fig


def get_bars(data,index,pilote,legend):
    
    speed = data["Speed"]
    elapsed_time = data["Elapsed"]
    


    colors = create_colors(speed)
    
    colors[index] = "purple"
    
    
    fig = go.Figure(data=[go.Bar(
        x=elapsed_time,
        y=speed,
        marker_color=colors,
        width=0.4,
        showlegend=False
    )])
    
    speed_index = [speed[index]]
    elapsed_time_index = [elapsed_time[index]]
    colors_index = ["purple"]  # ou toute autre couleur distincte pour la barre d'index

    fig.add_trace(go.Bar(x=[None], y=[None], marker_color='rgba(0,0,0,0)', showlegend=True, name="Légende"))
    
    fig.add_trace(go.Bar(x=elapsed_time_index, y=speed_index, marker_color=colors_index, width=0.6, showlegend=True, name="Point selectionné"))

    fig.add_trace(go.Bar(x=[None], y=[None], marker=dict(
        color=['rgba(0, 255, 0, 0.5)', 'rgba(0, 255, 0, 1)'],
        colorsrc="speed",
    ), showlegend=True, name="Encodage de la vitesse par l'intensité"))

    
    fig.update_layout(
        title=f'Vitesse de {pilote} lors de son tour', 
        xaxis_title='Temps en seconde', 
        yaxis_title='Vitesse en km/h', 
        showlegend = legend,
       
        # width = 800,
        # height = 500,
        autosize=True,
        
    )
    
    fig.update_layout(
        legend=dict(
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=10,
                color='black'
            ),
            bordercolor='#344feb',
            borderwidth=1,
            y=1.10,
            xanchor='right',  # 'left', 'center', 'right'
            yanchor='top',  # 'top', 'middle', 'bottom'
        )
    )
    
    fig.update_traces(hovertemplate=hover_template_3_circuit.get_speed_bar_hover_template())
    
   
    return fig



def create_colors(speed):
    
    colors = []
    for s in speed:
        colors.append(get_color_with_single_hue(s, 0, max(speed)))
       
    return colors
            


def get_color_with_single_hue(speed_value, min_speed, max_speed):
    
    hue = 90
    
    # Calculer la valeur relative de la vitesse pour varier la saturation
    relative_speed = (speed_value - min_speed) / (max_speed - min_speed)
    saturation = 100 * relative_speed  
    lumi= 10 + 45* relative_speed
    # Retourner la couleur HSL avec la saturation variable
    return f"hsl({hue}, {saturation}%, {lumi}%)"


