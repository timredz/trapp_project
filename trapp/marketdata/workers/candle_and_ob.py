import pandas as pd


def get_candle_ob(Candle, OB):
    Candle = pd.DataFrame.from_records(Candle)
    OB = pd.DataFrame.from_records(OB)
    OB['val'] = OB['price'] * OB['quantity']

    result = {}
    result['candle'] = Candle.to_dict('records')

    ob = {}
    dfb = OB[OB['buysell'] == 'B']
    dfs = OB[OB['buysell'] == 'S']
    ob['buy'] = dfb.sort_values('price', ascending=False).to_dict('records')
    ob['sell'] = dfs.to_dict('records')
    ob['buy_vol'] = dfb['quantity'].sum()
    ob['sell_vol'] = dfs['quantity'].sum()
    ob['buy_avg'] = dfb['val'].sum() / dfb['quantity'].sum()
    ob['sell_avg'] = dfs['val'].sum() / dfs['quantity'].sum()

    result['ob'] = ob

    return result
