import pandas as pd
import plotly.graph_objects as go
import numpy as np
from hover_template import hover_template_1_classement


def get_evol_classement(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['GP'],
        y=df['Cumul Hamilton'],
        name='Hamilton',
        mode='markers',
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
        mode='markers',
        marker=dict(color='#0600EF'),
        customdata = np.stack((df['Grand Prix'],df['Date'],df['Circuit'],df['Vainqueur'],df['Pole Position'],
                            df['Position Hamilton'],df['Position Verstappen'],df['Points Hamilton'],df['Points Verstappen'],
                            df['Cumul Hamilton'],df['Cumul Verstappen'],df['Classement Hamilton'],df['Classement Verstappen'])
                            ,axis=-1),
        hovertemplate=hover_template_1_classement.get_classement_hover_template('Verstappen')
    ))

    fig.update_layout(
        title='Évolution des points au classement du championnat du monde de F1<br><sup>Lewis Hamilton (Mercedes) et Max Verstappen (Red Bull)</sup>',
        xaxis_title='Grand Prix',
        yaxis_title='Points',
        legend_title='Pilotes'
    )

    return fig