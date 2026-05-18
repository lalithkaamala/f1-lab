"""
F1 Lab — Project 8: Virtual Strategist Agent
F1 Racing Environment

A custom Markov Decision Process (MDP) representing an F1 race.
The agent must learn to balance tyre degradation and pit-loss penalties.
"""

import numpy as np

class F1Env:
    """
    A minimal RL environment for an F1 pit strategy.
    
    State: (Lap_Number, Tyre_Age)
    Actions: 0 (Stay Out), 1 (Pit)
    Reward: -1 * (Lap Time)
    """
    
    def __init__(self, total_laps=50, base_pace=90.0, pit_loss=25.0):
        self.total_laps = total_laps
        self.base_pace = base_pace
        self.pit_loss = pit_loss
        
        self.lap = 1
        self.tyre_age = 1
        
    def reset(self):
        """Reset the environment to the start of the race."""
        self.lap = 1
        self.tyre_age = 1
        return (self.lap, self.tyre_age)
        
    def _calculate_lap_time(self, action):
        """
        Calculates lap time based on physics.
        Degradation is non-linear (tyres fall off a cliff after ~20 laps).
        """
        # Baseline lap time
        lap_time = self.base_pace
        
        # Action 1: Pit
        if action == 1:
            lap_time += self.pit_loss
            # Tyre age resets *after* this lap is completed
            
        # Add degradation penalty
        deg_penalty = 0.015 * (self.tyre_age ** 1.8)
        lap_time += deg_penalty
        
        return lap_time
        
    def step(self, action):
        """
        Take an action, return (next_state, reward, done).
        """
        if self.lap > self.total_laps:
            return (self.lap, self.tyre_age), 0.0, True
            
        # Calculate lap time based on action
        lap_time = self._calculate_lap_time(action)
        
        # Reward is negative lap time (we want to minimize time / maximize reward)
        reward = -lap_time
        
        # State transitions
        self.lap += 1
        if action == 1:
            self.tyre_age = 1  # Fresh tyres!
        else:
            self.tyre_age += 1
            
        done = (self.lap > self.total_laps)
        next_state = (self.lap, self.tyre_age)
        
        return next_state, reward, done
