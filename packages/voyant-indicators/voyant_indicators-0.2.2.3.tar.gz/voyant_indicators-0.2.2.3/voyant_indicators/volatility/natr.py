
import pandas as pd
from voyant_indicators.volatility.atr import atr


def natr(df, high, low, close, natr, n):
    """
    The Normalized Average True Range (NATR) is a measure of volatility that is
    directly comparable across assets with different price levels.

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

    df = atr(df, high, low, close, "average_true_range", n)
    df[natr] = 100 * (df["average_true_range"] / df[close])

    return df
