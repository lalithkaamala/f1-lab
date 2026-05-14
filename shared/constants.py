"""
F1 Lab — Constants

Team colors, driver mappings, compound colors, and other reference data
for the 2024–2025 F1 seasons.
"""

# ══════════════════════════════════════════════════════════════════════════════
# Team colors — official hex values (2024–2025 liveries)
# ══════════════════════════════════════════════════════════════════════════════
TEAM_COLORS: dict[str, str] = {
    # 2024-2025 teams
    "Red Bull Racing":   "#3671C6",
    "McLaren":           "#FF8000",
    "Ferrari":           "#E8002D",
    "Mercedes":          "#27F4D2",
    "Aston Martin":      "#229971",
    "Alpine":            "#FF87BC",
    "Williams":          "#64C4FF",
    "RB":                "#6692FF",
    "Haas F1 Team":      "#B6BABD",
    "Sauber":            "#52E252",
    # 2025 rebrand
    "Cadillac":          "#1E1E1E",
}

# Short names for plotting
TEAM_SHORT: dict[str, str] = {
    "Red Bull Racing":   "Red Bull",
    "McLaren":           "McLaren",
    "Ferrari":           "Ferrari",
    "Mercedes":          "Mercedes",
    "Aston Martin":      "Aston Martin",
    "Alpine":            "Alpine",
    "Williams":          "Williams",
    "RB":                "RB",
    "Haas F1 Team":      "Haas",
    "Sauber":            "Sauber",
    "Cadillac":          "Cadillac",
}

# ══════════════════════════════════════════════════════════════════════════════
# Driver numbers & abbreviations (2024–2025)
# ══════════════════════════════════════════════════════════════════════════════
DRIVER_NUMBERS: dict[str, dict[str, str | int]] = {
    "VER": {"name": "Max Verstappen",      "number": 1,  "team": "Red Bull Racing"},
    "PER": {"name": "Sergio Perez",        "number": 11, "team": "Red Bull Racing"},
    "NOR": {"name": "Lando Norris",        "number": 4,  "team": "McLaren"},
    "PIA": {"name": "Oscar Piastri",       "number": 81, "team": "McLaren"},
    "LEC": {"name": "Charles Leclerc",     "number": 16, "team": "Ferrari"},
    "SAI": {"name": "Carlos Sainz",        "number": 55, "team": "Ferrari"},
    "HAM": {"name": "Lewis Hamilton",      "number": 44, "team": "Ferrari"},
    "RUS": {"name": "George Russell",      "number": 63, "team": "Mercedes"},
    "ANT": {"name": "Kimi Antonelli",      "number": 12, "team": "Mercedes"},
    "ALO": {"name": "Fernando Alonso",     "number": 14, "team": "Aston Martin"},
    "STR": {"name": "Lance Stroll",        "number": 18, "team": "Aston Martin"},
    "GAS": {"name": "Pierre Gasly",        "number": 10, "team": "Alpine"},
    "DOO": {"name": "Jack Doohan",         "number": 7,  "team": "Alpine"},
    "ALB": {"name": "Alexander Albon",     "number": 23, "team": "Williams"},
    "SAR": {"name": "Logan Sargeant",      "number": 2,  "team": "Williams"},
    "TSU": {"name": "Yuki Tsunoda",        "number": 22, "team": "RB"},
    "LAW": {"name": "Liam Lawson",         "number": 30, "team": "Red Bull Racing"},
    "RIC": {"name": "Daniel Ricciardo",    "number": 3,  "team": "RB"},
    "MAG": {"name": "Kevin Magnussen",     "number": 20, "team": "Haas F1 Team"},
    "HUL": {"name": "Nico Hulkenberg",     "number": 27, "team": "Sauber"},
    "BEA": {"name": "Oliver Bearman",      "number": 87, "team": "Haas F1 Team"},
    "OCO": {"name": "Esteban Ocon",        "number": 31, "team": "Haas F1 Team"},
    "BOT": {"name": "Valtteri Bottas",     "number": 77, "team": "Sauber"},
    "ZHO": {"name": "Guanyu Zhou",         "number": 24, "team": "Sauber"},
    "BOR": {"name": "Gabriel Bortoleto",   "number": 5,  "team": "Sauber"},
    "COL": {"name": "Franco Colapinto",    "number": 43, "team": "Alpine"},
    "HAD": {"name": "Isack Hadjar",        "number": 6,  "team": "RB"},
}

# ══════════════════════════════════════════════════════════════════════════════
# Tyre compound colors (Pirelli)
# ══════════════════════════════════════════════════════════════════════════════
COMPOUND_COLORS: dict[str, str] = {
    "SOFT":         "#FF3333",
    "MEDIUM":       "#FFC300",
    "HARD":         "#EEEEEE",
    "INTERMEDIATE":  "#43B02A",
    "WET":          "#0067AD",
    "UNKNOWN":      "#888888",
}

# Compound display labels
COMPOUND_LABELS: dict[str, str] = {
    "SOFT":         "S",
    "MEDIUM":       "M",
    "HARD":         "H",
    "INTERMEDIATE":  "I",
    "WET":          "W",
}

# ══════════════════════════════════════════════════════════════════════════════
# Seasons we're analyzing
# ══════════════════════════════════════════════════════════════════════════════
SEASONS = [2024, 2025]

# ══════════════════════════════════════════════════════════════════════════════
# Points systems
# ══════════════════════════════════════════════════════════════════════════════
POINTS_SYSTEM: dict[int, float] = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1,
}

SPRINT_POINTS: dict[int, float] = {
    1: 8, 2: 7, 3: 6, 4: 5, 5: 4,
    6: 3, 7: 2, 8: 1,
}

FASTEST_LAP_BONUS: float = 1.0  # Only if finishing P1–P10
