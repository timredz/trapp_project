from datetime import datetime, date, timedelta
from io import StringIO
import pandas as pd
import pickle
import requests
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def predict_upon_candles(curr_date, delta_days=5, interval_min=1, last_ticks_num=10):
    """
    Predicts one next value using last_ticks_num history ticks from [start_date; to end_date] period with interval_min minutes lag.
    """
    def get_iss_candles(start_date, end_date, interval_min=1, start=0):
        """
        Gets market data candles for [start_date; to end_date] period with interval_min minutes lag.
        """
        if end_date == date(1970, 1, 1):
            end_date = start_date
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        url = f'http://iss.moex.com/iss/engines/currency/markets/selt/boards/cets/securities/usd000utstom/candles.csv?from={start_date_str}&till={end_date_str}&interval={interval_min}&start={start}'
        r = requests.get(url, allow_redirects=True, verify=False, timeout=5)
        return r.content.decode('utf-8')

    def get_iss_dataframe(curr_date, delta_days=1, interval_min=1):
        """
        Creates dataframe from market data for [start_date; to end_date] period with interval_min minutes lag.
        """
        iss_df = pd.DataFrame()
        for n in range(-delta_days, 1, 1):
            _date = curr_date + timedelta(n)
            for i in range(0, 1000000, 500):
                csv_iss_respond = get_iss_candles(start_date=_date, end_date=_date, interval_min=interval_min, start=i)
                if len(csv_iss_respond.split('\n')) <= 6: # stop parsing market data if is has no more rows
                    break
                else:
                    iss_df = iss_df.append(pd.read_csv(StringIO(csv_iss_respond), skiprows=2, sep=';'))
                    iss_df = iss_df.reset_index(drop=True)
        
        return iss_df

    def transform_input_dataframe(df, last_ticks_num):
        """
        Makes some preparations with input dataframe to make it suitable to predict the future price.
        """
        df = df[-(last_ticks_num+1):].reset_index(drop=True)
        df['avg'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4
        # Using price and volume indicators for last_ticks_num ticks:
        for i in range(1, last_ticks_num+1):
            df[f'avg-{i}'] = (df['avg'].shift(i) - df['avg']) / df['avg']
            df[f'volume-{i}'] = (df['volume'].shift(i) - df['volume']) / df['volume']

        df = df[['avg', 'volume', 'avg-1', 'volume-1', 'avg-2', 'volume-2', 'avg-3', 'volume-3', 'avg-4', 'volume-4', 'avg-5', 'volume-5', 'avg-6', 'volume-6', 'avg-7', 'volume-7', 'avg-8', 'volume-8', 'avg-9', 'volume-9', 'avg-10', 'volume-10']]
        df = df[-1:].reset_index(drop=True)
        return df

    result_df = get_iss_dataframe(curr_date=curr_date, delta_days=delta_days, interval_min=interval_min)
    result_df = transform_input_dataframe(result_df, last_ticks_num)

    # Load the trained model from disk
    filename = 'catboost_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(result_df)[0]
    return result


if __name__ == '__main__':
    prediction = predict_upon_candles(curr_date=datetime.today().date(), delta_days=5, interval_min=1)
    print(prediction)