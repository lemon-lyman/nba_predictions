from spreadsheet import get_fte



def create_fte_object(outcome):
    """

    :param outcome:
    :return: DataFrame - index with dates and only column is bool - whether prediction was correct
    """
    fte_df = get_fte()
    temp_object = fte_df[['date', 'score1', 'score2']]

