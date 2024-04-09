import sys
import subprocess
import pandas as pd


# subprocess.check_call([sys.executable, "-m", "pip", "install", "fastf1"])

import fastf1 as f1


# Activer le mode cache pour accélérer le chargement des données
# f1.Cache.enable_cache('projet_dash_f1\src\preprocessing\__pycache__') 

import sys
import subprocess
import pandas as pd



import fastf1 as f1


# Activer le mode cache pour accélérer le chargement des données
# f1.Cache.enable_cache('projet_dash_f1\src\preprocessing\__pycache__') 




#Colone: ['Time', 'Driver', 'DriverNumber', 'LapTime', 'LapNumber', 'Stint',
#        'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
#        'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime',
#        'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'IsPersonalBest',
#        'Compound', 'TyreLife', 'FreshTyre', 'Team', 'LapStartTime',
#        'LapStartDate', 'TrackStatus', 'Position', 'Deleted', 'DeletedReason',
#        'FastF1Generated', 'IsAccurate']

# Fonction pour extraire les données d'arrêts au stand pour une session donnée
def extract_pit_stops(laps_data, session_number, driver_name):
    # Filtrer les tours avec des données de PitIn ou PitOut
    pit_stops = laps_data.dropna(subset=['PitInTime', 'PitOutTime'], how='all')
    
    pit_stop_durations = []  # Liste pour stocker les informations sur les pit stops
    
    for i in range(len(pit_stops)-1):
        # Trouver les paires PitIn et PitOut consécutives
        if pd.notna(pit_stops.iloc[i]['PitInTime']) and pd.notna(pit_stops.iloc[i + 1]['PitOutTime']):
            pit_in_time = pit_stops.iloc[i]['PitInTime']
            pit_out_time = pit_stops.iloc[i + 1]['PitOutTime']
            
            # Calculer la durée du pit stop
            duration = pit_out_time - pit_in_time
            
            # Ajouter les informations au résultat
            pit_stop_durations.append({
                'SessionNumber': session_number,
                'Driver': driver_name,
                'PitInTime': pit_in_time,
                'PitOutTime': pit_out_time,
                'Duration': duration
            })
            
    # Créer un DataFrame à partir de la liste des informations
    return pd.DataFrame(pit_stop_durations)

def savedata():
    # SESSION 1 
    session1 = f1.get_session(2021, 1, 'R')
    session1.load()
    verstappen_laps1 = session1.laps.pick_driver('VER')
    hamilton_laps1 = session1.laps.pick_driver('HAM')


    # SESSION 2
    session2 = f1.get_session(2021, 2, 'R')
    session2.load()
    verstappen_laps2 = session2.laps.pick_driver('VER')
    hamilton_laps2 = session2.laps.pick_driver('HAM')

    # SESSION 3
    session3 = f1.get_session(2021, 3, 'R')
    session3.load()
    verstappen_laps3 = session3.laps.pick_driver('VER')
    hamilton_laps3 = session3.laps.pick_driver('HAM')

    # SESSION 4
    session4 = f1.get_session(2021, 4, 'R')
    session4.load()
    verstappen_laps4 = session4.laps.pick_driver('VER')
    hamilton_laps4 = session4.laps.pick_driver('HAM')
    
    # Utiliser la fonction pour chaque session de Verstappen et Hamilton
    df_session1_verstappen = extract_pit_stops(verstappen_laps1, 1, 'VER')
    df_session1_hamilton = extract_pit_stops(hamilton_laps1, 1, 'HAM')

    df_session2_verstappen = extract_pit_stops(verstappen_laps2, 2, 'VER')
    df_session2_hamilton = extract_pit_stops(hamilton_laps2, 2, 'HAM')

    df_session3_verstappen = extract_pit_stops(verstappen_laps3, 3, 'VER')
    df_session3_hamilton = extract_pit_stops(hamilton_laps3, 3, 'HAM')

    df_session4_verstappen = extract_pit_stops(verstappen_laps4, 4, 'VER')
    df_session4_hamilton = extract_pit_stops(hamilton_laps4, 4, 'HAM')

    # Combiner les DataFrames en un seul
    df_combined = pd.concat([df_session1_verstappen, df_session1_hamilton,
                            df_session2_verstappen, df_session2_hamilton,
                            df_session3_verstappen, df_session3_hamilton,
                            df_session4_verstappen, df_session4_hamilton])

    # Réinitialiser l'index du DataFrame combiné, si nécessaire
    df_combined.reset_index(drop=True, inplace=True)

    # Remplacer la colonne 'Duration' par sa valeur en secondes
    df_combined['Duration'] = df_combined['Duration'].dt.total_seconds()

    # Supprimer les lignes avec une durée de pit stop supérieure à 1000
    df_combined = df_combined[df_combined['Duration'] <= 1000]

    # Save le dataset
    df_combined.to_csv(f"assets/data/pitstops.csv", index=False)


def get_combined_pitstop_data(path):
    df_combined = pd.read_csv(path)
    return df_combined


