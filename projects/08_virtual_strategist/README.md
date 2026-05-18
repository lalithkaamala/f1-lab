# 🤖 Project 8: Virtual Strategist Agent (Grand Finale)

**Discipline:** Reinforcement Learning & AI  
**Seasons:** Agnostic  

---

## 🎯 Objective

In Project 4, we used a Monte Carlo brute-force search to find the optimal pit strategy by testing 10,000 combinations. 

But what if we could train an AI agent to *learn* strategy the same way a human does—through trial and error? 

For the grand finale of the `f1-lab` series, we build a **Reinforcement Learning (RL)** agent. We drop the AI into a custom F1 simulation environment, let it race thousands of times, and watch as it learns from scratch that pitting for fresh tyres is necessary to win.

---

## 🧠 Methodology

### 1. The Custom F1 Environment (`f1_env.py`)
We built a custom Markov Decision Process (MDP) environment following the OpenAI Gym standard.
- **State Space:** `(Lap_Number, Tyre_Age)`
- **Action Space:** `0 = Stay Out`, `1 = Pit`
- **Reward Function:** The negative lap time. Driving fast yields a small negative reward. Driving slow on dead tyres yields a massive negative reward. Pitting yields a massive negative reward (the pit loss penalty), but resets Tyre Age to 0.

### 2. Q-Learning Algorithm (`train_agent.py`)
We train a tabular Q-Learning agent:
- **Exploration (Epsilon-Greedy):** Initially, the agent takes random actions, discovering that pitting is even an option.
- **Exploitation:** Over 5,000 episodes, it updates its Q-Table, mapping the optimal action for every possible State.
- It organically learns the exact lap to pit that minimizes its total race time.

### 3. Visualizations
- **Reward Convergence:** A line chart showing the agent's total race time plummeting as it learns how to race.
- **The Agent's Strategy:** A visualization of the exact lap-by-lap decisions made by the fully trained agent.

---

## 🚀 How to Run

```bash
cd projects/08_virtual_strategist

# Train the AI and watch it learn
python src/train_agent.py
python src/visualizations.py
```

---

## 📂 Structure

```
08_virtual_strategist/
├── README.md
├── src/
│   ├── f1_env.py              # The simulated race environment
│   ├── train_agent.py         # The Q-Learning loop
│   └── visualizations.py      # Training curves & policy maps
├── outputs/                   
└── linkedin_post.md
```
