import requests
import pandas as pd

BASE = "https://api.collegefootballdata.com"

def get_fbs_teams():
    teams = requests.get(f"{BASE}/teams/fbs").json()
    return pd.DataFrame(teams)[["school", "conference"]]

def get_team_stats(team, year=2023):
    url = f"{BASE}/stats/season"
    params = {"year": year, "team": team}
    r = requests.get(url, params=params).json()

    stats = {s["statName"]: float(s["statValue"]) for s in r}

    return {
        "plays_per_game": stats.get("plays", 0) / 12 if stats.get("plays") else None,
        "pass_rate": stats.get("passAttempts", 0) / max(stats.get("plays", 1), 1),
        "qb_rush_rate": stats.get("qbRushAttempts", 0) / max(stats.get("rushAttempts", 1), 1),
        "explosive_rate": stats.get("explosivePlays", 0) / max(stats.get("plays", 1), 1)
    }

def build_scheme_table(year=2023):
    teams = get_fbs_teams()
    rows = []

    for _, row in teams.iterrows():
        team = row["school"]
        try:
            stats = get_team_stats(team, year)
            rows.append({
                "team": team,
                "conference": row["conference"],
                **stats
            })
        except Exception:
            continue

    df = pd.DataFrame(rows)

    # Normalize for scoring
    for col in ["plays_per_game", "pass_rate", "qb_rush_rate", "explosive_rate"]:
        df[col] = (df[col] - df[col].mean()) / df[col].std()

    return df

if __name__ == "__main__":
    df = build_scheme_table()
    df.to_csv("data/teams.csv", index=False)
    print("teams.csv built successfully")

