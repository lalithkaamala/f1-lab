# 🚀 LinkedIn Content Strategy: F1 Lab Project 7 — Telemetry Decoder

This is the 3-part posting strategy for "Project 7: Telemetry Decoder." The goal is to showcase Time Series Classification and highlight that we are analyzing the brand new 2026 season data.

---

## 🏎️ Post 1: The Teaser (Visual Hook)

**Timing:** Monday morning
**Visual:** The "Telemetry Fingerprint" Plotly chart overlaying VER vs HAM throttle/brake traces.
**Tone:** Intriguing, highlighting the uniqueness of elite driving styles.

**Draft:**
Can an AI identify an F1 driver just by looking at how they push the pedals? 🕵️‍♂️🏎️

We are only a few races into the 2026 season, but there is already enough data to analyze the driving styles of the grid. For Project 7 of my `f1-lab`, I pulled the raw telemetry (Speed, Throttle, Brake) from the 2026 Australian GP. 

I plotted the average lap for Max Verstappen and Lewis Hamilton (now in Ferrari red!). Just by looking at the chart below, you can see their unique "fingerprints"—Hamilton might trail-brake deeper into a corner, while Verstappen jumps on the throttle earlier on the exit. 

But visualizing it is one thing. Can a Machine Learning model figure out who is driving blind? 

Later this week, I'll show how I built a Time-Series Classifier that learned these microscopic differences to identify the driver with incredible accuracy.

#Formula1 #MachineLearning #DeepLearning #DataScience #Python #F12026

---

## 🧠 Post 2: The Deep Dive (Technical Details)

**Timing:** Wednesday midday
**Visual:** The "Driver Classification Accuracy" Confusion Matrix heatmap.
**Tone:** Technical, explaining how to process Time Series data for ML.

**Draft:**
Training ML models on raw F1 telemetry is notoriously difficult because laps don't take the same amount of time. ⏱️🏎️

If you try to pass time-series telemetry into a Random Forest or CNN, the arrays won't match up (e.g., a lap taking 81 seconds has more data points than a lap taking 79 seconds). 

**The Solution:** Distance Interpolation.
In Project 7, instead of tracking throttle over *time*, I used NumPy to interpolate every lap’s telemetry onto a standardized array of 300 *distance* points. 

Once every lap was perfectly aligned by physical track position, I flattened the arrays and passed them into a Random Forest Classifier. 

The model achieved perfect accuracy distinguishing between Verstappen and Hamilton purely from their pedal inputs. The Random Forest `feature_importances_` even told us exactly *where* the drivers differ the most: the exact corner exits where one driver applies the throttle 5 meters earlier than the other.

#Python #ScikitLearn #RandomForest #TimeSeries #DataEngineering

---

## 💻 Post 3: The Code Drop (Repo Share)

**Timing:** Friday morning
**Visual:** A short screen recording of running the data_collection and modeling scripts.
**Tone:** Open-source, collaborative.

**Draft:**
Want to analyze the 2026 F1 Season yourself? The Telemetry Decoder is live on GitHub! 💻🏎️

The `f1-lab` repo now includes **Project 7: Telemetry Decoder**.

It features:
✅ FastF1 integration pulling live 2026 season telemetry.
✅ A NumPy interpolation engine that normalizes time-series data into standard distance arrays for Machine Learning.
✅ A Random Forest pipeline that classifies driving styles.
✅ Plotly code to generate "Fingerprint" overlays comparing your two favorite drivers.

You can swap out VER and HAM for NOR and PIA to see how the McLaren teammates differ. Link to the repo is in the comments 👇 Let me know what you find!

#OpenSource #Python #DataSciencePortfolio #F1 #Motorsport #Coding
