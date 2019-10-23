import pandas as pd
import numpy as np
import requests
import datetime as dt
import io
import os


spreadsheet_file = "data/fte_spreadsheet.csv"
fte_latest_url = "https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv"

def pull_spreadsheet():
    """
    Gets the FTE data for the latests season off of GitHub
    :return: Pandas dataframe; None if response not OK
    """
    params ={'period1':1538761929,
             'period2':1541443929,
             'interval':'1d',
             'events':'history',
             'crumb':'v4z6ZpmoP98'}

    r = requests.get(fte_latest_url,data=params)
    if r.ok:
        data = r.content.decode('utf8')
        df = pd.read_csv(io.StringIO(data))
        df.to_csv(spreadsheet_file, index=False)
        return df
    else:
        return None

def read_spreadsheet(file_in=spreadsheet_file):
    """
    Reads FTE spreadsheet from local
    :param file_in: local, relative file path
    :return: Pandas dataframe
    """
    return pd.read_csv(file_in)

def pulled_recently(file_in=spreadsheet_file, seconds_passed=3600):
    """
    Checks if the FTE local spreadsheet has been pulled and stored recently
    :param file_in: local, relative file path
    :param days_passed: Time threshold that determines whether data is too old
    :return: Bool; Is data expired?
    """
    try:
        last_mod_unix = os.path.getmtime(file_in)
    except FileNotFoundError:
        return False
    last_mod_dt = dt.datetime.fromtimestamp(last_mod_unix)
    tdelta = dt.datetime.now()-last_mod_dt
    return tdelta.seconds <= seconds_passed

def get_fte(pull_override=None):
    if pull_override==None:
        if pulled_recently():
            print("FTE Pulled Recently; Reading")
            untrimmed_df = read_spreadsheet()
            last_valid_ind = np.where(untrimmed_df['score1'].notnull())[0][-1]
            return untrimmed_df.iloc[:last_valid_ind + 1, :]
        else:
            print("FTE Not Pulled Recently; Pulling")
            untrimmed_df = pull_spreadsheet()
            last_valid_ind = np.where(untrimmed_df['score1'].notnull())[0][-1]
            return untrimmed_df.iloc[:last_valid_ind + 1, :]
    elif pull_override:
        print("FTE Pull Override; Pulling")
        untrimmed_df = pull_spreadsheet()
        last_valid_ind = np.where(untrimmed_df['score1'].notnull())[0][-1]
        return untrimmed_df.iloc[:last_valid_ind + 1, :]
    else:
        print("FTE Pull Override; Reading")
        untrimmed_df = read_spreadsheet()
        last_valid_ind = np.where(untrimmed_df['score1'].notnull())[0][-1]
        return untrimmed_df.iloc[:last_valid_ind + 1, :]

if __name__ == "__main__":
    df = get_fte()
