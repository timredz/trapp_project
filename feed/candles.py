import time
import pandas as pd
from utils.connect_psql import bdengine
from utils.connect_iss import get_df
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

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


M10 = pd.DataFrame()
for ind in tickers:
    url = f'https://iss.moex.com/iss/engines/currency/markets/selt/boards/cets/securities/{ind}/candles.csv?from={today}&till={today}&interval=10'
    data = get_df(url)
    X = pd.read_csv(data, sep=';', skiprows=2)
    X['ticker'] = ind
    M10 = pd.concat([M10, X])
    time.sleep(0.1)

M10 = M10[['ticker', 'open', 'high', 'low', 'close', 'value', 'volume', 'begin']]
M10['value'] = M10['value'].astype('int64')
M10['venue'] = 'MOEX'
M10.columns = ['ticker', 'pr_open', 'pr_high', 'pr_low', 'pr_close', 'turnover', 'volume', 'valid_time', 'venue']
M10['valid_time'] = pd.to_datetime(M10['valid_time'])
M10['valid_time'] = M10['valid_time'].dt.tz_localize('Europe/Moscow')


M1 = pd.DataFrame()
for ind in tickers:
    for page in range(2):
        url = f'https://iss.moex.com/iss/engines/currency/markets/selt/boards/cets/securities/{ind}/candles.csv?from={today}&till={today}&interval=1&start={(500*page)}'
        data = get_df(url)
        X = pd.read_csv(data, sep=';', skiprows=2)
        X['ticker'] = ind
        M1 = pd.concat([M1, X])
        time.sleep(0.1)

M1 = M1[['ticker', 'open', 'high', 'low', 'close', 'value', 'volume', 'begin']]
M1['value'] = M1['value'].astype('int64')
M1['venue'] = 'MOEX'
M1.columns = ['ticker', 'pr_open', 'pr_high', 'pr_low', 'pr_close', 'turnover', 'volume', 'valid_time', 'venue']
M1['valid_time'] = pd.to_datetime(M1['valid_time'])
M1['valid_time'] = M1['valid_time'].dt.tz_localize('Europe/Moscow')

engine = bdengine()

with engine.begin() as conn:
    conn.execute("TRUNCATE TABLE marketdata_candles1min")
    conn.execute("TRUNCATE TABLE marketdata_candles10min")
    
    M1.to_sql('marketdata_candles1min', conn, index=False, if_exists="append")
    M10.to_sql('marketdata_candles10min', conn, index=False, if_exists="append")
