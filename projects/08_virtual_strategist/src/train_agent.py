"""
F1 Lab — Project 8: Virtual Strategist Agent
Q-Learning Agent

Trains a tabular Q-learning agent to find the optimal pit strategy
by interacting with the F1 environment.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from f1_env import F1Env

DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class QLearningAgent:
    def __init__(self, env: F1Env, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.999, min_epsilon=0.01):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        
        # Q-Table: Map State (Lap, TyreAge) to Action Values [Q(stay), Q(pit)]
        self.q_table = {}
        
    def _get_q(self, state):
        if state not in self.q_table:
            # Initialize extremely pessimistic (negative) so it learns quickly
            self.q_table[state] = np.full(2, -10000.0)
        return self.q_table[state]
        
    def choose_action(self, state):
        # Epsilon-greedy
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice([0, 1])
        else:
            return np.argmax(self._get_q(state))
            
    def learn(self, state, action, reward, next_state):
        current_q = self._get_q(state)[action]
        max_next_q = np.max(self._get_q(next_state))
        
        # Q-Learning Bellman Update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q
        

def train_agent(episodes=20000):
    print("=" * 60)
    print("🤖 F1 Lab — Training Virtual Strategist (Q-Learning)")
    print("=" * 60)
    
    env = F1Env(total_laps=50, pit_loss=25.0)
    agent = QLearningAgent(env)
    
    training_history = []
    
    print(f"Training for {episodes} races...")
    for episode in tqdm(range(episodes)):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            
            agent.learn(state, action, reward, next_state)
            
            state = next_state
            total_reward += reward
            
        # Decay epsilon
        agent.epsilon = max(agent.min_epsilon, agent.epsilon * agent.epsilon_decay)
        
        # Total reward is negative total race time. Convert back to positive time for logging.
        race_time = -total_reward
        training_history.append({"Episode": episode, "RaceTime": race_time, "Epsilon": agent.epsilon})
        
    # Save training history
    history_df = pd.DataFrame(training_history)
    history_df.to_csv(DATA_DIR / "rl_training_history.csv", index=False)
    
    # Run one final evaluation race (Greedy, epsilon=0)
    print("\n🏁 Evaluating Fully Trained Agent...")
    agent.epsilon = 0.0
    state = env.reset()
    done = False
    
    eval_trace = []
    total_time = 0
    
    while not done:
        action = agent.choose_action(state)
        # We also want to know *why* it chose it by looking at the Q-values
        q_vals = agent._get_q(state)
        
        eval_trace.append({
            "Lap": state[0],
            "TyreAge": state[1],
            "Action": "PIT" if action == 1 else "STAY",
            "Q_StayOut": q_vals[0],
            "Q_Pit": q_vals[1]
        })
        
        next_state, reward, done = env.step(action)
        total_time += -reward
        state = next_state
        
    trace_df = pd.DataFrame(eval_trace)
    trace_df.to_csv(DATA_DIR / "rl_evaluation_trace.csv", index=False)
    
    print(f"Final Race Time: {total_time:.2f}s")
    pits = trace_df[trace_df["Action"] == "PIT"]
    if len(pits) > 0:
        print(f"Chosen Pit Laps: {pits['Lap'].tolist()}")
    else:
        print("Agent chose a 0-Stop strategy (Did it fail to learn?)")
        
    print("\n💾 Saved training history and evaluation trace to data/processed")


if __name__ == "__main__":
    train_agent()
