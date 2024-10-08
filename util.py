# For utility functions that will be widely used in the project

import pandas as pd


def define_result(result):
    match result:
        case 'W':
            return 2
        case 'D':
            return 1
        case _:
            return 0


def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()  # closed ensures no future data
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)

    return group


def rolling_averages_2(group, cols, new_cols):
    group = group.sort_values("date_code")
    rolling_stats = group[cols].rolling(3, closed='left').mean()  # closed ensures no future data
    group[new_cols] = rolling_stats
    group = group.fillna(0)

    return group


class MissingDict(dict):
    __missing__ = lambda self, key: key


def fix_team_names(df: pd.DataFrame):
    map_values = {
        # Serie A
        "Internazionale": "Inter",

        # EPL
        "Nott'ham Forest": "Nottingham Forest",
        "Brighton and Hove Albion": "Brighton",
        "Manchester City": "Man City",
        "Manchester United": "Man Utd",
        "Newcastle United": "Newcastle Utd",
        "Tottenham Hotspur": "Tottenham",
        "West Ham United": "West Ham",
        "Wolverhampton Wanderers": "Wolves",

        # La Liga
        "AlmerÃa": "Almeria",
        "AtlÃ©tico Madrid": "Atletico Madrid",
        "AlavÃ©s": "Alaves",
        "CÃ¡diz": "Cadiz",

        # Bundesliga
        "Eintracht Frankfurt": "Eint Frankfurt",
        "KÃ¶ln": "Koln",
        "DÃ¼sseldorf": "Dusseldorf",

        # Ligue 1
        "Paris Saint Germain": "Paris S-G"
    }

    mapping = MissingDict(**map_values)
    df["team"] = df["team"].map(mapping)
    df["opponent"] = df["opponent"].map(mapping)

def fix_team_names_list(teams: list):
    map_values = {
        # Serie A
        "Internazionale": "Inter",

        # EPL
        "Nott'ham Forest": "Nottingham Forest",
        "Brighton and Hove Albion": "Brighton",
        "Manchester City": "Man City",
        "Manchester United": "Man Utd",
        "Newcastle United": "Newcastle Utd",
        "Tottenham Hotspur": "Tottenham",
        "West Ham United": "West Ham",
        "Wolverhampton Wanderers": "Wolves",

        # La Liga
        "AlmerÃa": "Almeria",
        "AtlÃ©tico Madrid": "Atletico Madrid",
        "AlavÃ©s": "Alaves",
        "CÃ¡diz": "Cadiz",

        # Bundesliga
        "Eintracht Frankfurt": "Eint Frankfurt",
        "KÃ¶ln": "Koln",
        "DÃ¼sseldorf": "Dusseldorf",

        # Ligue 1
        "Paris Saint Germain": "Paris S-G"
    }

    for i in range(len(teams)):
        if teams[i] in map_values:
            teams[i] = map_values[teams[i]]
