import copy

from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd


def create_fixtures(opp_codes: list):
    opp_codes_clone = copy.deepcopy(opp_codes)
    first_round = []
    rng = np.random.default_rng()

    half = len(opp_codes_clone) // 2
    rng.shuffle(opp_codes_clone)

    # split the teams into halves so we can run circle method:
    # https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    left = opp_codes_clone[:half]
    right = opp_codes_clone[half:][::-1]
    for i in range(len(opp_codes_clone) - 1):
        # pair
        matchweek = list(zip(left, right))

        # rotate - 1st in right goes to 2nd in left, last in left becomes last in right
        left.insert(1, right.pop(0))
        right.append(left.pop())

        # add matchweek to fixture list
        first_round.append(matchweek)

    second_round = [[(away, home) for (home, away) in day] for day in first_round]

    # shuffle both rounds and return them together
    rng.shuffle(first_round)
    rng.shuffle(second_round)

    return first_round + second_round


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

    fixtures = create_fixtures(opp_codes)

    print()
    for i in range(len(fixtures)):
        print(fixtures[i])

    # PHASE 2: Fit our model using our data - use the data for teams that are in the league

    # Get the avgs & sds of this team's data and use a normal distribution for each param


    # PHASE 3: Run predictions and assign points, to determine our league ranking


simulate()
