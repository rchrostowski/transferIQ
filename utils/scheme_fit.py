import numpy as np
import pandas as pd

# =========================
# CONFIG
# =========================

# These are the team scheme dimensions derived from play-level data
TEAM_SCHEME_FEATURES = [
    "plays_per_game",     # tempo
    "pass_rate",          # offensive balance
    "qb_rush_rate",       # QB usage
    "explosive_rate"      # aggressiveness
]

# These are the player usage features you either
# already have or can approximate
PLAYER_USAGE_FEATURES = {
    "QB": ["pass_rate", "qb_rush_rate"],
    "RB": ["rush_share", "explosive_rate"],
    "WR": ["target_share", "explosive_rate"],
    "TE": ["target_share", "pass_rate"],
    "OL": ["run_block_rate"],
    "DL": ["pressure_rate"],
    "LB": ["tackle_rate"],
    "DB": ["coverage_rate"]
}

# =========================
# CORE FUNCTIONS
# =========================

def normalize(series: pd.Series) -> pd.Series:
    """Z-score normalize with safety."""
    std = series.std()
    if std == 0 or np.isnan(std):
        return series * 0
    return (series - series.mean()) / std


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity safely."""
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.5  # neutral fit
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# =========================
# SCHEME VECTOR BUILDERS
# =========================

def build_team_scheme_vector(team_row: pd.Series) -> np.ndarray:
    """
    Convert a team row into a numeric scheme vector.
    """
    return np.array([
        team_row.get("plays_per_game", 0),
        team_row.get("pass_rate", 0),
        team_row.get("qb_rush_rate", 0),
        team_row.get("explosive_rate", 0)
    ], dtype=float)


def build_player_usage_vector(player_row: pd.Series, position: str) -> np.ndarray:
    """
    Convert a player row into a usage vector aligned to team scheme space.
    Missing features default to 0.
    """
    features = PLAYER_USAGE_FEATURES.get(position, [])

    # Map player usage into the same conceptual space
    vector = []

    for feature in TEAM_SCHEME_FEATURES:
        if feature in features:
            vector.append(player_row.get(feature, 0))
        else:
            vector.append(0)

    return np.array(vector, dtype=float)


# =========================
# MAIN PUBLIC API
# =========================

def compute_scheme_fit(player_row: pd.Series, team_row: pd.Series) -> float:
    """
    Compute scheme fit score between 0 and 1.
    Uses cosine similarity between usage vectors.
    """

    player_vector = build_player_usage_vector(
        player_row,
        player_row.get("position", "")
    )

    team_vector = build_team_scheme_vector(team_row)

    similarity = cosine_similarity(player_vector, team_vector)

    # Bound to [0, 1] for interpretability
    similarity = max(0.0, min(1.0, similarity))

    return similarity


# =========================
# BATCH APPLICATION
# =========================

def apply_scheme_fit(players_df: pd.DataFrame, team_row: pd.Series) -> pd.DataFrame:
    """
    Apply scheme fit to an entire player DataFrame.
    Returns a copy with `scheme_fit` column added.
    """
    df = players_df.copy()

    df["scheme_fit"] = df.apply(
        lambda row: compute_scheme_fit(row, team_row),
        axis=1
    )

    return df
