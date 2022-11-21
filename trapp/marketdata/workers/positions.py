import pandas as pd


def get_position(trades):
    T = pd.DataFrame.from_records(trades)

    sgn = {'B': 1, 'S': -1}
    T['pos'] = T['buysell'].map(sgn) * T['quantity']
    T = T.groupby('ticker')[['pos']].sum().reset_index()
    T = T[T['pos'] != 0]

    return T.to_dict('records')
