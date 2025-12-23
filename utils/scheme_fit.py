def compute_scheme_fit(player_position, team_offense):
    if player_position == "QB" and team_offense in ["Spread", "Air Raid"]:
        return 0.9
    if player_position == "RB" and team_offense == "Power":
        return 0.9
    if player_position == "WR" and team_offense == "Air Raid":
        return 0.95
    return 0.7

