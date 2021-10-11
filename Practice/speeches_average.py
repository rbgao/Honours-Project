import pandas as pd
from pandas.core.frame import DataFrame 

df = pd.read_excel('Speech_data.xlsx', parse_dates=True)

df['month'] = pd.to_datetime(df['Dates']).dt.month

df['year'] = pd.to_datetime(df['Dates']).dt.year

df['decfeb'] = (df['month'] == 12 or df['month'] == 1 or df['month'] == 2) * 1

