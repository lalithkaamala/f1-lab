"""
F1 Lab — Project 2: The Tyre Whisperer
Visualizations

Interactive Plotly charts for tyre degradation analysis.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.viz import F1PlotTheme
from shared.constants import COMPOUND_COLORS, TEAM_COLORS

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SEASON = 2024


def plot_degradation_curves(df: pd.DataFrame) -> go.Figure:
    """Degradation curves by compound — the signature chart."""
    fig = F1PlotTheme.create_figure(
        title=f"Tyre Degradation Curves — {SEASON} Season",
        xaxis_title="Tyre Age (laps)",
        yaxis_title="Fuel-Corrected Lap Time Delta (s)",
        height=600,
    )

    for compound in ["SOFT", "MEDIUM", "HARD"]:
        cdf = df[df["Compound"] == compound]
        if cdf.empty:
            continue
        color = COMPOUND_COLORS[compound]

        # Aggregate: mean + std per tyre age
        agg = cdf.groupby("TyreAge")["FuelCorrectedDelta"].agg(["mean", "std", "count"])
        agg = agg[agg["count"] >= 5]  # Need enough samples
        agg["std"] = agg["std"].fillna(0)

        # Confidence band
        fig.add_trace(go.Scatter(
            x=list(agg.index) + list(agg.index[::-1]),
            y=list(agg["mean"] + agg["std"]) + list((agg["mean"] - agg["std"])[::-1]),
            fill="toself", fillcolor=color.replace(")", ",0.15)").replace("rgb", "rgba")
            if "rgb" in color else f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)",
            line=dict(width=0), showlegend=False, hoverinfo="skip",
        ))

        # Mean line
        fig.add_trace(go.Scatter(
            x=agg.index, y=agg["mean"],
            mode="lines+markers",
            name=compound,
            line=dict(color=color, width=3),
            marker=dict(size=4, color=color),
            hovertemplate=(
                f"<b>{compound}</b><br>"
                "Age: %{x} laps<br>"
                "Delta: %{y:.3f}s<br>"
                "<extra></extra>"
            ),
        ))

    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_feature_importance(metrics_path: Path | None = None) -> go.Figure:
    """Horizontal bar chart of XGBoost feature importance."""
    if metrics_path is None:
        metrics_path = MODEL_DIR / "metrics.json"
    with open(metrics_path) as f:
        metrics = json.load(f)

    importance = metrics.get("xgboost", {}).get("feature_importance", {})
    if not importance:
        raise ValueError("No feature importance data found in metrics.json")

    # Sort by importance
    sorted_feats = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    names = [f[0] for f in sorted_feats]
    values = [f[1] for f in sorted_feats]

    # Color gradient
    n = len(names)
    colors = [f"rgba(255,{int(128 + 127*(i/n))},{0},0.85)" for i in range(n)]

    fig = F1PlotTheme.create_figure(
        title="Feature Importance — What Drives Tyre Degradation?",
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


def plot_prediction_scatter(test_preds_path: Path | None = None) -> go.Figure:
    """Predicted vs. Actual scatter plot — model accuracy check."""
    if test_preds_path is None:
        test_preds_path = DATA_DIR / f"tyre_test_preds_{SEASON}.parquet"
    df = pd.read_parquet(test_preds_path)

    fig = F1PlotTheme.create_figure(
        title="Predicted vs. Actual Degradation (Test Set)",
        xaxis_title="Actual Δ Lap Time (s)",
        yaxis_title="Predicted Δ Lap Time (s)",
        height=600,
    )

    # Perfect prediction line
    min_val = min(df["FuelCorrectedDelta"].min(), df["Predicted"].min())
    max_val = max(df["FuelCorrectedDelta"].max(), df["Predicted"].max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val], y=[min_val, max_val],
        mode="lines", line=dict(color="rgba(255,255,255,0.3)", dash="dash"),
        showlegend=False, hoverinfo="skip",
    ))

    for compound in ["SOFT", "MEDIUM", "HARD"]:
        cdf = df[df["Compound"] == compound]
        if cdf.empty:
            continue
        fig.add_trace(go.Scatter(
            x=cdf["FuelCorrectedDelta"], y=cdf["Predicted"],
            mode="markers",
            name=compound,
            marker=dict(
                color=COMPOUND_COLORS[compound], size=5, opacity=0.6,
                line=dict(width=0.5, color="white"),
            ),
            hovertemplate=(
                f"<b>{compound}</b><br>"
                "Actual: %{x:.3f}s<br>"
                "Predicted: %{y:.3f}s<br>"
                "<extra></extra>"
            ),
        ))

    F1PlotTheme.add_f1_watermark(fig)
    return fig


def plot_cliff_map(cliff_path: Path | None = None) -> go.Figure:
    """Heatmap: cliff lap by circuit × compound."""
    if cliff_path is None:
        cliff_path = DATA_DIR / f"tyre_cliffs_{SEASON}.parquet"
    cliff_df = pd.read_parquet(cliff_path)

    cliff_only = cliff_df[cliff_df["HasCliff"]].copy()
    if cliff_only.empty:
        print("  ⚠ No cliff events detected — skipping heatmap")
        return None

    pivot = cliff_only.pivot_table(
        index="EventName", columns="Compound",
        values="CliffLap", aggfunc="mean",
    ).reindex(columns=["SOFT", "MEDIUM", "HARD"])

    fig = F1PlotTheme.create_figure(
        title="The Cliff Map — When Do Tyres Fall Off?",
        height=max(400, len(pivot) * 35),
    )

    fig.add_trace(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0, "#E8002D"],    # Early cliff (red/danger)
            [0.5, "#FFC300"],  # Mid cliff (yellow)
            [1, "#52E252"],    # Late cliff (green/safe)
        ],
        text=np.round(pivot.values, 1),
        texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{y}</b><br>%{x}: Lap %{z:.1f}<extra></extra>",
        colorbar=dict(title="Cliff Lap", tickfont=dict(color="#AAAAAA")),
    ))

    F1PlotTheme.add_f1_watermark(fig)
    return fig


def main():
    print("=" * 60)
    print(f"🛞  Tyre Whisperer — Generating Visualizations")
    print("=" * 60)

    # Load feature data
    df = pd.read_parquet(DATA_DIR / f"tyre_features_{SEASON}.parquet")

    charts = {
        "degradation_curves": lambda: plot_degradation_curves(df),
        "feature_importance": plot_feature_importance,
        "prediction_scatter": plot_prediction_scatter,
        "cliff_map": plot_cliff_map,
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
