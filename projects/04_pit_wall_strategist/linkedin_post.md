# 🚀 LinkedIn Content Strategy: F1 Lab Project 4 — Pit Wall Strategist

This is the 3-part posting strategy for "Project 4: Pit Wall Strategist." The goal is to show how we transitioned from predictive modeling (Projects 2/3) to **Operations Research and Simulation**.

---

## 🏎️ Post 1: The Teaser (Visual Hook)

**Timing:** Monday morning
**Visual:** The "1-Stop Strategy Landscape" Heatmap.
**Tone:** Engaging, asking a strategy question.

**Draft:**
Why didn't Lando just pit for fresh Softs? 🏁🏎️

If you’ve ever screamed at your TV during an F1 race because a team made a terrible strategy call, this project is for you.

For Project 4 of my `f1-lab` series, I built the **Pit Wall Strategist** — a Monte Carlo race simulator. It doesn't just guess; it loads the XGBoost tyre degradation model I built in Project 2, adds in the physics of fuel weight burn (~0.065s per lap), and calculates exact pit-loss times.

Then, it simulates **10,000 permutations** of pit strategies to find the mathematical optimum. 

The chart below shows the "Strategy Landscape" for a 1-stop race at Monza. The X-axis is the lap you pit, the Y-axis is how many seconds you lose compared to the optimal strategy. You can literally see the "overcut" cliff where the tyres die, and why pitting too early ruins your race.

Later this week, I'll share the exact race trace comparing the optimal 1-stop vs. the optimal 2-stop. 

#Formula1 #OperationsResearch #DataScience #MonteCarlo #Simulation

---

## 🧠 Post 2: The Deep Dive (Technical Details)

**Timing:** Wednesday midday
**Visual:** The "Race Trace" line chart showing cumulative time for 1-stop vs 2-stop.
**Tone:** Technical, focusing on the physics engine and vectorization.

**Draft:**
Simulating a 53-lap F1 race 10,000 times sounds computationally expensive. Here is how I did it in 0.05 seconds. ⚡🏎️

In Project 4 of the `f1-lab`, I built a discrete-event physics engine to evaluate F1 pit strategies. The engine calculates three things for every lap:
1️⃣ Base Lap Time
2️⃣ Fuel Burn Penalty (cars get lighter and faster)
3️⃣ Tyre Degradation (using my XGBoost model from Project 2)

But calling `xgb.predict()` 530,000 times in a Python loop is slow. 

**The Optimization:** 
Before the Monte Carlo loop starts, I pre-compute the degradation curves for Soft, Medium, and Hard compounds across 80 laps for the specific track temperature and circuit profile. 
During the simulation, predicting tyre degradation becomes an `O(1)` array lookup. 

This allowed me to search the entire strategy space (every combination of 1-stop and 2-stop pit laps and compounds) almost instantly. 

The image shows the cumulative race trace for Monza. Notice how the 2-stop strategy (red dashed line) is faster on track (flatter slope), but the massive 24-second pit-loss at Monza means the 1-stop strategy still finishes 38 seconds ahead. 

#Python #XGBoost #F1Analytics #DataEngineering #PerformanceOptimization

---

## 💻 Post 3: The Code Drop (Repo Share)

**Timing:** Friday morning
**Visual:** A short screen recording of the terminal running the Monte Carlo script and printing the top 5 strategies.
**Tone:** Open-source, collaborative.

**Draft:**
The code for the F1 Monte Carlo Simulator is now live on GitHub! 💻🏎️

If you've ever wanted to build your own strategy engine, the `f1-lab` repo now includes **Project 4: Pit Wall Strategist**. 

It features:
✅ A discrete-event `F1RaceSimulator` that handles fuel physics and pit loss.
✅ A `monte_carlo.py` script that generates thousands of 1-stop and 2-stop permutations to find the optimal strategy.
✅ Plotly code to generate Strategy Heatmaps and Race Traces.

The best part? It's completely modular. You can plug in your own track profiles (e.g., change the `TrackTemp` or `CircuitAvgDeg`) and see how it instantly changes the optimal strategy from a 1-stop to a 2-stop.

Link to the repo is in the comments 👇 Let me know if you can find a track profile where a 3-stop is actually optimal!

#OpenSource #Python #DataSciencePortfolio #F1 #Motorsport #Coding
