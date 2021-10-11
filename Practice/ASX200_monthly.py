import datetime
import pandas as pd
from pandas.core.frame import DataFrame 

df = pd.read_csv('ASX200.csv', parse_dates=True)

df['month'] = pd.to_datetime(df['Date']).dt.month

df['year'] = pd.to_datetime(df['Date']).dt.year

mthly_avg = df.groupby(['year','month'],as_index=False)['Close'].mean()

df2 = mthly_avg
df2.to_excel('test1.xlsx', sheet_name='sheet1', index=False)
