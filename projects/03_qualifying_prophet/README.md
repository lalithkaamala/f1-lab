# 🔮 Project 3: Qualifying Prophet

**Discipline:** Classification & Regression (Supervised Learning)  
**Seasons:** 2024  
**Data Source:** FastF1 (Free Practice 1, 2, 3 and Qualifying results)

---

## 🎯 Objective

Predict the Qualifying order before the cars even hit the track for Q1. This model uses pace data from Free Practice (FP1, FP2, FP3) to answer two questions:
1. **Classification:** Will driver X make it to Q3 (Top 10)?
2. **Regression:** What will their exact grid position be?

---

## 🧠 Methodology

### Phase 1: Data Collection & Feature Engineering
- Pull FP1, FP2, FP3, and Qualifying session data.
- **Pace Features:** Driver's fastest lap in practice vs. session best (delta).
- **Teammate Features:** Gap to teammate in practice (indicates driver form vs car form).
- **Consistency Features:** Number of laps completed in practice.
- **Track History:** Driver's historical performance at this specific circuit.

### Phase 2: Modeling
- **Model 1 (Classifier):** XGBoost Classifier predicting `Made_Q3` (binary).
- **Model 2 (Regressor):** XGBoost Regressor predicting `GridPosition` (1-20).
- Time-aware validation split (e.g., train on Rounds 1-15, test on Rounds 16+).

### Phase 3: Visualizations
- **Feature Importance:** What practice session actually matters most? (Spoiler: Usually FP3).
- **Confusion Matrix:** How well do we predict Q3 appearances?
- **Pace Translation:** Scatter plot of FP3 Pace Delta vs. Actual Qualifying Position.
- **Grid Prediction Shift:** Bump chart showing actual vs predicted grid for a specific race.

---

## 🚀 How to Run

```bash
cd projects/03_qualifying_prophet

# Run the full pipeline
python src/data_collection.py
python src/feature_engineering.py
python src/modeling.py
python src/visualizations.py
```

---

## 📂 Structure

```
03_qualifying_prophet/
├── README.md
├── src/
│   ├── data_collection.py      
│   ├── feature_engineering.py  
│   ├── modeling.py             
│   └── visualizations.py       
├── models/                     
├── outputs/                    
└── linkedin_post.md
```
