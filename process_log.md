# Process Log: Salon Grid Sentinel Development

### Phase 1: Data Analysis & Decomposition
* Conducted **Seasonal Decomposition** on hourly load data.
* Identified a strong **24-hour seasonality** ($s=24$) and a slight downward trend in the daily mean load.
* Analyzed **ACF and PACF** plots: Identified $p=2$ and $q=0$ as initial parameters for the SARIMA model.

### Phase 2: Model Implementation
* Implemented **ARIMA-X** to calculate the probability of outages ($p\_outage$).
* Developed `Prioritizer.py` to map probabilities to appliance states (Load Shedding Logic).
* Achieved a **Brier Score of 0.0371**, indicating high probabilistic accuracy.

### Phase 3: Frontend Visualization
* Created a responsive dashboard using **Chart.js**.
* Integrated `live_plan.json` to bridge the gap between Python backend predictions and the UI.
* Refined the UI to handle dynamic appliance lists and color-coded status cards.
