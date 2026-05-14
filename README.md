# 🏎️ F1 Lab

**A series of Formula 1 Data Science, Machine Learning, AI & Decision Science projects.**

Built with real F1 telemetry, lap data, and race results from the **2024–2025 seasons** using [FastF1](https://docs.fastf1.dev/), [Jolpica-F1](https://api.jolpi.ca/ergast/f1), and [OpenF1](https://openf1.org/).

---

## 📊 Project Gallery

| # | Project | Discipline | Status |
|---|---------|-----------|--------|
| 1 | [**Grid to Chequered Flag**](projects/01_race_eda/) — Season EDA | Exploratory Data Analysis | 🔧 In Progress |
| 2 | [**The Tyre Whisperer**](projects/02_tyre_whisperer/) — Degradation Modeling | Regression / Time-Series | ⏳ Upcoming |
| 3 | [**Qualifying Prophet**](projects/03_qualifying_prophet/) — Position Prediction | Classification / ML | ⏳ Upcoming |
| 4 | [**Pit Wall Strategist**](projects/04_pit_wall_strategist/) — Strategy Simulation | Monte Carlo / Optimization | ⏳ Upcoming |
| 5 | [**The Undercut Game**](projects/05_undercut_game/) — Strategic Game Theory | Game Theory / Decision Science | ⏳ Upcoming |
| 6 | [**Championship Monte Carlo**](projects/06_championship_monte_carlo/) — Season Simulator | Statistical Modeling | ⏳ Upcoming |
| 7 | [**Telemetry Decoder**](projects/07_telemetry_decoder/) — Driving Style Classification | Deep Learning (LSTM/CNN) | ⏳ Upcoming |
| 8 | [**Virtual Strategist Agent**](projects/08_virtual_strategist_agent/) — AI Race Strategist | Reinforcement Learning | ⏳ Upcoming |

---

## 🛠️ Tech Stack

```
Python 3.12+  ·  FastF1  ·  Plotly  ·  scikit-learn  ·  XGBoost  ·  PyTorch  ·  nashpy
```

| Layer | Tools |
|-------|-------|
| **Data** | FastF1, Jolpica-F1, OpenF1, pandas, polars |
| **ML** | scikit-learn, XGBoost, LightGBM, PyTorch |
| **Viz** | Plotly (interactive), matplotlib (static), kaleido (export) |
| **Decision Science** | nashpy, scipy.optimize, gymnasium |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/f1-lab.git
cd f1-lab

# Install dependencies (with uv)
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Quick Start

```python
from shared import F1DataLoader, F1PlotTheme

# Load real 2024 Bahrain GP data
loader = F1DataLoader()
session = loader.load_session(2024, "Bahrain", "R")

# Get Verstappen's fastest lap telemetry
telemetry = loader.get_telemetry(session, driver="VER", fastest=True)

# Create an interactive visualization
fig = F1PlotTheme.create_figure(title="VER — Fastest Lap Speed Trace")
fig.add_scatter(x=telemetry["Distance"], y=telemetry["Speed"], mode="lines")
fig.show()
```

---

## 📂 Repository Structure

```
f1-lab/
├── shared/                     # Reusable data loaders, viz themes, constants
│   ├── data_loader.py          # FastF1/Jolpica unified data access
│   ├── viz.py                  # Plotly dark theme & export helpers
│   ├── constants.py            # Team colors, driver mappings, compounds
│   └── utils.py                # Common helper functions
├── projects/
│   ├── 01_race_eda/            # Exploratory Data Analysis
│   ├── 02_tyre_whisperer/      # Tyre degradation prediction
│   ├── 03_qualifying_prophet/  # Qualifying position prediction
│   ├── 04_pit_wall_strategist/ # Race strategy simulation
│   ├── 05_undercut_game/       # Game theory analysis
│   ├── 06_championship_mc/     # Championship Monte Carlo
│   ├── 07_telemetry_decoder/   # Deep learning driver ID
│   └── 08_virtual_strategist/  # RL race strategist
├── data/
│   ├── cache/                  # FastF1 cache (gitignored)
│   └── processed/              # Cleaned datasets
└── docs/                       # Methodology & data source docs
```

---

## 📡 Data Sources

All projects use **real Formula 1 data** — no synthetic or dummy data.

| Source | Data Type | Coverage |
|--------|----------|----------|
| [FastF1](https://docs.fastf1.dev/) | Telemetry, laps, weather, tyre data | 2018–present |
| [Jolpica-F1](https://api.jolpi.ca/ergast/f1) | Results, standings, circuits | 1950–present |
| [OpenF1](https://openf1.org/) | Real-time timing, race control | 2023–present |

---

## 📝 LinkedIn Series

Each project is accompanied by a LinkedIn post with interactive visualizations and key insights. Follow along for data-driven F1 analysis:

**[Connect on LinkedIn →](https://linkedin.com/in/YOUR_PROFILE)**

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <em>Built with 🏁 and data by <strong>Lalith Kaamala</strong></em>
</p>
