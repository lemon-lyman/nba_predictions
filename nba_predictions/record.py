from ftepy.spreadsheet import get_fte

def create_outcome():
    fte_df = get_fte()
    trimmed_df = fte_df[['date', 'team1', 'team2', 'score1', 'score2']].copy()
    outcome_series = trimmed_df['score1'] > trimmed_df['score2']
    outcome_val = outcome_series.values
    trimmed_df['outcome'] = outcome_val
    return trimmed_df

if __name__ == "__main__":
    outcome = create_outcome()
