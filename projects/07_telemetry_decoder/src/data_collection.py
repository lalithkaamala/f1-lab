"""
F1 Lab — Project 7: Telemetry Decoder
Data Collection (2025 Season)

Pulls high-frequency telemetry data for two specific drivers from
a 2025 race to use as the dataset for our classification model.
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

DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_driver_telemetry(session, driver: str) -> pd.DataFrame:
    """
    Extracts all telemetry laps for a specific driver in a session.
    Interpolates the time series to a standard distance array so laps
    are comparable as feature vectors.
    """
    laps = session.laps.pick_driver(driver).pick_quicklaps()
    
    # We will interpolate all telemetry to exactly 300 distance points per lap
    # This standardizes the length of the time series for ML
    num_points = 300
    all_laps_data = []
    
    for _, lap in laps.iterlaps():
        # Get raw telemetry
        try:
            tel = lap.get_telemetry()
        except:
            continue
            
        if tel.empty:
            continue
            
        # We want to interpolate based on Distance, not Time, because cars 
        # take different amounts of time to complete the same physical distance
        dist_array = np.linspace(tel['Distance'].min(), tel['Distance'].max(), num_points)
        
        # Interpolate the channels we care about
        lap_data = {
            "Driver": driver,
            "LapNumber": lap['LapNumber'],
        }
        
        for channel in ["Speed", "Throttle", "Brake", "nGear"]:
            # Interpolate raw channel data to our standard distance array
            interp_vals = np.interp(dist_array, tel['Distance'], tel[channel])
            
            # Flatten into columns (e.g., Speed_0, Speed_1, ..., Speed_299)
            for i, val in enumerate(interp_vals):
                lap_data[f"{channel}_{i}"] = val
                
        all_laps_data.append(lap_data)
        
    return pd.DataFrame(all_laps_data)


def main():
    print("=" * 60)
    print("🔍 F1 Lab — Telemetry Decoder Data Collection")
    print("=" * 60)
    
    fastf1.Cache.enable_cache(str(PROJECT_ROOT / "data" / "cache"))
    
    # User requested 2025 data! Let's pull Round 1 of 2025 (Australia)
    year = 2025
    round_num = 1
    
    print(f"📡 Fetching 2025 Season, Round {round_num} Race...")
    session = fastf1.get_session(year, round_num, 'R')
    session.load(telemetry=True, laps=True, weather=False)
    
    # Let's compare two teammates with very different driving styles, or two rivals
    # Norris vs Piastri, or Verstappen vs Hamilton (now at Ferrari!)
    driver_A = "VER"
    driver_B = "HAM"
    
    print(f"\n🏎️  Extracting telemetry for {driver_A}...")
    df_A = get_driver_telemetry(session, driver_A)
    
    print(f"🏎️  Extracting telemetry for {driver_B}...")
    df_B = get_driver_telemetry(session, driver_B)
    
    df_final = pd.concat([df_A, df_B], ignore_index=True)
    
    out_path = DATA_DIR / "telemetry_2025_R1.parquet"
    df_final.to_parquet(out_path, index=False)
    
    print(f"\n💾 Saved {len(df_final)} standardized telemetry laps to {out_path}")
    print(f"   Shape: {df_final.shape}")


if __name__ == "__main__":
    main()
