# ♟️ Project 5: The Undercut Game

**Discipline:** Game Theory & Decision Science  
**Seasons:** 2024  

---

## 🎯 Objective

In Formula 1, the "Undercut" is the most powerful strategic weapon. It occurs when a trailing car (the Follower) pits before the leading car (the Leader) to take advantage of fresh, faster tyres, successfully passing the leader when they pit a lap later.

But if it's so powerful, why doesn't the Leader just pit first? Because pitting early forces you to run a longer final stint, risking a tyre "cliff" at the end of the race.

This project models the Undercut scenario as a **Stackelberg Game** (Leader-Follower dynamic) and calculates the **Nash Equilibrium** using `nashpy`.

---

## 🧠 Methodology

### 1. The Payoff Matrix
We simulate a classic scenario: Two drivers are battling for the win. They have a pit window between Lap 20 and Lap 25. 
The payoff (probability of winning) for pitting on Lap $X$ vs Lap $Y$ depends on:
- **The Undercut Delta:** The time gained per lap on fresh tyres vs old tyres (e.g., 1.5 seconds).
- **The Tyre Life Penalty:** The risk of running out of tyres at the end of the race by pitting too early.
- **Track Position:** The Leader has a baseline advantage (e.g., 55% win probability if both pit on the same lap).

### 2. Nash Equilibrium & Stackelberg Solutions
- **Simultaneous Game:** What if neither driver knows what the other is doing? (Nash Equilibrium)
- **Sequential Game:** The Leader acts first, but the Follower can react instantly (Stackelberg Equilibrium). 

### 3. Visualizations
- **Payoff Matrix Heatmap:** A visual representation of the game matrix.
- **Undercut Power vs Nash Equilibrium:** How the optimal strategy shifts as tyre degradation increases.

---

## 🚀 How to Run

```bash
cd projects/05_undercut_game

# Run the game theory pipeline
python src/undercut_model.py
python src/visualizations.py
```

---

## 📂 Structure

```
05_undercut_game/
├── README.md
├── src/
│   ├── undercut_model.py      # Nashpy game setup and equilibrium solver
│   └── visualizations.py      # Heatmaps and strategy boundaries
├── outputs/                   
└── linkedin_post.md
```
