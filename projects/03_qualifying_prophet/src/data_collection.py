"""
F1 Lab — Project 3: Qualifying Prophet
Data Collection Pipeline

Collects Free Practice (FP1, FP2, FP3) pace and Qualifying results.
Excludes Sprint weekends for a consistent FP1/FP2/FP3 -> Quali mapping.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import fastf1
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.data_loader import F1DataLoader

# ══════════════════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════════════════
SEASON = 2024
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = DATA_DIR / f"qualifying_data_{SEASON}.parquet"

loader = F1DataLoader()


def get_fastest_laps(session) -> pd.DataFrame:
    """Extract each driver's absolute fastest lap in a session."""
    if session is None:
        return pd.DataFrame()
    
    laps = loader.get_laps(session)
    if laps.empty:
        return pd.DataFrame()
    
    # Get absolute fastest lap for each driver
    fastest = laps.loc[laps.groupby("Driver")["LapTime"].idxmin().dropna()]
    
    df = fastest[["Driver", "Team", "LapTime", "Compound"]].copy()
    df["LapTimeSec"] = df["LapTime"].dt.total_seconds()
    return df.drop(columns=["LapTime"])


def collect_race_weekend(year: int, round_num: int) -> pd.DataFrame | None:
    """Collect FP1, FP2, FP3 and Quali data for a single standard weekend."""
    try:
        # Check if it's a sprint weekend by trying to load FP3
        # If FastF1 raises an error or it's named 'Sprint', we skip.
        event = fastf1.get_event(year, round_num)
        if event.get("EventFormat") == "sprint":
            print(f"  ⏭️ Skipping Round {round_num} (Sprint weekend format)")
            return None
            
        print(f"  📥 Fetching Round {round_num}: {event['EventName']}...")
        
        # Load sessions
        fp1 = loader.load_session(year, round_num, "FP1")
        fp2 = loader.load_session(year, round_num, "FP2")
        fp3 = loader.load_session(year, round_num, "FP3")
        quali = loader.load_session(year, round_num, "Q")
        
        # Extract fastest laps
        df_fp1 = get_fastest_laps(fp1)
        df_fp2 = get_fastest_laps(fp2)
        df_fp3 = get_fastest_laps(fp3)
        
        if df_fp1.empty or df_fp2.empty or df_fp3.empty:
            print(f"  ⚠ Missing practice data for Round {round_num}")
            return None
            
        # Get qualifying results
        quali_results = loader.get_results(quali)
        
        # Merge everything together
        # Base dataframe is all drivers in Quali
        df = quali_results[["Abbreviation", "TeamName", "Position", "Q1", "Q2", "Q3"]].copy()
        df = df.rename(columns={"Abbreviation": "Driver", "TeamName": "Team"})
        
        # Rename columns before merging
        df_fp1 = df_fp1.rename(columns={"LapTimeSec": "FP1_Time", "Compound": "FP1_Compound"})
        df_fp2 = df_fp2.rename(columns={"LapTimeSec": "FP2_Time", "Compound": "FP2_Compound"})
        df_fp3 = df_fp3.rename(columns={"LapTimeSec": "FP3_Time", "Compound": "FP3_Compound"})
        
        df = df.merge(df_fp1[["Driver", "FP1_Time", "FP1_Compound"]], on="Driver", how="left")
        df = df.merge(df_fp2[["Driver", "FP2_Time", "FP2_Compound"]], on="Driver", how="left")
        df = df.merge(df_fp3[["Driver", "FP3_Time", "FP3_Compound"]], on="Driver", how="left")
        
        # Convert Q1/Q2/Q3 to seconds
        for col in ["Q1", "Q2", "Q3"]:
            df[f"{col}_Time"] = pd.to_timedelta(df[col]).dt.total_seconds()
            
        # Target: Fastest Quali Time overall for that driver
        df["Quali_Time"] = df[["Q1_Time", "Q2_Time", "Q3_Time"]].min(axis=1)
        
        # Target Class: Made Q3
        df["Made_Q3"] = df["Position"] <= 10
        
        # Metadata
        df["Season"] = year
        df["Round"] = round_num
        df["EventName"] = event["EventName"]
        
        return df.drop(columns=["Q1", "Q2", "Q3"])
        
    except Exception as e:
        print(f"  ⚠ Error processing Round {round_num}: {e}")
        return None


def collect_season(year: int) -> pd.DataFrame:
    """Collect practice and quali data for all standard weekends in a season."""
    schedule = loader.get_schedule(year)
    all_data = []

    rounds = schedule[schedule["RoundNumber"] > 0]["RoundNumber"].tolist()
    
    # FastF1 takes time to load 4 sessions per weekend, so be patient
    for round_num in tqdm(rounds, desc=f"Collecting {year} Quali data"):
        df = collect_race_weekend(year, round_num)
        if df is not None and not df.empty:
            all_data.append(df)
            print(f"  ✅ Round {round_num} processed ({len(df)} drivers)")

    if not all_data:
        raise ValueError(f"No data collected for {year}")

    combined = pd.concat(all_data, ignore_index=True)
    return combined


def main():
    print("=" * 60)
    print(f"🔮 F1 Lab — Qualifying Prophet Data Collection ({SEASON})")
    print("=" * 60)

    # Collect season data
    df = collect_season(SEASON)

    # Save to parquet
    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"\n💾 Saved to: {OUTPUT_PATH}")
    print(f"   Shape: {df.shape}")
    print(f"   Races: {df['Round'].nunique()} (Sprint weekends excluded)")
    
    return df


if __name__ == "__main__":
    main()
