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
    while len(odds) < max_len:
        odds.append(None)
    return odds


def implied_odds(prob):
    prob = round(prob)
    if prob < 1:
        prob = prob * 100
    if prob > 50:
        left = 100 - prob
        moneyline = -(100 * prob / left)
    else:
        moneyline = (10000 / prob) - 100
    return moneyline


def implied_prob(moneyline):
    if moneyline > 0:
        prob = 100 / (moneyline + 100)
    else:
        prob = (moneyline / (moneyline - 100))
    return prob


def create_today(odd_format=False):
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
    if odd_format:
        for i in range(len(odds)):
            odds[i][0] = [implied_prob(odds[i][0][x]) for x in range(len(odds[i][0]))]
            odds[i][1] = [implied_prob(odds[i][1][x]) for x in range(len(odds[i][1]))]
    return matchups, odds


def create_df(matchups, odds):
    max_odds = 12
    # print('Warning: max_odds has been hardcoded to', max_odds)

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


def vig(df):
    ind = df.index
    labels = np.asarray(ind.labels)[-2]
    levels = ind.levels[-2]
    all_matchups = levels[labels]
    matchups = all_matchups[::2]
    # df_vig = pd.DataFrame()
    data = []

    for i in range(len(matchups)):
        temp = np.asarray(df.iloc[i * 2] + df.iloc[(i * 2) + 1]).tolist()


##        if i == 0:
##            data = temp
##        else:
##            data = data.append(temp)
####        df_temp = pd.DataFrame(data = temp, index = matchups[i])
####        df_vig.append(df_temp)
##
##    df_vig = pd.DataFrame(data=data, index=matchups)
##    return df_vig


def parse_tag(tag):
    url = tag['href']
    first_half, second_half = url.split('-@-')
    team_one = abbr(first_half.split('/')[-1])
    team_two = abbr(second_half.split('.')[0])
    result = re.search('date/(.*)', url)
    date_of_game = result.group(1).split('#')[0]

    whole_line = str(tag)
    _, string_one, almost_two = whole_line.split('<br/>')
    string_two = almost_two.split('\n', 1)[0]
    return team_one, team_two, int(string_one), int(string_two), date_of_game


def simple_get(url):
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
    print(e)


if __name__ == "__main__":
    5/0
    start = time.time()
    matchups, odds = create_today()
    df = create_df(matchups, odds)
    df_vig = vig(df)
    print('dt:', time.time() - start)
    print(df)