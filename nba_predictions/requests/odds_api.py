from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from teamDef import abbr
import numpy as np
import pandas as pd
import time
import datetime
import re


print('time_stamp', datetime.datetime.now().strftime("%m-%d-%y %H:%M"))


def pad_odds(odds, max_len):

    """
    Fill out odds with None so that every row has the same number of objects
    :param odds:
    :param max_len:
    :return:
    """

    while len(odds) < max_len:
        odds.append(None)
    return odds


def create_today():

    """

    :return:
    matchups:
    odds:
    """

    url = 'http://www.vegasinsider.com/nba/odds/las-vegas/money/'
    raw = simple_get(url)
    soup = BeautifulSoup(raw, 'html.parser')
    table = soup.find_all('a', class_='cellTextNorm')

    matchups = []
    odds = []

    for i in range(len(table)):
        if '@' in table[i]['href']:
            try:
                team_one, team_two, line_one, line_two, date_of_game = parse_tag(table[i])
                try:
                    ind = matchups.index([team_one, team_two, date_of_game])
                    odds[ind][0].append(line_one)
                    odds[ind][1].append(line_two)
                except ValueError:
                    ind = len(matchups)
                    matchups.append([team_one, team_two, date_of_game])
                    odds.append([[line_one], [line_two]])
            except ValueError:
                print('ValueError')
                continue

    return matchups, odds


def create_df(matchups, odds):

    ###################################
    # max_odds has been hardcoded to 12
    max_odds = 12
    ###################################

    df = pd.DataFrame()

    for match, odd in zip(matchups, odds):
        time_stamp = datetime.datetime.now().strftime("%m-%d-%y %H:%M")
        df_temp = pd.DataFrame(
            data=[pad_odds(odd[0], max_odds), pad_odds(odd[1], max_odds)],
            index=[[time_stamp, time_stamp], [match[0] + ' ' + match[1],
                                              match[1] + ' ' + match[0]],
                   [match[-1], match[-1]]]
        )
        df = df.append(df_temp)

    return df


def parse_tag(tag):

    """
    Parses bs4 object.
    :param tag:
    <class 'bs4.element.Tag'> taken from the table of tags.

    :return:
    team one - string
    team two - string
    odds one, moneyline - string
    odds two, moneyline - string
    date_of_game - string e.g. 10-22-19
    """

    url = tag['href']
    first_half, second_half = url.split('-@-')
    team_one = abbr(first_half.split('/')[-1])
    team_two = abbr(second_half.split('.')[0])

    ## As of 10/06/19, date on LVI is formatted as e.g. '.../date/10-22-19#BT
    ## I think the BT at the end (or J, CS, L, or X) has something to do with
    ## the company providing the odds, BT for open and consensus.
    result = re.search('date/(.*)', url)
    date_of_game = result.group(1).split('#')[0]

    whole_line = str(tag)
    _, string_one, almost_two = whole_line.split('<br/>')
    string_two = almost_two.split('\n', 1)[0]
    return team_one, team_two, int(string_one), int(string_two), date_of_game


def simple_get(url):

    """
    Simple but robust url get. Copied from some stack overflow. Unfortunately, link lost.
    :param url:
    :return:
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):

    """
    'Logs' error by printing to terminal. Current pi setup captures everything printed to terminal so error is logged
    :param e:
    :return:
    """

    print(e)


if __name__ == "__main__":
    start = time.time()
    matchups, odds = create_today()
    df = create_df(matchups, odds)
    print('dt:', time.time() - start)
    print(df)