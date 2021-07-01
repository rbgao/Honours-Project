import pandas as pd
xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')
negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

positivelist=positive.values.tolist()
positivelist += [["Able"]]
negativelist = negative.values.tolist()
negativelist += [["Abandon"]]

negative_list = []
for sublist in negativelist:
    for item in sublist:
        negative_list.append(item.lower())

negative_list.remove('unemployed')
negative_list.remove('unemployment')
print(positive_list)