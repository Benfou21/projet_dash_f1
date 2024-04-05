import fastf1 as f1
import numpy as np
import pandas as pd



#Permet de ne pas à avoir re downlaod les données 
# f1.Cache.enable_cache('./cache')  # replace with your cache directory





def load_and_save_telemetry_race_pilote(year, pilote):
    # Chargement de la session de qualification pour Monza de l'année donnée
    session = f1.get_session(year, 'Spain', 'Q')
    session.load()
    
    # Chargement de la session de course pour obtenir les données de tour
    race_session = f1.get_session(year, 'Spain', 'R')
    race_session.load(telemetry=True)
    
    # Obtenir les données du tour le plus rapide pour le pilote en position de pole
    fastest_lap = race_session.laps.pick_driver(pilote).pick_fastest()
    
    # Extraire les données de télémétrie
    telemetry = fastest_lap.get_telemetry()
    telemetry['Speed_m_s'] = telemetry['Speed'] / 3.6  # Convertir la vitesse en m/s
    telemetry['Elapsed'] = telemetry['Time'].dt.total_seconds()
    
    # Calculer la distance pour chaque point de télémétrie
    telemetry['Distance'] = telemetry['Speed_m_s'] * telemetry['Time'].diff().dt.total_seconds().fillna(0).cumsum()
    
    # Ajout de l'année et du pilote comme colonnes constantes pour chaque ligne
    telemetry['Year'] = year
    telemetry['Pilote'] = pilote

    # Sauvegarde du DataFrame en CSV
    telemetry.to_csv(f"assets/data/telemetry_spain_{year}_{pilote}.csv", index=False)
    
    return telemetry

# load_and_save_telemetry_race_pilote(2021,'HAM')
# load_and_save_telemetry_race_pilote(2021,'VER')



def resample_based_on_speed(x, y, speed):
    # Pseudo-code pour illustrer le concept
    new_x, new_y, new_speed = [], [], []
    for i in range(len(x) - 1):
        distance = np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2)
        num_points = int(max(1, distance / np.mean(speed[i:i+2])) )   # Plus de points si la vitesse moyenne est faible
        
        for j in range(num_points):
            new_x.append(np.linspace(x[i], x[i+1], num_points+1)[j])
            new_y.append(np.linspace(y[i], y[i+1], num_points+1)[j])
            new_speed.append(np.linspace(speed[i], speed[i+1], num_points+1)[j])
    return new_x, new_y, new_speed


def resample_based_on_time(x, y, speed,time):
    new_x, new_y, new_speed = [], [], []
    for i in range(len(x) - 1):

        # Calcul du temps écoulé entre les deux points
        time_elapsed = time[i+1] - time[i]
        # Détermination du nombre de points basé sur le temps écoulé
        num_points = int(max(1, time_elapsed * 0.2))  # Multiplier par un facteur pour ajuster la densité des points
        
        # Génération des points intermédiaires
        for j in range(num_points):
            new_x.append(np.linspace(x[i], x[i+1], num_points+1)[j])
            new_y.append(np.linspace(y[i], y[i+1], num_points+1)[j])
            new_speed.append(np.linspace(speed[i], speed[i+1], num_points+1)[j])
            

    return new_x, new_y, new_speed

def get_data(path):
    
    df = pd.read_csv(path)
    
    return df


def get_max_speed(speed1,speed2):
    max1 = max(speed1)
    max2 = max(speed2)
    if max1 < max2:
        return max2
    else :
        return max1