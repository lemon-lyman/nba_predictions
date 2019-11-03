import numpy as np
import pandas as pd
import time
import models
from record import create_record
import matplotlib.pyplot as plt


po = None
record = create_record(pull_override=po)
odds_raw = pd.read_csv("data/odds.csv", header=None)

dates_mdy = odds_raw[2].values
dates_ymd = []
for date in dates_mdy:
    m, d, y = date.split('-')
    dates_ymd.append('20' + y + '-' + m + '-' + d)
odds_raw[2] = dates_ymd

matchups_lvi = odds_raw[1].values

## Format team names. LVI uses different abbreviations than fte for these three teams
lvi2npw = {'BKN': 'BRK',
           'CHA': 'CHO',
           'PHX': 'PHO'}

matchups_npw = []
for idx, m_lvi in enumerate(matchups_lvi):

    team1, team2 = m_lvi.split(" ")

    if team1 in lvi2npw:
        team1 = lvi2npw[team1]
    if team2 in lvi2npw:
        team2 = lvi2npw[team2]

    matchups_npw.append(team1 + " " + team2)
odds_raw[1] = matchups_npw

odds_raw = odds_raw.set_index([2, 1]).drop(0, axis=1)  ## Drops the column of rpi scrape-times

matchups = list(np.unique(odds_raw.index))

dates = []
prediction_history = []
while len(matchups) > 0:

    matchup_initial = matchups.pop()

    date = matchup_initial[0]

    team1, team2 = matchup_initial[1].split(" ")

    matchup_switched = (matchup_initial[0], team2 + " " + team1)
    matchups.pop(matchups.index(matchup_switched))

    team1_ml = odds_raw.loc[date, team1 + " " + team2].iloc[-1].mean()
    team2_ml = odds_raw.loc[date, team2 + " " + team1].iloc[-1].mean()

    try:
        winner = record.loc[matchup_initial[0], team2 + " " + team1]['winner']
    except KeyError:
        try:
            winner = record.loc[matchup_initial[0], team1 + " " + team2]['winner']
        except KeyError:
            break

    ## TODO - no fucking way this is right
    if team1_ml < team2_ml:
        projected_winner = team1
    else:
        projected_winner = team2

    if projected_winner == winner:
        prediction_history.append(1)
    else:
        prediction_history.append(0)
    dates.append(date)

lvi = models.Model(np.asarray(prediction_history), dates, "LVI")