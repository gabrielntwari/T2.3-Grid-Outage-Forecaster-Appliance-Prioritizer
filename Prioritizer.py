import pandas as pd
import json
import os

class AppliancePrioritizer:
    def __init__(self, appliance_file="appliances.json"):
        with open(appliance_file, 'r') as f:
            self.appliances = json.load(f)
        
        # Priority mapping: Luxury dropped first, Critical protected longest
        self.category_weights = {
            "luxury": 1,
            "comfort": 2,
            "critical": 3
        }

    def generate_plan(self, forecast_df):
        """
        Creates a 24-hour plan for the salon.
        forecast_df: Output from GridForecaster (p_outage, expected_duration_min)
        """
        plan = []

        for _, row in forecast_df.iterrows():
            hour = int(row['hour_ahead'])
            p = row['p_outage']
            
            hourly_decisions = {"hour": hour, "p_outage": p}
            
            # Sort appliances: Higher category weight first, then higher revenue
            sorted_apps = sorted(
                self.appliances,
                key=lambda x: (self.category_weights.get(x['category'].lower(), 0), 
                               x['revenue_if_running_rwf_per_h']),
                reverse=True
            )

            for app in sorted_apps:
                status = "ON"
                cat = app['category'].lower()
                
                # Rule-based shedding thresholds
                if cat == "luxury" and p > 0.15:
                    status = "OFF"
                elif cat == "comfort" and p > 0.30:
                    status = "OFF"
                elif cat == "critical" and p > 0.60:
                    status = "OFF"
                
                # Use 'name' to match your specific JSON schema
                hourly_decisions[app['name']] = status
            
            plan.append(hourly_decisions)
            
        return pd.DataFrame(plan)

    def calculate_savings(self, plan_df, actual_outage_series):
        """
        Quantifies the business impact. 
        Saves are calculated based on avoided replacement costs.
        """
        total_saved_rwf = 0
        
        # Create a mapping of appliance name to replacement cost
        cost_map = {app['name']: app.get('replacement_cost_rwf', 50000) for app in self.appliances}
        
        for i, row in plan_df.iterrows():
            # If an outage actually occurred in this hour
            if actual_outage_series.iloc[i] == 1:
                for app_name, status in row.items():
                    if status == "OFF" and app_name in cost_map:
                        # We successfully protected this appliance
                        total_saved_rwf += cost_map[app_name]
                        
        return total_saved_rwf

if __name__ == "__main__":
    prioritizer = AppliancePrioritizer()
    
    # 1. Generate Mock Forecast (In production, this comes from Forecaster.py)
    mock_forecast = pd.DataFrame({
        "hour_ahead": range(1, 25),
        "p_outage": [0.02, 0.05, 0.22, 0.45, 0.08] + [0.02]*19,
        "expected_duration_min": [108.0]*24
    })
    
    # 2. Generate the Plan
    plan = prioritizer.generate_plan(mock_forecast)
    
    # 3. EXPORT FOR LITE_UI.HTML
    plan.to_json("live_plan.json", orient="records", indent=4)
    
    print("--- 24-HOUR APPLIANCE PRIORITIZATION PLAN ---")
    # Verify the specific names in your JSON show up here
    cols_to_show = ['hour', 'p_outage', 'ac', 'fridge', 'hair_dryer']
    # Filter only columns that exist to prevent KeyErrors
    existing_cols = [c for c in cols_to_show if c in plan.columns]
    print(plan[existing_cols].head(10))
    
    print("\n[SUCCESS] live_plan.json updated for Dashboard.")