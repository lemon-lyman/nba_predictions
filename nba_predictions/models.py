import numpy as np
import pandas as pd
from fte_spreadsheet import get_fte
from record import create_record
import datetime


class Model:

    def __init__(self, prediction_history, dates, label):
        self.prediction_history = prediction_history
        self.dates = dates
        self.label = label

    def ongoing_average(self):
        return [np.mean(self.prediction_history[:ii + 1]) for ii in range(len(self.prediction_history))]

    def moving_average(self, prediction_history, window=10):
        pass

    def __repr__(self):
        return '\nModel: {}\nAccuracy: {:.3f}\nGames: {}\n'.format(self.label,
                                                                 float(self.prediction_history.mean()),
                                                                 int(len(self.prediction_history)))

    def __str__(self):
        return '\nModel: {}\nAccuracy: {:.3f}\nGames: {}\n'.format(self.label,
                                                                 float(self.prediction_history.mean()),
                                                                 int(len(self.prediction_history)))

def create_user_model(record, user):

    user_df_raw = pd.read_csv("data/" + user + ".csv")
    last_valid_ind = np.where(user_df_raw['Pick'].notnull())[0][-1]
    user_df = user_df_raw.iloc[:last_valid_ind + 1, :].copy()

    unformatted_dates = user_df['date'].values
    datetime_arr = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in unformatted_dates]
    dates = [date.strftime("%m/%d/%Y") for date in datetime_arr]

    prediction_history = np.zeros(user_df.shape[0])

    for ii in range(user_df.shape[0]):
        if user_df['Pick'].iloc[ii] == record['winner'].iloc[ii]:
            prediction_history[ii] = 1

    return Model(prediction_history, dates, user)



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

def create_lvi_model():
    pass




    pass

if __name__ == "__main__":
    record = create_record()


