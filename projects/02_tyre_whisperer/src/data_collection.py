"""
F1 Lab — Project 2: The Tyre Whisperer
Data Collection Pipeline

Collects lap-by-lap timing data from multiple 2024 races via FastF1,
cleans it, and produces a unified dataset for degradation modeling.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.data_loader import F1DataLoader
from shared.utils import filter_representative_laps

# ══════════════════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════════════════
SEASON = 2024
DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = DATA_DIR / f"tyre_stints_{SEASON}.parquet"

loader = F1DataLoader()


def collect_race_data(year: int, round_num: int) -> pd.DataFrame | None:
    """
    Collect and clean lap data for a single race.
    Returns a DataFrame with one row per lap, enriched with stint info.
    """
    try:
        session = loader.load_session(year, round_num, "R")
    except Exception as e:
        print(f"  ⚠ Could not load round {round_num}: {e}")
        return None

    laps = loader.get_laps(session)
    weather = loader.get_weather(session)

    if laps.empty:
        return None

    # ── Basic cleaning ────────────────────────────────────────────────────
    df = laps[[
        "Driver", "Team", "LapNumber", "LapTime", "Stint",
        "Compound", "TyreLife", "FreshTyre",
        "Sector1Time", "Sector2Time", "Sector3Time",
        "SpeedI1", "SpeedI2", "SpeedFL", "SpeedST",
        "Position", "PitInTime", "PitOutTime",
        "TrackStatus", "IsAccurate",
    ]].copy()

    # Convert timedeltas to seconds
    for col in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
        if col in df.columns:
            df[f"{col}Sec"] = df[col].dt.total_seconds()

    # ── Filter to representative laps ─────────────────────────────────────
    # Remove pit in/out laps
    df = df[df["PitInTime"].isna() & df["PitOutTime"].isna()]

    # Remove lap 1 (standing start)
    df = df[df["LapNumber"] > 1]

    # Remove safety car / VSC laps (TrackStatus != '1' means non-green)
    if "TrackStatus" in df.columns:
        df = df[df["TrackStatus"].isin(["1", "2"])]  # 1=Green, 2=Yellow (localized)

    # Remove inaccurate laps
    if "IsAccurate" in df.columns:
        df = df[df["IsAccurate"] == True]

    # Remove anomalous times (> 110% of median per driver)
    driver_medians = df.groupby("Driver")["LapTimeSec"].transform("median")
    df = df[df["LapTimeSec"] <= driver_medians * 1.10]
    df = df[df["LapTimeSec"] > 0]

    # ── Add race metadata ─────────────────────────────────────────────────
    df["Season"] = year
    df["Round"] = round_num
    df["EventName"] = session.event["EventName"]
    df["CircuitKey"] = session.event.get("CircuitKey", "")

    # ── Add weather (median for the session) ──────────────────────────────
    if weather is not None and not weather.empty:
        df["TrackTemp"] = weather["TrackTemp"].median()
        df["AirTemp"] = weather["AirTemp"].median()
        df["Humidity"] = weather["Humidity"].median()
        df["WindSpeed"] = weather["WindSpeed"].median()
        df["Rainfall"] = weather["Rainfall"].max() > 0  # Boolean: did it rain?
    else:
        df["TrackTemp"] = np.nan
        df["AirTemp"] = np.nan
        df["Humidity"] = np.nan
        df["WindSpeed"] = np.nan
        df["Rainfall"] = False

    # ── Compute stint-level metrics ───────────────────────────────────────
    # TyreLife is provided by FastF1 (laps on current set)
    # But we also compute tyre age within each stint
    df = df.sort_values(["Driver", "LapNumber"])
    df["TyreAge"] = df.groupby(["Driver", "Stint"]).cumcount() + 1

    # Stint start lap time (baseline for delta calculation)
    stint_baselines = df.groupby(["Driver", "Stint"])["LapTimeSec"].transform("first")
    df["LapTimeDelta"] = df["LapTimeSec"] - stint_baselines

    # Normalized degradation (delta per lap from stint start)
    df["DegPerLap"] = df["LapTimeDelta"] / df["TyreAge"].clip(lower=1)

    # ── Total race laps for fuel estimation ───────────────────────────────
    total_laps = df["LapNumber"].max()
    df["TotalRaceLaps"] = total_laps
    # Fuel load proxy: remaining fuel as fraction (linear burn)
    df["FuelLoad"] = 1.0 - (df["LapNumber"] / total_laps)

    # ── Drop helper columns ───────────────────────────────────────────────
    df = df.drop(columns=["PitInTime", "PitOutTime", "TrackStatus", "IsAccurate",
                           "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"],
                 errors="ignore")

    return df


def collect_season(year: int, max_rounds: int | None = None) -> pd.DataFrame:
    """
    Collect cleaned lap data for an entire season.
    """
    schedule = loader.get_schedule(year)
    all_data = []

    rounds = schedule[schedule["RoundNumber"] > 0]["RoundNumber"].tolist()
    if max_rounds:
        rounds = rounds[:max_rounds]

    for round_num in tqdm(rounds, desc=f"Collecting {year} season data"):
        race_df = collect_race_data(year, round_num)
        if race_df is not None and not race_df.empty:
            all_data.append(race_df)
            print(f"  ✅ Round {round_num}: {race_df['EventName'].iloc[0]} — {len(race_df)} laps")

    if not all_data:
        raise ValueError(f"No data collected for {year}")

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n📊 Total: {len(combined)} clean laps across {len(all_data)} races")

    return combined


def main():
    print("=" * 60)
    print(f"🛞  F1 Lab — Tyre Data Collection ({SEASON})")
    print("=" * 60)

    # Collect first 10 races for initial modeling (can expand later)
    df = collect_season(SEASON, max_rounds=10)

    # Save to parquet for fast loading
    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"\n💾 Saved to: {OUTPUT_PATH}")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Compounds: {df['Compound'].value_counts().to_dict()}")
    print(f"   Avg TyreAge: {df['TyreAge'].mean():.1f} laps")

    return df


if __name__ == "__main__":
    main()
