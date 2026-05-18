"""
F1 Lab — Project 5: The Undercut Game
Game Theory Model

Builds a payoff matrix for the Leader vs Follower pit strategy decision.
Uses `nashpy` to find the Nash Equilibrium for simultaneous games.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import nashpy as nash

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_payoffs(
    undercut_delta: float = 1.5,
    cliff_penalty: float = 0.5,
    base_leader_win_prob: float = 0.55
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Calculates the payoff matrix (Win Probability) for pitting between Lap 20 and 25.
    
    Args:
        undercut_delta: Seconds gained per lap by pitting for fresh tyres.
        cliff_penalty: Win probability penalty for every lap you pit earlier than optimal (tyre degradation at end of race).
        base_leader_win_prob: The Leader's win probability if both pit on the same lap.
        
    Returns:
        (Leader Matrix, Follower Matrix, pit_laps_list)
    """
    pit_laps = list(range(20, 26))  # Possible pit laps: 20, 21, 22, 23, 24, 25
    n = len(pit_laps)
    
    # Leader's payoff matrix (Win Probability)
    # Rows: Leader's pit lap, Cols: Follower's pit lap
    A = np.zeros((n, n))
    
    for i, l_lap in enumerate(pit_laps):
        for j, f_lap in enumerate(pit_laps):
            
            win_prob = base_leader_win_prob
            
            # 1. Undercut / Overcut Effect
            if l_lap > f_lap:
                # Follower undercut the leader
                laps_undercut = l_lap - f_lap
                # Follower gains time. Leader's win prob drops by e.g. 10% per lap of undercut
                time_gained = laps_undercut * undercut_delta
                win_prob -= (time_gained * 0.08) 
            elif f_lap > l_lap:
                # Leader undercut the follower (defended successfully)
                laps_undercut = f_lap - l_lap
                time_gained = laps_undercut * undercut_delta
                win_prob += (time_gained * 0.08)
                
            # 2. Tyre Life Penalty (Pitting early ruins your tyres at the end)
            # Optimal pit lap is 24. 
            optimal_lap = 24
            
            # Leader penalty
            if l_lap < optimal_lap:
                l_penalty = (optimal_lap - l_lap) * cliff_penalty * 0.1
                win_prob -= l_penalty
                
            # Follower penalty
            if f_lap < optimal_lap:
                f_penalty = (optimal_lap - f_lap) * cliff_penalty * 0.1
                win_prob += f_penalty # If follower burns tyres, leader benefits
                
            # Cap probability between 0 and 1
            A[i, j] = max(0.01, min(0.99, win_prob))
            
    # Zero-sum game: Follower's win prob is 1 - Leader's win prob
    B = 1.0 - A
    
    return A, B, pit_laps


def solve_game(A: np.ndarray, B: np.ndarray, pit_laps: list[int]) -> dict:
    """
    Solves the game using Nashpy.
    """
    # Create the game
    f1_game = nash.Game(A, B)
    
    # Find all Nash Equilibria (using Support Enumeration)
    equilibria = list(f1_game.support_enumeration())
    
    results = []
    for eq in equilibria:
        leader_strat, follower_strat = eq
        
        # Get the highest probability action (for pure or mixed strategies)
        leader_best_idx = np.argmax(leader_strat)
        follower_best_idx = np.argmax(follower_strat)
        
        results.append({
            "Leader_Prob": leader_strat,
            "Follower_Prob": follower_strat,
            "Leader_Best_Lap": pit_laps[leader_best_idx],
            "Follower_Best_Lap": pit_laps[follower_best_idx],
            "Leader_Expected_Value": f1_game[leader_strat, follower_strat][0]
        })
        
    return results[0] if results else None


def main():
    print("=" * 60)
    print("♟️  F1 Lab — The Undercut Game (Game Theory)")
    print("=" * 60)

    # Calculate standard game
    A, B, pit_laps = calculate_payoffs(undercut_delta=1.5, cliff_penalty=0.6)
    
    # Save the payoff matrix for visualization
    df_A = pd.DataFrame(A, index=[f"L_Lap_{l}" for l in pit_laps], columns=[f"F_Lap_{l}" for l in pit_laps])
    df_A.to_csv(DATA_DIR / "undercut_payoff_matrix.csv")
    print("📊 Generated Payoff Matrix (Leader Win Probability):")
    print(df_A.round(2))
    
    # Solve Nash Equilibrium
    eq = solve_game(A, B, pit_laps)
    
    print("\n⚖️  Nash Equilibrium Found:")
    print(f"   Leader Strategy: Pit Lap {eq['Leader_Best_Lap']}")
    print(f"   Follower Strategy: Pit Lap {eq['Follower_Best_Lap']}")
    print(f"   Leader's Expected Win Probability: {eq['Leader_Expected_Value']*100:.1f}%")
    
    # Generate sensitivity analysis for the visualization
    # How does the Nash Eq change as Undercut Power increases?
    sensitivity = []
    for delta in np.arange(0.5, 3.0, 0.1):
        A_sens, B_sens, _ = calculate_payoffs(undercut_delta=delta)
        eq_sens = solve_game(A_sens, B_sens, pit_laps)
        sensitivity.append({
            "Undercut_Delta": delta,
            "Leader_Eq_Lap": eq_sens["Leader_Best_Lap"],
            "Follower_Eq_Lap": eq_sens["Follower_Best_Lap"],
            "Leader_Win_Prob": eq_sens["Leader_Expected_Value"]
        })
        
    pd.DataFrame(sensitivity).to_csv(DATA_DIR / "undercut_sensitivity.csv", index=False)
    print("\n💾 Saved payoff matrix and sensitivity analysis to data/processed")


if __name__ == "__main__":
    main()
