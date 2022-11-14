import pandas as pd


def get_candle_ob(Candle, OB):
    Candle = pd.DataFrame.from_records(Candle)
    OB = pd.DataFrame.from_records(OB)

    result = {}
    result['candle'] = Candle.to_dict('records')
    result['ob'] = OB.to_dict('records')

    return result
