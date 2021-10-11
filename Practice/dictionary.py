import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')

##-------------------------------------Dictionary--------------------------------------------------# 

## Load in dictionary 

xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')

## Read dictionary

negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

## Remove duplicate function

def removedup(x):
  return list(dict.fromkeys(x))

## Append missing values that were cut off 

positivelist=positive.values.tolist()
positivelist += [["ABLE"]]
negativelist = negative.values.tolist()
negativelist += [["ABANDON"]]

## Transforming dictionary into a flattened list, and processing each word (e.g. lemmatisation, lower case)

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

## This is removing unemployment given its ambigious context - robustness check for when it is included
negative_list_with_unemploy = removedup(negative_list)
print(len(negative_list_with_unemploy))
print(len(positive_list))
negative_list.remove('unemployed')
negative_list.remove('unemployment')
negative_list = removedup(negative_list)

#-------------------------------------Putting dictionary into phrase matcher for Spacy--------------------------------------------------#

## Phrase matcher

matcher_negative = PhraseMatcher(nlp.vocab)
matcher_positive = PhraseMatcher(nlp.vocab)
matcher_negative_with_unemploy = PhraseMatcher(nlp.vocab)

neglist = [nlp.make_doc(text) for text in negative_list]
matcher_negative.add("Negativewords", neglist)

neglist_with_unemploy =  [nlp.make_doc(text) for text in negative_list_with_unemploy]
matcher_negative_with_unemploy.add("Negativewords", neglist_with_unemploy)

poslist = [nlp.make_doc(text) for text in positive_list]
matcher_positive.add("Positivewords", poslist)



