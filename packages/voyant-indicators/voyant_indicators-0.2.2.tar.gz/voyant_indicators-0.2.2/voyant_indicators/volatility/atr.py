
import pandas as pd
from voyant_indicators.trend.ema import ema
from voyant_indicators.util.trange import trange


def atr(df, high, low, close, atr, n):
    """
    The Average True Range (ATR) is a Welles Wilder style moving average of the
    True Range. The ATR is a measure of volatility. High ATR values indicate
    high volatility, and low values indicate low volatility, often seen when
    the price is flat.

    Parameters:
        df (pd.DataFrame): DataFrame which contain the asset information.
        high (string): the column name for the period highest price  of the asset.
        low (string): the column name for the period lowest price of the asset.
        close (string): the column name for the closing price of the asset.
        atr (string): the column name for the atr values.
        n (int): the total number of periods.

    Returns:
        df (pd.DataFrame): Dataframe with average true range of the asset calculated.

    """

    df = trange(df, high, low, close, "true_range")
    prev_atr = df.loc[0 : n - 1, "true_range"].sum() / n
    df.loc[n - 1, atr] = prev_atr
    df = df.drop(df.index[: n - 1]).reset_index(drop=True)
    df = df.fillna(0)
    avg_trs = [0.0]
    for row in df.loc[1:, ["true_range", atr]].itertuples(index=False):
        avg_trs.append((prev_atr * (n - 1) + row[0]) / n)
        prev_atr = avg_trs[-1]
    df[atr] += avg_trs

    return df
