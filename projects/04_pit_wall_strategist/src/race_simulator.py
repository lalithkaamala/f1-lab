"""
F1 Lab — Project 4: Pit Wall Strategist
Race Simulator

A discrete-event physics simulator that models an F1 race.
Uses the pre-trained XGBoost tyre degradation model from Project 2.
To ensure speed for Monte Carlo (10k+ simulations), we pre-compute
the degradation profiles for the specific track conditions.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Models from Project 2
P2_MODEL_DIR = PROJECT_ROOT / "projects" / "02_tyre_whisperer" / "models"


class F1RaceSimulator:
    """Simulates race time given a track profile and a pit strategy."""
    
    def __init__(self, track_profile: dict, fuel_effect: float = 0.065):
        """
        Args:
            track_profile: Dict containing track specifics (base lap time, temp, etc.)
            fuel_effect: Seconds gained per lap of fuel burn
        """
        self.track = track_profile
        self.total_laps = track_profile["TotalLaps"]
        self.pit_loss = track_profile["PitLoss"]
        self.base_lap_time = track_profile["BaseLapTime"]
        self.fuel_effect = fuel_effect
        
        self.model = self._load_degradation_model()
        self.deg_curves = self._precompute_degradation()
        
    def _load_degradation_model(self) -> xgb.XGBRegressor:
        """Load the trained XGBoost model from Project 2."""
        model_path = P2_MODEL_DIR / "xgb_tyre_degradation.json"
        if not model_path.exists():
            raise FileNotFoundError(f"Missing P2 model: {model_path}. Run P2 first.")
            
        model = xgb.XGBRegressor()
        model.load_model(str(model_path))
        return model
        
    def _precompute_degradation(self) -> dict[str, np.ndarray]:
        """
        Pre-compute degradation time loss for ages 1..TotalLaps for each compound.
        This changes inference time from minutes down to milliseconds per 10k races.
        """
        compounds = {
            "SOFT": {"ordinal": 3, "IsSoft": 1, "IsMedium": 0, "IsHard": 0},
            "MEDIUM": {"ordinal": 2, "IsSoft": 0, "IsMedium": 1, "IsHard": 0},
            "HARD": {"ordinal": 1, "IsSoft": 0, "IsMedium": 0, "IsHard": 1},
        }
        
        curves = {}
        max_age = self.total_laps + 5
        
        for name, enc in compounds.items():
            features = pd.DataFrame({
                "TyreAge": np.arange(1, max_age + 1),
                "TyreAgeSq": np.arange(1, max_age + 1) ** 2,
                "CompoundOrdinal": enc["ordinal"],
                "IsSoft": enc["IsSoft"],
                "IsMedium": enc["IsMedium"],
                "IsHard": enc["IsHard"],
                "TyreAge_x_Compound": np.arange(1, max_age + 1) * enc["ordinal"],
                "TrackTemp_x_TyreAge": np.arange(1, max_age + 1) * self.track["TrackTemp"],
                "TrackTemp": self.track["TrackTemp"],
                "AirTemp": self.track["AirTemp"],
                "Humidity": 50.0,
                "WindSpeed": 2.0,
                "FuelLoad": 0, # Model expects FuelLoad, we use a constant since we handle fuel physics ourselves
                "Stint": 1,
                "RollingDegRate": 0.05, # Baseline assumption
                "CircuitAvgDeg": self.track["CircuitAvgDeg"],
                "CircuitStdDeg": 0.5,
            })
            
            # Predict
            preds = self.model.predict(features)
            
            # The model predicts FuelCorrectedDelta. 
            # We enforce monotonically increasing degradation to prevent the XGBoost curve from
            # dipping unrealistically at extreme, unseen tyre ages.
            curves[name] = np.maximum.accumulate(preds)
            
        return curves

    def simulate_race(self, pit_laps: list[int], compounds: list[str]) -> tuple[float, list[float]]:
        """
        Simulate a race given pit laps and tyre compounds.
        
        Args:
            pit_laps: List of lap numbers where the driver pits (e.g. [15, 35])
            compounds: List of compounds for each stint (e.g. ["SOFT", "HARD", "MEDIUM"])
            
        Returns:
            total_race_time (seconds), lap_by_lap_times
        """
        if len(compounds) != len(pit_laps) + 1:
            raise ValueError("Must have one more compound than pit stops.")
            
        lap_times = []
        total_time = 0.0
        
        stint_idx = 0
        tyre_age = 1
        current_compound = compounds[stint_idx]
        
        for lap in range(1, self.total_laps + 1):
            
            # Check if pitting this lap
            if lap in pit_laps:
                stint_idx += 1
                current_compound = compounds[stint_idx]
                tyre_age = 1
                total_time += self.pit_loss
                lap_times[-1] += self.pit_loss # Add pit loss to the in-lap
            
            # 1. Base Time
            lap_time = self.base_lap_time
            
            # 2. Fuel Physics (Add time for fuel weight)
            remaining_laps = self.total_laps - lap
            fuel_penalty = remaining_laps * self.fuel_effect
            lap_time += fuel_penalty
            
            # 3. Tyre Degradation (Lookup pre-computed curve)
            # Clip tyre age to prevent index out of bounds if they don't pit
            safe_age = min(tyre_age, len(self.deg_curves[current_compound]))
            deg_penalty = self.deg_curves[current_compound][safe_age - 1]
            lap_time += deg_penalty
            
            lap_times.append(lap_time)
            total_time += lap_time
            tyre_age += 1
            
        return total_time, lap_times


if __name__ == "__main__":
    # Smoke test
    track_profile = {
        "Name": "Silverstone",
        "TotalLaps": 52,
        "PitLoss": 28.0,
        "BaseLapTime": 88.0,
        "TrackTemp": 35.0,
        "AirTemp": 22.0,
        "CircuitAvgDeg": 1.5,
    }
    
    sim = F1RaceSimulator(track_profile)
    time_1stop, _ = sim.simulate_race([22], ["MEDIUM", "HARD"])
    time_2stop, _ = sim.simulate_race([15, 35], ["SOFT", "MEDIUM", "SOFT"])
    
    print(f"1-Stop Race Time: {time_1stop:.2f}s")
    print(f"2-Stop Race Time: {time_2stop:.2f}s")
    print(f"Delta: {time_1stop - time_2stop:.2f}s")
