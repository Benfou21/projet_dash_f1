import plotly.graph_objects as go
import numpy as np


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.preprocess_idriss import preprocess_idriss
import plotly.express as px
import webcolors  



def get_color_gradient(percentage, color_for_positive, color_for_negative):
    """
    Retourne une couleur sur un gradient en fonction du pourcentage.
    Si le pourcentage est positif, interpole vers color_for_positive,
    si négatif vers color_for_negative.
    """
    if percentage > 0:
        return interpolate_color(color_for_positive, 'white', percentage)
    else:
        return interpolate_color('white', color_for_negative, -percentage)
    
def parse_color(color):
    if color.startswith('rgb'):
        # La couleur est déjà en format RGB, la convertir en array numpy
        return np.array([int(num) for num in color[4:-1].split(',') if num.strip()])
    elif color.startswith('#'):
        # La couleur est en format hexadécimal, la convertir en RGB puis en array numpy
        return np.array(px.colors.hex_to_rgb(color))
    else:
        # La couleur est un nom CSS, obtenir le code hexadécimal puis convertir en RGB
        try:
            hex_color = webcolors.name_to_hex(color)
            return np.array(px.colors.hex_to_rgb(hex_color))
        except ValueError:
            # Si le nom de la couleur n'est pas trouvé, retourner du noir ou une autre couleur par défaut
            return np.array([0, 0, 0])  # Noir par défaut

# Utilitaire pour interpoler entre deux couleurs
def interpolate_color(color1, color2, factor: float):
    """
    Interpole entre deux couleurs.
    Factor = 0 -> color1, factor = 1 -> color2.
    """
    color1_rgb = parse_color(color1)
    color2_rgb = parse_color(color2)

    # Interpolation linéaire entre les deux couleurs
    new_color_rgb = (1 - factor) * color1_rgb + factor * color2_rgb

    # Convertir le résultat en chaîne RGB pour Plotly
    return f'rgb({int(new_color_rgb[0])}, {int(new_color_rgb[1])}, {int(new_color_rgb[2])})'


# Fonction principale pour créer le graphique
def graph_idriss(ver_csv_path, ham_csv_path):
    ver_df, ham_df = preprocess_idriss(ver_csv_path, ham_csv_path)
    max_delta = max(abs(ver_df['delta_speed'].min()), ver_df['delta_speed'].max())

    fig = go.Figure()

    for i in range(len(ver_df) - 1):
        delta_speed = ver_df['delta_speed'].iloc[i]
        delta_speed_normalized = delta_speed / max_delta
        color = get_color_based_on_speed(delta_speed_normalized)

        
        if delta_speed > 0:
                faster_pilot = "Plus rapide: Max Verstappen"
        else:
            faster_pilot = "Plus rapide: Lewis Hamilton"
    
        hovertemplate = f"<b>Vitesse Delta: {delta_speed:.2f} m/s </b><br>" \
                    f"<b>{faster_pilot}</b><br>" \
                    "<extra></extra>"  # Supprime les informations supplémentaires par défaut

        fig.add_trace(go.Scatter(
            x=ver_df['X'].iloc[i:i+2],
            y=ver_df['Y'].iloc[i:i+2],
            mode='lines',
            line=dict(color=color, width=6),
            hoverinfo='all',
            hovertemplate=hovertemplate,
            showlegend=False
        ))
        
        

    # Mise à jour du layout
    fig.update_layout(
        title=dict(
            text=f'<b>Vitesse relative de Max Vertsappen en coparaison avec Lewis Hamilton</b>',
            x=0.5,  # Centrage horizontal du titre
            font=dict(
                family='sans-serif',  # Famille de police
                size=20,  # Taille de la police
                color='black'  # Couleur de la police
                )
        ),
        
        legend_title='Légende',
        showlegend=True,
        plot_bgcolor='white',  # Définir le fond à blanc
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(l=0, r=0, t=40, b=0),  # Margin top pour le titre
        autosize=True,
        
    )
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='lines',
        name='Lewis plus rapide (rouge)',
        line=dict(color='red', width=10)
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='lines',
        name='Vitesse égale (jaune)',
        line=dict(color='yellow', width=10)
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='lines',
        name='Max plus rapide (vert)',
        line=dict(color='green', width=10)
    ))

    # Mise à jour de la mise en page pour afficher la légende
    fig.update_layout(  
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        font=dict(
                family='sans-serif',
                size=15,
                color='black'
            ),
    )
    return fig

# Fonction pour obtenir une couleur basée sur la vitesse
def get_color_based_on_speed(normalized_speed):
    # Ici vous pouvez créer un gradient de couleurs personnalisé
    
    if normalized_speed == 0:
        return f"hsl(60, 100%, {50}%)"
    if normalized_speed < 0:
        # Pour les vitesses plus lentes que la moyenne, du rouge au blanc
        return get_color_with_hue(0,-normalized_speed)
    else:
        return get_color_with_hue(120,normalized_speed)
    #     return px.colors.sample_colorscale(px.colors.diverging.RdYlGn, -normalized_speed)[0]
    # else:
    #     # Pour les vitesses plus rapides que la moyenne, du blanc au vert
    #     return px.colors.sample_colorscale(px.colors.diverging.RdYlGn, normalized_speed)[0]


def get_color_with_hue(hue,normalized_speed):
    
    saturation = 50 + 50 * normalized_speed  
   
    return f"hsl({hue}, {saturation}%, {50}%)"
