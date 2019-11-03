import numpy as np
import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
from fte_spreadsheet import get_fte
from record import create_record
import datetime as dt


class Model:

    def __init__(self, prediction_history, dates, label):
        self.prediction_history = prediction_history
        self.accuracy = self.prediction_history.mean()
        self.dates = dates
        self.label = label
        self._ongoing_average()
        self._consolidate()

    def _ongoing_average(self):
        self.ongoing_average = [np.mean(self.prediction_history[:ii + 1]) for ii in range(len(self.prediction_history))]

    def moving_average(self, prediction_history, window=10):
        ## TODO
        pass

    def _consolidate(self):

        self.consolidated_dates = list(np.unique(self.dates))
        self.consolidated_predictions = np.zeros(len(self.consolidated_dates))

        temp_date = self.dates[0]

        count = 0
        for idx, date in enumerate(self.dates):
            if date != temp_date:
                temp_date = date
                count += 1
            self.consolidated_predictions[count] = self.ongoing_average[idx]


    def __repr__(self):
        return '\nModel: {}\nAccuracy: {:.3f}\nGames: {}\n'.format(self.label,
                                                                 float(self.prediction_history.mean()),
                                                                 int(len(self.prediction_history)))

    def __str__(self):
        return '\nModel: {}\nAccuracy: {:.3f}\nGames: {}\n'.format(self.label,
                                                                 float(self.prediction_history.mean()),
                                                                 int(len(self.prediction_history)))

def create_user_model(record, user):
    """

    :param record:
    :param user: str - Name of user
    :return:
    """

    user_df_raw = pd.read_csv("data/" + user + " - fte_spreadsheet.csv")
    valid_rows = user_df_raw.dropna()

    last_date = valid_rows['Date'].iloc[-1]
    last_date_dt = dt.datetime.strptime(last_date, "%Y-%m-%d")
    now_full = dt.datetime.now()
    now_simple = dt.datetime(now_full.year, now_full.month, now_full.day)
    time_delta = last_date_dt - now_simple
    print(user + " days ahead: " + str(time_delta.days))

    dates = []
    prediction_history = []

    for ii in range(valid_rows.shape[0]):

        team1 = valid_rows['Home'].iloc[ii]
        team2 = valid_rows['Away'].iloc[ii]

        date_ymd = valid_rows['Date'].iloc[ii] ## YYYY-m-d
        date_split_out = date_ymd.split('-')
        date_mdy = date_split_out[1] + "/" + date_split_out[2] + "/" + date_split_out[0] ## m/d/YYYY

        try:
            record.loc[date_ymd, team1 + " " + team2]['winner']
        except KeyError:
            continue

        dates.append(date_ymd)

        if valid_rows['Pick'].iloc[ii] == record.loc[date_ymd, team1 + " " + team2]['winner']:
            prediction_history.append(1)
        else:
            prediction_history.append(0)

    return Model(np.asarray(prediction_history), dates, user)

def create_raptor_model(record, pull_override):
    fte_df = get_fte(pull_override=pull_override)
    dates = fte_df['date'].values

    prediction_history = np.zeros(fte_df.shape[0])

    for ii in range(fte_df.shape[0]):

        date = fte_df['date'].iloc[ii]

        prob1 = fte_df['raptor_prob1'].iloc[ii]
        prob2 = fte_df['raptor_prob2'].iloc[ii]

        team1 = fte_df['team1'].iloc[ii]
        team2 = fte_df['team2'].iloc[ii]

        if prob1 > prob2:
            if record.loc[date, team1 + " " + team2]['winner'] == team1:
                prediction_history[ii] = 1
        else:
            if record.loc[date, team1 + " " + team2]['winner'] == team2:
                prediction_history[ii] = 1


    return Model(prediction_history, dates, "RAPTOR")

def create_carmelo_model(record, pull_override):
    fte_df = get_fte(pull_override=pull_override)
    dates = fte_df['date'].values

    prediction_history = np.zeros(fte_df.shape[0])

    for ii in range(fte_df.shape[0]):

        date = fte_df['date'].iloc[ii]

        prob1 = fte_df['carmelo1_pre'].iloc[ii]
        prob2 = fte_df['carmelo2_pre'].iloc[ii]

        team1 = fte_df['team1'].iloc[ii]
        team2 = fte_df['team2'].iloc[ii]

        if prob1 > prob2:
            if record.loc[date, team1 + " " + team2]['winner'] == team1:
                prediction_history[ii] = 1
        else:
            if record.loc[date, team1 + " " + team2]['winner'] == team2:
                prediction_history[ii] = 1


    return Model(prediction_history, dates, "CARMELO")

def create_carm_elo_model(record, pull_override):
    fte_df = get_fte(pull_override=pull_override)
    dates = fte_df['date'].values

    prediction_history = np.zeros(fte_df.shape[0])

    for ii in range(fte_df.shape[0]):

        date = fte_df['date'].iloc[ii]

        prob1 = fte_df['carm-elo1_pre'].iloc[ii]
        prob2 = fte_df['carm-elo2_pre'].iloc[ii]

        team1 = fte_df['team1'].iloc[ii]
        team2 = fte_df['team2'].iloc[ii]

        if prob1 > prob2:
            if record.loc[date, team1 + " " + team2]['winner'] == team1:
                prediction_history[ii] = 1
        else:
            if record.loc[date, team1 + " " + team2]['winner'] == team2:
                prediction_history[ii] = 1


    return Model(prediction_history, dates, "CARM-ELO")

def create_elo_model(record, pull_override):
    fte_df = get_fte(pull_override=pull_override)
    dates = fte_df['date'].values

    prediction_history = np.zeros(fte_df.shape[0])

    for ii in range(fte_df.shape[0]):

        date = fte_df['date'].iloc[ii]

        prob1 = fte_df['elo1_pre'].iloc[ii]
        prob2 = fte_df['elo2_pre'].iloc[ii]

        team1 = fte_df['team1'].iloc[ii]
        team2 = fte_df['team2'].iloc[ii]

        if prob1 > prob2:
            if record.loc[date, team1 + " " + team2]['winner'] == team1:
                prediction_history[ii] = 1
        else:
            if record.loc[date, team1 + " " + team2]['winner'] == team2:
                prediction_history[ii] = 1


    return Model(prediction_history, dates, "ELO")

def create_lvi_model(record):
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

        matchup_initial = matchups.pop(0)

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

    return Model(np.asarray(prediction_history), dates, "LVI")

if __name__ == "__main__":
    record = create_record()


