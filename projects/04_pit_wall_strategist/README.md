# ♟️ Project 4: Pit Wall Strategist

**Discipline:** Simulation & Operations Research  
**Seasons:** 2024  
**Dependencies:** Uses the XGBoost Tyre Degradation model built in Project 2.

---

## 🎯 Objective

In Formula 1, the fastest car doesn't always win. The strategy team on the pit wall must decide when to pit, which tyres to fit, and how to navigate traffic. 

This project builds a **Monte Carlo Race Simulator** to evaluate thousands of potential pit stop strategies and identify the mathematically optimal race plan.

---

## 🧠 Methodology

### 1. The Physics Engine
We simulate a full race distance (e.g., 50+ laps) using a custom discrete-event simulator:
- **Base Pace:** The driver's expected lap time on fresh tyres with zero fuel.
- **Fuel Burn:** Cars gain ~0.065s per lap as fuel burns off.
- **Tyre Degradation:** We load the trained XGBoost model from **Project 2** to predict exact time loss per lap based on compound (Soft, Medium, Hard) and tyre age.
- **Pit Loss:** A static time penalty applied when a driver enters the pits (e.g., ~22 seconds).

### 2. The Monte Carlo Simulation
We don't just test one strategy. We generate **10,000 permutations** of:
- **Stint lengths** (e.g., Pit Lap 15 vs. Pit Lap 22)
- **Compound choices** (e.g., Soft-Hard vs. Medium-Hard-Medium)
- **Number of stops** (1-stop vs 2-stop vs 3-stop)

We simulate the total race time for each permutation. The strategy with the lowest total race time is our optimal theoretical strategy.

### 3. Visualizations
- **Strategy Heatmap:** A contour plot showing total race time across different pit laps for a 1-stop strategy.
- **Simulated Race Trace:** A line chart showing the cumulative race time of the optimal 1-stop vs the optimal 2-stop.

---

## 🚀 How to Run

```bash
cd projects/04_pit_wall_strategist

# Run the simulation pipeline
python src/race_simulator.py
python src/monte_carlo.py
python src/visualizations.py
```

---

## 📂 Structure

```
04_pit_wall_strategist/
├── README.md
├── src/
│   ├── race_simulator.py      # Core physics and time-loss logic
│   ├── monte_carlo.py         # Runs 10k simulations to find the optimum
│   └── visualizations.py      # Generates strategy heatmaps
├── outputs/                   # Interactive Plotly charts
└── linkedin_post.md
```
