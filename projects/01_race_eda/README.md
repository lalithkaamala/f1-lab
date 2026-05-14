# 🏁 Project 1: Grid to Chequered Flag — Race EDA

**Discipline:** Exploratory Data Analysis  
**Seasons:** 2024–2025  
**Data Source:** FastF1 (real telemetry + lap data)

---

## 🎯 Objective

Conduct a comprehensive visual exploration of the 2024 F1 season, uncovering patterns and insights that the TV broadcast never shows. Every visualization is interactive (Plotly) and built on real race data.

---

## 📊 Key Analyses

### 1. Lap Time Distributions by Team
- Violin/box plots showing each team's race pace consistency
- Reveals which teams are fast but inconsistent vs. slow but reliable

### 2. Position Change Heatmap
- Grid position → Finish position for every driver at every race
- Identifies best overtakers and "reverse grid" specialists

### 3. Speed Trap Analysis
- Top speeds across all circuits — who has the fastest car vs. best downforce?
- Circuit-by-circuit power vs. aero tradeoff visualization

### 4. Tyre Strategy Overview
- Stint lengths by compound across the season
- Which teams made the right compound choices?

### 5. Wet vs. Dry Performance Delta
- How do teams/drivers' performance rankings shift in wet conditions?
- Scatter plot: dry pace rank vs. wet pace rank

### 6. Season Momentum Tracker
- Cumulative points curve showing championship momentum shifts
- Interactive — hover to see the gap at each round

### 7. Fastest Lap Telemetry Comparison
- Overlay speed/throttle/brake traces for top drivers at selected circuits
- Corner-by-corner technique comparison

---

## 🚀 How to Run

```bash
cd projects/01_race_eda

# Run the full analysis
python src/analysis.py

# Or open the notebook
jupyter notebook notebooks/race_eda.ipynb
```

---

## 📂 Structure

```
01_race_eda/
├── README.md              # This file
├── notebooks/
│   └── race_eda.ipynb     # Interactive notebook
├── src/
│   └── analysis.py        # Standalone analysis script
├── outputs/               # Generated interactive HTML charts
└── linkedin_post.md       # Draft LinkedIn post
```

---

## 📈 Sample Outputs

*Interactive HTML charts will be generated in `outputs/` after running the analysis.*
