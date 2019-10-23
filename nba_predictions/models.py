import numpy as np
from fte_spreadsheet import get_fte
from record import create_record


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

def create_carmelo_model(record):
    fte_df = get_fte()
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


    return Model(prediction_history, dates, "Carmelo")

def create_carm_elo_model(record):
    fte_df = get_fte()
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


    return Model(prediction_history, dates, "Carm-elo")

def create_elo_model(record):
    fte_df = get_fte()
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


    return Model(prediction_history, dates, "elo")

def create_lvi_model():
    pass

def create_user_model():
    pass

if __name__ == "__main__":
    record = create_record()
    carmelo = create_carmelo_model(record)
