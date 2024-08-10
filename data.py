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

        # predictors
        matches['venue_code'] = matches["venue"].astype("category").cat.codes
        matches['team_code'] = matches["team"].astype("category").cat.codes
        matches['date_code'] = matches.index

        self.team_codes = dict(zip(matches['team'], matches['team_code']))
        for opp in matches["opponent"]:
            if self.team_codes.get(opp) is None:
                self.team_codes[opp] = len(self.team_codes) + 1

        matches["opp_code"] = matches["opponent"].map(self.team_codes)

        # Rolling averages
        cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
        new_cols = [f"{c}_rolling" for c in cols]
        matches_rolling = matches.groupby("team").apply(lambda x: util.rolling_averages(x, cols, new_cols))
        matches_rolling = matches_rolling.droplevel('team')
        matches_rolling.index = range(matches_rolling.shape[0])

        # fit our model
        self.train = matches_rolling
        predictors = ["venue_code", "opp_code", "date_code"] + new_cols
        self.rf.fit(self.train[predictors], self.train["target"])
