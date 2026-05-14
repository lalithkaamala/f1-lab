"""
F1 Lab — Shared utilities for the Formula 1 Data Science project series.

Provides unified data loading, visualization theming, and constants
across all projects.
"""

from shared.constants import TEAM_COLORS, DRIVER_NUMBERS, COMPOUND_COLORS
from shared.data_loader import F1DataLoader
from shared.viz import F1PlotTheme

__all__ = [
    "TEAM_COLORS",
    "DRIVER_NUMBERS",
    "COMPOUND_COLORS",
    "F1DataLoader",
    "F1PlotTheme",
]
