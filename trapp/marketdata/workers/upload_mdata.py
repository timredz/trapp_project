import pandas as pd
from sqlalchemy import create_engine

db_string = f"postgresql://timredz:fxworld@localhost:5432/trapp"

    
def bdengine():
    DB = create_engine(db_string)
    return DB


I = pd.read_csv('instruments.csv')
O = pd.read_csv('orderbook.csv')
C10 = pd.read_csv('candles10min.csv')
C1 = pd.read_csv('candles1min.csv')

q = "DROP table marketdata_balance"

engine = bdengine()
with engine.begin() as conn:
    I.to_sql('marketdata_instruments', conn, index=False, if_exists="append")
    O.to_sql('marketdata_orderbook', conn, index=False, if_exists="append")
    C10.to_sql('marketdata_candles10min', conn, index=False, if_exists="append")
    C1.to_sql('marketdata_candles1min', conn, index=False, if_exists="append")

