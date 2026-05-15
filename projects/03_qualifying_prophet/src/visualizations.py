"""
F1 Lab — Project 3: Qualifying Prophet
Visualizations

Interactive Plotly charts for the qualifying predictions.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SEASON = 2024


def plot_feature_importance() -> go.Figure:
    metrics_path = MODEL_DIR / "metrics.json"
    with open(metrics_path) as f:
        metrics = json.load(f)

    # Let's use the classifier's feature importance
    importance = metrics.get("classification", {}).get("feature_importance", {})
    
    sorted_feats = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    names = [f[0].replace("_", " ") for f in sorted_feats]
    values = [f[1] for f in sorted_feats]

    n = len(names)
    colors = [f"rgba(147, 51, 234, {0.9 - i*0.05})" for i in range(n)]  # Purple gradient

    fig = F1PlotTheme.create_figure(
        title="Feature Importance — What Predicts Q3?",
        xaxis_title="Importance Score",
        height=500,
    )

    fig.add_trace(go.Bar(
        x=values, y=names,
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.2)", width=1)),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
    ))

    fig.update_yaxes(autorange="reversed")
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_confusion_matrix() -> go.Figure:
    metrics_path = MODEL_DIR / "metrics.json"
    with open(metrics_path) as f:
        metrics = json.load(f)

    cm = metrics.get("classification", {}).get("confusion_matrix", [[0,0],[0,0]])
    cm = np.array(cm)
    
    z = cm[::-1]
    x = ["Predicted OUT", "Predicted Q3"]
    y = ["Actual Q3", "Actual OUT"]
    
    # Calculate percentages for hover
    total = np.sum(cm)
    hovertext = [[f"{val} ({val/total*100:.1f}%)" for val in row] for row in z]

    fig = ff.create_annotated_heatmap(
        z=z, x=x, y=y,
        annotation_text=z,
        text=hovertext,
        colorscale=[[0, "#111111"], [1, "#9333ea"]],
        hoverinfo="text"
    )
    
    fig.update_layout(
        title="Q3 Prediction Confusion Matrix (Test Set)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        margin=dict(t=80, b=40, l=40, r=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_grid_prediction_scatter() -> go.Figure:
    df = pd.read_parquet(DATA_DIR / f"quali_test_preds_{SEASON}.parquet")

    fig = F1PlotTheme.create_figure(
        title="Predicted vs. Actual Grid Position",
        xaxis_title="Actual Position",
        yaxis_title="Predicted Position",
        height=600,
    )

    # Perfect prediction line
    fig.add_trace(go.Scatter(
        x=[1, 20], y=[1, 20],
        mode="lines", line=dict(color="rgba(255,255,255,0.3)", dash="dash"),
        showlegend=False, hoverinfo="skip",
    ))

    # Calculate error to color the points
    df["Error"] = abs(df["Position"] - df["Predicted_Grid"])
    
    fig.add_trace(go.Scatter(
        x=df["Position"], y=df["Predicted_Grid"],
        mode="markers",
        marker=dict(
            color=df["Error"],
            colorscale=[[0, "#52E252"], [0.5, "#FFC300"], [1, "#E8002D"]],
            size=10, 
            opacity=0.7,
            line=dict(width=1, color="white"),
            showscale=True,
            colorbar=dict(title="Error (Pos)")
        ),
        text=df["Driver"] + " (" + df["EventName"] + ")",
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Actual: P%{x}<br>"
            "Predicted: P%{y}<br>"
            "Off by: %{marker.color} places"
            "<extra></extra>"
        ),
    ))
    
    fig.update_xaxes(autorange="reversed")
    fig.update_yaxes(autorange="reversed")

    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_fp3_translation() -> go.Figure:
    """Scatter of FP3 Pace Delta vs Actual Qualifying Position"""
    df = pd.read_parquet(DATA_DIR / f"qualifying_features_{SEASON}.parquet")

    fig = F1PlotTheme.create_figure(
        title="FP3 Pace Translation to Qualifying",
        xaxis_title="FP3 Pace Delta to Leader (%)",
        yaxis_title="Actual Grid Position",
        height=600,
    )

    # Color by team
    for team in df["Team"].unique():
        team_df = df[df["Team"] == team]
        color = F1PlotTheme.get_team_color(team)
        
        fig.add_trace(go.Scatter(
            x=team_df["FP3_PaceDelta"],
            y=team_df["Position"],
            mode="markers",
            name=team,
            marker=dict(color=color, size=8, line=dict(width=0.5, color="white")),
            text=team_df["Driver"] + " (" + team_df["EventName"] + ")",
            hovertemplate=(
                "<b>%{text}</b><br>"
                "FP3 Delta: +%{x:.2f}%<br>"
                "Grid: P%{y}<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_yaxes(autorange="reversed")
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print(f"🔮 Qualifying Prophet — Generating Visualizations")
    print("=" * 60)

    charts = {
        "feature_importance": plot_feature_importance,
        "confusion_matrix": plot_confusion_matrix,
        "grid_prediction": plot_grid_prediction_scatter,
        "fp3_translation": plot_fp3_translation,
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
