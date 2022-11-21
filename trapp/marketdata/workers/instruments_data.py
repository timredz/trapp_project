import pandas as pd


def get_instruments(QS):
    X = pd.DataFrame.from_records(QS)

    result = {}
    for item in X['ticker'].unique():
        df = X[X['ticker'] == item]
        every_n = 1 + df.shape[0] // 100
        result[item] = df[['pr_close', 'valid_time']].sort_values('valid_time')[::every_n].to_dict('records')

    return result
