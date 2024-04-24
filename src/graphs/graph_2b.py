import sys
import subprocess
import pandas as pd



import plotly.graph_objects as go
import numpy as np


def create_pitstop_plot(df_combined):
   # Créer une figure Plotly
    fig = go.Figure()

    # Ajouter les temps des pitstops pour Hamilton
    fig.add_trace(go.Scatter(
        x=df_combined[df_combined['Driver'] == 'HAM']['Duration'],
        y=['Hamilton'] * len(df_combined[df_combined['Driver'] == 'HAM']),
        mode='markers',
        marker=dict(color='blue', size=10),
        name='Temps de pit stop<br>avant le Grand prix d\'Espagne',
        legendgroup='pit_avant',
        hovertemplate='Temps  au stand: %{x}s<br>Grand Prix: %{customdata[0]}<br>Ordre d\'arrêt au stand: %{customdata[1]} arrêt <extra></extra>',  
        customdata=df_combined[df_combined['Driver'] == 'HAM'][['GP', 'PitOrder']] 

    ))

    # Ajouter les temps des pitstops pour Verstappen
    fig.add_trace(go.Scatter(
        x=df_combined[df_combined['Driver'] == 'VER']['Duration'],
        y=['Verstappen'] * len(df_combined[df_combined['Driver'] == 'VER']),
        mode='markers',
        marker=dict(color='blue', size=10),
        legendgroup='pit_avant',  
        showlegend=False,  # Masquer la légende pour éviter la duplication
        hovertemplate='Temps au stand: %{x}s<br>Grand Prix: %{customdata[0]}<br>Ordre d\'arrêt au stand: %{customdata[1]} arrêt <extra></extra>',  
        customdata=df_combined[df_combined['Driver'] == 'VER'][['GP', 'PitOrder']]
    ))

    # Marquer en vert les points correspondant à la session 4 (Grand Prix d'Espagne)
    session_4_data_verstappen = df_combined[(df_combined['Driver'] == 'VER') & (df_combined['SessionNumber'] == 4)]
    session_4_data_hamilton = df_combined[(df_combined['Driver'] == 'HAM') & (df_combined['SessionNumber'] == 4)]

    fig.add_trace(go.Scatter(
        x=session_4_data_verstappen['Duration'],
        y=['Verstappen'] * len(session_4_data_verstappen),
        mode='markers',
        marker=dict(color='orange', size=10),
        name='Pit stop Grand prix d\'Espagne',  # Utilisation d'un seul nom pour les deux ensembles de données
        legendgroup='pit_esp',
        hovertemplate=(
        "Temps  au stand: %{x}s<br>"
        "Grand Prix:Espagne<br>"  
        "Ordre du pit stop: %{customdata} arrêt <extra></extra>" 
        ),
        customdata=session_4_data_verstappen['PitOrder']

    ))

    fig.add_trace(go.Scatter(
        x=session_4_data_hamilton['Duration'],
        y=['Hamilton'] * len(session_4_data_hamilton),
        mode='markers',
        marker=dict(color='orange',size=10),
        legendgroup='pit_esp',  
        showlegend=False,
        hovertemplate=(
        "Temps  au stand: %{x}s<br>"
        "Grand Prix:Espagne<br>"  
        "Ordre du pit stop: %{customdata} arrêt <extra></extra>"  
        ),
        customdata=session_4_data_verstappen['PitOrder'] 
    ))

    # Ajouter la moyenne des pit stops pour Hamilton
    fig.add_trace(go.Scatter(
        x=[df_combined[df_combined['Driver'] == 'HAM']['Duration'].mean()],  # Moyenne des pit stops pour Hamilton
        y=['Hamilton'],
        mode='markers',
        marker=dict(color='black', symbol='line-ns-open' , size=15, line=dict(width=2)),
        name='Moyenne des pit stops<br>avant le Grand prix d\'Espagne',
        legendgroup='moyenne',
        hovertemplate='Temps moyen des pitstops d\'Hamilton en 2021 avant le GP d\'Espagne: %{x}s <extra></extra>',

    ))

    # Ajouter la moyenne des pit stops pour Verstappen
    fig.add_trace(go.Scatter(
        x=[df_combined[df_combined['Driver'] == 'VER']['Duration'].mean()],  # Moyenne des pit stops pour Verstappen
        y=['Verstappen'],
        mode='markers',
        marker=dict(color='black', symbol='line-ns-open' , size=15, line=dict(width=2)),
        legendgroup='moyenne', 
        showlegend=False,  # Masquer la légende pour éviter la duplication
        hovertemplate='Temps moyen des pitstops de Verstappen en 2021 avant le GP d\'Espagne: %{x}s <extra></extra>',  
    ))

    # Mise en forme du graphique
    fig.update_layout(
        title=dict(
        text='<b>Temps de pit stop pour Hamilton et Verstappen</b>',  # Titre en gras avec HTML
        x=0.5,  # Centrage horizontal du titre
        y=0.95,  # Position verticale, ajustable selon le besoin
        xanchor='center',  # Le titre est centré autour de ce point
        font=dict(
            family='sans-serif',  # Famille de police
            size=20,  # Taille de la police
            color='black'  # Couleur de la police
        )
    ),
        xaxis_title='Temps (s)',
        yaxis_title='Pilotes',
        showlegend=True,
        autosize=True,
        # width=1200,  # Largeur en pixels
        # height=600   # Hauteur en pixels
    )

    fig.update_yaxes(
        tickvals=[0, 1],
        ticktext=['Hamilton', 'Verstappen'],
        range=[-0.5, 1.5]  # Vous pouvez ajuster cette plage pour réduire l'espace
    )

    return fig
