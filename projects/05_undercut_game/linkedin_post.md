# 🚀 LinkedIn Content Strategy: F1 Lab Project 5 — The Undercut Game

This is the 3-part posting strategy for "Project 5: The Undercut Game." The goal is to highlight the application of Game Theory to F1 strategy.

---

## 🏎️ Post 1: The Teaser (Visual Hook)

**Timing:** Monday morning
**Visual:** The "Payoff Matrix Heatmap" showing the win probabilities.
**Tone:** Analytical, engaging the audience with a hypothetical scenario.

**Draft:**
You are the Race Strategist for P1. P2 is 1.5 seconds behind you. Do you pit on Lap 20, or wait until Lap 21? 🛑⏱️

For Project 5 of my `f1-lab` series, I modeled the famous F1 "Undercut" as a **Stackelberg Game**. 

If you pit too early, you risk your tyres falling off a cliff at the end of the race. If you wait, P2 will pit first, bolt on fresh tyres, and pass you while you are stuck on old rubber.

To solve this, I built a mathematical payoff matrix (see the heatmap) that balances the time gained from fresh tyres against the penalty of late-race degradation. Then, I used `nashpy` to find the exact Nash Equilibrium.

The math proves why the Undercut is so powerful: even if the optimal tyre life suggests pitting on Lap 24, the Nash Equilibrium forces *both* drivers to pit on Lap 20 just to defend against each other.

Later this week, I'll share how the equilibrium completely changes if the Undercut Delta (time gained on fresh tyres) increases.

#Formula1 #GameTheory #NashEquilibrium #DataScience #Python

---

## 🧠 Post 2: The Deep Dive (Technical Details)

**Timing:** Wednesday midday
**Visual:** The "Nash Equilibrium Shift vs Undercut Power" line chart.
**Tone:** Deeply technical, explaining Nash Equilibriums in competitive environments.

**Draft:**
Why do F1 teams constantly make "sub-optimal" pit stops? Because they are trapped in a Nash Equilibrium. 🧠🏎️

In Project 5, I used Game Theory to prove why F1 strategy looks the way it does. 

If both drivers agreed to pit on the optimal tyre-life lap (Lap 24), the Leader would win 55% of the time. But this is a classic Prisoner's Dilemma. The Follower has a massive incentive to deviate and pit on Lap 23 (the Undercut), jumping their win probability to 73%. 

Knowing this, the Leader is forced to pit on Lap 23 to defend. But then the Follower pits on Lap 22. 

The chart below maps the Nash Equilibrium as the Undercut gets more powerful (X-axis). Once fresh tyres give you an advantage of more than 1.5 seconds per lap, the Nash Equilibrium cascades. The optimal strategy collapses backwards, forcing both drivers to pit 4-5 laps earlier than the tyres dictate. 

This is exactly why you see entire trains of F1 cars diving into the pits the moment the pit window opens. It’s not about tyre wear; it’s about game theory.

#Nashpy #Python #DataScience #OperationsResearch #Analytics

---

## 💻 Post 3: The Code Drop (Repo Share)

**Timing:** Friday morning
**Visual:** A screenshot of the Python code defining the Game Theory payoff matrix.
**Tone:** Open-source, collaborative.

**Draft:**
The Game Theory F1 Model is now live on GitHub! 💻🏎️

If you've ever wanted to learn Game Theory, modeling F1 pit stops is the perfect use case. The `f1-lab` repo now includes **Project 5: The Undercut Game**.

It features:
✅ A custom Payoff Matrix generator that balances Undercut Time-Gained vs Tyre-Life Penalties.
✅ Integration with the `nashpy` Python library to solve for simultaneous Nash Equilibria.
✅ Plotly code to generate Heatmaps and Sensitivity boundaries.

You can tweak the variables (e.g., what happens if passing is impossible, like at Monaco?) and see how the equilibrium shifts from an Undercut to an Overcut.

Link to the repo is in the comments 👇 Let me know what track you simulate!

#OpenSource #Python #DataSciencePortfolio #F1 #Motorsport #GameTheory
