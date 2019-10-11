from fte_spreadsheet import get_fte
import numpy as np
import pandas as pd


def create_record():
    fte_df = get_fte()
    trimmed_df = fte_df[['date', 'team1', 'team2', 'score1', 'score2']].copy()
    outcome_series = trimmed_df['score1'] > trimmed_df['score2']
    outcome_val = outcome_series.values
    trimmed_df['outcome'] = outcome_val

    ## Citation: https://stackoverflow.com/questions/14016247/find-integer-index-of-rows-with-nan-in-pandas-dataframe#comment19385278_14033137
    last_valid_ind = np.where(trimmed_df['score1'].notnull())[0][-1]

    valid_team1 = trimmed_df['team1'].iloc[:last_valid_ind + 1].values
    valid_team2 = trimmed_df['team2'].iloc[:last_valid_ind + 1].values
    valid_score1 = trimmed_df['score1'].iloc[:last_valid_ind + 1].values
    valid_score2 = trimmed_df['score2'].iloc[:last_valid_ind + 1].values
    dates = trimmed_df['date'].iloc[:last_valid_ind + 1].values

    winners = []
    for ii in range(last_valid_ind + 1):
        if valid_score1[ii] > valid_score2[ii]:
            winners.append(valid_team1[ii])
        else:
            winners.append(valid_team2[ii])

    matchup_labels = [t1 + " " + t2 for t1, t2 in zip(valid_team1, valid_team2)]

    record = pd.DataFrame(data=winners, index=[dates, matchup_labels], columns = ['winner'])


    # for ii in range(trimmed_df.shape[0])
    return record

if __name__ == "__main__":
    outcome = create_record()
