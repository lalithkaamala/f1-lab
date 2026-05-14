"""
F1 Lab — Project 1: Grid to Chequered Flag
Race EDA Analysis Script

Generates interactive Plotly visualizations from real 2024 F1 season data.
All outputs are saved as interactive HTML files in the outputs/ directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add project root to path for shared imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.data_loader import F1DataLoader
from shared.viz import F1PlotTheme
from shared.constants import TEAM_COLORS, COMPOUND_COLORS, TEAM_SHORT
from shared.utils import filter_representative_laps, timedelta_to_seconds

# ══════════════════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════════════════
SEASON = 2024
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

loader = F1DataLoader()


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 1: Lap Time Distributions by Team
# ══════════════════════════════════════════════════════════════════════════════
def plot_lap_time_distributions(session) -> go.Figure:
    """
    Create violin plots showing each team's lap time distribution.
    Reveals pace consistency — are you fast AND reliable?
    """
    laps = loader.get_laps(session)
    laps = filter_representative_laps(laps)
    laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()

    fig = F1PlotTheme.create_figure(
        title=f"Lap Time Distribution by Team — {session.event['EventName']} {SEASON}",
        xaxis_title="Team",
        yaxis_title="Lap Time (seconds)",
        height=650,
    )

    teams = laps["Team"].unique()
    for team in sorted(teams):
        team_laps = laps[laps["Team"] == team]["LapTimeSec"].dropna()
        color = F1PlotTheme.get_team_color(team)
        short_name = TEAM_SHORT.get(team, team)

        fig.add_trace(go.Violin(
            y=team_laps,
            name=short_name,
            box_visible=True,
            meanline_visible=True,
            fillcolor=color,
            line_color="white",
            opacity=0.75,
        ))

    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 2: Position Changes — Grid vs Finish
# ══════════════════════════════════════════════════════════════════════════════
def plot_position_changes(session) -> go.Figure:
    """
    Scatter plot: grid position vs. finish position for every driver.
    Points below the diagonal = gained positions. Above = lost positions.
    """
    results = loader.get_results(session)

    fig = F1PlotTheme.create_figure(
        title=f"Grid → Finish Position — {session.event['EventName']} {SEASON}",
        xaxis_title="Grid Position",
        yaxis_title="Finish Position",
        height=600,
    )

    # Add diagonal reference line (no change)
    fig.add_trace(go.Scatter(
        x=[1, 20], y=[1, 20],
        mode="lines",
        line=dict(color="rgba(255,255,255,0.2)", dash="dash", width=1),
        showlegend=False,
        hoverinfo="skip",
    ))

    for _, row in results.iterrows():
        grid = row.get("GridPosition", None)
        finish = row.get("Position", None)
        driver = row.get("Abbreviation", "?")
        team = row.get("TeamName", "")
        color = F1PlotTheme.get_team_color(team)

        if pd.notna(grid) and pd.notna(finish):
            places_gained = int(grid) - int(finish)
            emoji = "🟢" if places_gained > 0 else "🔴" if places_gained < 0 else "⚪"

            fig.add_trace(go.Scatter(
                x=[int(grid)],
                y=[int(finish)],
                mode="markers+text",
                marker=dict(size=14, color=color, line=dict(width=1, color="white")),
                text=[driver],
                textposition="top center",
                textfont=dict(size=10, color="#FFFFFF"),
                name=driver,
                hovertemplate=(
                    f"<b>{driver}</b><br>"
                    f"Grid: P{int(grid)}<br>"
                    f"Finish: P{int(finish)}<br>"
                    f"Change: {emoji} {abs(places_gained)} places<br>"
                    f"<extra>{team}</extra>"
                ),
                showlegend=False,
            ))

    fig.update_xaxis(range=[0.5, 20.5], dtick=1)
    fig.update_yaxis(range=[0.5, 20.5], dtick=1, autorange="reversed")

    # Annotation
    fig.add_annotation(
        text="↗ Lost positions",
        x=3, y=15, showarrow=False,
        font=dict(color="rgba(232,0,45,0.5)", size=12),
    )
    fig.add_annotation(
        text="↙ Gained positions",
        x=15, y=3, showarrow=False,
        font=dict(color="rgba(82,226,82,0.5)", size=12),
    )

    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 3: Tyre Strategy Visualization
# ══════════════════════════════════════════════════════════════════════════════
def plot_tyre_strategy(session) -> go.Figure:
    """
    Horizontal bar chart showing each driver's tyre strategy —
    which compounds they used and for how many laps.
    """
    laps = loader.get_laps(session)

    # Group consecutive stints
    drivers = laps["Driver"].unique()
    stint_data = []

    for driver in drivers:
        driver_laps = laps[laps["Driver"] == driver].sort_values("LapNumber")
        if driver_laps.empty:
            continue

        # Detect stint changes (compound change = new stint)
        prev_compound = None
        stint_start = None

        for _, lap in driver_laps.iterrows():
            compound = lap.get("Compound", "UNKNOWN")
            lap_num = lap["LapNumber"]

            if compound != prev_compound:
                if prev_compound is not None:
                    stint_data.append({
                        "Driver": driver,
                        "Compound": prev_compound,
                        "Start": stint_start,
                        "End": lap_num - 1,
                        "Length": lap_num - stint_start,
                    })
                stint_start = lap_num
                prev_compound = compound

        # Final stint
        if prev_compound is not None:
            stint_data.append({
                "Driver": driver,
                "Compound": prev_compound,
                "Start": stint_start,
                "End": int(driver_laps["LapNumber"].max()),
                "Length": int(driver_laps["LapNumber"].max()) - stint_start + 1,
            })

    stints_df = pd.DataFrame(stint_data)

    # Sort drivers by finishing position
    results = loader.get_results(session)
    driver_order = results.sort_values("Position")["Abbreviation"].tolist()

    fig = F1PlotTheme.create_figure(
        title=f"Tyre Strategy — {session.event['EventName']} {SEASON}",
        xaxis_title="Lap Number",
        yaxis_title="",
        height=max(500, len(driver_order) * 30),
    )

    for _, stint in stints_df.iterrows():
        color = COMPOUND_COLORS.get(stint["Compound"], "#888888")
        fig.add_trace(go.Bar(
            x=[stint["Length"]],
            y=[stint["Driver"]],
            base=stint["Start"],
            orientation="h",
            marker=dict(color=color, line=dict(color="rgba(0,0,0,0.3)", width=1)),
            name=stint["Compound"],
            showlegend=False,
            hovertemplate=(
                f"<b>{stint['Driver']}</b><br>"
                f"Compound: {stint['Compound']}<br>"
                f"Laps {stint['Start']}–{stint['End']} ({stint['Length']} laps)"
                f"<extra></extra>"
            ),
        ))

    fig.update_yaxis(categoryorder="array", categoryarray=list(reversed(driver_order)))

    # Add compound legend manually
    for compound, color in COMPOUND_COLORS.items():
        if compound in stints_df["Compound"].values:
            fig.add_trace(go.Bar(
                x=[0], y=[""],
                marker=dict(color=color),
                name=compound,
                showlegend=True,
                visible="legendonly" if compound in ("UNKNOWN",) else True,
            ))

    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 4: Championship Points Progression
# ══════════════════════════════════════════════════════════════════════════════
def plot_championship_progression(sessions: list) -> go.Figure:
    """
    Cumulative points over the season — shows momentum shifts.
    Interactive: hover to see gap to leader at each round.
    """
    points_data = []

    for session in sessions:
        results = loader.get_results(session)
        event_name = session.event["EventName"]
        round_num = session.event["RoundNumber"]

        for _, row in results.iterrows():
            driver = row.get("Abbreviation", "?")
            points = row.get("Points", 0)
            team = row.get("TeamName", "")

            points_data.append({
                "Round": round_num,
                "Event": event_name,
                "Driver": driver,
                "Points": float(points) if pd.notna(points) else 0.0,
                "Team": team,
            })

    df = pd.DataFrame(points_data)

    # Cumulative sum per driver
    df = df.sort_values(["Driver", "Round"])
    df["CumulativePoints"] = df.groupby("Driver")["Points"].cumsum()

    # Get top 10 drivers by total points
    totals = df.groupby("Driver")["Points"].sum().nlargest(10)
    top_drivers = totals.index.tolist()

    fig = F1PlotTheme.create_figure(
        title=f"Championship Points Progression — {SEASON}",
        xaxis_title="Round",
        yaxis_title="Cumulative Points",
        height=650,
    )

    for driver in top_drivers:
        driver_df = df[df["Driver"] == driver]
        team = driver_df["Team"].iloc[0] if not driver_df.empty else ""
        color = F1PlotTheme.get_team_color(team)

        fig.add_trace(go.Scatter(
            x=driver_df["Round"],
            y=driver_df["CumulativePoints"],
            mode="lines+markers",
            name=driver,
            line=dict(color=color, width=3),
            marker=dict(size=6),
            hovertemplate=(
                f"<b>{driver}</b><br>"
                "Round %{x}: %{customdata}<br>"
                "Total: %{y} pts"
                "<extra></extra>"
            ),
            customdata=driver_df["Event"],
        ))

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 5: Fastest Lap Speed Trace Comparison
# ══════════════════════════════════════════════════════════════════════════════
def plot_speed_traces(session, drivers: list[str] | None = None) -> go.Figure:
    """
    Overlay speed traces for drivers' fastest laps.
    Corner-by-corner comparison of driving technique.
    """
    if drivers is None:
        # Default: top 3 finishers
        results = loader.get_results(session)
        drivers = results.sort_values("Position")["Abbreviation"].head(3).tolist()

    fig = F1PlotTheme.create_figure(
        title=f"Fastest Lap Speed Traces — {session.event['EventName']} {SEASON}",
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
        height=500,
    )

    for driver in drivers:
        try:
            telemetry = loader.get_telemetry(session, driver=driver, fastest=True)
            team = session.laps.pick_drivers(driver)["Team"].iloc[0]
            color = F1PlotTheme.get_team_color(team)

            fig.add_trace(go.Scatter(
                x=telemetry["Distance"],
                y=telemetry["Speed"],
                mode="lines",
                name=driver,
                line=dict(color=color, width=2),
                hovertemplate=(
                    f"<b>{driver}</b><br>"
                    "Distance: %{x:.0f}m<br>"
                    "Speed: %{y:.0f} km/h"
                    "<extra></extra>"
                ),
            ))
        except Exception as e:
            print(f"  ⚠ Could not load telemetry for {driver}: {e}")

    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Analysis 6: Lap Time Evolution (Race Pace)
# ══════════════════════════════════════════════════════════════════════════════
def plot_lap_time_evolution(session, drivers: list[str] | None = None) -> go.Figure:
    """
    Lap time vs. lap number — shows tyre degradation, pit stops, and pace evolution.
    """
    if drivers is None:
        results = loader.get_results(session)
        drivers = results.sort_values("Position")["Abbreviation"].head(5).tolist()

    laps = loader.get_laps(session, drivers=drivers)
    laps = filter_representative_laps(laps)
    laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()

    fig = F1PlotTheme.create_figure(
        title=f"Lap Time Evolution — {session.event['EventName']} {SEASON}",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        height=550,
    )

    for driver in drivers:
        driver_laps = laps[laps["Driver"] == driver].sort_values("LapNumber")
        if driver_laps.empty:
            continue

        team = driver_laps["Team"].iloc[0]
        color = F1PlotTheme.get_team_color(team)

        fig.add_trace(go.Scatter(
            x=driver_laps["LapNumber"],
            y=driver_laps["LapTimeSec"],
            mode="lines+markers",
            name=driver,
            line=dict(color=color, width=2),
            marker=dict(
                size=5,
                color=[COMPOUND_COLORS.get(c, "#888") for c in driver_laps["Compound"]],
                line=dict(width=1, color=color),
            ),
            hovertemplate=(
                f"<b>{driver}</b><br>"
                "Lap %{x}<br>"
                "Time: %{y:.3f}s<br>"
                "<extra></extra>"
            ),
        ))

    F1PlotTheme.add_f1_watermark(fig)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Main — Run all analyses
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print(f"🏎️  F1 Lab — Project 1: Race EDA ({SEASON} Season)")
    print("=" * 60)

    # ── Load a showcase race ─────────────────────────────────────────────
    print("\n📡 Loading race data (this may take a moment on first run)...")
    race_name = "Bahrain"  # Season opener — great showcase
    session = loader.load_session(SEASON, race_name, "R")

    # ── Generate visualizations ──────────────────────────────────────────
    analyses = [
        ("lap_time_distributions", plot_lap_time_distributions),
        ("position_changes", plot_position_changes),
        ("tyre_strategy", plot_tyre_strategy),
        ("speed_traces", plot_speed_traces),
        ("lap_time_evolution", plot_lap_time_evolution),
    ]

    for name, func in analyses:
        print(f"\n📊 Generating: {name}...")
        try:
            fig = func(session)
            output_path = OUTPUT_DIR / f"{name}.html"
            F1PlotTheme.save_interactive(fig, str(output_path))
            print(f"   ✅ Saved: {output_path}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # ── Championship progression (requires multiple races) ───────────────
    print("\n📊 Generating: championship_progression (loading season data)...")
    try:
        # Load first 5 races for a quick demo
        sessions = loader.load_season_races(SEASON, "R", rounds=[1, 2, 3, 4, 5])
        fig = plot_championship_progression(sessions)
        output_path = OUTPUT_DIR / "championship_progression.html"
        F1PlotTheme.save_interactive(fig, str(output_path))
        print(f"   ✅ Saved: {output_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print(f"🏁 Done! Interactive charts saved to: {OUTPUT_DIR}")
    print("   Open any .html file in your browser to explore.")
    print("=" * 60)


if __name__ == "__main__":
    main()
