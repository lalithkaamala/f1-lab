"""
F1 Lab — Visualization Theme

Premium, dark-themed Plotly templates and helper functions for creating
eye-catching, interactive F1 data visualizations.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import plotly.io as pio

from shared.constants import TEAM_COLORS, COMPOUND_COLORS


# ══════════════════════════════════════════════════════════════════════════════
# Custom Plotly Template — "F1 Lab Dark"
# ══════════════════════════════════════════════════════════════════════════════

_F1_DARK_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        # Background
        paper_bgcolor="#0D0D0D",
        plot_bgcolor="#1A1A2E",

        # Typography
        font=dict(
            family="Inter, Roboto, -apple-system, sans-serif",
            size=14,
            color="#E0E0E0",
        ),
        title=dict(
            font=dict(size=24, color="#FFFFFF"),
            x=0.5,
            xanchor="center",
        ),

        # Grid lines — subtle
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.1)",
            title_font=dict(size=13, color="#AAAAAA"),
            tickfont=dict(size=11, color="#888888"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.1)",
            title_font=dict(size=13, color="#AAAAAA"),
            tickfont=dict(size=11, color="#888888"),
        ),

        # Legend
        legend=dict(
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=12, color="#CCCCCC"),
        ),

        # Hover
        hoverlabel=dict(
            bgcolor="rgba(20,20,40,0.95)",
            bordercolor="rgba(255,255,255,0.2)",
            font=dict(size=13, color="#FFFFFF", family="Inter, monospace"),
        ),

        # Color sequence — F1 team-inspired palette
        colorway=[
            "#FF8000",  # McLaren orange
            "#3671C6",  # Red Bull blue
            "#E8002D",  # Ferrari red
            "#27F4D2",  # Mercedes teal
            "#229971",  # Aston Martin green
            "#FF87BC",  # Alpine pink
            "#64C4FF",  # Williams blue
            "#6692FF",  # RB blue
            "#B6BABD",  # Haas silver
            "#52E252",  # Sauber green
        ],

        # Margins
        margin=dict(l=60, r=30, t=80, b=60),
    )
)

# Register the template
pio.templates["f1_dark"] = _F1_DARK_TEMPLATE
pio.templates.default = "f1_dark"


class F1PlotTheme:
    """
    Helper class for creating consistently-styled F1 visualizations.

    All methods return Plotly Figure objects that are interactive,
    dark-themed, and ready for export.
    """

    TEMPLATE = "f1_dark"

    @staticmethod
    def get_team_color(team_name: str) -> str:
        """Get the official hex color for a team."""
        return TEAM_COLORS.get(team_name, "#888888")

    @staticmethod
    def get_compound_color(compound: str) -> str:
        """Get the Pirelli compound color."""
        return COMPOUND_COLORS.get(compound.upper(), "#888888")

    @classmethod
    def create_figure(
        cls,
        title: str = "",
        xaxis_title: str = "",
        yaxis_title: str = "",
        height: int = 600,
        width: int | None = None,
        **kwargs: Any,
    ) -> go.Figure:
        """
        Create a pre-styled Plotly figure with the F1 dark theme.

        Args:
            title: Chart title
            xaxis_title: X-axis label
            yaxis_title: Y-axis label
            height: Figure height in pixels
            width: Figure width (None = responsive)
            **kwargs: Additional layout kwargs

        Returns:
            Styled Plotly Figure
        """
        fig = go.Figure()
        fig.update_layout(
            template=cls.TEMPLATE,
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            height=height,
            width=width,
            **kwargs,
        )
        return fig

    @classmethod
    def style_team_bar_chart(
        cls,
        fig: go.Figure,
        teams: list[str],
    ) -> go.Figure:
        """Apply team colors to a bar chart's traces."""
        for i, team in enumerate(teams):
            if i < len(fig.data):
                fig.data[i].marker.color = cls.get_team_color(team)
        return fig

    @classmethod
    def add_f1_watermark(cls, fig: go.Figure) -> go.Figure:
        """Add a subtle F1 Lab watermark to the bottom-right."""
        fig.add_annotation(
            text="F1 Lab",
            xref="paper", yref="paper",
            x=0.99, y=0.01,
            showarrow=False,
            font=dict(size=10, color="rgba(255,255,255,0.15)"),
            xanchor="right",
            yanchor="bottom",
        )
        return fig

    @classmethod
    def save_interactive(
        cls,
        fig: go.Figure,
        filepath: str,
        auto_open: bool = False,
    ) -> None:
        """Save figure as an interactive HTML file."""
        fig.write_html(
            filepath,
            include_plotlyjs="cdn",
            full_html=True,
            auto_open=auto_open,
            config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                "displaylogo": False,
            },
        )

    @classmethod
    def save_linkedin_image(
        cls,
        fig: go.Figure,
        filepath: str,
        width: int = 1200,
        height: int = 675,  # LinkedIn recommended aspect ratio
        scale: int = 2,  # 2x for retina
    ) -> None:
        """Export a high-res static image optimized for LinkedIn posts."""
        fig.write_image(
            filepath,
            width=width,
            height=height,
            scale=scale,
            format="png",
        )
