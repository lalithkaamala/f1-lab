# 🔍 Project 7: Telemetry Decoder

**Discipline:** Time Series Classification & Deep Learning  
**Seasons:** 2025 (Current Season)

---

## 🎯 Objective

Every Formula 1 driver has a unique "fingerprint"—the exact way they trail-brake into a corner, how aggressively they apply the throttle on exit, and how they shift gears. 

This project asks the question: **Can a Machine Learning model identify a driver based solely on their raw foot pedals?**

We will extract high-resolution telemetry data from a **2025** race, and train a Time Series Classification model to predict the driver based purely on the shapes of their Speed, Throttle, and Brake curves.

---

## 🧠 Methodology

### 1. Data Collection (2025 Season)
We use `FastF1` to pull raw telemetry channels at high frequency (approx 10Hz):
- **Inputs:** `Speed`, `Throttle`, `Brake`, `RPM`, `nGear`
- **Target:** Driver ID (e.g., `VER` vs `HAM`)

We extract these traces for every valid lap of the race for our chosen drivers.

### 2. Time-Series Feature Extraction & Modeling
Raw time series are difficult for traditional models because laps take different amounts of time. 
We standardize the traces by interpolating them to a fixed distance array (e.g., 500 distance samples per lap).

We train a **Random Forest Classifier** (or 1D CNN) on these flattened distance-normalized traces.

### 3. Visualizations
- **The Fingerprint:** A overlaid plot of Driver A vs Driver B's throttle/brake application through a specific corner sequence.
- **Model Accuracy Matrix:** A confusion matrix showing how accurately the model identifies the driver blind.

---

## 🚀 How to Run

```bash
cd projects/07_telemetry_decoder

# Run the pipeline
python src/data_collection.py
python src/modeling.py
python src/visualizations.py
```

---

## 📂 Structure

```
07_telemetry_decoder/
├── README.md
├── src/
│   ├── data_collection.py     # Pulls 2025 telemetry
│   ├── modeling.py            # Interpolates distance and trains classifier
│   └── visualizations.py      # Telemetry trace overlays
├── outputs/                   
└── linkedin_post.md
```
