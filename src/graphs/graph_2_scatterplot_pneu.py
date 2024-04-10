import plotly.graph_objs as go


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.preprocessing_2 import preprocess_data

def create_scatter_plot(reference_pilot, ver_csv_path, ham_csv_path):
    # Charger les données des CSV dans des DataFrames et ajouter les segments
    ver_df, ham_df = preprocess_data(ver_csv_path, ham_csv_path)

    # Définition d'un dictionnaire pour la correspondance des couleurs
    color_map = {
        'SOFT': 'red',
        'MEDIUM': 'blue',
        'HARD': 'green'
        # Ajoutez d'autres correspondances de couleurs si nécessaire
    }

    # Sélectionner le DataFrame en fonction du pilote de référence
    df_to_plot = ver_df if reference_pilot == 'VER' else ham_df
    delta_column = 'delta_' + reference_pilot.lower() + '_seconds'

    # Initialiser la figure
    fig = go.Figure()

    # Un ensemble pour suivre les composés déjà tracés (pour la légende)
    plotted_compounds = set()
    
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color="black", width=1, dash="dot"),
        name='Pit Stop 1'
         ))


    # Un dictionnaire pour garder une trace des numéros de pit stop pour chaque compound
    pit_stop_counts = {}

    # Traiter et tracer une ligne pour chaque segment de chaque compound
    for (compound, segment), segment_df in df_to_plot.groupby(['Compound', 'Segment']):
        show_legend = compound not in plotted_compounds
        color = color_map.get(compound, 'black')  # Utiliser 'black' si le compound n'est pas dans le dictionnaire

        
        hovertemplate = (
            "Tour: %{x}<br>" +
            f"Pilote: {reference_pilot}<br>" +
            "Delta Temps: %{y:.2f} s<br>" +
            f"Type de Pneu: {compound}<br>" +
            "<extra></extra>"  # Cela empêche l'affichage du nom de la trace supplémentaire
            )
        
        fig.add_trace(go.Scatter(
            x=segment_df['LapNumber'], y=segment_df[delta_column],
            mode='lines+markers',
            name=f'{compound}',
            line=dict(color=color, width=2),
            marker=dict(color=color, size=8, line=dict(width=1)),
            showlegend=show_legend,
            hoverinfo='all',
            hovertemplate=hovertemplate
        ))
        
        
        plotted_compounds.add(compound)
        
        
        # Ajouter une démarcation pour les pit stops
        if segment > 1:
            pit_stop_lap = segment_df['LapNumber'].iloc[0]
            pit_stop_counts[compound] = pit_stop_counts.get(compound, 0) + 1                
            pit_stop_number = pit_stop_counts[compound]

            fig.add_vline(
                x=pit_stop_lap,
                line=dict(color="black", width=1, dash="dot"),
                annotation_text=f"Pit Stop {pit_stop_number}",  # Ajoute le numéro du pit stop
                annotation_position="top left",
            )
            
            if pit_stop_number == 2:  # Vous pouvez étendre cette logique pour plus de pit stops si nécessaire
                fig.add_trace(go.Scatter(
                    x=[None],
                    y=[None],
                    mode='lines',
                    line=dict(color="black", width=1, dash="dot"),
                    name=f'Pit Stop {pit_stop_number}'
                ))


    # Définir la plage de l'axe des abscisses
    fig.update_xaxes(range=[0, 70])
    lim = max(df_to_plot[delta_column]+1)
    lim2 = -lim
    # Ajouter un arrière-plan coloré pour les valeurs positives et négatives
    fig.add_shape(
        # Rectangle coloré pour les valeurs positives
        type="rect",
        x0=0, y0 = 0 , x1=70, y1=(lim+1),  # y1 dépend de vos données
        line=dict(width=0),
        fillcolor="green",  # Choisir une couleur pour la zone positive
        opacity=0.2,  # Choisir un niveau d'opacité
        layer="below"
    )
    fig.add_shape(
        # Rectangle coloré pour les valeurs négatives
        type="rect",
        x0=0, y0=min(df_to_plot[delta_column]-1), x1=70, y1=0,  # y0 dépend de vos données
        line=dict(width=0),
        fillcolor="red",  # Choisir une couleur pour la zone négative
        opacity=0.2,  # Choisir un niveau d'opacité
        layer="below"
    )



    # Personnaliser davantage le graphique si nécessaire
    fig.update_layout(
    title_text=f"Différences de temps au tour par rapport à {reference_pilot}",
    title_x=0.5,  # Centrer le titre
    title_font_size=24,
    legend_title_text='Pneus',
    legend_title_side='top',
    plot_bgcolor='white',  # Fond blanc pour une apparence plus propre
    xaxis=dict(
        title='Numéro du Tour',
        title_font_size=18,
        tickfont_size=14,
        showgrid=False,  # Cacher la grille pour moins de clutter
        zeroline=False,  # Cacher la ligne zéro
    ),
    yaxis=dict(
        title='Delta Temps (s)',
        title_standoff=10,
        title_font_size=18,
        tickfont_size=14,
        gridcolor='lightgrey',  # Couleur légère pour la grille
    ),
    legend=dict(
        title_font_size=16,
        font_size=14,
        bgcolor='rgba(255,255,255,0.8)',  # Fond légèrement transparent pour la légende
        bordercolor='lightgrey',
        borderwidth=1
    ),
    margin=dict(l=40, r=40, t=60, b=40),  # Marges autour du graphique
    autosize=False, width=1400, height=800
)

    # Retourner la figure prête pour l'affichage
    return fig

