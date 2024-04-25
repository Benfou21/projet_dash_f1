import pandas as pd

def get_data(path):
    telemetry_df = pd.read_csv(path)
    return telemetry_df

def preprocess_idriss(ver_csv_path, ham_csv_path):
    ver_df = pd.read_csv(ver_csv_path)
    ham_df = pd.read_csv(ham_csv_path)
    
    ver_df['Speed'] = ver_df['Speed'].astype(float)
    ham_df['Speed'] = ham_df['Speed'].astype(float)
    
    # Calculer la différence de vitesse
    ver_df['delta_speed'] = ver_df['Speed'] - ham_df['Speed']
    ham_df['delta_speed'] = -ver_df['delta_speed']

    return ver_df, ham_df


import os
path_max = os.path.join("src","assets", "data", "telemetry_spain_2021_VER.csv")
path_ham = os.path.join("src","assets", "data", "telemetry_spain_2021_HAM.csv")

ver_df, ham_df = preprocess_idriss(path_max, path_ham)


