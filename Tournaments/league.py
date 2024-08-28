import copy

from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd

import util


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


def apply_results(result, table: dict):
    match result['prediction']:
        case 0:
            table[result['opp_code']] += 3
        case 1:
            table[result['team_code']] += 1
            table[result['opp_code']] += 1
        case 2:
            table[result['team_code']] += 3


def simulate(data, teams: list):
    # PHASE 1: Prepare team data and create a fixture list
    # team_codes = {
    #     "Inter": 1,
    #     "Milan": 2,
    #     "Juventus": 3,
    #     "Atalanta": 4,
    #     "Bologna": 5,
    #     "Roma": 6,
    #     "Lazio": 7,
    #     "Fiorentina": 8,
    #     "Torino": 9,
    #     "Napoli": 10,
    # }

    # teams = ["Inter", "Milan", "Juventus", "Atalanta", "Bologna", "Roma", "Lazio", "Fiorentina", "Torino", "Napoli",
    #          "Genoa", "Monza", "Hellas Verona", "Lecce", "Udinese", "Cagliari", "Empoli", "Parma", "Como", "Venezia"]
    opp_codes = []

    # code to test - allows for adding new opponents we haven't seen before
    for team in teams:
        if data.team_codes.get(team) is None:
            data.team_codes[team] = len(data.team_codes)*10 + 1 #change
        opp_codes.append(data.team_codes[team])

    print(data.team_codes)
    print(opp_codes)

    fixtures = create_fixtures(opp_codes)

    print()
    for i in range(len(fixtures)):
        print(fixtures[i])

    # PHASE 2: Create and prepare our dataframe for simulating
    match_arr = np.zeros((len(opp_codes) * (len(opp_codes) - 1), 18), dtype=int)

    for i in range(len(opp_codes) * (len(opp_codes) - 1)):
        # venue code - 'team' will always be home
        match_arr[i][0] = 1

        # team code
        match_arr[i][1] = fixtures[i // (len(opp_codes) // 2)][i % (len(opp_codes)//2)][0]

        # date code
        match_arr[i][2] = i // (len(opp_codes)//2)

        # opponent code
        match_arr[i][3] = fixtures[i // (len(opp_codes)//2)][i % (len(opp_codes)//2)][1]

        # Get the avgs & sds of this team's data and use a normal distribution for each param
        team_pos = list(data.team_codes.values()).index(fixtures[i // (len(opp_codes)//2)][i % (len(opp_codes)//2)][0])
        opp_pos = list(data.team_codes.values()).index(fixtures[i // (len(opp_codes)//2)][i % (len(opp_codes)//2)][1])
        match_arr[i][4:] = np.array(data.create_stats(list(data.team_codes.keys())[team_pos], list(data.team_codes.keys())[opp_pos])) # Last error to be fixed

    # Transform into dataframe
    cols = ["venue_code", "team_code", "date_code", "opp_code", "gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt",
            "sh_against", "sot_against", "dist_against",
            "fk_against", "pk_against", "pkatt_against"]
    matches = pd.DataFrame(match_arr, columns=cols)

    cols = cols[4:]
    new_cols = [f"{c}_rolling" for c in cols]
    matches_rolling = matches.groupby("team_code").apply(lambda x: util.rolling_averages_2(x, cols, new_cols))
    matches_rolling = matches_rolling.droplevel('team_code')
    matches_rolling.index = range(matches_rolling.shape[0])

    # PHASE 3: Run predictions and assign points, to determine our league ranking
    # The fun part - running the simulation
    predictors = ["venue_code", "opp_code", "date_code"] + new_cols
    predictions = pd.Series(data.rf.predict(matches_rolling[predictors]), name='prediction')
    results = matches_rolling[["team_code", "opp_code"]]
    results['prediction'] = predictions

    # Now that our sim is done, we simply add up the points
    table = dict(zip(opp_codes, [0] * len(opp_codes)))
    results.apply(lambda x: apply_results(x, table), axis=1)

    team_names = [list(data.team_codes.keys())[list(data.team_codes.values()).index(t)] for t in table.keys()]

    table_dict = {'team': team_names,
                  'points': table.values()}

    final_table = pd.DataFrame.from_dict(table_dict).sort_values('points', ascending=False)
    print(final_table)

