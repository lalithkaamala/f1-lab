# 🚀 LinkedIn Content Strategy: F1 Lab Project 2 — The Tyre Whisperer

This is the 3-part posting strategy for "Project 2: The Tyre Whisperer." The goal is to show how we move from basic EDA (Project 1) to actual predictive modeling, isolating physics (fuel burn) from degradation.

---

## 🏎️ Post 1: The Teaser (Visual Hook)

**Timing:** Monday morning
**Visual:** The "Degradation Curves" chart (clean line chart with confidence intervals for Soft, Medium, Hard).
**Tone:** Analytical but accessible.

**Draft:**
In F1, tyres don't just "get old"—they fall off a cliff. 📉🛞

For Project 2 of my `f1-lab` series, I wanted to build a model that actually predicts tyre degradation. But to do that, you have to solve a massive physics problem first: **Fuel Burn**.

F1 cars start with ~110kg of fuel and get about 0.065 seconds faster per lap just by burning weight. If you look at raw lap times, the tyres look like they are getting *better* as the race goes on. 

To build "The Tyre Whisperer", I pulled 9,500 laps from the 2024 season using `FastF1`, stripped out safety cars and anomalies, and engineered a `FuelCorrectedDelta` to isolate the pure tyre wear. 

The result? The chart below. You can literally see the exact lap where the Softs cross over with the Mediums, and where the Hards start to grain. 

In my next post, I’ll share how I used XGBoost and rolling-rate changepoint detection to mathematically predict the "Cliff". 

#DataScience #Formula1 #F1 #MachineLearning #Python #PredictiveModeling

---

## 🧠 Post 2: The Deep Dive (Technical Architecture)

**Timing:** Wednesday midday
**Visual:** Carousel containing the "Cliff Map" (heatmap) and "Feature Importance" chart.
**Tone:** Technical, aimed at fellow data scientists.

**Draft:**
How do you mathematically define the exact moment an F1 tyre "falls off the cliff"? 🏔️

In Project 2 of the `f1-lab` series, building the XGBoost regression model was the easy part (we achieved a Mean Absolute Error of 0.52s per lap). The hard part was defining the cliff.

I implemented a changepoint detection algorithm based on the **rolling degradation rate**. 
1️⃣ Calculate the average lap-over-lap time loss for the first half of a stint.
2️⃣ Scan the stint for the lap where the degradation rate permanently exceeds 2x the baseline average.
3️⃣ Flag that as the Cliff.

I applied this to every stint in the first 10 rounds of the 2024 season. The result is the **Cliff Map** (first image). You can see exactly how a high-degradation track like Suzuka forces the cliff 5-6 laps earlier than a smooth track like Jeddah. 

The XGBoost feature importance (second image) also revealed something interesting: Circuit average degradation and the `TrackTemp_x_TyreAge` interaction term are massively predictive. Raw air temperature? Barely registers.

I’m packaging up this model because we’ll need it for Project 4: The Pit Wall Strategist. Code drops Friday. 🛠️

#MachineLearning #XGBoost #F1Analytics #DataEngineering #Analytics

---

## 💻 Post 3: The Code Drop (Repo Share)

**Timing:** Friday morning
**Visual:** A clean screenshot of the Plotly Predicted vs. Actual scatter plot, or a short screen recording of the interactive charts.
**Tone:** Collaborative, open-source focus.

**Draft:**
The code for "The Tyre Whisperer" is now live on GitHub. 🏎️💻

If you want to play with real 2024 F1 telemetry and build predictive models, the `f1-lab` repo is designed for you. Project 2 walks through the entire Machine Learning lifecycle:

✅ `data_collection.py`: Multi-race FastF1 extraction & noise filtering
✅ `feature_engineering.py`: Fuel-weight correction & compound encoding
✅ `modeling.py`: Polynomial baselines vs. XGBoost (w/ Time-Aware splits)
✅ `visualizations.py`: 4 interactive Plotly charts

The architecture is heavily modular so you can swap in your own models (maybe a Gaussian Process for better uncertainty bands?). 

Repo link in the comments 👇 Let me know if you can beat my 0.52s MAE!

#OpenSource #Python #DataSciencePortfolio #F1 #Motorsport #Coding
