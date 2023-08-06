def ohlcv(df,col,n=1):

	df = df.copy()
	df = df[['datetime',col]]

	return df.tail(n)