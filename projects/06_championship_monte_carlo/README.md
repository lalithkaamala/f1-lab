# 🎲 Project 6: Championship Monte Carlo

**Discipline:** Statistical Modeling & Simulation  
**Seasons:** 2026 (Current Season)  

---

## 🎯 Objective

In the middle of a tightly contested F1 season, it's impossible to know who will win the Drivers' Championship with absolute certainty. A driver might have a 50-point lead, but a single DNF (Did Not Finish) or a sudden drop in car performance can flip the script.

This project builds a **Monte Carlo Simulation** to project the outcome of the Drivers' Championship. By running 100,000 simulations of the remaining races of the **2026** season, we can calculate the exact statistical probability of each driver winning the title.

---

## 🧠 Methodology

### 1. The Power Ranking Model
Before we can simulate future races, we need to know how likely a driver is to finish in a given position. We calculate a "Power Ranking" for each driver based on:
- **Average Finish Position** in the first half of the season.
- **Finish Variance (Standard Deviation)** to account for inconsistency or unreliability.
- **DNF Probability** based on historical retirement rates.

### 2. The Monte Carlo Engine
We simulate the remaining races of the season 100,000 times. For each simulated race:
- We draw a random performance score for each driver from a normal distribution defined by their Power Ranking (Mean and StdDev).
- We apply a random chance of DNF.
- We rank the drivers based on their performance scores and award points using the official F1 points system (25, 18, 15, 12, 10, 8, 6, 4, 2, 1).

### 3. Probability Aggregation
After 100,000 seasons are simulated, we aggregate the final points standings. 
- The percentage of simulations where Driver X scores the most points is their **Championship Win Probability**.
- We also calculate the 5th and 95th percentile point totals to provide a confidence interval.

---

## 🚀 How to Run

```bash
cd projects/06_championship_monte_carlo

# Run the simulation pipeline
python src/championship_sim.py
python src/visualizations.py
```

---

## 📂 Structure

```
06_championship_monte_carlo/
├── README.md
├── src/
│   ├── championship_sim.py      # Core Monte Carlo engine
│   └── visualizations.py        # Generates probability distributions
├── outputs/                   
└── linkedin_post.md
```
