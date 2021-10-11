import time
import datetime
import pandas as pd

ticker = '^AXJO'
period1 = int(time.mktime(datetime.datetime(1992, 11, 23, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2020, 8, 21, 23, 59).timetuple()))
interval = '1d' # 1d, 1m

query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

df = pd.read_csv(query_string)
# print(df)
df.to_csv('AAPL.csv')

# Source: https://www.youtube.com/watch?v=NjEc7PB0TxQ