import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd


def get_figure(data):
    
    # fig = go.Figure()
    fig = make_subplots(rows=1, cols=1)
    x = data['x']
    y = data['y']
    speed = data['speed']
    
    # Add the trace of the circuit
    # fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Track'))
    
    
    
    speed_normalized = (speed - min(speed)) / (max(speed) - min(speed))
    color_scale = [(v, f"rgb({int(255 * v)}, {int(255 * (1 - v))}, 0)") for v in speed_normalized]

    for i in range(len(x) - 1):
        fig.add_trace(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=color_scale[i][1], width=2),
            showlegend=False))

    
    fig.add_trace(
        go.Scatter(x=[x[0]], y=[y[0]], mode='markers', marker=dict(size=10, color='red'), name='Car'),
        row=1, col=1
    )
    
    
    # Set up the layout of the figure
    fig.update_layout(
        title='F1 Telemetry Data Animation',
        showlegend=False,
        xaxis=dict(range=[min(x), max(x)], autorange=False),
        yaxis=dict(range=[min(y), max(y)], autorange=False)
    )
    
    frames = [go.Frame(
        data=[
            go.Scatter(x=x, y=y, mode='lines', name='Track'),  # include the track in each frame
            go.Scatter(x=[x[k]], y=[y[k]], mode='markers', marker=dict(size=10, color='red'))  # car's position
        ],
        name=str(k)
    ) for k in range(len(x))]


    fig.frames = frames
    
    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True, mode='immediate')]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')]
                    )
                ],
                direction='left',
                pad={'r': 10, 't': 87},
                showactive=False,
                x=0.1,
                xanchor='right',
                y=0,
                yanchor='top'
            )
        ]
    )
    
    
    
    return fig

