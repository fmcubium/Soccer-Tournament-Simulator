# Nodes for our tournament tree
import math
import random

import numpy as np
import pandas as pd


class Node:
    def __init__(self, val="", left=None, right=None, height=0):
        self.val = val
        self.left = left
        self.right = right
        self.height = height

# Our actual knockout tournament code

def apply_result(result, strs: list):
    match result['prediction']:
        case 2:
            strs[0] = strs[1]

        case 0:
            strs[0] = strs[2]
        case 1:
            # if we have a draw, penalties :)
            cmps = [strs[1], strs[2]]
            random.shuffle(cmps)
            strs[0] = cmps[0]

def preorder_builder(node: Node, teams: list, h: int):
    # if h == 1 set the team and return
    if h <= 1:
        node.val = teams.pop(0)
        return

    node.left = Node()
    node.right = Node()
    node.height = h

    preorder_builder(node.left, teams, h - 1)
    preorder_builder(node.right, teams, h - 1)


def create_tree(teams: list):
    # determine the height: since our tree is always perfect, h = 1 + log_2(n)
    # where n = number of nodes at the bottom layer = number of teams
    height = 1 + int(math.log2(len(teams)))

    # construct a perfect tree of height h. The nodes that are not on the bottom layer will have None/"" as their val
    # nodes at the bottom contain the teams, as listed in the list.
    bracketRoot = Node()
    preorder_builder(bracketRoot, teams, height)

    # return the completed tree given a root with None as its val.
    return bracketRoot


def sim_helper(data, node: Node):
    if node.left is None:
        return

    sim_helper(data, node.left)
    sim_helper(data, node.right)

    home = node.left.val
    away = node.right.val

    # create match, look at league code - We will use node.left for the subject of this matcharr
    match_arr = np.zeros((1, 18), dtype=int)
    match_arr[0][0] = 1  # venue code
    match_arr[0][1] = data.team_codes[home]  # team code
    match_arr[0][2] = data.team_codes[away]  # opponent code
    match_arr[0][3] = node.height - 1  # date code
    match_arr[0][4:] = np.array(data.create_stats(home, away))

    # transform into dataframe (silly hack that's technically not true)
    cols = ["venue_code", "team_code", "opp_code", "date_code", "gf_rolling", "ga_rolling", "sh_rolling", "sot_rolling",
            "dist_rolling", "fk_rolling", "pk_rolling", "pkatt_rolling", "sh_against_rolling", "sot_against_rolling",
            "dist_against_rolling", "fk_against_rolling", "pk_against_rolling", "pkatt_against_rolling"]
    match = pd.DataFrame(match_arr, columns=cols)

    newCols = ["venue_code", "opp_code", "date_code", "gf_rolling", "ga_rolling", "sh_rolling", "sot_rolling",
            "dist_rolling", "fk_rolling", "pk_rolling", "pkatt_rolling", "sh_against_rolling", "sot_against_rolling",
            "dist_against_rolling", "fk_against_rolling", "pk_against_rolling", "pkatt_against_rolling"]
    predictors = match[newCols]

    # simulate it
    predictions = pd.Series(data.rf.predict(predictors), name='prediction')
    results = match[["team_code", "opp_code"]]
    results.loc[:, 'prediction'] = predictions

    winner = ""  # fix later
    strs = [winner, home, away]

    results.apply(lambda x: apply_result(x, strs), axis=1)
    # match results['prediction']:
    #     case 2:
    #         winner = home
    #     case 0:
    #         winner = away
    #     case 1:
    #         # if we have a draw, penalties :)
    #         cmps = [home, away]
    #         random.shuffle(cmps)
    #         winner = cmps[0]

    node.val = strs[0]
    print(f"match: {home} vs. {away} __________ winner: {strs[0]}")
    return


def simulate(data, teams: list):
    pass
    # PHASE 1: Prepare team data and seed teams
    # for now, for seeding we randomize the order of teams in teams
    random.shuffle(teams)

    opp_codes = []

    # code to test - allows for adding new opponents we haven't seen before
    for team in teams:
        if data.team_codes.get(team) is None:
            data.team_codes[team] = len(data.team_codes) * 10 + 1  # change
        opp_codes.append(data.team_codes[team])

    print(data.team_codes)
    print(opp_codes)

    # PHASE 2: Create our tree and dataframe for simulating
    bracket = create_tree(teams)

    # PHASE 3: Run the simulation
    sim_helper(data, bracket)

    print(f"Our winner is: {bracket.val}!")
