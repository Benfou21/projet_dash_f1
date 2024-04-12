import plotly.graph_objs as go
from preprocessing.preprocessing_2 import preprocess_data

def create_scatter_plot(reference_pilot, ver_csv_path, ham_csv_path):
    # Charger les données et préparer le DataFrame
    ver_df, ham_df = preprocess_data(ver_csv_path, ham_csv_path)

    # Définition des couleurs pour chaque type de pneu
    color_map = {'SOFT': 'red', 'MEDIUM': 'blue', 'HARD': 'green'}

    # Sélection du DataFrame en fonction du pilote de référence
    df_to_plot = ver_df if reference_pilot == 'VER' else ham_df
    delta_column = f'delta_{reference_pilot.lower()}_seconds'

    # Initialisation de la figure Plotly
    fig = go.Figure()

    plotted_compounds = set()

    # Ajout des lignes pour chaque segment de pneu et pour les pit stops
    for (compound, segment), segment_df in df_to_plot.groupby(['Compound', 'Segment']):
        show_legend = compound not in plotted_compounds
        color = color_map.get(compound, 'black')

        # Ajout de la trace pour le segment actuel
        fig.add_trace(go.Scatter(
            x=segment_df['LapNumber'], 
            y=segment_df[delta_column],
            mode='lines+markers',
            name=compound if show_legend else None,
            line=dict(color=color, width=2),
            marker=dict(color=color, size=8, line=dict(width=1)),
            showlegend=show_legend,
            hovertemplate=(
                "Tour: %{x}<br>"
                f"Pilote: {reference_pilot}<br>"
                "Delta Temps: %{y:.2f} s<br>"
                f"Type de Pneu: {compound}<extra></extra>"
            )
        ))
        
        # Ajouter une ligne verticale pour les pit stops
        pit_stop_laps = segment_df[segment_df['Pit_stop']].index
        for idx in pit_stop_laps:
            lap_number = segment_df.loc[idx, 'LapNumber']
            fig.add_vline(
                x=lap_number,
                line=dict(color="black", width=2, dash="dash"),
                annotation_text="Pit Stop",
                annotation_position="bottom right"
            )

        plotted_compounds.add(compound)

    # Mise à jour des plages pour l'axe x et les autres personnalisations du graphique
    fig.update_xaxes(range=[0, 70])
    max_delta = df_to_plot[delta_column].max() + 1
    min_delta = df_to_plot[delta_column].min() - 1

    # Ajout d'arrière-plans colorés pour les valeurs de delta positives et négatives
    fig.add_shape(type="rect", x0=0, y0=0, x1=70, y1=max_delta,
                  line=dict(width=0), fillcolor="green", opacity=0.2, layer="below")
    fig.add_shape(type="rect", x0=0, y0=min_delta, x1=70, y1=0,
                  line=dict(width=0), fillcolor="red", opacity=0.2, layer="below")

    # Personnalisation de la mise en page du graphique
    fig.update_layout(
        title_text=f"Différences de temps au tour par rapport à {reference_pilot}",
        title_x=0.5,  # Centrer le titre
        title_font_size=24,
        legend_title_text='Pneus',
        legend_title_side='top',
        plot_bgcolor='white',  # Fond blanc
        xaxis=dict(
            title='Numéro du Tour',
            title_font_size=18,
            tickfont_size=14,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title='Delta Temps (s)',
            title_standoff=10,
            title_font_size=18,
            tickfont_size=14,
            gridcolor='lightgrey'
        ),
        legend=dict(
            title_font_size=16,
            font_size=14,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='lightgrey',
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        height=800,
        autosize=True
    )

    return fig
