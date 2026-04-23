# Salon Grid Sentinel ⚡

An intelligent, probabilistic energy load-shedding system designed for salons in Kigali, Rwanda. This project uses time-series forecasting to predict grid instability and automatically prioritize appliance usage to prevent total blackouts.

## 🚀 Overview
The system employs an **ARIMA-X** probabilistic model to forecast outage probabilities over a 24-hour window. Based on the predicted risk, the "Prioritizer" engine makes real-time decisions on which appliances to keep **ON** or shed (**OFF**) based on priority levels:
* **Critical:** Lighting, Sewing Machines (Essential for business)
* **Comfort:** Fans, TV (Secondary priority)
* **Luxury:** AC, Water Heater (Shed first during high-risk hours)

## 🛠️ Tech Stack
* **Backend:** Python 3.10+ (Pandas, Statsmodels, NumPy)
* **Frontend:** HTML5, JavaScript (Chart.js), CSS3
* **Model:** SARIMA

## 📂 Repository Structure
* `analysis.ipynb`: Jupyter Notebook containing Seasonal Decomposition, ACF/PACF plots, and model validation.
* `Prioritizer.py`: The core engine that runs the forecast and generates the appliance schedule.
* `live_plan.json`: The data bridge—contains the 24-hour forecast and appliance states.
* `index.html`: The live dashboard for salon managers.
* `data/`: Directory for historical load data CSVs.

## ⚙️ How to Use

### 1. Model Training & Prediction
Run the prioritizer script to generate the latest forecast based on the SARIMA parameters identified in the analysis phase:
```bash
python Prioritizer.py
