#-------------------------------------Packages--------------------------------------------------#

import xlwt 
import json
import spacy
import pandas as pd
from json_flatten import flatten
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token

#-------------------------------------Setup--------------------------------------------------#

## Load in NLP

nlp = spacy.load('en_core_web_sm')

## Test text

# text = "Members noted that the rebound in the demand for goods globally and the upturn in industrial production, particularly in China and elsewhere in east Asia, had continued to support commodity prices. Iron ore prices remained at high levels and the prices of many other commodities, including oil, coal and base metals, had increased strongly in recent months. The rebound in energy prices had been supported by cold weather in the northern hemisphere and the strong recovery in industrial production; base metals prices had also benefited from the rebound in global industrial activity. Other input costs, such as those for shipping, had also risen sharply in preceding months."

## Phrase matcher

matcher_negative = PhraseMatcher(nlp.vocab)
matcher_positive = PhraseMatcher(nlp.vocab)

## is_negation new attribute for SpaCy tokens

Token.set_extension("is_negation", default=False)
assert Token.has_extension("is_negation")

## Add sentencizer

nlp.add_pipe('sentencizer')

#-------------------------------------Dictionary--------------------------------------------------# 

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

## This is removing unemployment given its ambigious context - will investigate other words like high, low
negative_list.remove('unemployed')
negative_list.remove('unemployment')
negative_list = removedup(negative_list)

#-------------------------------------Putting dictionary into phrase matcher for Spacy--------------------------------------------------#

neglist = [nlp.make_doc(text) for text in negative_list]
matcher_negative.add("Negativewords", neglist)

poslist = [nlp.make_doc(text) for text in positive_list]
matcher_positive.add("Positivewords", poslist)

neglist = [nlp.make_doc(text) for text in negative_list]
matcher_negative.add("Negativewords", neglist)

poslist = [nlp.make_doc(text) for text in positive_list]
matcher_positive.add("Positivewords", poslist)

#-------------------------------------Set up output file--------------------------------------------------#

# def output(filename, sheet, list1, list2, list3, list4, x):
#     book = xlwt.Workbook()
#     sh = book.add_sheet(sheet)
# 
#     variables = [x]
#     x_desc = 'Title'
#     desc = [x_desc]
# 
#     col1_name = 'Date'
#     col2_name = 'Negative word count'
#     col3_name = 'Positive word count'
#     col4_name = 'Net negativity score'

#-------------------------------------Tokenisation process--------------------------------------------------#

## Adjusting stopwords

# nlp.Defaults.stop_words -= {"n't", "not"}
# 
# def remove_stopwords(minutes):
#  bag = nlp(minutes)
#  processed_minutes = ' '.join([token.text for token in bag if token.is_stop != True ])
#  return processed_minutes

stopwords = nlp.Defaults.stop_words
stopwords -= {"n't", "not", "no"}

def remove_stopwords(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag if token.text.lower() not in stopwords ])
 return processed_minutes
 
## Removing punctuation

def remove_punctuation_special_chars(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag 
 if token.is_punct != True and 
     token.is_quote != True and 
     token.is_bracket != True and 
     token.is_currency != True and 
     token.is_digit != True])
 return processed_minutes

## Lowercase

def lowercase(minutes):
    bag = nlp(minutes)
    processed_minutes = ' '.join([token.text.lower() for token in bag])
    return processed_minutes

## Lemmatization

def lemmatize_text(minutes):
    bag = nlp(minutes)
    processed_minutes = ''
    for tokens in bag:
        if tokens.pos_ == "ADV":
            if tokens.text[-2:] == "ly":
                tokens.lemma_ = tokens.lemma_[:-2]
        processed_minutes = processed_minutes + " " +tokens.lemma_
    return processed_minutes

## Negation words

def negation_words(input):
    doc = nlp(input)
    for token in doc:
        if token.text == "n't" or token.text == "not" or token.text == "no":
            token._.is_negation = True
            doc[token.i+1]._.is_negation = True 
    processed_minutes = " ".join([token.text for token in doc if token._.is_negation == False])
    return processed_minutes

#-------------------------------------Test code for test text--------------------------------------------------#

# text = remove_punctuation_special_chars(text)
# text = remove_stopwords(text)
# text = lowercase(text)
# text = lemmatize_text(text)
# text = negation_words(text)
## print(text)

#-------------------------------------Creating lists for dates and matches ready for excel--------------------------------------------------#

dates = []

number_negative = []

number_positive = []

number_difference = []

number_total = []



#-------------------------------------Opening JSON file--------------------------------------------------#

with open('test_data.json') as json_file:
 data = json.load(json_file)

#-------------------------------------Looping over each date in JSON, and flattening to a list--------------------------------------------------#

for p in data:
    # del data[0]['Text']['Members present']
    # del data[0]['Text']['Others participating']
    # del data[0]['Text']['The decision']
    data_flattened=flatten(p)
    data_list = data_flattened.values()
    
#-------------------------------------Putting date into list--------------------------------------------------#

    dates += p['Date']

#-------------------------------------Turning the text in each date into a string, and cleaning it--------------------------------------------------#

    string = ""
    for paragraph in data_list:
        string = string + " " + paragraph
        #para = nlp(paragraph)
        # print(para.text)
        #minutess = [sent.string.strip() for sent in para.sents]
        #print(minutess)

    string = remove_punctuation_special_chars(string)
    string = remove_stopwords(string)
    string = lowercase(string)
    string = lemmatize_text(string)

#-------------------------------------Identifying negative and positive words for each date--------------------------------------------------#

    doc = nlp(string)

    negative_matches = matcher_negative(doc)
    #print("Negative matches found:", len(negative_matches))
    number_negative.append(len(negative_matches))

    positive_matches = matcher_positive(doc)
    #print("Positive matches found:", len(positive_matches))
    number_positive.append(len(positive_matches))

    #print("Net negativity score:", len(negative_matches) - len(positive_matches))
    number_difference.append(len(negative_matches) - len(positive_matches))

    #print("Total number of tokens:", len(doc))
    number_total.append(len(doc))

print(dates)
print(number_negative)
print(number_positive)
print(number_difference)
print(number_total)
# with open("words.txt", "w") as text_file:
#     for match_id, start, end in negative_matches:
#         text_file.write("Negative word: " + doc[start:end].text + " \n")
#     for match_id, start, end in positive_matches:
#         text_file.write("Positive word: " + doc[start:end].text + '\n')
# text_file.close()



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
