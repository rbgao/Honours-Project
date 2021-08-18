#-------------------------------------Packages--------------------------------------------------#

## JSON
import json
from json_flatten import flatten

## Pandas
import pandas as pd
from pandas import DataFrame

## Spacy
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token

## Other
import re
from datetime import datetime

## Strippers
from footnote_stripper import footnote_stripper
from html_stripper import strip_tags

## Sentiment matcher
from dictionary import matcher_positive, matcher_negative, matcher_negative_with_unemploy

## Text cleaning
from text_cleaning import remove_stopwords, remove_punctuation_special_chars, negation_words, lowercase, lemmatize_text

## Date conversion
from date_converter import date_converter_SMP, date_converter_minutes

## Token checker
from token_checker import token_checker
#-------------------------------------Setup--------------------------------------------------#

## Load in NLP

nlp = spacy.load('en_core_web_sm')

#-------------------------------------Creating lists for dates and matches ready for excel--------------------------------------------------#

dates_1 = []

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
#
##-------------------------------------Looping over each date in JSON, and flattening to a list. Deleting useless elements--------------------------------------------------#
number1 = 0

for p in data:

    #dates_first.append(p['Date'])    # For minutes, SMP
    dates_first.append(p['Date'][0])
    try:
        dates_second.append(p['Date'][1])
    except:
        dates_second.append('')
    
    speaker_first.append(p['Speaker'][0])
    try:
        speaker_second.append(p['Speaker'][1])
    except:
        speaker_second.append('')
    position_first.append(p['Position'][0])
    try:
        position_second.append(p['Position'][1])
    except:
        position_second.append('')
    del p['Date']
    del p['Speaker']
    del p['Position']
    del p['URL']

    data_flattened=flatten(p)
    data_list = data_flattened.values()

##-------------------------------------Turning the text in each date into a string, and cleaning it--------------------------------------------------#
    string = ""
    for paragraph in data_list:
        paragraph = footnote_stripper(paragraph)      # For speeches
        string = string + " " + paragraph

    string = strip_tags(string)
    string = remove_punctuation_special_chars(string)
    string = remove_stopwords(string)
    string = lowercase(string)
    string = lemmatize_text(string)
    string = negation_words(string)
##-------------------------------------Identifying negative and positive words for each date--------------------------------------------------#

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
    #token_checker(doc)

#-------------------------------------Cleaning up dates and converting them to datetime format for minutes--------------------------------------------------#

#dates_2 = date_converter_minutes(dates_first)

#-------------------------------------Cleaning up dates and converting them to datetime format for SMP--------------------------------------------------#

#dates_2 = date_converter_SMP(dates_first)
    
#-------------------------------------Printing out lists--------------------------------------------------#

# print(dates_2)
# print(number_negative)
# print(number_positive)
# print(number_difference)
# print(number_total)

#-------------------------------------Output to excel by putting lists into each column, and then sorting by date--------------------------------------------------#
#print(dates_first)
#print(dates_2)
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
#df = DataFrame({'Dates': dates_2, 'Number of negative words': number_negative, 'Number of negative words including unemploy':number_negative_with_unemploy, 'Number of positive words': number_positive, 'Net negativity count': number_difference, 'Total token count': number_total, 'Net negativity score': net_negativity_score, 'Net negativity score with unemploy': net_negativity_score_with_unemploy,'Percentage negative': percentage_negative, 'Percentage positive': percentage_positive})

df = df.sort_values(by="Dates")

print(df) 

df.to_excel('test.xlsx', sheet_name='sheet1', index=False)

print("Done")