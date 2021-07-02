import pandas as pd
import spacy
xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')
negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

nlp = spacy.load('en_core_web_sm')

def removedup(x):
  return list(dict.fromkeys(x))

positivelist=positive.values.tolist()
positivelist += [["ABLE"]]
negativelist = negative.values.tolist()
negativelist += [["ABANDON"]]

positive_list = []
for sublist in positivelist:
    for item in sublist:
        doc = nlp(item.lower())
        for word in doc:
            if word.pos_ == "ADV":
                if word.text[-2:] == "ly":
                    word.lemma_ = word.lemma_[:-2]
            positive_list.append(word.lemma_.lower())
positive_list = removedup(positive_list)

negative_list = []
for sublist in negativelist:
    for item in sublist:
        doc = nlp(item.lower())
        for word in doc:
            if word.pos_ == "ADV":
                if word.text[-2:] == "ly":
                    word.lemma_ = word.lemma_[:-2]
            negative_list.append(word.lemma_.lower())
negative_list.remove('unemployed')
negative_list.remove('unemployment')
negative_list = removedup(negative_list)

print(negative_list)

