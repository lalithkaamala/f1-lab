# 🛞 Project 2: The Tyre Whisperer — Tyre Degradation Modeling

**Discipline:** Regression / Time-Series Modeling  
**Seasons:** 2024  
**Data Source:** FastF1 (real lap-by-lap timing + tyre compound data)

---

## 🎯 Objective

Build a predictive model that captures how F1 tyre performance degrades over a stint. The model learns the relationship between **tyre age** and **lap time delta** — and can predict the exact lap where performance "falls off a cliff."

This is a foundational model that feeds directly into **Project 4 (Pit Wall Strategist)** and **Project 5 (The Undercut Game)**.

---

## 🧠 Methodology

### Phase 1: Data Collection & Feature Engineering
- Pull lap-by-lap data for all 2024 races using FastF1
- Engineer features: tyre age, compound, track temp, fuel-corrected lap time, stint number
- Filter noise: remove pit laps, safety car laps, first-lap anomalies

### Phase 2: Degradation Curve Fitting
- **Baseline**: Polynomial regression (degree 2–3) per compound
- **Advanced**: Gaussian Process Regression for uncertainty quantification
- **Visualization**: Interactive degradation curves with confidence bands

### Phase 3: Cliff Detection
- Identify the "cliff" point where degradation accelerates non-linearly
- Use changepoint detection (PELT algorithm) on the residuals
- Classify stints as "linear degradation" vs. "cliff"

### Phase 4: Predictive Model
- **XGBoost/LightGBM** regressor: predict lap time delta given features
- Feature importance analysis — what drives degradation most?
- Cross-validated performance metrics (RMSE, MAE)

---

## 📊 Key Visualizations

1. **Degradation Curves by Compound** — Lap time vs. tyre age for S/M/H
2. **Fuel-Corrected Pace** — Isolating tyre effect from fuel burn
3. **The Cliff Map** — Heatmap of cliff lap by circuit × compound
4. **Feature Importance** — What matters most for tyre life?
5. **Prediction vs. Actual** — Model accuracy scatter plot
6. **Interactive Stint Explorer** — Select any driver/race to see predicted vs. actual deg

---

## 🚀 How to Run

```bash
cd projects/02_tyre_whisperer

# Run the full pipeline
python src/tyre_model.py

# Or step by step
python src/data_collection.py    # Collect & process data
python src/feature_engineering.py # Engineer features
python src/modeling.py            # Train models
python src/visualizations.py      # Generate charts
```

---

## 📂 Structure

```
02_tyre_whisperer/
├── README.md
├── notebooks/
│   └── tyre_degradation.ipynb
├── src/
│   ├── data_collection.py      # Multi-race data pipeline
│   ├── feature_engineering.py  # Fuel correction, stint detection
│   ├── modeling.py             # Regression models + cliff detection
│   └── visualizations.py       # Interactive Plotly charts
├── models/                     # Saved model artifacts
├── outputs/                    # Generated charts
└── linkedin_post.md
```
