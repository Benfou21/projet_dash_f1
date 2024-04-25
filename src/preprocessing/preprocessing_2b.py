import sys
import subprocess
import pandas as pd



import fastf1 as f1



import sys
import subprocess
import pandas as pd



import fastf1 as f1



# Fonction pour extraire les données d'arrêts au stand pour une session donnée
def extract_pit_stops(laps_data, session_number, driver_name):
    # On filtre les tours correpondant aux sortie ou entrées de stand
    pit_stops = laps_data.dropna(subset=['PitInTime', 'PitOutTime'], how='all')
    
    pit_stop_durations = []  
    
    for i in range(len(pit_stops)-1):
        # On récupérer les les pairs de ligne correspondant à une entrée de stand et sa sortie
        if pd.notna(pit_stops.iloc[i]['PitInTime']) and pd.notna(pit_stops.iloc[i + 1]['PitOutTime']):
            pit_in_time = pit_stops.iloc[i]['PitInTime']
            pit_out_time = pit_stops.iloc[i + 1]['PitOutTime']
            
            # On calcule la durée du pit stop en faisant la différence
            duration = pit_out_time - pit_in_time
            
            pit_stop_durations.append({
                'SessionNumber': session_number,
                'Driver': driver_name,
                'PitInTime': pit_in_time,
                'PitOutTime': pit_out_time,
                'Duration': duration
            })
            
    # On crée le dataframe contenant nos pit stop, nos temps d'entrée et de sorties, la durée du pit stop
    # le conducteur ayant effectué le pit stop et le grand prix (session)
    return pd.DataFrame(pit_stop_durations)

def savedata():
    # Récupération des données de Verstappen et Hamilton pour le Grand Prix de Bahreïn
    session1 = f1.get_session(2021, 1, 'R')
    session1.load()
    verstappen_laps1 = session1.laps.pick_driver('VER')
    hamilton_laps1 = session1.laps.pick_driver('HAM')


    # Récupération des données de Verstappen et Hamilton pour le Grand Prix d'Émilie-Romagne
    session2 = f1.get_session(2021, 2, 'R')
    session2.load()
    verstappen_laps2 = session2.laps.pick_driver('VER')
    hamilton_laps2 = session2.laps.pick_driver('HAM')

    # Récupération des données de Verstappen et Hamilton pour le Grand Prix du Portugal
    session3 = f1.get_session(2021, 3, 'R')
    session3.load()
    verstappen_laps3 = session3.laps.pick_driver('VER')
    hamilton_laps3 = session3.laps.pick_driver('HAM')

    # Récupération des données de Verstappen et Hamilton pour le Grand Prix d'Espagne
    session4 = f1.get_session(2021, 4, 'R')
    session4.load()
    verstappen_laps4 = session4.laps.pick_driver('VER')
    hamilton_laps4 = session4.laps.pick_driver('HAM')
    
    # Utiliser la fonction de récupération de pitstop pour chaque Grand prix de Verstappen et Hamilton
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

    df_combined.reset_index(drop=True, inplace=True)
    df_combined['Duration'] = df_combined['Duration'].dt.total_seconds()
    df_combined = df_combined[df_combined['Duration'] <= 1000]

    df_combined.to_csv(f"assets/data/pitstops.csv", index=False)


def get_combined_pitstop_data(path):
    df_combined = pd.read_csv(path)
    return df_combined


