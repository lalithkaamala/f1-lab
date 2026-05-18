"""
F1 Lab — Project 7: Telemetry Decoder
Visualizations

Generates the Telemetry Fingerprint (Throttle/Brake overlays)
and the Model Confusion Matrix.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme
from shared.constants import DRIVER_NUMBERS

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "projects" / "07_telemetry_decoder" / "models"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_telemetry_fingerprint() -> go.Figure:
    """Overlays the average throttle and brake traces for both drivers."""
    df = pd.read_parquet(DATA_DIR / "telemetry_2026_R1.parquet")
    
    drivers = df["Driver"].unique()
    if len(drivers) != 2:
        print("Need exactly 2 drivers for overlay.")
        return None
        
    driver_A, driver_B = drivers[0], drivers[1]
    
    # Calculate the mean lap for each driver
    # We drop the LapNumber column and groupby Driver to average across all laps
    mean_traces = df.drop(columns=["LapNumber"]).groupby("Driver").mean()
    
    # Extract the distance arrays
    num_points = 300
    dist = np.arange(num_points)
    
    # We'll plot Throttle and Brake
    throttle_A = mean_traces.loc[driver_A, [f"Throttle_{i}" for i in range(num_points)]].values
    throttle_B = mean_traces.loc[driver_B, [f"Throttle_{i}" for i in range(num_points)]].values
    
    brake_A = mean_traces.loc[driver_A, [f"Brake_{i}" for i in range(num_points)]].values
    brake_B = mean_traces.loc[driver_B, [f"Brake_{i}" for i in range(num_points)]].values
    
    color_A = F1PlotTheme.get_team_color(DRIVER_NUMBERS.get(driver_A, {}).get("team", "Unknown"))
    color_B = F1PlotTheme.get_team_color(DRIVER_NUMBERS.get(driver_B, {}).get("team", "Unknown"))
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        subplot_titles=("Throttle Application (%)", "Brake Pressure (%)"))
    
    # Throttle
    fig.add_trace(go.Scatter(x=dist, y=throttle_A, name=driver_A, line=dict(color=color_A, width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=dist, y=throttle_B, name=driver_B, line=dict(color=color_B, width=2)), row=1, col=1)
    
    # Brake
    fig.add_trace(go.Scatter(x=dist, y=brake_A, name=driver_A, showlegend=False, line=dict(color=color_A, width=2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=dist, y=brake_B, name=driver_B, showlegend=False, line=dict(color=color_B, width=2)), row=2, col=1)
    
    fig.update_layout(
        title=f"The Driver Fingerprint: {driver_A} vs {driver_B} (Average Lap)",
        height=700,
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(title_text="Normalized Lap Distance", row=2, col=1)
    fig.update_yaxes(range=[0, 105], showgrid=True, gridcolor="rgba(255,255,255,0.1)", row=1, col=1)
    fig.update_yaxes(range=[0, 105], showgrid=True, gridcolor="rgba(255,255,255,0.1)", row=2, col=1)
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_confusion_matrix() -> go.Figure:
    """Plots the confusion matrix of the Random Forest."""
    with open(MODEL_DIR / "telemetry_metrics.json", "r") as f:
        metrics = json.load(f)
        
    z = metrics["matrix"]
    x = [f"Predicted {c}" for c in metrics["classes"]]
    y = [f"Actual {c}" for c in metrics["classes"]]
    
    annotation_text = [[str(val) for val in row] for row in z]

    fig = ff.create_annotated_heatmap(
        z=z, x=x, y=y,
        annotation_text=annotation_text,
        colorscale="Blues",
        showscale=False
    )
    
    fig.update_layout(
        title=f"Driver Classification Accuracy: {metrics['accuracy']*100:.1f}%",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        margin=dict(t=80, b=40, l=80, r=40),
        xaxis=dict(showgrid=False, side="bottom"),
        yaxis=dict(showgrid=False, autorange="reversed"),
    )
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print("🔍 Telemetry Decoder — Generating Visualizations")
    print("=" * 60)

    charts = {
        "telemetry_fingerprint": plot_telemetry_fingerprint,
        "classification_matrix": plot_confusion_matrix,
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
