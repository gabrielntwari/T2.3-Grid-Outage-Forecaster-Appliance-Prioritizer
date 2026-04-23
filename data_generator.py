import pandas as pd
import numpy as np
import json

np.random.seed(42)

#date range creation
def create_time_index():
    return pd.DataFrame({
        "timestamp": pd.date_range(
            start="2023-01-01",
            periods=180 * 24,
            freq="h"
        )
    })


# Generate load 

def generate_load(df):
    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.dayofweek

    base = 50

    daily = 20 * np.sin(2 * np.pi * df["hour"] / 24)
    weekly = 10 * np.sin(2 * np.pi * df["dayofweek"] / 7)

    morning_peak = np.where(df["hour"].between(7, 10), 30, 0)
    evening_peak = np.where(df["hour"].between(18, 21), 40, 0)

    noise = np.random.normal(0, 5, len(df))

    df["load_mw"] = base + daily + weekly + morning_peak + evening_peak + noise

    return df


# Generate weather

def generate_weather(df):
    df["temp_c"] = 25 + 5 * np.sin(2 * np.pi * df["hour"] / 24) + np.random.normal(0, 1, len(df))
    df["humidity"] = 60 + np.random.normal(0, 10, len(df))
    df["wind_ms"] = np.abs(np.random.normal(3, 1, len(df)))

    df["rain_mm"] = np.random.exponential(1, len(df))

    # Rainy season boost
    rainy_months = df["timestamp"].dt.month.isin([3, 4, 5])
    df.loc[rainy_months, "rain_mm"] *= 2

    return df


# Outage probability

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_outages(df):
    df["load_lag1"] = df["load_mw"].shift(1).bfill()

    a0 = -5.2  
    a1 = 0.01
    a2 = 0.10  
    a3 = 0.1

    df["p_outage"] = sigmoid(
        a0 
        + a1 * df["load_lag1"] 
        + a2 * df["rain_mm"] 
        + a3 * df["hour"]
    )

    df["outage"] = np.random.binomial(1, df["p_outage"])
    return df


# Outage duration

def generate_duration(df):
    df["duration_min"] = 0.0  

    mask = df["outage"] == 1

    df.loc[mask, "duration_min"] = np.random.lognormal(
        mean=np.log(90),
        sigma=0.6,
        size=int(mask.sum()) 
    )

    return df



#  Save dataset

def save_grid_history(df):
    df_final = df[[
        "timestamp",
        "load_mw",
        "temp_c",
        "humidity",
        "wind_ms",
        "rain_mm",
        "outage",
        "duration_min"
    ]]

    df_final.to_csv("grid_history.csv", index=False)


#  Appliances dataset

def create_appliances():
    appliances = [
        {"name": "fridge", "category": "critical", "watts_avg": 300, "start_up_spike_w": 600, "revenue_if_running_rwf_per_h": 2000},
        {"name": "hair_dryer", "category": "critical", "watts_avg": 1500, "start_up_spike_w": 2000, "revenue_if_running_rwf_per_h": 3000},
        {"name": "sewing_machine", "category": "critical", "watts_avg": 500, "start_up_spike_w": 800, "revenue_if_running_rwf_per_h": 2500},
        {"name": "freezer", "category": "critical", "watts_avg": 400, "start_up_spike_w": 700, "revenue_if_running_rwf_per_h": 2200},
        {"name": "tv", "category": "comfort", "watts_avg": 200, "start_up_spike_w": 300, "revenue_if_running_rwf_per_h": 500},
        {"name": "fan", "category": "comfort", "watts_avg": 100, "start_up_spike_w": 150, "revenue_if_running_rwf_per_h": 300},
        {"name": "lighting", "category": "critical", "watts_avg": 150, "start_up_spike_w": 200, "revenue_if_running_rwf_per_h": 1000},
        {"name": "ac", "category": "luxury", "watts_avg": 2000, "start_up_spike_w": 3000, "revenue_if_running_rwf_per_h": 1000},
        {"name": "sound_system", "category": "luxury", "watts_avg": 500, "start_up_spike_w": 800, "revenue_if_running_rwf_per_h": 400},
        {"name": "water_heater", "category": "luxury", "watts_avg": 1800, "start_up_spike_w": 2500, "revenue_if_running_rwf_per_h": 700}
    ]

    with open("appliances.json", "w") as f:
        json.dump(appliances, f, indent=2)



# Businesses

def create_businesses():
    businesses = {
        "salon": ["hair_dryer", "tv", "fan", "lighting", "ac"],
        "cold_room": ["fridge", "freezer", "lighting"],
        "tailor": ["sewing_machine", "fan", "lighting"]
    }

    with open("businesses.json", "w") as f:
        json.dump(businesses, f, indent=2)



# MAIN

def main():
    df = create_time_index()
    df = generate_load(df)
    df = generate_weather(df)
    df = generate_outages(df)
    df = generate_duration(df)

    print("Outage rate:", df["outage"].mean())

    save_grid_history(df)
    create_appliances()
    create_businesses()

    print("✅ Data generated successfully!")


if __name__ == "__main__":
    main()