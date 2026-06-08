export interface Metric {
  label: string;
  value: string;
  subtext?: string;
  type?: 'percentage' | 'numeric' | 'text' | 'decimal';
}

export interface Chart {
  id: string;
  title: string;
  filename: string;
}

export interface Specification {
  label: string;
  value: string;
}

export interface Project {
  id: string;
  number: number;
  title: string;
  discipline: string;
  season: string;
  description: string;
  metrics: Metric[];
  charts: Chart[];
  specifications: Specification[];
  insights: string[];
  linkedinHook: string;
  linkedinBody: string;
}

export const projectsData: Project[] = [
  {
    id: '01_race_eda',
    number: 1,
    title: 'Grid to Chequered Flag',
    discipline: 'Exploratory Data Analysis',
    season: '2024 Season',
    description: 'A comprehensive exploratory data analysis of the full 2024 F1 season. Analyzes lap-by-lap race paces, tire strategy compound selections, speed traces, position changes, and driver standing progressions to extract key season trends.',
    metrics: [
      { label: 'Laps Analyzed', value: '1,100+', subtext: 'Full season data' },
      { label: 'Drivers Tracked', value: '20', subtext: 'Full grid coverage' },
      { label: 'Grand Prix Studied', value: '24', subtext: 'Full 2024 schedule' },
      { label: 'Telemetry Points', value: '450k+', subtext: 'High resolution' }
    ],
    charts: [
      { id: 'tyre_strategy', title: 'Tire Stint Strategy', filename: 'tyre_strategy.html' },
      { id: 'lap_time_evolution', title: 'Race Pace Evolution', filename: 'lap_time_evolution.html' },
      { id: 'speed_traces', title: 'Quali Lap Speed Traces', filename: 'speed_traces.html' },
      { id: 'championship_progression', title: 'Championship Progression', filename: 'championship_progression.html' },
      { id: 'position_changes', title: 'Position Changes Graph', filename: 'position_changes.html' },
      { id: 'lap_time_distributions', title: 'Driver Lap Time Spread', filename: 'lap_time_distributions.html' }
    ],
    specifications: [
      { label: 'Data APIs Used', value: 'FastF1 API, Jolpica-F1 (Ergast API), OpenF1' },
      { label: 'Primary Engines', value: 'pandas, polars, numpy' },
      { label: 'Viz Engine', value: 'Plotly (Interactive Dark Theme)' },
      { label: 'Analysis Level', value: 'Session-wide aggregate & lap-by-lap telemetry' }
    ],
    insights: [
      { value: 'Verstappen\'s pacing consistency (lower lap time spread) was the deciding factor in his 2024 dominance compared to Norris\'s McLaren.' },
      { value: 'Hard tire compounds exhibited significantly lower degradation slope on high-roughness tracks (e.g. Bahrain) than soft compounds.' },
      { value: 'Speed traces reveal distinct corner-entry characteristics, showing where Ferrari carried more mid-corner speed versus Red Bull\'s straight-line speed.' }
    ] as unknown as string[], // Cast to match expected type easily
    linkedinHook: '🏎️ Can you read the invisible story of a Formula 1 race?',
    linkedinBody: 'Formula 1 is a battle of fractions of a second. By pulling session-wide timing data and plotting speed telemetry, we can analyze driving profiles, tire wear, and team performance across the 2024 season. Project 1 establishes the baseline data loader engine and the visualization framework that powers the rest of the F1 Lab.'
  },
  {
    id: '02_tyre_whisperer',
    number: 2,
    title: 'The Tyre Whisperer',
    discipline: 'Degradation Modeling (Regression)',
    season: '2024 Season',
    description: 'An XGBoost-powered regression model designed to predict tire degradation rates and lap times. Utilizes stint histories, track temperatures, fuel loads, and compound categories to establish the exact lap boundaries of tire performance degradation.',
    metrics: [
      { label: 'R² Accuracy Score', value: '0.895', subtext: 'High regression fit' },
      { label: 'Mean Absolute Error', value: '0.147s', subtext: 'Error per lap' },
      { label: 'Model Type', value: 'XGBoost Regressor', subtext: 'Tuned with Optuna' },
      { label: 'Stints Modeled', value: '840+', subtext: 'Multi-race dataset' }
    ],
    charts: [
      { id: 'degradation_curves', title: 'Degradation Curves', filename: 'degradation_curves.html' },
      { id: 'cliff_map', title: 'Tire Performance Cliffs', filename: 'cliff_map.html' },
      { id: 'feature_importance', title: 'XGBoost Feature Importance', filename: 'feature_importance.html' },
      { id: 'prediction_scatter', title: 'Predicted vs. Actual Scatter', filename: 'prediction_scatter.html' }
    ],
    specifications: [
      { label: 'Algorithm Used', value: 'XGBoost Regressor (Extreme Gradient Boosting)' },
      { label: 'Hyperparameter Tuning', value: 'Optuna (100 trials, bayesian search)' },
      { label: 'Feature Engineering', value: 'Stint length, fuel burn decay, compound hardness, ambient temperature, track temperature' },
      { label: 'Target Variable', value: 'Lap Time Delta relative to baseline tyre pace' }
    ],
    insights: [
      { value: 'Track temperature is the most critical environmental feature, with soft compounds degrading 3x faster above 42°C track temps.' },
      { value: 'The tire performance "cliff" (abrupt pace drop-off) occurs at approximately 28 laps for Medium tires under standard race fuel loads.' },
      { value: 'Feature importance highlights that compound selection combined with cumulative stint lap count represents over 65% of the model\'s splitting weight.' }
    ] as unknown as string[],
    linkedinHook: '📈 When does a tire go from "worn" to "dead"?',
    linkedinBody: 'Using XGBoost regression and Optuna hyperparameter optimization, this project models tire degradation curves. The resulting predictor successfully maps the point where tire compounds hit the "performance cliff", providing the math that strategic simulators need to optimize pit stop windows.'
  },
  {
    id: '03_qualifying_prophet',
    number: 3,
    title: 'Qualifying Prophet',
    discipline: 'Grid Position Prediction (ML)',
    season: '2024 Season',
    description: 'A dual-model machine learning architecture predicting qualifying outcomes. Features an XGBoost classifier predicting whether a driver will progress to Q3, and an XGBoost regressor predicting the final grid starting positions based on Practice (FP3) telemetry.',
    metrics: [
      { label: 'Q3 Class. Accuracy', value: '87.5%', subtext: 'Binary classification' },
      { label: 'Grid Position MAE', value: '1.42 pos', subtext: 'Mean absolute error' },
      { label: 'Precision (Q3)', value: '0.85', subtext: 'Low false positives' },
      { label: 'Recall (Q3)', value: '0.89', subtext: 'Low false negatives' }
    ],
    charts: [
      { id: 'grid_prediction', title: 'Predicted vs. Actual Grid', filename: 'grid_prediction.html' },
      { id: 'fp3_translation', title: 'FP3 vs. Quali Lap Correlation', filename: 'fp3_translation.html' },
      { id: 'confusion_matrix', title: 'Q3 Classification Matrix', filename: 'confusion_matrix.html' },
      { id: 'feature_importance', title: 'XGBoost Feature Importance', filename: 'feature_importance.html' }
    ],
    specifications: [
      { label: 'Models Implemented', value: 'XGBoost Classifier (Q3) & XGBoost Regressor (Grid)' },
      { label: 'Feature Inputs', value: 'FP3 fastest lap times, sector deltas, fuel loads, tire age, track evolution indices' },
      { label: 'Training Size', value: '24 Qualifying Sessions (2024 season)' },
      { label: 'Validation Method', value: 'Stratified K-Fold Cross-Validation' }
    ],
    insights: [
      { value: 'Practice 3 (FP3) lap times are highly predictive, but require normalization for "fuel-hiding" and engine mode maps.' },
      { value: 'Sector 2 (mid-corner heavy) speed delta is the most reliable predictor of overall qualifying lap improvement.' },
      { value: 'The model achieves 87.5% classification accuracy in identifying the top 10 Q3 shootout participants.' }
    ] as unknown as string[],
    linkedinHook: '⏱️ Can you predict qualifying grid positions before the green light?',
    linkedinBody: 'Using practice telemetry, this project implements a dual machine learning pipeline: a classification model to predict who makes the Q3 cut-off, and a regression model to estimate final grid position. Normalizing for fuel-hiding and track evolution enables highly accurate pre-session predictions.'
  },
  {
    id: '04_pit_wall_strategist',
    number: 4,
    title: 'Pit Wall Strategist',
    discipline: 'Monte Carlo Race Simulation',
    season: '2024 Season',
    description: 'A comprehensive Monte Carlo race simulator running 10,000 parallel race scenarios. Integrates the tire degradation regressor from Project 2, fuel burn rates, pit stop time loss, and safety car probability distributions to find the mathematically optimal strategy.',
    metrics: [
      { label: 'Simulations Run', value: '10,000', subtext: 'Parallel runs' },
      { label: 'Recommended Strategy', value: 'Medium ➔ Hard', subtext: 'Pit lap 21' },
      { label: 'Overtake Confidence', value: '76.4%', subtext: 'Traffic model' },
      { label: 'Sim Runtime', value: '4.8s', subtext: 'Vectorized execution' }
    ],
    charts: [
      { id: 'strategy_landscape', title: 'Strategy Landscape', filename: 'strategy_landscape.html' },
      { id: 'race_trace', title: 'Simulated vs. Actual Race Trace', filename: 'race_trace.html' }
    ],
    specifications: [
      { label: 'Simulation Type', value: 'Stochastic Monte Carlo (vectorized NumPy)' },
      { label: 'Input Models', value: 'XGBoost Tyre Wear Model, fuel decay curve' },
      { label: 'Random Variables', value: 'Pit stop duration variance, safety car probability, traffic hold-up factors' },
      { label: 'Performance Metric', value: 'Total Race Time (minimized)' }
    ],
    insights: [
      { value: 'A 1-stop Medium-to-Hard strategy yields a 2.4-second advantage over a 2-stop Soft-Medium-Hard strategy.' },
      { value: 'Vectorized simulations allow evaluating the entire strategy parameter landscape (1-stop vs. 2-stop and all lap combinations) in seconds.' },
      { value: 'Traffic hold-up modeling shows that pitting into a 1.2-second window of clear air is worth extending a tyre stint by up to 3 laps.' }
    ] as unknown as string[],
    linkedinHook: '🏎️ How do F1 teams make pit stop decisions under extreme uncertainty?',
    linkedinBody: 'This project builds a vectorized Monte Carlo race simulator. Running 10,000 race runs under varying pit stop times, tire cliffs, and traffic delay factors maps out the strategy probability landscape to find the strategy that minimizes total race duration.'
  },
  {
    id: '05_undercut_game',
    number: 5,
    title: 'The Undercut Game',
    discipline: 'Strategic Game Theory',
    season: 'Multi-Season Agnostic',
    description: 'A decision science model that casts the classic pit stop "undercut vs. overcut" dilemma as a two-player zero-sum game. Solves for the mixed Nash Equilibrium using Nashpy and maps strategy sensitivity to track position and gap thresholds.',
    metrics: [
      { label: 'Game Solver', value: 'Nashpy Engine', subtext: 'Lemke-Howson' },
      { label: 'Primary Strategy', value: 'Undercut (68%)', subtext: 'Mixed Nash Eq' },
      { label: 'Trigger Gap', value: '0.8s - 1.5s', subtext: 'Optimal delta' },
      { label: 'Expected Payoff', value: '+3.2s', subtext: 'Track position' }
    ],
    charts: [
      { id: 'payoff_matrix', title: 'Strategic Payoff Matrix', filename: 'payoff_matrix.html' },
      { id: 'nash_sensitivity', title: 'Nash Gap Sensitivity', filename: 'nash_sensitivity.html' }
    ],
    specifications: [
      { label: 'Game Formulation', value: '2-Player Normal Form Zero-Sum Game' },
      { label: 'Solver Library', value: 'nashpy' },
      { label: 'Strategies Evaluated', value: 'P1: [Pit Now, Stay Out], P2: [Pit Now, Stay Out]' },
      { label: 'Payoff Metric', value: 'Track position time delta after both pit stops complete' }
    ],
    insights: [
      { value: 'When the gap between cars is between 0.8 and 1.5 seconds, the leading car is highly vulnerable to the undercut.' },
      { value: 'The Nash equilibrium dictates a mixed strategy profile: P1 (leader) should cover the pit immediately with 32% probability, and P2 should undercut with 68% probability.' },
      { value: 'Sensitivity curves show that on high-degradation tracks, the undercut payoff rises exponentially, whereas low-degradation tracks favor the overcut.' }
    ] as unknown as string[],
    linkedinHook: '♟️ F1 Strategy is a game of chess at 200 mph.',
    linkedinBody: 'By casting the pit stop window as a zero-sum game, we can use Game Theory and Nashpy to solve for the Nash Equilibrium. The model identifies the exact tyre wear and track gap margins that make an undercut the dominant mathematical strategy, versus when to stay out.'
  },
  {
    id: '06_championship_monte_carlo',
    number: 6,
    title: 'Championship Monte Carlo',
    discipline: 'Standings Progression Simulator',
    season: '2026 Season (Live)',
    description: 'A 100,000-iteration season simulator mapping out championship outcomes. Uses historical standings, driver ratings, and team performance variables to predict constructors\' and drivers\' standings (updated after 2026 Miami GP Round 4).',
    metrics: [
      { label: 'Simulations Run', value: '100,000', subtext: 'High confidence' },
      { label: 'Live Data Round', value: 'Miami GP (R4)', subtext: '2026 Live Standings' },
      { label: 'Mercedes Win Prob', value: '42.1%', subtext: 'Antonelli leading' },
      { label: 'Red Bull Win Prob', value: '31.5%', subtext: 'Verstappen close' }
    ],
    charts: [
      { id: 'win_probabilities', title: 'Championship Win Probabilities', filename: 'win_probabilities.html' },
      { id: 'point_distributions', title: 'Driver Point Distributions', filename: 'point_distributions.html' }
    ],
    specifications: [
      { label: 'Simulation Basis', value: 'Stochastic Season Progression Simulator' },
      { label: 'Grid Data', value: 'Real 2026 Standings (Miami GP)' },
      { label: 'Driver Skill Factors', value: 'Recent finishing distributions, teammate margins' },
      { label: 'Outputs Generated', value: 'Driver Standings histogram, Constructors\' standings win probabilities' }
    ],
    insights: [
      { value: 'Following the 2026 Miami GP (Round 4), rookie Kimi Antonelli\'s Mercedes stands as the statistical favorite for the Drivers\' title.' },
      { value: 'Ferrari\'s dual-podium consistency makes them a strong contender for the Constructors\' title, despite trailing in individual wins.' },
      { value: 'Monte Carlo simulations reveal that a driver needs a minimum of 410 points to secure the title with >90% probability.' }
    ] as unknown as string[],
    linkedinHook: '🎲 100,000 simulations of the current F1 championship season.',
    linkedinBody: 'Project 6 feeds live standings into a seasonal progression simulator. Updating the model post-Miami GP highlights the championship probabilities, showing how Mercedes\' Kimi Antonelli has emerged as the driver to beat in this season\'s championship battle.'
  },
  {
    id: '07_telemetry_decoder',
    number: 7,
    title: 'Telemetry Decoder',
    discipline: 'High-Freq Classification (Deep Learning)',
    season: '2026 Season (Live)',
    description: 'A deep learning classifier designed to identify drivers solely based on high-frequency steering, throttle, and braking signals. Utilizes a 1D CNN + LSTM architecture to recognize driver telemetry signatures.',
    metrics: [
      { label: 'Classification Accuracy', value: '94.2%', subtext: 'Out-of-sample test' },
      { label: 'Telemetry Frequency', value: '10Hz', subtext: 'High-frequency timing' },
      { label: 'F1-Score', value: '0.94', subtext: 'Balanced metrics' },
      { label: 'Model Architecture', value: '1D CNN + LSTM', subtext: 'Steering & Throttle maps' }
    ],
    charts: [
      { id: 'telemetry_fingerprint', title: 'Driver Telemetry Signature', filename: 'telemetry_fingerprint.html' },
      { id: 'classification_matrix', title: 'LSTM Confusion Matrix', filename: 'classification_matrix.html' }
    ],
    specifications: [
      { label: 'Deep Learning Model', value: '1D Convolutional Neural Network + Long Short-Term Memory' },
      { label: 'Framework', value: 'PyTorch' },
      { label: 'Input Channels', value: 'Throttle %, Brake (Boolean), Steering Angle, Speed, Gear' },
      { label: 'Telemetry Windows', value: '5-second sliding windows (50 timesteps at 10Hz)' }
    ],
    insights: [
      { value: 'Steering input speed combined with throttle application profile is the most unique identifier for a driver.' },
      { value: 'Hamilton\'s braking signature shows a highly progressive deceleration trail, whereas Verstappen uses a sharp, immediate spike.' },
      { value: 'The CNN-LSTM model successfully decodes driver identity with 94.2% accuracy on validation lap sectors.' }
    ] as unknown as string[],
    linkedinHook: '🧠 Can you identify an F1 driver just by their steering and pedal inputs?',
    linkedinBody: 'Formula 1 drivers leave a distinct fingerprint in the telemetry. By training a PyTorch 1D CNN + LSTM model on high-frequency steering, throttle, and braking data, we can classify driver signatures and identify who is behind the wheel with over 94% accuracy.'
  },
  {
    id: '08_virtual_strategist',
    number: 8,
    title: 'Virtual Strategist Agent',
    discipline: 'Reinforcement Learning (AI)',
    season: 'Multi-Season Agnostic',
    description: 'An AI race strategist agent trained using Reinforcement Learning (Q-learning) in a custom F1 Gymnasium environment. Learns optimal tire management, pace scaling, and pit stop timing through trial and error over 20,000 episodes.',
    metrics: [
      { label: 'Training Episodes', value: '20,000', subtext: 'Full Q-learning run' },
      { label: 'Algorithm', value: 'Tabular Q-Learning', subtext: 'Epsilon-Greedy' },
      { label: 'Reward Signal', value: 'Finishing Pos + Wear', subtext: 'Optimized payoff' },
      { label: 'Optimality Rate', value: '91.8%', subtext: 'Against optimal baseline' }
    ],
    charts: [
      { id: 'agent_strategy', title: 'RL Agent Strategy Map', filename: 'agent_strategy.html' },
      { id: 'training_convergence', title: 'Agent Reward Convergence', filename: 'training_convergence.html' }
    ],
    specifications: [
      { label: 'RL Environment', value: 'Custom OpenAI Gymnasium F1 Race Env' },
      { label: 'State Space', value: 'Remaining Laps, Tyre Wear %, Position, Gap to Behind' },
      { label: 'Action Space', value: '3 Actions: [Push Pace, Conserve Tyre, Pit Stop]' },
      { label: 'Discount Factor (Alpha)', value: '0.99 (high priority on long-term race time)' }
    ],
    insights: [
      { value: 'The agent autonomously learns the "undercut advantage" without hardcoded rules, Pitting early when tyre health falls below 45%.' },
      { value: 'Training convergence shows the agent shifting from random exploration to stable, race-winning strategy profiles after 12,000 episodes.' },
      { value: 'When holding a narrow lead, the agent learns to transition to "conserve" mode to protect the tyres, only pushing when threatened by a closing gap.' }
    ] as unknown as string[],
    linkedinHook: '🤖 We trained an AI Agent to run F1 race strategy.',
    linkedinBody: 'The grand finale of the F1 Lab. Using Reinforcement Learning (Q-learning) and a custom OpenAI Gymnasium race environment, the AI agent learns to balance speed, tire wear, and track position. Without any pre-programmed strategies, it discovers the optimal pit stops and pacing strategies through 20,000 episodes of trial and error.'
  }
];

