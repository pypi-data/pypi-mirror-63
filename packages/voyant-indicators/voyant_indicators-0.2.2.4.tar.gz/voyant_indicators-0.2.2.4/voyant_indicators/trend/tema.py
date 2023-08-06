
import pandas as pd

from voyant_indicators.overlapping_studies.sma import sma
from voyant_indicators.overlapping_studies.ema import ema
from voyant_indicators.overlapping_studies.wma import wma
from voyant_indicators.overlapping_studies.dema import dema
from voyant_indicators.overlapping_studies.tema import tema

def tema(df, price, tema, n):
    """
    Triple Exponential Moving Average (TEMA) was designed to smooth price
    fluctuations and filter out volatility, thereby making it easier to
    dentify trends without the lag associated with moving averages.

    The TEMA equation is a composite of a single exponential moving average,
    a double exponential moving average, and a triple exponential moving average.

    TEMA = 3 * EMA(p, n) - 3 * EMA(EMA(p, n), n) + EMA(EMA(EMA(p, n), n), n)

    Parameters:
        df (pd.DataFrame): DataFrame which contain the asset price.
        price (string): the column name of the price of the asset.
        tema (string): the column name for the n-day double exponential moving average results.
        n (int): the total number of periods.

    Returns:
        df (pd.DataFrame): Dataframe with n-day double exponential moving average of the asset calculated.

    """

    df = ema(df, price, tema + "_ema", n)
    df = ema(df[n - 1 :], tema + "_ema", tema + "_ema_2", n)
    df = ema(df[n - 1 :], tema + "_ema_2", tema + "_ema_3", n)
    df[tema] = (
        3 * df[tema + "_ema"] - 3 * df[tema + "_ema_2"] + df[tema + "_ema_3"]
    )
    df = df.dropna().reset_index(drop=True)
    df.drop(
        [tema + "_ema", tema + "_ema_2", tema + "_ema_3"], axis=1, inplace=True
    )

    return df
