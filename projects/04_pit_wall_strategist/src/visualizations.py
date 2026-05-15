"""
F1 Lab — Project 4: Pit Wall Strategist
Visualizations

Creates Strategy Heatmaps and Race Traces using Plotly.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_strategy_heatmap() -> go.Figure:
    """Creates a heatmap of 1-stop strategies: Soft-Hard vs Medium-Hard etc."""
    df = pd.read_parquet(DATA_DIR / "strategy_sim_results.parquet")
    
    # Filter to 1-stop only
    df1 = df[df["Stops"] == 1].copy()
    
    # Extract the pit lap from the string "[15]" -> 15
    df1["PitLap"] = df1["PitLaps"].str.extract(r"\[(\d+)\]").astype(int)
    
    fig = F1PlotTheme.create_figure(
        title="1-Stop Strategy Landscape (Monza)",
        xaxis_title="Pit Stop Lap",
        yaxis_title="Total Race Time (Delta to Optimal)",
        height=600
    )
    
    # Plot a curve for each compound pair
    colors = {"S-H": "#E8002D", "M-H": "#FFC300", "S-M": "#E8002D", "H-M": "#FFFFFF"}
    
    for compounds in df1["Compounds"].unique():
        subset = df1[df1["Compounds"] == compounds].sort_values("PitLap")
        
        # Determine color based on starting tyre
        color = "#FFFFFF"
        if compounds.startswith("SOFT"): color = "#E8002D"
        elif compounds.startswith("MEDIUM"): color = "#FFC300"
        
        fig.add_trace(go.Scatter(
            x=subset["PitLap"],
            y=subset["DeltaToBest"],
            mode="lines",
            name=compounds,
            line=dict(color=color, width=3),
            hovertemplate="<b>" + compounds + "</b><br>Pit Lap: %{x}<br>Delta: +%{y:.2f}s<extra></extra>"
        ))

    # Add a marker for the absolute optimal
    best = df1.loc[df1["DeltaToBest"].idxmin()]
    fig.add_annotation(
        x=best["PitLap"], y=0,
        text=f"Optimal 1-Stop<br>Lap {best['PitLap']}",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="white",
        ax=0, ay=-40, font=dict(color="white")
    )
        
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_race_trace() -> go.Figure:
    """Plots the cumulative race time of the Best 1-Stop vs Best 2-Stop"""
    top_strats = pd.read_pickle(DATA_DIR / "top_strategies.pkl")
    
    # Get best 1-stop
    best_1 = top_strats[top_strats["Stops"] == 1].iloc[0]
    # Get best 2-stop
    best_2 = top_strats[top_strats["Stops"] == 2].iloc[0]
    
    fig = F1PlotTheme.create_figure(
        title="Optimal 1-Stop vs Optimal 2-Stop Race Trace",
        xaxis_title="Lap Number",
        yaxis_title="Cumulative Race Time (Seconds)",
        height=600
    )
    
    laps = list(range(1, len(best_1["LapTimes"]) + 1))
    
    # We plot the cumulative sum of lap times
    trace_1 = np.cumsum(best_1["LapTimes"])
    trace_2 = np.cumsum(best_2["LapTimes"])
    
    fig.add_trace(go.Scatter(
        x=laps, y=trace_1,
        mode="lines", name="Best 1-Stop",
        line=dict(color="#FFC300", width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=laps, y=trace_2,
        mode="lines", name="Best 2-Stop",
        line=dict(color="#E8002D", width=3, dash="dash")
    ))
    
    # Add vertical lines for pit stops
    import ast
    pit1_laps = ast.literal_eval(best_1["PitLaps"])
    pit2_laps = ast.literal_eval(best_2["PitLaps"])
    
    for pit in pit1_laps:
        fig.add_vline(x=pit, line_width=1, line_dash="dash", line_color="rgba(255, 195, 0, 0.5)")
        
    for pit in pit2_laps:
        fig.add_vline(x=pit, line_width=1, line_dash="dash", line_color="rgba(232, 0, 45, 0.5)")
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print("♟️  Pit Wall Strategist — Generating Visualizations")
    print("=" * 60)

    charts = {
        "strategy_landscape": plot_strategy_heatmap,
        "race_trace": plot_race_trace,
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
