import pandas as pd
from utils.connect_psql import bdengine


tickers = [
    'CNYRUB_TOM',
    'EURUSD000TOM',
    'EUR_RUB__TOM',
    'HKDRUB_TOM',
    'KZTRUB_TOM',
    'TRYRUB_TOM',
    'USD000UTSTOM',
    'USDCNY_TOM',
]

q_get_candles = """
        
    select * from marketdata_candles1min
    
"""

q_get_waiting_orders = """

    select * from marketdata_myorders
    where balance > 0

"""

q_remove_waiting_orders = """

    delete from marketdata_myorders
    where balance > 0

"""


# -----> main thread
engine = bdengine()
with engine.begin() as conn:
    X = pd.read_sql(q_get_candles, conn)

    X = X.sort_values('valid_time', ascending=False)
    X['max'] = X.groupby('ticker')['pr_high'].cummax()
    X['min'] = X.groupby('ticker')['pr_low'].cummin()
    X['time'] = X['valid_time'].astype(str).str[11:16]

    O = pd.read_sql(q_get_waiting_orders, conn)
    O['time'] = O['entrytime'].astype(str).str[11:16]
    print(O)
    O = pd.merge(O, X[['time', 'ticker', 'min', 'max']], how='left', on=['time', 'ticker'])

    O.loc[((O['price'] >= O['min']) | (O['price'] <= O['max'])), 'balance'] = 0
    del O['id']
    del O['time']
    del O['min']
    del O['max']

    conn.execute(q_remove_waiting_orders)

    O.to_sql('marketdata_myorders', conn, if_exists='append', index=None)

print(O)
