"""
F1 Lab — Project 4: Pit Wall Strategist
Monte Carlo Strategy Optimizer

Generates thousands of strategy permutations and uses the Race Simulator
to find the mathematically optimal pit strategy.
"""

from __future__ import annotations

import sys
import itertools
from pathlib import Path

import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from race_simulator import F1RaceSimulator

DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_1_stop_strategies(total_laps: int) -> list[dict]:
    strategies = []
    compounds = ["SOFT", "MEDIUM", "HARD"]
    
    # Generate all pairs of compounds (must use 2 different compounds per rules)
    for c1, c2 in itertools.product(compounds, repeat=2):
        if c1 == c2: 
            continue # F1 rules mandate using 2 different compounds
            
        # Try pitting on every lap from lap 5 to total_laps - 5
        for pit_lap in range(5, total_laps - 4):
            strategies.append({
                "stops": 1,
                "pit_laps": [pit_lap],
                "compounds": [c1, c2],
                "name": f"1-Stop: {c1[:1]}-{c2[:1]} (L{pit_lap})"
            })
            
    return strategies


def generate_2_stop_strategies(total_laps: int) -> list[dict]:
    strategies = []
    compounds = ["SOFT", "MEDIUM", "HARD"]
    
    # Trios of compounds (at least two must be different)
    for c1, c2, c3 in itertools.product(compounds, repeat=3):
        if c1 == c2 and c2 == c3:
            continue 
            
        # First stop window
        for pit1 in range(8, int(total_laps * 0.6), 2): # Step by 2 to reduce search space
            # Second stop window
            for pit2 in range(pit1 + 10, total_laps - 5, 2):
                strategies.append({
                    "stops": 2,
                    "pit_laps": [pit1, pit2],
                    "compounds": [c1, c2, c3],
                    "name": f"2-Stop: {c1[:1]}-{c2[:1]}-{c3[:1]} (L{pit1}, L{pit2})"
                })
                
    return strategies


def run_monte_carlo(track_profile: dict) -> pd.DataFrame:
    print(f"\n🏎️  Running Strategy Optimizer for {track_profile['Name']}")
    
    sim = F1RaceSimulator(track_profile)
    
    strategies = []
    strategies.extend(generate_1_stop_strategies(track_profile["TotalLaps"]))
    strategies.extend(generate_2_stop_strategies(track_profile["TotalLaps"]))
    
    print(f"Generated {len(strategies)} permutations. Simulating...")
    
    results = []
    for strat in tqdm(strategies, desc="Simulating"):
        total_time, lap_times = sim.simulate_race(strat["pit_laps"], strat["compounds"])
        
        results.append({
            "Strategy": strat["name"],
            "Stops": strat["stops"],
            "Compounds": "-".join(strat["compounds"]),
            "PitLaps": str(strat["pit_laps"]),
            "TotalTime": total_time,
            "LapTimes": lap_times # Save traces for plotting
        })
        
    df = pd.DataFrame(results)
    
    # Calculate delta to the winning strategy
    best_time = df["TotalTime"].min()
    df["DeltaToBest"] = df["TotalTime"] - best_time
    
    # Sort by fastest
    df = df.sort_values("TotalTime").reset_index(drop=True)
    
    print("\n🏆 Top 5 Optimal Strategies:")
    print(df[["Strategy", "TotalTime", "DeltaToBest"]].head(5).to_string())
    
    return df


def main():
    print("=" * 60)
    print("♟️  F1 Lab — Pit Wall Strategist (Monte Carlo)")
    print("=" * 60)

    # Let's run a simulation for the Italian GP (Monza) 
    # Monza: Low degradation, high pit loss, 53 laps
    monza_profile = {
        "Name": "Monza",
        "TotalLaps": 53,
        "PitLoss": 24.0,     # Time lost in pit lane
        "BaseLapTime": 84.0, # 1m24s base pace
        "TrackTemp": 42.0,   # Hot European summer
        "AirTemp": 28.0,
        "CircuitAvgDeg": 1.1, # Relatively low deg
    }
    
    results = run_monte_carlo(monza_profile)
    
    # Save the full results DataFrame
    out_path = DATA_DIR / "strategy_sim_results.parquet"
    
    # Parquet doesn't like Python lists in cells, so we'll drop LapTimes for the main table 
    # but keep the top 100 for visualizations in a separate JSON/Pickle
    main_df = results.drop(columns=["LapTimes"])
    main_df.to_parquet(out_path, index=False)
    
    # Save top 50 1-stops and top 50 2-stops with lap traces for plotting
    top_1 = results[results["Stops"] == 1].head(50)
    top_2 = results[results["Stops"] == 2].head(50)
    top_traces = pd.concat([top_1, top_2])
    top_traces.to_pickle(DATA_DIR / "top_strategies.pkl")
    
    print(f"\n💾 Results saved to {DATA_DIR}")


if __name__ == "__main__":
    main()
