### Packages ###

import json
import spacy
import pandas as pd
from json_flatten import flatten
# from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

#+# Packages #+#

nlp = spacy.load('en_core_web_sm')
text = "Members noted that the rebound in the demand for goods globally and the upturn in industrial production, particularly in China and elsewhere in east Asia, had continued to support commodity prices. Iron ore prices remained at high levels and the prices of many other commodities, including oil, coal and base metals, had increased strongly in recent months. The rebound in energy prices had been supported by cold weather in the northern hemisphere and the strong recovery in industrial production; base metals prices had also benefited from the rebound in global industrial activity. Other input costs, such as those for shipping, had also risen sharply in preceding months."
matcher_negative = PhraseMatcher(nlp.vocab)
matcher_positive = PhraseMatcher(nlp.vocab)
xlsx = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')

### Dictionary ### 

negative = pd.read_excel(xlsx, 'Negative')
positive = pd.read_excel(xlsx, 'Positive')

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

#+# Dictionary #+# 

nlp.add_pipe('sentencizer')
with open('test_data.json') as json_file:
 data = json.load(json_file)

for p in data:
    del data[0]['Text']['Members present']
    del data[0]['Text']['Others participating']
    del data[0]['Text']['The decision']
    data_flattened=flatten(data)

data_list = data_flattened.values()

nlp.Defaults.stop_words -= {"n't", "not"}

def remove_stopwords(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag if token.is_stop != True ])
 return processed_minutes

def remove_punctuation_special_chars(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag 
 if token.is_punct != True and 
     token.is_quote != True and 
     token.is_bracket != True and 
     token.is_currency != True and 
     token.is_digit != True])
 return processed_minutes

def lowercase(minutes):
    bag = nlp(minutes)
    processed_minutes = ' '.join([token.text.lower() for token in bag])
    return processed_minutes

def lemmatize_text(minutes):
    bag = nlp(minutes)
    processed_minutes = ''
    for tokens in bag:
        if tokens.pos_ == "ADV":
            if tokens.text[-2:] == "ly":
                tokens.lemma_ = tokens.lemma_[:-2]
        processed_minutes = processed_minutes + " " + "" +tokens.lemma_
    return processed_minutes

### For running on text string ###

text = remove_punctuation_special_chars(text)
text = remove_stopwords(text)
text = lowercase(text)
text = lemmatize_text(text)
print(text)

#+# For running on text string #+#

### For running on json files ###

# string = ""
# for paragraph in data_list:
#     string = string + " " + paragraph
#     #para = nlp(paragraph)
#     # print(para.text)
#     #minutess = [sent.string.strip() for sent in para.sents]
#     #print(minutess)
# 
# string = remove_punctuation_special_chars(string)
# string = remove_stopwords(string)
# string = lowercase(string)
# string = lemmatize_text(string)

#+# For running on json files #+#


### Defining list of negative and positive words ###

neglist = [nlp.make_doc(text) for text in negative_list]
matcher_negative.add("Negativewords", neglist)

poslist = [nlp.make_doc(text) for text in positive_list]
matcher_positive.add("Positivewords", poslist)

#+# Defining list of negative and positive words #+#

doc = nlp(text)
negative_matches = matcher_negative(doc)
print("Negative matches found:", len(negative_matches))
positive_matches = matcher_positive(doc)
print("Positive matches found:", len(positive_matches))
with open("words.txt", "w") as text_file:
    for match_id, start, end in negative_matches:
        text_file.write("Negative word: " + doc[start:end].text + " \n")
    for match_id, start, end in positive_matches:
        text_file.write("Positive word: " + doc[start:end].text + '\n')
text_file.close()

#+# Identifying negative and positive words #+#



### Don't worry about this ###
# import spacy
# from spacy.lang.en import English # updated
# from spacy.lang.en.stop_words import STOP_WORDS
# from collections import Counter
# import re
# 
# nlp = spacy.load("en_core_web_sm")
# 
# def split_minutess(document):
#  minutess = [sent.string.strip() for sent in doc.sents]
#  return minutess
# 
# def remove_stopwords(minutes):
#  minutes = nlp(minutes)
#  processed_minutes = ' '.join([token.text for token in minutes if token.is_stop != True ])
#  return processed_minutes
# Removes stopwords from spaCy default stopword list
# nlp.Defaults.stop_words -= {"my_stopword_1", "my_stopword_2"}
# # Adds custom stopwords into spaCy default stopword list
# nlp.Defaults.stop_words |= {"my_stopword_1", "my_stopword_2"}
# # Prints spaCy default stopwords
# def remove_punctuation_special_chars(minutes):
#  minutes = nlp(minutes)
#  processed_minutes = ' '.join([token.text for token in minutes 
#  if token.is_punct != True and 
#      token.is_quote != True and 
#      token.is_bracket != True and 
#      token.is_currency != True and 
#      token.is_digit != True])
#  return processed_minutes
# 
# def lemmatize_text(minutes):
#     minutes = nlp(minutes)
#     processed_minutes = ' '.join([word.lemma_ for word in 
#     minutes])
#     
#     return processed_minutes
