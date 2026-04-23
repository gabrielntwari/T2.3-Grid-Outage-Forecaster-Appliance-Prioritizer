import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class GridForecaster:
    def __init__(self):
        self.model_path = 'sarimax_model.pkl'
        self.dur_model_path = 'duration_regressor.pkl'
        # Calibrated coefficients for ~4% outage rate
        self.a_coeffs = {"a0": -5.2, "a1": 0.01, "a2": 0.10, "a3": 0.1}

    def train(self, data_path="grid_history.csv"):
        """Fits both the Outage (SARIMAX) and Duration (RandomForest) models."""
        if not os.path.exists(data_path):
            print(f"Error: {data_path} not found. Generate data first!")
            return

        df = pd.read_csv(data_path, parse_dates=['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        
        print("Training Outage Model (SARIMAX)...")
        model = SARIMAX(
            df["load_mw"], 
            exog=df[["temp_c", "rain_mm", "hour"]], 
            order=(2, 0, 0),
            enforce_stationarity=False
        )
        results = model.fit(disp=False)
        joblib.dump(results, self.model_path)

        print("Training Duration Model (Random Forest)...")
        # We train the duration model ONLY on rows where an outage occurred
        outage_data = df[df["outage"] == 1].copy()
        
        if len(outage_data) > 0:
            dur_model = RandomForestRegressor(n_estimators=100, random_state=42)
            dur_model.fit(outage_data[["load_mw", "rain_mm", "hour"]], outage_data["duration_min"])
            joblib.dump(dur_model, self.dur_model_path)
        else:
            print("Warning: No outages found in history to train duration model.")

    def get_forecast_24h(self, future_exog):
        """Generates the 24h probabilistic forecast."""
        # Ensure models exist
        if not os.path.exists(self.model_path) or not os.path.exists(self.dur_model_path):
            self.train()

        model_results = joblib.load(self.model_path)
        dur_model = joblib.load(self.dur_model_path)
        
        # 1. Predict Future Load
        load_pred = model_results.forecast(steps=24, exog=future_exog)
        
        # 2. Calculate P(outage) via Sigmoid
        logit = (self.a_coeffs["a0"] + 
                 self.a_coeffs["a1"] * load_pred.values + 
                 self.a_coeffs["a2"] * future_exog["rain_mm"].values + 
                 self.a_coeffs["a3"] * future_exog["hour"].values)
        p_outage = 1 / (1 + np.exp(-logit))
        
        # 3. Predict Variable Duration
        pred_features = pd.DataFrame({
            "load_mw": load_pred.values,
            "rain_mm": future_exog["rain_mm"].values,
            "hour": future_exog["hour"].values
        })
        expected_durations = dur_model.predict(pred_features)
        
        # 4. Final Dataframe
        return pd.DataFrame({
            "hour_ahead": range(1, 25),
            "p_outage": np.round(p_outage, 4),
            "expected_duration_min": np.round(expected_durations, 1)
        })

if __name__ == "__main__":
    forecaster = GridForecaster()
    
    # Mock Future Weather Data
    future_data = pd.DataFrame({
        "temp_c": np.random.uniform(22, 28, 24),
        "rain_mm": [0, 0, 0, 5.0, 8.0, 2.0] + [0]*18, # Added some rain to see duration change
        "hour": range(24)
    })
    
    output = forecaster.get_forecast_24h(future_data)
    print("\n--- 24-HOUR PROBABILISTIC FORECAST ---")
    print(output)