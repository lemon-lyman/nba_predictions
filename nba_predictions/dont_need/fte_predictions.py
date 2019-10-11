from nba_predictions.fte_spreadsheet import get_fte
import sys
from odds.prediction_format import Model



def create_fte_model(outcome):
    """

    :param outcome:
    :return: Model()
    """
    fte_df = get_fte()
    temp_object = fte_df[['date', 'score1', 'score2']]


