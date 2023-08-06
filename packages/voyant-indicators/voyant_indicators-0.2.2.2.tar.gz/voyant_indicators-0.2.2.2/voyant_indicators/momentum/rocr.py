import pandas as pd


def rocr(df, n, price="close", col="rocr"):
    """
    The Rate-of-Change Ratio (ROCR) indicator, which is also referred to as simply
    Momentum, is a pure momentum oscillator that measures the percent change in
    price from one period to the next.

    Parameters:
        df (pd.DataFrame): DataFrame which contain the asset information.
        price (string): the column name of the price of the asset.
        rocr (string): the column name for the rate of change ratio.
        n (int): the total number of periods.

    Returns:
        df (pd.DataFrame): Dataframe with rocr of the asset calculated.

    """

    df = df.copy().reset_index(drop=True)
    if df.shape[0] < n:
        df[col] = None
        return df

    df[col] = df[price] / df[price].shift(n)
    #df = df.dropna().reset_index(drop=True)

    return df
