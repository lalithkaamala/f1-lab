"""
F1 Lab — Project 3: Qualifying Prophet
Feature Engineering

Takes the collected FP and Quali data, and engineers relative pace features.
In F1, absolute lap time doesn't matter (track evolution). 
What matters is your delta to P1 and your delta to your teammate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ══════════════════════════════════════════════════════════════════════════════
# Paths
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR = PROJECT_ROOT / "data" / "processed"
SEASON = 2024


def load_data() -> pd.DataFrame:
    path = DATA_DIR / f"qualifying_data_{SEASON}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Run data_collection.py first: {path}")
    return pd.read_parquet(path)


def engineer_relative_pace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the % delta to the session leader for FP1, FP2, FP3.
    This normalizes lap times across different tracks and changing weather.
    """
    df = df.copy()
    
    for session in ["FP1", "FP2", "FP3"]:
        time_col = f"{session}_Time"
        
        # Get the fastest time in that session for that race
        best_time = df.groupby("EventName")[time_col].transform("min")
        
        # Calculate percentage delta to P1 (e.g., 1.015 = 1.5% slower)
        df[f"{session}_PaceDelta"] = (df[time_col] - best_time) / best_time * 100
        
        # Also track raw delta in seconds
        df[f"{session}_SecDelta"] = df[time_col] - best_time
        
    return df


def engineer_teammate_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the gap between a driver and their teammate.
    This controls for car performance — if the car is bad, can you outdrive it?
    """
    df = df.copy()
    
    for session in ["FP1", "FP2", "FP3"]:
        time_col = f"{session}_Time"
        
        # Get teammate's time (mean of all team times - which is usually just 2 drivers)
        # Using a clever trick: Team Sum - My Time = Teammate Time
        team_sum = df.groupby(["EventName", "Team"])[time_col].transform("sum")
        team_count = df.groupby(["EventName", "Team"])[time_col].transform("count")
        
        # If both drivers set a time
        mask = team_count == 2
        
        df[f"{session}_Teammate_Sec"] = np.nan
        df.loc[mask, f"{session}_Teammate_Sec"] = team_sum[mask] - df.loc[mask, time_col]
        
        # Gap to teammate in seconds (negative means driver is faster)
        df[f"{session}_TeammateGap"] = df[time_col] - df[f"{session}_Teammate_Sec"]
        
    return df


def aggregate_practice_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine FP1, FP2, FP3 into 'overall practice' metrics.
    """
    df = df.copy()
    
    # Best practice pace delta across all sessions
    df["Best_Practice_Delta"] = df[["FP1_PaceDelta", "FP2_PaceDelta", "FP3_PaceDelta"]].min(axis=1)
    
    # FP3 is usually most representative of Quali, let's create an improvement trend
    df["Pace_Improvement_FP2_to_FP3"] = df["FP2_PaceDelta"] - df["FP3_PaceDelta"]
    
    return df


def prepare_modeling_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Prepare final feature matrix."""
    
    # Target variables
    target_class = "Made_Q3"
    target_reg = "Position"
    
    # Drop rows where driver didn't set an FP3 time (crashed, broke down)
    # FP3 is critical for prediction
    model_df = df.dropna(subset=["FP3_PaceDelta"]).copy()
    
    # Fill missing FP1/FP2 with FP3 performance (imputation)
    model_df["FP1_PaceDelta"] = model_df["FP1_PaceDelta"].fillna(model_df["FP3_PaceDelta"])
    model_df["FP2_PaceDelta"] = model_df["FP2_PaceDelta"].fillna(model_df["FP3_PaceDelta"])
    model_df["FP1_TeammateGap"] = model_df["FP1_TeammateGap"].fillna(0)
    model_df["FP2_TeammateGap"] = model_df["FP2_TeammateGap"].fillna(0)
    model_df["FP3_TeammateGap"] = model_df["FP3_TeammateGap"].fillna(0)
    
    feature_cols = [
        "FP1_PaceDelta",
        "FP2_PaceDelta",
        "FP3_PaceDelta",
        "Best_Practice_Delta",
        "Pace_Improvement_FP2_to_FP3",
        "FP1_TeammateGap",
        "FP2_TeammateGap",
        "FP3_TeammateGap",
    ]
    
    print(f"\n📐 Modeling dataset prepared:")
    print(f"   Samples: {len(model_df)}")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target Class: {target_class} ({model_df[target_class].mean()*100:.1f}% positive)")
    print(f"   Target Reg: {target_reg}")
    
    return model_df, feature_cols


def main():
    print("=" * 60)
    print(f"🔮 F1 Lab — Feature Engineering ({SEASON})")
    print("=" * 60)

    df = load_data()
    print(f"📂 Loaded {len(df)} qualifying records")

    df = engineer_relative_pace(df)
    df = engineer_teammate_gaps(df)
    df = aggregate_practice_features(df)
    
    model_df, features = prepare_modeling_dataset(df)

    output_path = DATA_DIR / f"qualifying_features_{SEASON}.parquet"
    model_df.to_parquet(output_path, index=False)
    print(f"\n💾 Saved engineered features to: {output_path}")

    return model_df, features


if __name__ == "__main__":
    main()
