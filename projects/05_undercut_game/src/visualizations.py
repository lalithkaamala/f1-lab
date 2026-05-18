"""
F1 Lab — Project 5: The Undercut Game
Visualizations

Creates the Payoff Matrix Heatmap and the Nash Equilibrium Boundary chart.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_payoff_matrix() -> go.Figure:
    """Creates a heatmap of the Leader's Win Probability Matrix."""
    df = pd.read_csv(DATA_DIR / "undercut_payoff_matrix.csv", index_col=0)
    
    # We want rows to be Leader, cols to be Follower
    z = df.values
    x = [col.replace("F_", "") for col in df.columns]
    y = [row.replace("L_", "") for row in df.index]
    
    # Format text for hover
    hovertext = [[f"Leader Win Prob: {val*100:.1f}%" for val in row] for row in z]
    # For annotations, show just the percentage
    annotation_text = [[f"{val*100:.0f}%" for val in row] for row in z]

    fig = ff.create_annotated_heatmap(
        z=z, x=x, y=y,
        annotation_text=annotation_text,
        text=hovertext,
        colorscale=[[0, "#E8002D"], [0.5, "#111111"], [1, "#52E252"]], # Red = Follower wins, Green = Leader wins
        hoverinfo="text"
    )
    
    fig.update_layout(
        title="Undercut Payoff Matrix (Leader's Win Probability)",
        xaxis_title="Follower Pit Lap",
        yaxis_title="Leader Pit Lap",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        margin=dict(t=80, b=40, l=60, r=40),
        xaxis=dict(showgrid=False, side="bottom"),
        yaxis=dict(showgrid=False),
    )
    
    # Add a box around the Nash Equilibrium (we know it's at Lap 23, 23 from our standard run)
    # This is a bit hardcoded for the visualization, but serves the purpose
    fig.add_shape(
        type="rect",
        x0=2.5, x1=3.5, y0=2.5, y1=3.5, # Lap 23 is index 3
        line=dict(color="#FFC300", width=3),
        fillcolor="rgba(0,0,0,0)"
    )
    
    fig.add_annotation(
        x=3, y=3,
        text="Nash<br>Equilibrium",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="#FFC300",
        ax=0, ay=-50, font=dict(color="#FFC300")
    )
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_nash_sensitivity() -> go.Figure:
    """Plots how the Nash Equilibrium shifts as the Undercut gets more powerful."""
    df = pd.read_csv(DATA_DIR / "undercut_sensitivity.csv")
    
    fig = F1PlotTheme.create_figure(
        title="Nash Equilibrium Shift vs. Undercut Power",
        xaxis_title="Undercut Time Delta (Seconds per Lap)",
        yaxis_title="Optimal Pit Lap (Nash Eq)",
        height=500
    )
    
    # Leader and Follower usually have the same optimal lap in this symmetric subgame, 
    # but we plot both to be sure
    fig.add_trace(go.Scatter(
        x=df["Undercut_Delta"], y=df["Leader_Eq_Lap"],
        mode="lines+markers", name="Leader's Strategy",
        line=dict(color="#52E252", width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Undercut_Delta"], y=df["Follower_Eq_Lap"],
        mode="lines+markers", name="Follower's Strategy",
        line=dict(color="#FFC300", width=3, dash="dash"),
        marker=dict(size=6)
    ))
    
    # Add Win Probability on a secondary axis
    fig.add_trace(go.Scatter(
        x=df["Undercut_Delta"], y=df["Leader_Win_Prob"] * 100,
        mode="lines", name="Leader Win Prob (%)",
        line=dict(color="rgba(255,255,255,0.2)", width=2),
        fill="tozeroy", yaxis="y2"
    ))
    
    fig.update_layout(
        yaxis2=dict(
            title="Leader Win Prob (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False
        )
    )
    
    # Reverse primary Y axis so earlier laps are higher up
    fig.update_layout(yaxis=dict(autorange="reversed"))
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print("♟️  The Undercut Game — Generating Visualizations")
    print("=" * 60)

    charts = {
        "payoff_matrix": plot_payoff_matrix,
        "nash_sensitivity": plot_nash_sensitivity,
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
