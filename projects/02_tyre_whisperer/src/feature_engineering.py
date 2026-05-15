"""
F1 Lab — Project 2: The Tyre Whisperer
Feature Engineering

Takes the collected lap data and engineers features specifically
designed for tyre degradation modeling.
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


def load_stint_data() -> pd.DataFrame:
    """Load the collected stint data from parquet."""
    path = DATA_DIR / f"tyre_stints_{SEASON}.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"No data found at {path}. Run data_collection.py first."
        )
    return pd.read_parquet(path)


def estimate_fuel_correction(df: pd.DataFrame, fuel_effect_per_lap: float = 0.065) -> pd.DataFrame:
    """
    Apply fuel correction to lap times.

    F1 cars carry ~110kg of fuel. Each kg ≈ 0.035s/lap slower.
    Over a 57-lap race, that's roughly 0.065s/lap gained from burning fuel.
    We ADD this back to early laps to isolate tyre degradation.

    Args:
        df: DataFrame with LapTimeSec and LapNumber columns
        fuel_effect_per_lap: Seconds gained per lap from fuel burn (default 0.065)

    Returns:
        DataFrame with FuelCorrectedLapTime column
    """
    df = df.copy()

    # Fuel correction: early laps are faster due to lighter car at end
    # We normalize all laps as if the car had a constant fuel load
    remaining_laps = df["TotalRaceLaps"] - df["LapNumber"]
    df["FuelCorrection"] = remaining_laps * fuel_effect_per_lap
    df["FuelCorrectedLapTimeSec"] = df["LapTimeSec"] + df["FuelCorrection"]

    # Recalculate delta using fuel-corrected times
    stint_baselines = df.groupby(["Driver", "Stint", "Round"])[
        "FuelCorrectedLapTimeSec"
    ].transform("first")
    df["FuelCorrectedDelta"] = df["FuelCorrectedLapTimeSec"] - stint_baselines

    return df


def encode_compound(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode tyre compound as ordinal and one-hot features.
    Softer compounds degrade faster (higher ordinal = softer).
    """
    df = df.copy()

    compound_order = {"HARD": 1, "MEDIUM": 2, "SOFT": 3, "INTERMEDIATE": 4, "WET": 5}
    df["CompoundOrdinal"] = df["Compound"].map(compound_order).fillna(0).astype(int)

    # One-hot for the main dry compounds
    for compound in ["SOFT", "MEDIUM", "HARD"]:
        df[f"Is{compound.capitalize()}"] = (df["Compound"] == compound).astype(int)

    return df


def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction features that capture compound-specific degradation.
    """
    df = df.copy()

    # Tyre age × compound interaction (softs degrade differently than hards)
    df["TyreAge_x_Compound"] = df["TyreAge"] * df["CompoundOrdinal"]

    # Tyre age squared (non-linear degradation / cliff effect)
    df["TyreAgeSq"] = df["TyreAge"] ** 2

    # Track temp × tyre age (hotter = faster degradation)
    df["TrackTemp_x_TyreAge"] = df["TrackTemp"].fillna(35) * df["TyreAge"]

    # Stint number (later stints may have different deg characteristics)
    # Already have "Stint" column

    # Rolling degradation rate (slope of last 3 laps)
    df = df.sort_values(["Driver", "Round", "LapNumber"])
    df["RollingDegRate"] = (
        df.groupby(["Driver", "Stint", "Round"])["FuelCorrectedDelta"]
        .transform(lambda x: x.rolling(window=3, min_periods=2).apply(
            lambda w: np.polyfit(range(len(w)), w, 1)[0] if len(w) >= 2 else 0
        ))
    )
    df["RollingDegRate"] = df["RollingDegRate"].fillna(0)

    return df


def add_circuit_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add circuit-level aggregates as features.
    Different tracks stress tyres differently.
    """
    df = df.copy()

    # Average degradation rate per circuit (from historical data in this dataset)
    circuit_deg = df.groupby("EventName")["FuelCorrectedDelta"].agg(
        CircuitAvgDeg="mean",
        CircuitStdDeg="std",
    ).reset_index()

    df = df.merge(circuit_deg, on="EventName", how="left")

    return df


def prepare_modeling_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], str]:
    """
    Prepare the final feature matrix for modeling.

    Returns:
        (DataFrame, feature_column_names, target_column_name)
    """
    feature_cols = [
        # Tyre state
        "TyreAge",
        "TyreAgeSq",
        "CompoundOrdinal",
        "IsSoft",
        "IsMedium",
        "IsHard",

        # Interactions
        "TyreAge_x_Compound",
        "TrackTemp_x_TyreAge",

        # Environmental
        "TrackTemp",
        "AirTemp",
        "Humidity",
        "WindSpeed",

        # Fuel
        "FuelLoad",

        # Stint context
        "Stint",
        "RollingDegRate",

        # Circuit
        "CircuitAvgDeg",
        "CircuitStdDeg",
    ]

    target_col = "FuelCorrectedDelta"

    # Drop rows with missing target or features
    model_df = df.dropna(subset=[target_col] + feature_cols)

    # Remove extreme outliers in target (> 3 std from mean per compound)
    for compound in model_df["Compound"].unique():
        mask = model_df["Compound"] == compound
        mean = model_df.loc[mask, target_col].mean()
        std = model_df.loc[mask, target_col].std()
        model_df = model_df[~(mask & (model_df[target_col].abs() > mean + 3 * std))]

    print(f"\n📐 Modeling dataset prepared:")
    print(f"   Samples: {len(model_df)}")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target: {target_col}")
    print(f"   Compounds: {model_df['Compound'].value_counts().to_dict()}")

    return model_df, feature_cols, target_col


def main():
    print("=" * 60)
    print(f"🛞  F1 Lab — Feature Engineering ({SEASON})")
    print("=" * 60)

    # Load raw data
    df = load_stint_data()
    print(f"📂 Loaded {len(df)} laps")

    # Apply transformations
    df = estimate_fuel_correction(df)
    df = encode_compound(df)
    df = add_interaction_features(df)
    df = add_circuit_features(df)

    # Prepare for modeling
    model_df, features, target = prepare_modeling_dataset(df)

    # Save engineered dataset
    output_path = DATA_DIR / f"tyre_features_{SEASON}.parquet"
    model_df.to_parquet(output_path, index=False)
    print(f"\n💾 Saved engineered features to: {output_path}")

    return model_df, features, target


if __name__ == "__main__":
    main()
