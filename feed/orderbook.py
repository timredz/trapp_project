import time
import pandas as pd
from datetime import date
from utils.connect_psql import bdengine
from utils.connect_iss import get_df
import datetime


needed_tickers = [
    'CNYRUB_TOM',
    'EURUSD000TOM',
    'EUR_RUB__TOM',
    'HKDRUB_TOM',
    'KZTRUB_TOM',
    'TRYRUB_TOM',
    'USD000UTSTOM',
    'USDCNY_TOM',
]


columns = [
    'SECID',
    'BUYSELL',
    'PRICE',
    'QUANTITY',
    'UPDATETIME',
    'DECIMALS'
]

columns_trans = {
    'SECID': 'ticker',
    'BUYSELL': 'buysell',
    'PRICE': 'price',
    'QUANTITY': 'quantity',
    'UPDATETIME': 'valid_time',
    'DECIMALS': 'decimals'
}

columns_str = ",".join(columns)


def get_orderbook():
    A = pd.DataFrame()
    for page in range(1):
        url = f'https://iss.moex.com/iss/engines/currency/markets/selt/boards/cets/orderbook.csv?orderbook.columns={columns_str}&start={3000*page}'
        data = get_df(url)
        X = pd.read_csv(data, sep=';', skiprows=2)[:-3]
        A = pd.concat([A, X])
        time.sleep(0.1)
        
    today = date.today()
    A['UPDATETIME'] = today.strftime('%Y-%m-%d ') + A['UPDATETIME'].astype(str)
    A.columns = A.columns.map(columns_trans)
    A['venue'] = 'MOEX'
    
    return A
    


O = get_orderbook()

engine = bdengine()
with engine.begin() as conn:
    conn.execute("truncate table marketdata_orderbook")
    O.to_sql('marketdata_orderbook', conn, if_exists = 'append', index=None)
