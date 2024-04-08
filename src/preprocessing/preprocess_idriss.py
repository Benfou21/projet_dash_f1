import pandas as pd

def get_data(path):
    telemetry_df = pd.read_csv(path)
    return telemetry_df

def preprocess_idriss(ver_csv_path, ham_csv_path):
    ver_df = pd.read_csv(ver_csv_path)
    ham_df = pd.read_csv(ham_csv_path)
    
    # Assurez-vous que la colonne 'Speed' est un float et non un timedelta
    ver_df['Speed'] = ver_df['Speed'].astype(float)
    ham_df['Speed'] = ham_df['Speed'].astype(float)
    
    # Calculer la différence de vitesse
    ver_df['delta_speed'] = ver_df['Speed'] - ham_df['Speed']
    ham_df['delta_speed'] = -ver_df['delta_speed']

    return ver_df, ham_df

# Chemins vers les fichiers CSV
ver_csv_path = "assets/data/telemetry_spain_2021_VER.csv"
ham_csv_path = "assets/data/telemetry_spain_2021_HAM.csv"

# Appeler la fonction avec les chemins des fichiers CSV
ver_df, ham_df = preprocess_idriss(ver_csv_path, ham_csv_path)

# Afficher les DataFrames modifiés
