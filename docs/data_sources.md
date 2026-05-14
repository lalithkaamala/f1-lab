# 📡 Data Sources

## Overview

All F1 Lab projects use **real Formula 1 data**. No synthetic or dummy data is used anywhere.

---

## Primary Sources

### 1. FastF1 (Python Library)

**What it provides:**
- High-frequency car telemetry (Speed, Throttle, Brake, Gear, DRS, RPM)
- GPS coordinates (X, Y, Z) for track position mapping
- Lap-by-lap timing with sector splits
- Tyre compound and tyre life data
- Weather conditions (air temp, track temp, humidity, wind, rainfall)
- Session results

**Coverage:** 2018–present (telemetry); limited data for earlier seasons

**Usage in F1 Lab:**
```python
from shared import F1DataLoader

loader = F1DataLoader()  # automatically enables cache
session = loader.load_session(2024, "Bahrain", "R")
```

**Important notes:**
- Always use caching (`data/cache/`) to avoid re-downloading large files
- Telemetry data can be 100MB+ per session
- Data becomes available shortly after each real session concludes

---

### 2. Jolpica-F1 API (Ergast Successor)

**What it provides:**
- Historical race results (1950–present)
- Driver & constructor standings
- Circuit information
- Qualifying results
- Pit stop data (from 2012)

**Base URL:** `https://api.jolpi.ca/ergast/f1`

**Coverage:** 1950–present

**Note:** This is the community-maintained replacement for the original Ergast API, which shut down at the end of 2024. FastF1 uses this internally.

---

### 3. OpenF1 API

**What it provides:**
- Real-time timing data
- Race control messages (flags, safety cars, penalties)
- Driver radio transcriptions
- Car location data

**Base URL:** `https://api.openf1.org/v1`

**Coverage:** 2023–present

---

## Data Ethics & Usage

These are community-driven, unofficial data sources. We:
- **Cache aggressively** to minimize server load
- **Do not scrape** any official F1 properties
- Use data for **educational and personal portfolio** purposes
- Comply with each source's terms of use
