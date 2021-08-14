#-------------------------------------Packages--------------------------------------------------#

import re
import json
import spacy
import pandas as pd
from pandas import DataFrame
from json_flatten import flatten
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token
from datetime import datetime
from io import StringIO

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
#-------------------------------------Setup--------------------------------------------------#

## Load in NLP

nlp = spacy.load('en_core_web_sm')

## Test text

#text = "<li>they have expertise in <strong>credit and liquidity risk management</strong>, having a long history and ongoing relationships that generate private information about customers.</li>"

## Phrase matcher

matcher_negative = PhraseMatcher(nlp.vocab)
matcher_positive = PhraseMatcher(nlp.vocab)
matcher_negative_with_unemploy = PhraseMatcher(nlp.vocab)

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
negative_list_with_unemploy = removedup(negative_list)
negative_list.remove('unemployed')
negative_list.remove('unemployment')
negative_list = removedup(negative_list)

## Keeping them in 

#-------------------------------------Putting dictionary into phrase matcher for Spacy--------------------------------------------------#

neglist = [nlp.make_doc(text) for text in negative_list]
matcher_negative.add("Negativewords", neglist)

neglist_with_unemploy =  [nlp.make_doc(text) for text in negative_list_with_unemploy]
matcher_negative_with_unemploy.add("Negativewords", neglist_with_unemploy)

poslist = [nlp.make_doc(text) for text in positive_list]
matcher_positive.add("Positivewords", poslist)

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
            try:
                if doc[token.i+1].text in positive_list or doc[token.i+1].text in negative_list:
                    doc[token.i+1]._.is_negation = True 
            except:
                pass
    processed_minutes = " ".join([token.text for token in doc if token._.is_negation == False])
    return processed_minutes

#-------------------------------------Test code for test text--------------------------------------------------#

#text = strip_tags(text)
#text = remove_punctuation_special_chars(text)
#text = remove_stopwords(text)
#text = lowercase(text)
#text = lemmatize_text(text)
#text = negation_words(text)
#
#print(text)
# doc = nlp(text)
# number = -1
# for token in doc:
#     number += 1
# print(number)
# with open("words.txt", "w") as text_file:
#     for token in doc:
#         text_file.write(token.text+ " \n")
# text_file.close()

#-------------------------------------Creating lists for dates and matches ready for excel--------------------------------------------------#

dates_1 = []

dates_2 = []

dates_first = [] # Use with speeches, as multiple dates

dates_second = [] 

speaker = [] # Use with speeches

speaker_first = []

speaker_second = []

position = [] # Use with speeches

position_first = []

position_second = []


number = []

number_negative = []

number_negative_with_unemploy = []

number_positive = []

number_difference = []

number_difference_with_unemploy = [] 

number_total = []

net_negativity_score = []

net_negativity_score_with_unemploy = []

percentage_negative = [] 

percentage_positive = []

#-------------------------------------Opening JSON file--------------------------------------------------#

with open('speeches_data.json', encoding='utf-8') as json_file:
 data = json.load(json_file)

#-------------------------------------Looping over each date in JSON, and flattening to a list. Deleting useless elements--------------------------------------------------#
number1 = 0

for p in data:
    

    dates_first.append(p['Date'][0])
    #try:
    #    dates_second.append(p['Date'][1])
    #except:
    #    dates_second.append('')
    #
    #speaker_first.append(p['Speaker'][0])
    #try:
    #    speaker_second.append(p['Speaker'][1])
    #except:
    #    speaker_second.append('')
#
    #position_first.append(p['Position'][0])
    #try:
    #    position_second.append(p['Position'][1])
    #except:
    #    position_second.append('')
    del p['Date']
    #del p['Speaker']
    #del p['Position']
    #del p['URL']
#    try:
#        del p['Text']['Members Present']
#    except: 
#        pass
#    try:
#        del p['Text']['Members present']
#    except: 
#        pass
#    try:
#        del p['Text']['Others Present']
#    except: 
#        pass
#    try:
#        del p['Text']['Others present']
#    except: 
#        pass
#    try:
#        del p['Text']['Members Participating']
#    except: 
#        pass
#    try:
#        del p['Text']['Members participating']
#    except: 
#        pass
#    try:
#        del p['Text']['Others Participating']
#    except: 
#        pass
#    try:
#        del p['Text']['Others participating']
#    except: 
#        pass
#    try:
#        del p['Text']['The decision']
#    except: 
#        pass
#    try:
#        del p['Text']['The Decision']
#    except: 
#        pass
#    try:
#        del p['Text']['Present']
#    except: 
#        pass
#    try:
#        del p['Text']['Minutes']
#    except: 
#        pass
#    try:
#        del p['Text']['Board Member']
#    except: 
#        pass
#    try:
#        del p['Text']['Board Members']
#    except: 
#        pass
#    try:
#        del p['Text']['Governor - Final Meeting'] ## Maybe not? 
#    except: 
#        pass
    data_flattened=flatten(p)
    data_list = data_flattened.values()

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
    string = negation_words(string)

