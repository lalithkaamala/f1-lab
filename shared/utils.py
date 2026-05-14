"""
F1 Lab — Common Utilities

Helper functions used across multiple projects.
"""

from __future__ import annotations

import pandas as pd
import numpy as np


def timedelta_to_seconds(td: pd.Timedelta | None) -> float | None:
    """Convert a pandas Timedelta to total seconds (float)."""
    if td is None or pd.isna(td):
        return None
    return td.total_seconds()


def format_laptime(seconds: float) -> str:
    """
    Format lap time in seconds to M:SS.mmm string.

    Example: 83.456 → "1:23.456"
    """
    if seconds is None or np.isnan(seconds):
        return "—"
    minutes = int(seconds // 60)
    remainder = seconds - (minutes * 60)
    return f"{minutes}:{remainder:06.3f}"


def gap_to_leader(
    laps_df: pd.DataFrame,
    time_col: str = "LapTime",
) -> pd.Series:
    """
    Calculate the gap to the fastest lap time in the DataFrame.

    Returns:
        Series of deltas in seconds
    """
    fastest = laps_df[time_col].min()
    return (laps_df[time_col] - fastest).dt.total_seconds()


def normalize_driver_name(abbrev: str) -> str:
    """Normalize driver abbreviation to uppercase 3-letter code."""
    return abbrev.strip().upper()[:3]


def filter_representative_laps(laps_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to representative laps by removing:
    - Pit in/out laps
    - Safety car laps
    - First lap of the race (formation effects)
    - Laps with anomalous times (>107% of median)
    """
    filtered = laps_df.copy()

    # Remove pit laps
    if "PitInTime" in filtered.columns:
        filtered = filtered[filtered["PitInTime"].isna()]
    if "PitOutTime" in filtered.columns:
        filtered = filtered[filtered["PitOutTime"].isna()]

    # Remove lap 1 (standing start effects)
    if "LapNumber" in filtered.columns:
        filtered = filtered[filtered["LapNumber"] > 1]

    # Remove anomalous laps (>107% of session median)
    if "LapTime" in filtered.columns:
        lap_seconds = filtered["LapTime"].dt.total_seconds()
        median_time = lap_seconds.median()
        if not pd.isna(median_time):
            filtered = filtered[lap_seconds <= median_time * 1.07]

    return filtered
