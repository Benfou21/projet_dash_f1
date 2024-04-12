import fastf1 as f1
import numpy as np
import pandas as pd


import fastf1
import fastf1.plotting


#Permet de ne pas à avoir re downlaod les données 
# f1.Cache.enable_cache('../cache')  # replace with your cache directory



def load_and_save_driver_laps_race_pilote(year, pilote):
    # Chargement de la session de qualification pour Monza de l'année donnée
    session = f1.get_session(year, 'Spain', 'Q')
    session.load()
    
    # Chargement de la session de course pour obtenir les données de tour
    race_session = f1.get_session(year, 'Spain', 'R')
    race_session.load(telemetry=True)
    
    # Obtenir les données du tour le plus rapide pour le pilote en position de pole
    driver_laps = race_session.laps.pick_driver(pilote).pick_quicklaps().reset_index()
    

    # Sauvegarde du DataFrame en CSV
    driver_laps.to_csv(f"../assets/data/driver_laps_{year}_{pilote}.csv", index=False)
    
    return driver_laps

#load_and_save_driver_laps_race_pilote(2021,'HAM')
#load_and_save_driver_laps_race_pilote(2021,'VER')

import os
def add_delta_columns(ver_csv_path, ham_csv_path):
    # Charger les données des CSV dans des DataFrames
    
    # ver_df = pd.read_csv(ver_csv_path)
    # ham_df = pd.read_csv(ham_csv_path)

    ver_df = remplir_lignes_manquantes(ver_csv_path)
    
    ham_df = remplir_lignes_manquantes(ham_csv_path)
    
    
    # print(ver_df[["LapNumber"]])

    # Convertir les temps au tour en timedelta
    ver_df['LapTime'] = pd.to_timedelta(ver_df['LapTime'])
    ham_df['LapTime'] = pd.to_timedelta(ham_df['LapTime'])
    
    
    # Calculer les différences de temps entre VER et HAM
    delta_ver = ver_df['LapTime'] - ham_df['LapTime']
    delta_ham = ham_df['LapTime'] - ver_df['LapTime']

    # Convertir les deltas en secondes pour une analyse plus facile
    ver_df['delta_ver_seconds'] = delta_ver.dt.total_seconds()
    ham_df['delta_ham_seconds'] = delta_ham.dt.total_seconds()

    return ver_df, ham_df

def add_segments(df):
    # Assurez-vous que 'LapNumber' et 'Compound' sont des colonnes dans votre DataFrame
    if 'LapNumber' not in df or 'Compound' not in df:
        raise ValueError("Les données requises 'LapNumber' ou 'Compound' sont manquantes dans le DataFrame.")
    
    # Trier le DataFrame par LapNumber pour s'assurer que les données sont dans l'ordre
    df = df.sort_values(by='LapNumber')

    # Ajouter une colonne 'Segment' qui s'incrémente à chaque changement de compound
    df['Segment'] = (df['Compound'] != df['Compound'].shift(1)).cumsum()

    return df

def preprocess_data(ver_csv_path, ham_csv_path):
    
    # Ajoutez ici d'autres traitements si nécessaire
    ver_df, ham_df = add_delta_columns(ver_csv_path, ham_csv_path)
    
    #pour debug
    # print(ver_df[["LapNumber"]])
    
    
    # Assurez-vous que les colonnes nécessaires sont présentes
    if 'Compound' not in ver_df or 'LapNumber' not in ver_df:
        raise ValueError("Les données requises sont manquantes dans ver_df")
    if 'Compound' not in ham_df or 'LapNumber' not in ham_df:
        raise ValueError("Les données requises sont manquantes dans ham_df")

    # Appel de la fonction add_segments
    ver_df = add_segments(ver_df)
    ham_df = add_segments(ham_df)
    ham_df['Compound'][41] = 'MEDIUM'
    ham_df['Segment'][40:-1] = 2
    ham_df = ham_df.drop(ham_df.index[-1])
    ver_df['Pit_stop'] = False
    ham_df['Pit_stop'] = False
    ver_df.loc[ver_df['LapNumber'].isin([26, 61]), 'Pit_stop'] = True
    ham_df.loc[ham_df['LapNumber'].isin([30, 42]), 'Pit_stop'] = True

    # ver_df['Pit_stop'][26] = True
    # ver_df['Pit_stop'][60] = True
    # ham_df['Pit_stop'][30] = True
    # ham_df['Pit_stop'][42] = True


    # # Encore une fois, imprimez les tours manquants pour vérifier
    print(ver_df[ver_df['LapNumber'] == 26])
    print(ham_df[ham_df['LapNumber'] == 42])
    
    return ver_df, ham_df

def remplir_lignes_manquantes(fichier_csv):
    # Charger le fichier CSV
    df = pd.read_csv(fichier_csv)
    
    # Convertir 'LapNumber' en int si nécessaire
    df['LapNumber'] = df['LapNumber'].astype(int)
    
    # Trouver les numéros de tour manquants
    tous_les_tours = range(1, int(df['LapNumber'].max()) + 1)
    tours_manquants = set(tous_les_tours) - set(df['LapNumber'])
    
    # Tri préalable du DataFrame par 'LapNumber' pour éviter des problèmes lors de l'utilisation de iloc
    df.sort_values('LapNumber', inplace=True)
    
    # Pour chaque tour manquant, ajouter une ligne avec les infos du tour précédent
    for tour in sorted(tours_manquants):
        # Trouver l'index du dernier tour avant le tour manquant
        index_du_dernier = df[df['LapNumber'] < tour].index.max()
        # S'assurer qu'il existe un tour précédent
        if pd.isna(index_du_dernier):
            print(f"Aucun tour précédent trouvé pour le tour {tour}.")
            continue
        ligne_precedente = df.loc[index_du_dernier].copy()
        ligne_precedente['LapNumber'] = tour
        df = pd.concat([df, ligne_precedente.to_frame().T], ignore_index=True)
    
    # Trier le DataFrame par 'LapNumber' après l'ajout
    df.sort_values('LapNumber', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # print(df['LapNumber'].head(11))
    
    return df




# path_scatter_max = os.path.join("src","assets", "data", "driver_laps_2021_VER.csv")
# # Utiliser la fonction
# df_modifie = remplir_lignes_manquantes(path_scatter_max)

# import os
# # Chemins vers les fichiers CSV
# ver_csv_path = os.path.join("src","assets", "data", "driver_laps_2021_VER.csv")
# ham_csv_path = os.path.join("src","assets", "data", "driver_laps_2021_HAM.csv")


# ver_df = pd.read_csv(ver_csv_path)
# ham_df = pd.read_csv(ham_csv_path)

# # Par exemple, si vous savez que le tour 5 est manquant, vérifiez:
# print(ver_df[ver_df['LapNumber'] == 24])
# print(ham_df[ham_df['LapNumber'] == 24])


# Appeler la fonction avec les chemins des fichiers CSV
#ver_df, ham_df = add_delta_columns(ver_csv_path, ham_csv_path)

# Afficher les DataFrames modifiés
