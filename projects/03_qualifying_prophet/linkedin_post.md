# 🚀 LinkedIn Content Strategy: F1 Lab Project 3 — Qualifying Prophet

This is the 3-part posting strategy for "Project 3: Qualifying Prophet." The goal is to highlight the transition to predictive classification and regression models based on practice data.

---

## 🏎️ Post 1: The Teaser (Visual Hook)

**Timing:** Monday morning
**Visual:** The "FP3 Pace Translation to Qualifying" scatter plot (colorful, team-colored dots).
**Tone:** Curious, asking the audience a question.

**Draft:**
Does Free Practice pace actually matter in Formula 1? 🤔⏱️

We've all seen a driver top the timesheets in FP3, only to get knocked out in Q2. But is that the exception or the rule? 

For Project 3 of my `f1-lab` series, I built the **Qualifying Prophet** — an XGBoost model that ingests FP1, FP2, and FP3 lap times, teammate gaps, and historical data to predict exactly where a driver will qualify.

Look at the chart below. It plots every driver's FP3 Pace Delta (how close they were to the fastest FP3 lap) against their actual Qualifying Grid Position for 11 races in 2024. 

You can clearly see the "Perez Zone" (fast car, inconsistent quali) vs the "Alonso Effect" (over-performing the practice pace). 

Later this week, I’ll share the confusion matrix showing exactly how well the model predicts who makes it to Q3. 

#Formula1 #DataScience #MachineLearning #PredictiveModeling #Python

---

## 🧠 Post 2: The Deep Dive (Technical Details)

**Timing:** Wednesday midday
**Visual:** The Confusion Matrix and Feature Importance bar chart.
**Tone:** Analytical, diving into model performance and feature engineering.

**Draft:**
Predicting an F1 Qualifying session is a nightmare for Machine Learning. 🏎️📉

Why? Because track evolution, engine modes, and sandbagging make absolute lap times useless. If you train a model on raw lap times, it will fail.

To build the "Qualifying Prophet", I engineered two key relative features:
1️⃣ **Pace Delta to Leader:** How many % slower were you than P1 in that specific session?
2️⃣ **Teammate Gap:** Are you out-driving your teammate, indicating the car has more potential?

I trained an XGBoost Classifier on the 2024 season to predict a simple binary outcome: **Will this driver make Q3?**

The results (see the Confusion Matrix): 64% accuracy on the test set. 
While 64% might sound low for a generic classification problem, in the context of F1 — where red flags, traffic, and track limits delete laps constantly — correctly predicting the top 10 cars purely based on practice data is a strong signal. 

The most predictive feature? (See second image). FP3 Pace Delta, followed closely by the Teammate Gap in FP2. 

#XGBoost #F1Analytics #DataEngineering #Classification #Analytics

---

## 💻 Post 3: The Code Drop (Repo Share)

**Timing:** Friday morning
**Visual:** A short screen recording scrolling through the interactive Plotly outputs (or a split-screen of code and the Predicted vs Actual scatter plot).
**Tone:** Open-source, collaborative.

**Draft:**
Want to build your own F1 predictive models? 💻🏎️

The code for Project 3: "Qualifying Prophet" is now live on the `f1-lab` GitHub repo. 

This module shows how to:
✅ Pull and clean 2024 Free Practice data using `FastF1`.
✅ Engineer relative "Pace Delta" features to ignore track evolution.
✅ Train an XGBoost Classifier (for Q3 appearance) and an XGBoost Regressor (for exact Grid Position).
✅ Generate publication-ready Plotly visualizations.

My regression model achieved a Mean Absolute Error of ~4.3 grid positions. The midfield is incredibly tight! 

Repo link in the comments 👇 Feel free to fork it, add weather data (it's included in the data loader!), and see if you can beat my MAE.

#OpenSource #Python #DataSciencePortfolio #F1 #Motorsport #Coding
