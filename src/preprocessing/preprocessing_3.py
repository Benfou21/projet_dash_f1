import fastf1 as f1
import numpy as np
import pandas as pd





def load_and_save_telemetry_race_pilote(year, pilote):
    # Chargement de la session de qualification 
    session = f1.get_session(year, 'Spain', 'Q')
    session.load()
    
    # Chargement de la session de course 
    race_session = f1.get_session(year, 'Spain', 'R')
    race_session.load(telemetry=True)
    
    # On récupère les données du tour le plus rapide pour le pilote en pole position 
    fastest_lap = race_session.laps.pick_driver(pilote).pick_fastest()
    
    # On extrait les données de télémétrie
    telemetry = fastest_lap.get_telemetry()
    telemetry['Speed_m_s'] = telemetry['Speed'] / 3.6  # Convertir la vitesse en m/s
    telemetry['Elapsed'] = telemetry['Time'].dt.total_seconds()
    
    # On calcule la distance pour chaque point de télémétrie
    telemetry['Distance'] = telemetry['Speed_m_s'] * telemetry['Time'].diff().dt.total_seconds().fillna(0).cumsum()
    
    telemetry['Year'] = year
    telemetry['Pilote'] = pilote

    telemetry.to_csv(f"assets/data/telemetry_spain_{year}_{pilote}.csv", index=False)
    
    return telemetry



def get_data(path):
    
    telemetry_df = pd.read_csv(path)
    
    return telemetry_df


def get_max_speed(speed1,speed2):
    max1 = max(speed1)
    max2 = max(speed2)
    if max1 < max2:
        return max2
    else :
        return max1
