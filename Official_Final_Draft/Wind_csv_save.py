import os
import requests
import pandas as pd
import numpy as np
import time
import config
from datetime import datetime


# Cache dictionary to hold previously fetched results


def wind_function_main(self, latitude, longitude, turbine_name_user, turbine_capacity_user, rotor_diameter_user, turbine_efficiency_user):
    # Check if latitude and longitude are valid
    
    if not (isinstance(latitude, (int, float)) and isinstance(longitude, (int, float))):
        raise ValueError("Latitude and longitude must be numeric.")


    # Definitions for API key
    lon = longitude
    lat = latitude

    wind_data_type = "windspeed_100m"
    year = 2023
    user_email = "malakaicrane@gmail.com"
    api_key = "YT5auN6kF3hMbh7c1bQeyKCZYssN2DH0sv3zmZpG"

    turbine_name = turbine_name_user
    turbine_capacity = turbine_capacity_user
    rotor_diameter = rotor_diameter_user
    turbine_efficiency = turbine_efficiency_user


    # Define file paths
    wind_speed_file = os.path.join(config.timestamped_folder, f"{turbine_name}_wind_data_saved.csv")

    # Download the CSV data (always overwrite)
    download_wind_csv(lon, lat, user_email, api_key, wind_speed_file)

    # Calculate wind power from CSV and add a column for power output
    total_power = calculate_wind_power_with_columns(wind_speed_file, turbine_capacity, turbine_efficiency, rotor_diameter)


    return total_power


def download_wind_csv(lon, lat, user_email, api_key, wind_speed_file):
    """
    Downloads hourly wind speed (WS10M) data from NASA POWER API and saves it as a CSV file.
    Parameters user_email and api_key are included for compatibility but not used by the NASA POWER API.
    """
    # NASA POWER API expects date strings
    start_date = "20230101"
    end_date = "20231231"
    parameter = "WS10M"
    community = "RE"
    format_type = "JSON"

    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?"
        f"parameters={parameter}&community={community}&"
        f"longitude={lon}&latitude={lat}&"
        f"start={start_date}&end={end_date}&format={format_type}"
    )

    try:
        time.sleep(2)
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()

            # Extract and process data
            try:
                raw_data = data["properties"]["parameter"]["WS10M"]
                records = []
                for timestamp_str, value in raw_data.items():
                    dt = datetime.strptime(timestamp_str, "%Y%m%d%H")
                    records.append({
                        
                        "Month": dt.month,
                        "Day": dt.day,
                        "Hour": dt.hour,
                        "Minute": 0,
                        "Wind Speed at 100m (m/s)": value
                    })
                df = pd.DataFrame(records)

                # Save to CSV
                df.to_csv(wind_speed_file, index=False)
                print(f"Data successfully downloaded and saved to {wind_speed_file}")
            except KeyError:
                print("Error: Wind speed data not found in the API response.")
        else:
            print(f"Failed to download data. HTTP Status Code: {response.status_code}")
            print(f"Error Details: {response.text}")
    except Exception as e:
        print(f"An error occurred while downloading wind data: {e}")


def calculate_wind_power_with_columns(wind_speed_file, turbine_capacity, turbine_efficiency, rotor_diameter):
    """
    Reads wind speed data from a CSV file, calculates power output, and adds a column for power output.
    """
    try:
        df = pd.read_csv(wind_speed_file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Check for necessary columns and extract wind speed
        required_columns = [ 'Month', 'Day', 'Hour', 'Minute']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"The column '{col}' is missing from the data.")

        wind_speed_column = next((col for col in df.columns if "wind speed" in col.lower()), None)
        if not wind_speed_column:
            raise ValueError("Wind speed column not found in the data.")

        # Convert wind speed column to numeric
        df['wind_speed'] = pd.to_numeric(df[wind_speed_column], errors='coerce')

        # Calculate power output only for valid entries
        air_density = 1.225  # kg/m^3
        swept_area = np.pi * (rotor_diameter / 2) ** 2  # m^2
        
        # Calculate power output and apply capacity limits in one go
        df['power_output'] = np.minimum(
            0.5 * air_density * swept_area * (df['wind_speed'] ** 3) * (turbine_efficiency / 1000),
            turbine_capacity
        )

        # Save the updated DataFrame back to the same CSV file
        df.to_csv(wind_speed_file, index=False)

        print(f"Detailed wind power output saved to: {wind_speed_file}")

        # Calculate and print total power output
        total_power_kwh = df['power_output'].sum()
        print(f"Total wind power produced: {total_power_kwh:.2f} kWh")
        return total_power_kwh
    
    except Exception as e:
        print(f"An error occurred while calculating wind power: {e}")