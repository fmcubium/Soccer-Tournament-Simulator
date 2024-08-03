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
