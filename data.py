import numpy as np
import numpy.random
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import util


class Data:

    def __init__(self):
        # Initialize our model
        self.rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

        # Prepare our data
        serie_a_matches = pd.read_csv("data/serie_a_matches.csv", index_col=0)
        epl_matches = pd.read_csv("data/premier_league_matches.csv", index_col=0)
        la_liga_matches = pd.read_csv("data/la_liga_matches.csv", index_col=0)
        bundesliga_matches = pd.read_csv("data/bundesliga_matches.csv", index_col=0)
        ligue_1_matches = pd.read_csv("data/ligue_1_matches.csv", index_col=0)

        matches = pd.concat([serie_a_matches, epl_matches, la_liga_matches, bundesliga_matches, ligue_1_matches])

        # Clean up the data (inefficient - might upgrade)
        for opp in matches["opponent"]:
            start = 0
            for i in range(len(opp)):
                if opp[i].isupper():
                    start = i
                    break
            matches = matches.replace(to_replace=opp, value=opp[start:])
        util.fix_team_names(matches)

        # predictors
        matches['venue_code'] = matches["venue"].astype("category").cat.codes
        matches['team_code'] = matches["team"].astype("category").cat.codes
        matches['date_code'] = matches.index

        self.team_codes = dict(zip(matches['team'], matches['team_code']))
        for opp in matches["opponent"]:
            if self.team_codes.get(opp) is None:
                self.team_codes[opp] = len(self.team_codes) + 1

        matches["opp_code"] = matches["opponent"].map(self.team_codes)
        matches["gf"] = [float(gf[0]) for gf in matches["gf"]]
        matches["ga"] = [float(ga[0]) for ga in matches["ga"]]
        matches["target"] = [util.define_result(r) for r in matches["result"]]

        # Rolling averages
        cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt", "sh_against", "sot_against", "dist_against",
                "fk_against", "pk_against", "pkatt_against"]
        new_cols = [f"{c}_rolling" for c in cols]
        matches_rolling = matches.groupby("team").apply(lambda x: util.rolling_averages(x, cols, new_cols))
        matches_rolling = matches_rolling.droplevel('team')
        matches_rolling.index = range(matches_rolling.shape[0])

        # fit our model
        self.train = matches_rolling
        predictors = ["venue_code", "opp_code", "date_code"] + new_cols
        self.rf.fit(self.train[predictors], self.train["target"])

    def averages(self, team: str, opponent=None):
        ret = [0] * 14
        if team in self.train["team"].unique():
            group = self.train.groupby("team").get_group(team) # Error here is happening because the team has no data
            if opponent is not None:
                group = group[group["opponent"] == opponent]

            cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt", "sh_against", "sot_against", "dist_against",
                    "fk_against", "pk_against", "pkatt_against"]

            ret = group[cols].fillna(0).mean()

        return ret

    def st_devs(self, team: str, opponent=None):
        ret = [0] * 14
        if team in self.train["team"].unique():
            group = self.train.groupby("team").get_group(team) # see this line in averages
            if opponent is not None:
                group = group[group["opponent"] == opponent]

            cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt", "sh_against", "sot_against", "dist_against",
                    "fk_against", "pk_against", "pkatt_against"]

            ret = group[cols].fillna(0).std(ddof=0, numeric_only=True)

        return ret

    def create_stats(self, team: str, opponent: str):
        # Create 2 random normal variables for 1. Overall stats and 2. stats vs opponent
        rng = numpy.random.default_rng()

        # missing gf and ga
        overall_avgs = np.array(self.averages(team))
        overall_stds = np.array(self.st_devs(team))

        opponent_avgs = np.array(self.averages(team, opponent))
        opponent_stds = np.array(self.averages(team, opponent))

        # Convert NaN to 0
        overall_avgs[np.isnan(overall_avgs)] = 0
        overall_stds[np.isnan(overall_stds)] = 0
        opponent_avgs[np.isnan(opponent_avgs)] = 0
        opponent_stds[np.isnan(opponent_stds)] = 0

        # Apply weights w1 and w2
        w1 = 1.00
        w2 = 0.10

        overall_avgs = overall_avgs * w1
        opponent_avgs = opponent_avgs * w2

        # Combine, randomly select once from each distribution, return completed list
        new_stats = [int(rng.normal(overall_avgs[i] + opponent_avgs[i], overall_stds[i] + opponent_stds[i])) for i in range(overall_avgs.size)]
        return new_stats