#-------------------------------------Identifying negative and positive words for each date--------------------------------------------------#

    doc = nlp(string)

    negative_matches = matcher_negative(doc)
    #print("Negative matches found:", len(negative_matches))
    number_negative.append(len(negative_matches))
    
    negative_matches_with_unemploy = matcher_negative_with_unemploy(doc)
    #print("Negative matches found:", len(negative_matches))
    number_negative_with_unemploy.append(len(negative_matches_with_unemploy))

    positive_matches = matcher_positive(doc)
    #print("Positive matches found:", len(positive_matches))
    number_positive.append(len(positive_matches))

    #print("Net negativity score:", len(negative_matches) - len(positive_matches))
    number_difference.append(len(negative_matches) - len(positive_matches))

    number_difference_with_unemploy.append(len(negative_matches_with_unemploy) - len(positive_matches))

    #print("Total number of tokens:", len(doc))
    number = -1
    for token in doc:
        number += 1
    number_total.append(number)

    net_negativity_score.append((len(negative_matches) - len(positive_matches))/number)
    
    net_negativity_score_with_unemploy.append((len(negative_matches_with_unemploy) - len(positive_matches))/number)
    
    percentage_negative.append(len(negative_matches)/number)

    percentage_positive.append(len(positive_matches)/number)

    number1 += 1
    print(number1)
    
    #with open("words1.txt", "w") as text_file:
    #    for token in doc:
    #        text_file.write(token.text+ " \n")
    ##for match_id, start, end in negative_matches:
    ##    text_file.write("Negative word: " + doc[start:end].text + " \n")
    ##for match_id, start, end in positive_matches:
    ##    text_file.write("Positive word: " + doc[start:end].text + '\n')
    #text_file.close()

#-------------------------------------Cleaning up dates and converting them to datetime format for minutes--------------------------------------------------#

#for date in dates_1:
#        location_date = date.replace(u'\xa0', ' ')
#        sep = '– ' 
#        sep1 = "- "
#        date_only = location_date.split(sep, 1)[-1]
#        date_only = date_only.split(sep1, 1)[-1]
#        converted_date = datetime.strptime(date_only, '%d %B %Y')
#        dates_2.append(converted_date)

#-------------------------------------Printing out lists--------------------------------------------------#

# print(dates_2)
# print(number_negative)
# print(number_positive)
# print(number_difference)
# print(number_total)

#-------------------------------------Output to excel by putting lists into each column, and then sorting by date--------------------------------------------------#

#print(len(dates_2))
#print(len(number_negative))
#print(len(number_positive))
#print(len(number_negative_with_unemploy))
#print(len(number_difference))
#print(len(number_total))
#print(len(net_negativity_score_with_unemploy))
#print(len(net_negativity_score))
#print(len(percentage_negative))
#print(len(percentage_positive))

## For speeches
df = DataFrame({'Dates': dates_first,'Second date': dates_second, 'Speaker':speaker_first, 'Position': position_first ,'Secondary speaker': speaker_second, 'Seconday position': position_second, 'Number of negative words': number_negative, 'Number of negative words including unemploy':number_negative_with_unemploy, 'Number of positive words': number_positive, 'Net negativity count': number_difference, 'Total token count': number_total, 'Net negativity score': net_negativity_score, 'Net negativity score with unemploy': net_negativity_score_with_unemploy,'Percentage negative': percentage_negative, 'Percentage positive': percentage_positive})


## For minutes
# For minutes df = DataFrame({'Dates': dates_2, 'Number of negative words': number_negative, 'Number of negative words including unemploy':number_negative_with_unemploy, 'Number of positive words': number_positive, 'Net negativity count': number_difference, 'Total token count': number_total, 'Net negativity score': net_negativity_score, 'Net negativity score with unemploy': net_negativity_score_with_unemploy,'Percentage negative': percentage_negative, 'Percentage positive': percentage_positive, 'Speaker': speaker, 'Position': position})

df = df.sort_values(by="Dates")

print(df) 

df.to_excel('test.xlsx', sheet_name='sheet1', index=False)

print("Done")