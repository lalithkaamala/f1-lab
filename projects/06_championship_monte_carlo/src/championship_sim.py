"""
F1 Lab — Project 6: Championship Monte Carlo
Monte Carlo Simulation Engine

Simulates the remaining 10 races of the 2024 season (post-Spa) 100,000 times
to calculate the exact Championship Win Probabilities.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Simulation Configuration
# ══════════════════════════════════════════════════════════════════════════════
N_SIMULATIONS = 100_000
RACES_REMAINING = 10

# Official F1 Point System for Top 10
POINTS_SYSTEM = np.array([25, 18, 15, 12, 10, 8, 6, 4, 2, 1])

# Current Standings (After Round 14 - Belgium 2024)
DRIVERS = ["VER", "NOR", "LEC", "PIA", "SAI", "HAM", "PER", "RUS"]
CURRENT_POINTS = np.array([277, 199, 177, 167, 162, 150, 131, 116])

# Power Rankings (Estimated from Rounds 10-14 form)
# Mean finish position, StdDev, DNF Probability
# Lower mean is better.
POWER_RANKINGS = {
    "NOR": {"mean": 2.0, "std": 1.2, "dnf_prob": 0.05}, # Fastest car (McLaren)
    "PIA": {"mean": 2.5, "std": 1.5, "dnf_prob": 0.05},
    "VER": {"mean": 3.5, "std": 2.0, "dnf_prob": 0.05}, # Red Bull struggling
    "HAM": {"mean": 3.5, "std": 2.5, "dnf_prob": 0.05}, # Mercedes surging
    "RUS": {"mean": 4.5, "std": 3.0, "dnf_prob": 0.08},
    "LEC": {"mean": 4.5, "std": 2.0, "dnf_prob": 0.05}, # Ferrari inconsistent
    "SAI": {"mean": 5.0, "std": 2.0, "dnf_prob": 0.05},
    "PER": {"mean": 7.5, "std": 3.0, "dnf_prob": 0.10}, # Struggling
}


def simulate_season(n_sims: int) -> pd.DataFrame:
    """
    Run the Monte Carlo simulation using highly optimized numpy vectorization.
    Instead of simulating 1 race at a time, we simulate the entire matrix
    of (100,000 seasons x 10 races x 8 drivers) simultaneously.
    """
    n_drivers = len(DRIVERS)
    
    # Pre-allocate arrays
    means = np.array([POWER_RANKINGS[d]["mean"] for d in DRIVERS])
    stds = np.array([POWER_RANKINGS[d]["std"] for d in DRIVERS])
    dnf_probs = np.array([POWER_RANKINGS[d]["dnf_prob"] for d in DRIVERS])
    
    # Shape: (100_000, 10, 8) -> (simulations, races, drivers)
    # 1. Draw raw performance scores from normal distribution
    print(f"🎲 Rolling dice for {n_sims:,} seasons...")
    raw_performance = np.random.normal(
        loc=means,
        scale=stds,
        size=(n_sims, RACES_REMAINING, n_drivers)
    )
    
    # 2. Apply DNFs (If random uniform < dnf_prob, set performance to infinity)
    # So they finish last
    dnf_rolls = np.random.uniform(0, 1, size=(n_sims, RACES_REMAINING, n_drivers))
    dnf_mask = dnf_rolls < dnf_probs
    raw_performance[dnf_mask] = 999.0 
    
    # 3. Determine race positions
    # Argsort gives the indices of the sorted array (lowest score = P1)
    # We want to map these indices back to points.
    # First, sort the scores to get the rank of each driver (0-indexed, so 0 is P1)
    print("🏁 Resolving race results...")
    race_ranks = np.argsort(np.argsort(raw_performance, axis=2), axis=2)
    
    # 4. Award points
    # Points system is 10 places. We only have 8 drivers, so we just take the first 8.
    points_to_award = min(len(POINTS_SYSTEM), n_drivers)
    padded_points = np.zeros(n_drivers)
    padded_points[:points_to_award] = POINTS_SYSTEM[:points_to_award]
    
    # Map ranks to points
    points_scored = padded_points[race_ranks]
    
    # 5. Sum points across the remaining races for each simulation
    # Shape: (100_000, 8)
    sim_points_gained = np.sum(points_scored, axis=1)
    
    # Add current points
    final_standings = sim_points_gained + CURRENT_POINTS
    
    # 6. Determine Championship Winner for each simulation
    winners_idx = np.argmax(final_standings, axis=1)
    
    # Create results dataframe
    results = pd.DataFrame(final_standings, columns=DRIVERS)
    results["Winner"] = [DRIVERS[idx] for idx in winners_idx]
    
    return results


def main():
    print("=" * 60)
    print(f"🎲 F1 Lab — Championship Monte Carlo")
    print("=" * 60)
    
    results = simulate_season(N_SIMULATIONS)
    
    # Save the raw simulation results
    # We'll save a subset to avoid huge files, or just the summary stats
    # Actually, saving 100k rows x 9 cols is small enough for Parquet
    out_path = DATA_DIR / "championship_simulations.parquet"
    results.to_parquet(out_path, index=False)
    
    # Calculate Probabilities
    win_counts = results["Winner"].value_counts(normalize=True) * 100
    
    print("\n🏆 Championship Win Probabilities:")
    for driver, prob in win_counts.items():
        if prob > 0.01:
            print(f"   {driver}: {prob:5.2f}%")
            
    print(f"\n💾 Saved {N_SIMULATIONS:,} simulation outcomes to {out_path}")


if __name__ == "__main__":
    main()
