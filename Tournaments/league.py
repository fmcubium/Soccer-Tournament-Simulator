import pandas as pd


def simulate(*args: str):
    # PHASE 1: Prepare team data and create a fixture list
    team_codes = {
        "Inter": 1,
        "Milan": 2,
        "Juventus": 3,
        "Atalanta": 4,
        "Bologna": 5,
        "Roma": 6,
        "Lazio": 7,
        "Fiorentina": 8,
        "Torino": 9,
        "Napoli": 10,
    }

    teams = ["Inter", "Milan", "Juventus", "Atalanta", "Bologna", "Roma", "Lazio", "Fiorentina", "Torino", "Napoli",
             "Genoa", "Monza", "Hellas Verona", "Lecce", "Udinese", "Cagliari", "Empoli", "Parma", "Como", "Venezia"]
    opp_codes = []

    # code to test - allows for adding new opponents we haven't seen before
    for team in teams:
        if team_codes.get(team) is None:
            team_codes[team] = len(team_codes) + 1
        opp_codes.append(team_codes[team])

    print(team_codes)
    print(opp_codes)

    # Go through opp codes and match w each other
    matches = []
    for i in range(len(opp_codes)):
        for j in range(len(opp_codes)):
            if i != j:
                matches.append((opp_codes[i], opp_codes[j]))

    print(len(matches))  # should be 380
    print("\n")
    print(matches)

    # PHASE 2: Fit our model using our data - use the data for teams that are in the league

    # PHASE 3: Run predictions and assign points, to determine our league ranking
