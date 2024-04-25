import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hover_template import hover_template_1_classement


def get_evol_classement(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['GP'],
        y=df['Cumul Hamilton'],
        name='Hamilton',
        mode='lines+markers',
        marker=dict(color='#00D2BE'),
        customdata = np.stack((df['Grand Prix'],df['Date'],df['Circuit'],df['Vainqueur'],df['Pole Position'],
                            df['Position Hamilton'],df['Position Verstappen'],df['Points Hamilton'],df['Points Verstappen'],
                            df['Cumul Hamilton'],df['Cumul Verstappen'],df['Classement Hamilton'],df['Classement Verstappen'])
                            ,axis=-1),
        hovertemplate=hover_template_1_classement.get_classement_hover_template('Hamilton')
    ))


    fig.add_trace(go.Scatter(
        x=df['GP'],
        y=df['Cumul Verstappen'],
        name='Verstappen',
        mode='lines+markers',
        marker=dict(color='#0600EF', symbol="diamond"),
        customdata = np.stack((df['Grand Prix'],df['Date'],df['Circuit'],df['Vainqueur'],df['Pole Position'],
                            df['Position Hamilton'],df['Position Verstappen'],df['Points Hamilton'],df['Points Verstappen'],
                            df['Cumul Hamilton'],df['Cumul Verstappen'],df['Classement Hamilton'],df['Classement Verstappen'])
                            ,axis=-1),
        hovertemplate=hover_template_1_classement.get_classement_hover_template('Verstappen')
    ))

    fig.update_layout(
        title='Évolution des points au classement du championnat du monde de F1 2021<br><sup>Lewis Hamilton (Mercedes) et Max Verstappen (Red Bull)</sup>',
        xaxis_title='Grand Prix',
        yaxis_title='Points',
        legend_title='Pilotes',    
    )
    fig.update_layout(
        legend=dict(
            font=dict(
                family='sans-serif',
                size=15,
                color='black'
            ),
        ),
        title=dict(
            font=dict(
                family='sans-serif',
                size=20,
                color='black'
            ),
        )
    )
    # Ajout de la ligne de highlight pour le gp d'espagne étudié
    fig.add_vline(x=3, line_width=3,
                  line_dash="dash", line_color="red",
                  annotation_text="Grand Prix<br>d'Espagne",
                  annotation_position="top right",
                  annotation=dict(font_size=20, font_family="Times New Roman")
                  )

    return fig