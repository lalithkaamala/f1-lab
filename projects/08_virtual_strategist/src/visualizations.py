"""
F1 Lab — Project 8: Virtual Strategist Agent
Visualizations

Generates the RL Training Convergence curve and the Strategy Evaluation Trace.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_training_curve() -> go.Figure:
    """Line chart showing the agent minimizing race time over 5000 episodes."""
    df = pd.read_csv(DATA_DIR / "rl_training_history.csv")
    
    # Calculate a moving average to smooth the highly noisy exploration phase
    window = 100
    df["SmoothedTime"] = df["RaceTime"].rolling(window=window, min_periods=1).mean()
    
    fig = F1PlotTheme.create_figure(
        title=f"RL Agent Training Convergence (Q-Learning)",
        xaxis_title="Training Episode",
        yaxis_title="Total Race Time (Seconds)",
        height=500
    )
    
    # Plot raw noisy data lightly
    fig.add_trace(go.Scatter(
        x=df["Episode"], y=df["RaceTime"],
        mode="lines", name="Raw Race Time",
        line=dict(color="rgba(255, 255, 255, 0.2)", width=1)
    ))
    
    # Plot smoothed curve
    fig.add_trace(go.Scatter(
        x=df["Episode"], y=df["SmoothedTime"],
        mode="lines", name=f"{window}-Ep Moving Avg",
        line=dict(color="#FFC300", width=3)
    ))
    
    # Add secondary axis for Epsilon decay
    fig.add_trace(go.Scatter(
        x=df["Episode"], y=df["Epsilon"],
        mode="lines", name="Exploration Rate (Epsilon)",
        line=dict(color="#E8002D", width=2, dash="dot"),
        yaxis="y2"
    ))
    
    fig.update_layout(
        yaxis2=dict(
            title="Epsilon (Exploration Rate)",
            overlaying="y",
            side="right",
            range=[0, 1.05],
            showgrid=False
        ),
        legend=dict(x=0.6, y=0.9)
    )
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_agent_strategy() -> go.Figure:
    """Visualizes the agent's chosen strategy and internal Q-values."""
    df = pd.read_csv(DATA_DIR / "rl_evaluation_trace.csv")
    
    # Create a feature that tracks the gap between the Q-values
    # If Q(Pit) is higher than Q(Stay), the agent pits.
    df["Q_Advantage_Pit"] = df["Q_Pit"] - df["Q_StayOut"]
    
    fig = F1PlotTheme.create_figure(
        title="Trained Agent's Internal Decision Brain (Q-Values)",
        xaxis_title="Lap Number",
        yaxis_title="Action Value Advantage: Q(Pit) - Q(Stay Out)",
        height=500
    )
    
    # Plot the Q-Advantage
    # When this line crosses 0, the agent decides to pit
    colors = ["#E8002D" if val > 0 else "#FFFFFF" for val in df["Q_Advantage_Pit"]]
    
    fig.add_trace(go.Bar(
        x=df["Lap"], y=df["Q_Advantage_Pit"],
        marker_color=colors,
        name="Q-Value Advantage"
    ))
    
    # Add horizontal line at 0 (Decision Boundary)
    fig.add_hline(y=0, line_width=2, line_color="#52E252", line_dash="dash", annotation_text="Pit Decision Threshold")
    
    # Add markers for actual pit stops
    pit_laps = df[df["Action"] == "PIT"]["Lap"].tolist()
    for pit in pit_laps:
        fig.add_vline(x=pit, line_width=1, line_color="#FFC300")
        fig.add_annotation(
            x=pit, y=df["Q_Advantage_Pit"].max() * 0.8,
            text="Agent Pits",
            showarrow=False, font=dict(color="#FFC300")
        )
        
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print("🤖 Virtual Strategist — Generating Visualizations")
    print("=" * 60)

    charts = {
        "training_convergence": plot_training_curve,
        "agent_strategy": plot_agent_strategy,
    }

    for name, fn in charts.items():
        print(f"\n📊 Generating: {name}...")
        try:
            fig = fn()
            if fig is not None:
                path = OUTPUT_DIR / f"{name}.html"
                F1PlotTheme.save_interactive(fig, str(path))
                print(f"   ✅ Saved: {path}")
        except Exception as e:
            print(f"   ❌ {e}")

    print(f"\n🏁 Done! Charts in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