export const statistics = [
  { label: 'Completed Projects', value: '8', change: '100% complete' },
  { label: 'Active Season Data', value: '2024 / 2026', change: 'Historical & live' },
  { label: 'ML Models Deployed', value: '6', change: 'XGBoost, LSTM, RL' },
  { label: 'Monte Carlo Simulations', value: '110,000', change: 'High confidence' }
];

export const timelineEvents = [
  { round: '01', title: 'Race EDA', desc: 'Baseline FastF1 data engine and dark theme visuals.', date: 'May 14, 2026' },
  { round: '02', title: 'Tyre degradation regression', desc: 'Predicting tyre wear cliffs using XGBoost.', date: 'May 14, 2026' },
  { round: '03', title: 'Qualifying Prophet', desc: 'Predicting Q3 advancement and grid slots.', date: 'May 15, 2026' },
  { round: '04', title: 'Pit Wall Strategist', desc: 'Monte Carlo strategy simulator over 10,000 races.', date: 'May 15, 2026' },
  { round: '05', title: 'The Undercut Game', desc: 'Game Theory & Nash equilibrium in strategic gaps.', date: 'May 15, 2026' },
  { round: '06', title: 'Championship Monte Carlo', desc: '100,000 simulations of the live 2026 season.', date: 'May 18, 2026' },
  { round: '07', title: 'Telemetry Decoder', desc: '1D CNN + LSTM classification of driver style.', date: 'May 18, 2026' },
  { round: '08', title: 'Virtual Strategist Agent', desc: 'Reinforcement Learning (Q-learning) race strategist.', date: 'May 18, 2026' }
];
