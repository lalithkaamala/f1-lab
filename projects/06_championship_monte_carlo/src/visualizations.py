"""
F1 Lab — Project 6: Championship Monte Carlo
Visualizations

Generates Probability Distributions of final championship points.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_win_probabilities() -> go.Figure:
    """Bar chart of Championship Win Probabilities."""
    df = pd.read_parquet(DATA_DIR / "championship_simulations.parquet")
    
    # Calculate probabilities
    probs = df["Winner"].value_counts(normalize=True) * 100
    probs = probs[probs > 0.1] # Filter out the <0.1% miracles
    
    fig = F1PlotTheme.create_figure(
        title="Drivers' Championship Win Probability (100k Simulations)",
        xaxis_title="Driver",
        yaxis_title="Probability (%)",
        height=500
    )
    
    from shared.constants import DRIVER_NUMBERS
    colors = [F1PlotTheme.get_team_color(DRIVER_NUMBERS.get(d, {}).get("team", "Unknown")) for d in probs.index]
    
    fig.add_trace(go.Bar(
        x=probs.index,
        y=probs.values,
        marker=dict(color=colors, line=dict(color="white", width=1)),
        text=[f"{v:.1f}%" for v in probs.values],
        textposition='auto',
    ))
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_point_distributions() -> go.Figure:
    """Density plots (KDE) of the final points for the top contenders."""
    df = pd.read_parquet(DATA_DIR / "championship_simulations.parquet")
    
    # We'll plot the top 4 contenders
    top_drivers = df["Winner"].value_counts().head(4).index.tolist()
    
    hist_data = [df[driver].values for driver in top_drivers]
    group_labels = top_drivers
    from shared.constants import DRIVER_NUMBERS
    colors = [F1PlotTheme.get_team_color(DRIVER_NUMBERS.get(d, {}).get("team", "Unknown")) for d in top_drivers]
    
    fig = ff.create_distplot(
        hist_data, group_labels, 
        colors=colors,
        show_hist=False, # Just the KDE lines
        show_rug=False
    )
    
    fig.update_layout(
        title="Projected Final Championship Points Distribution",
        xaxis_title="Total Points",
        yaxis_title="Density",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        legend=dict(x=0.85, y=0.95),
        height=600
    )
    
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print("🎲 Championship Monte Carlo — Generating Visualizations")
    print("=" * 60)

    charts = {
        "win_probabilities": plot_win_probabilities,
        "point_distributions": plot_point_distributions,
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
