"""
F1 Lab — Unified Data Loader

Wraps FastF1 and the Jolpica-F1 API to provide a clean, cached interface
for loading real F1 session data, lap times, telemetry, and results.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import fastf1
import pandas as pd

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# Cache configuration
# ══════════════════════════════════════════════════════════════════════════════
_DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"


def _ensure_cache(cache_dir: Path | None = None) -> None:
    """Enable FastF1 caching to avoid re-downloading large telemetry files."""
    cache_path = cache_dir or _DEFAULT_CACHE_DIR
    cache_path.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_path))
    logger.info(f"FastF1 cache enabled at: {cache_path}")


class F1DataLoader:
    """
    Unified loader for real F1 data via FastF1.

    Usage:
        loader = F1DataLoader()
        session = loader.load_session(2024, "Bahrain", "R")
        laps = loader.get_laps(session)
        telemetry = loader.get_telemetry(session, driver="VER")
    """

    def __init__(self, cache_dir: Path | str | None = None):
        _ensure_cache(Path(cache_dir) if cache_dir else None)

    # ──────────────────────────────────────────────────────────────────────
    # Core session loading
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def load_session(
        year: int,
        grand_prix: str | int,
        session_type: Literal["FP1", "FP2", "FP3", "Q", "SQ", "S", "R"] = "R",
    ) -> fastf1.core.Session:
        """
        Load a complete F1 session with all available data.

        Args:
            year: Season year (e.g. 2024)
            grand_prix: Grand Prix name (e.g. "Bahrain") or round number
            session_type: Session identifier —
                FP1/FP2/FP3 = Practice, Q = Qualifying, SQ = Sprint Qualifying,
                S = Sprint, R = Race

        Returns:
            Loaded FastF1 Session object with laps, telemetry, weather, etc.
        """
        logger.info(f"Loading {year} {grand_prix} — {session_type}")
        session = fastf1.get_session(year, grand_prix, session_type)
        session.load()
        logger.info(
            f"Loaded: {session.event['EventName']} | "
            f"{len(session.laps)} laps | "
            f"{len(session.laps['Driver'].unique())} drivers"
        )
        return session

    # ──────────────────────────────────────────────────────────────────────
    # Lap data
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def get_laps(
        session: fastf1.core.Session,
        drivers: list[str] | None = None,
        quick_laps_only: bool = False,
    ) -> pd.DataFrame:
        """
        Extract lap data from a session, optionally filtered by drivers.

        Args:
            session: Loaded FastF1 session
            drivers: List of driver abbreviations (e.g. ["VER", "NOR"])
            quick_laps_only: If True, filters to representative quick laps
                             (excludes pit laps, safety car laps, etc.)

        Returns:
            DataFrame with lap-by-lap timing, compound, tyre life, sector times
        """
        laps = session.laps

        if drivers:
            laps = laps.pick_drivers(drivers)

        if quick_laps_only:
            laps = laps.pick_quicklaps()

        return laps

    # ──────────────────────────────────────────────────────────────────────
    # Telemetry (high-frequency car data)
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def get_telemetry(
        session: fastf1.core.Session,
        driver: str,
        lap_number: int | None = None,
        fastest: bool = False,
    ) -> pd.DataFrame:
        """
        Get high-frequency telemetry for a driver.

        Args:
            session: Loaded FastF1 session
            driver: Driver abbreviation (e.g. "VER")
            lap_number: Specific lap number. If None, returns all laps.
            fastest: If True, returns telemetry for the driver's fastest lap

        Returns:
            DataFrame with Speed, Throttle, Brake, nGear, RPM, DRS, X, Y, Z
        """
        driver_laps = session.laps.pick_drivers(driver)

        if fastest:
            lap = driver_laps.pick_fastest()
            return lap.get_telemetry()

        if lap_number is not None:
            lap = driver_laps[driver_laps["LapNumber"] == lap_number].iloc[0]
            return lap.get_telemetry()

        # All laps telemetry (can be very large!)
        return driver_laps.get_telemetry()

    # ──────────────────────────────────────────────────────────────────────
    # Weather data
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def get_weather(session: fastf1.core.Session) -> pd.DataFrame:
        """
        Get weather data for the session.

        Returns:
            DataFrame with AirTemp, TrackTemp, Humidity, Pressure, WindSpeed, etc.
        """
        return session.weather_data

    # ──────────────────────────────────────────────────────────────────────
    # Results
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def get_results(session: fastf1.core.Session) -> pd.DataFrame:
        """
        Get session results (finishing positions, times, points).

        Returns:
            DataFrame with Position, Driver, Team, Time, Points, Status
        """
        return session.results

    # ──────────────────────────────────────────────────────────────────────
    # Season-level helpers
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def get_schedule(year: int) -> pd.DataFrame:
        """Get the full race schedule for a season."""
        return fastf1.get_event_schedule(year)

    def load_season_races(
        self,
        year: int,
        session_type: Literal["FP1", "FP2", "FP3", "Q", "SQ", "S", "R"] = "R",
        rounds: list[int] | None = None,
    ) -> list[fastf1.core.Session]:
        """
        Load multiple race sessions for an entire season.

        Args:
            year: Season year
            session_type: Which session to load per round
            rounds: Specific round numbers. If None, loads all completed rounds.

        Returns:
            List of loaded Session objects
        """
        schedule = self.get_schedule(year)
        sessions = []

        for _, event in schedule.iterrows():
            round_num = event["RoundNumber"]
            if round_num == 0:  # Skip pre-season testing
                continue
            if rounds and round_num not in rounds:
                continue

            try:
                session = self.load_session(year, round_num, session_type)
                sessions.append(session)
            except Exception as e:
                logger.warning(f"Could not load round {round_num}: {e}")

        logger.info(f"Loaded {len(sessions)} sessions for {year}")
        return sessions
