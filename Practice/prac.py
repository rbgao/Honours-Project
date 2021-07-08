from pandas import DataFrame
from datetime import datetime
import spacy
from spacy.tokens import Token
from pprint import pprint
import json

with open('test_data.json', encoding='utf-8') as json_file:
 data = json.load(json_file)

#-------------------------------------Identify all useless keys--------------------------------------------------#

#def getKeys(object, prev_key = None, keys = []):
#    if type(object) != type({}):
#        keys.append(prev_key)
#        return keys
#    new_keys = []
#    for k, v in object.items():
#        if prev_key != None:
#            new_key = "{}.{}".format(prev_key, k)
#        else:
#            new_key = k
#        new_keys.extend(getKeys(v, new_key, []))
#    return new_keys
#
#tokens = []
#for p in data:
#    list = getKeys(p)
#    for x in list:
#        if x not in tokens:
#            tokens.append(x)
#print(tokens)
#    #for p1 in p['Text']:
#    #    for key, value in p1.items():
#    #        pprint("Key:")
#    #        pprint(key)

##-------------------------------------Check dates--------------------------------------------------#

Dates = []
dates_2 = []

for p in data:
    Dates += p["Date"]

for date in Dates:
        location_date = date.replace(u'\xa0', ' ')
        sep = '– ' 
        sep1 = "- "
        date_only = location_date.split(sep, 1)[-1]
        date_only = date_only.split(sep1, 1)[-1]
        converted_date = datetime.strptime(date_only, '%d %B %Y')
        dates_2.append(converted_date.date())

#print(dates_2)

df = DataFrame({'Dates': dates_2, 'Values': ['3','2']})

df = df.sort_values(by="Values")
print(df) 

df.to_excel('test1.xlsx', sheet_name='sheet1', index=False)

# Token.set_extension("is_negation", default=False)
# assert Token.has_extension("is_negation")
# 
# nlp = spacy.load('en_core_web_sm')
# 
# text = " You don't help. You do not care. no care in the world game no lol"
# 
# doc = nlp(text)
# 
# 
# stopwords = nlp.Defaults.stop_words
# stopwords -= {"n't", "not", "no"}
# 
# def negation_words(input):
#     doc = nlp(input)
#     for token in doc:
#         if token.text == "n't" or token.text == "not" or token.text == "no":
#             token._.is_negation = True
#             doc[token.i+1]._.is_negation = True 
#     processed_minutes = " ".join([token.text for token in doc if token._.is_negation == False])
#     return processed_minutes
#         
# 
# def remove_stopwords(minutes):
#  bag = nlp(minutes)
#  processed_minutes = ' '.join([token.text for token in bag if token.text.lower() not in stopwords ])
#  return processed_minutes
# 
# def remove_punctuation_special_chars(minutes):
#  bag = nlp(minutes)
#  processed_minutes = ' '.join([token.text for token in bag 
#  if token.is_punct != True and 
#      token.is_quote != True and 
#      token.is_bracket != True and 
#      token.is_currency != True and 
#      token.is_digit != True])
#  return processed_minutes
# 
# text = remove_stopwords(text)
# text = negation_words(text)
# text = remove_punctuation_special_chars(text)
# doc = nlp(text)
# Number_tokens = 0
# for token in doc:    
#     if token.text != " ":
#         Number_tokens += 1
#     print(token.text)
# print(Number_tokens)
# print(print(len(doc)))