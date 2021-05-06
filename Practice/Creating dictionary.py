import pandas as pd
xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')
negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

positivelist=positive.values.tolist()
positivelist.append('Able')
negativelist = negative.values.tolist()
negativelist.append('Abandon')

negative_list = []
for sublist in negativelist:
    for item in sublist:
        negative_list.append(item.lower())
print(negative_list)
