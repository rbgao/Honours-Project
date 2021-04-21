import pandas as pd
xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')
negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

print(positive)
