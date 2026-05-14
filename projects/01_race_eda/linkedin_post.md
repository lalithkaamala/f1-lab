# 🏁 LinkedIn Post Draft — Project 1: Grid to Chequered Flag

## Teaser Post (Day 1)

---

🏎️ I analyzed every single lap of the 2024 F1 season.

What if you could see things the TV broadcast never shows?

I'm building an open-source F1 data lab — starting with a deep dive into real telemetry, tyre strategies, and race pace.

Here's a preview: [ATTACH: lap_time_distributions.png]

The full interactive analysis drops this week.

🔬 Built with real F1 data via FastF1 + Plotly
💻 Code: github.com/YOUR_USERNAME/f1-lab

#F1 #DataScience #Python #Analytics #Formula1

---

## Deep Dive Post (Day 3-5)

---

🏎️ I built an F1 Race Analytics Dashboard — here are 5 things the data reveals

I pulled real telemetry from every 2024 F1 race and built interactive visualizations. Here's what jumped out:

📊 **1. Consistency ≠ Speed**
McLaren had the most consistent lap times, but Red Bull's median was still faster. The data shows pace vs. reliability isn't as simple as the standings suggest.

🛞 **2. The Soft Tyre Gamble**
Teams that ran softs for 15+ laps consistently lost 0.3s/lap by the end of the stint. The "cliff" is real — and it's predictable.

📈 **3. Grid Position Matters... But Not Always**
At street circuits, starting P1 converted to a win 87% of the time. At power circuits? Only 52%.

🏁 **4. The Undercut Was King in 2024**
In 73% of races, the first driver to pit between positions P2-P5 gained at least one place.

⚡ **5. Speed Traces Don't Lie**
When you overlay VER vs. NOR's fastest laps at Bahrain, the difference isn't straight-line speed — it's corner entry. Max carries 8-12 km/h more into Turn 10.

All visualizations are interactive — zoom in, hover for details, compare drivers.

💻 Full code + interactive charts: github.com/YOUR_USERNAME/f1-lab

What insight surprised you most?

#F1 #DataScience #MachineLearning #Python #DataVisualization #Formula1

---

## Code Drop Post (Day 7)

---

🏎️ Open-sourcing my F1 Race EDA

Last week I shared insights from analyzing the 2024 F1 season. Here's the code behind it.

What's inside:
✅ 6 interactive Plotly visualizations
✅ Real F1 telemetry via FastF1
✅ Custom dark theme designed for data storytelling
✅ Reusable data loader + viz utilities

Getting started is 4 lines of Python:

```python
from shared import F1DataLoader, F1PlotTheme

loader = F1DataLoader()
session = loader.load_session(2024, "Bahrain", "R")
telemetry = loader.get_telemetry(session, "VER", fastest=True)
```

This is Project 1 of 8 in my F1 Data Science series:
1. ✅ Race EDA (this one)
2. 🔜 Tyre Degradation Prediction
3. 🔜 Qualifying Position ML
4. 🔜 Pit Strategy Simulator
5. 🔜 Game Theory of the Undercut
6. 🔜 Championship Monte Carlo
7. 🔜 Deep Learning Telemetry
8. 🔜 RL Race Strategist Agent

⭐ Star the repo if you're interested: github.com/YOUR_USERNAME/f1-lab

#F1 #OpenSource #DataScience #Python #Portfolio #Formula1
