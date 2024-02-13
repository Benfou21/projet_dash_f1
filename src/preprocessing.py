import fastf1 as f1
import numpy as np
import pandas as pd



f1.Cache.enable_cache('./cache')  # replace with your cache directory


def load_and_save_telemetry() :
    
    # Initialize a dictionary to hold your data
    telemetry_data = {
        'year': [],
        'x': [],
        'y': [],
        'speed': [],
        'time': [],
        'distance': []
    }

    for year in range(2018, 2024):  # range of years
        # Load the qualifying session for Monza of the given year
        session = f1.get_session(year, 'Monza', 'Q')
        session.load()
        
        # Get the pole position driver
        pole_position_driver = session.results.iloc[0]['DriverNumber']
        
        # Load the race session to get lap data
        race_session = f1.get_session(year, 'Monza', 'R')
        race_session.load(telemetry=True)
        
        # Get the fastest lap data for the pole position driver
        fastest_lap = race_session.laps.pick_driver(pole_position_driver).pick_fastest()
        
        # Extract telemetry data
        telemetry = fastest_lap.get_telemetry()
        telemetry['Speed_m_s'] = telemetry['Speed'] / 3.6  # Convert speed to m/s
        telemetry['Elapsed'] = telemetry['Time'].cumsum()
        # Calculate the distance for each telemetry point
        telemetry['Distance'] = telemetry['Speed_m_s'] * telemetry['Time'].diff().dt.total_seconds().fillna(0).cumsum()
        
        # Store telemetry data
        telemetry_data['year'].append(year)
        telemetry_data['x'].append(telemetry['X'].tolist())
        telemetry_data['y'].append(telemetry['Y'].tolist())
        telemetry_data['speed'].append(telemetry['Speed'].tolist())
        telemetry_data['distance'].append(telemetry['Distance'].tolist())
        telemetry_data['time'].append(telemetry['Elapsed'].dt.total_seconds().tolist())  # Store elapsed time in seconds
    
    telemetry_df = pd.DataFrame(telemetry_data)
    telemetry_df.to_csv("src/assets/data/telemetry.csv")
    return telemetry_df


print(load_and_save_telemetry())
