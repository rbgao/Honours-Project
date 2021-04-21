import json
import spacy
nlp = spacy.load('en_core_web_sm')
from json_flatten import flatten
with open('test_data.json') as json_file:
 data = json.load(json_file)

for p in data:
    del data[0]['Text']['Members present']
    del data[0]['Text']['Others participating']
    del data[0]['Text']['The decision']
    data_flattened=flatten(data)

data_list = data_flattened.values()
string = ""
for paragraph in data_list:
    string = string +" " + paragraph

bag = nlp(string)

filtered_tokens = [token for token in  if not token.is_stop]


# print(data)
# import spacy
# from spacy.lang.en import English # updated
# from spacy.lang.en.stop_words import STOP_WORDS
# from collections import Counter
# import re
# 
# nlp = spacy.load("en_core_web_sm")
# 
# def split_sentences(document):
#  sentences = [sent.string.strip() for sent in doc.sents]
#  return sentences
# 
# def remove_stopwords(sentence):
#  sentence = nlp(sentence)
#  processed_sentence = ' '.join([token.text for token in sentence if token.is_stop != True ])
#  return processed_sentence
# Removes stopwords from spaCy default stopword list
# nlp.Defaults.stop_words -= {"my_stopword_1", "my_stopword_2"}
# # Adds custom stopwords into spaCy default stopword list
# nlp.Defaults.stop_words |= {"my_stopword_1", "my_stopword_2"}
# # Prints spaCy default stopwords
# def remove_punctuation_special_chars(sentence):
#  sentence = nlp(sentence)
#  processed_sentence = ' '.join([token.text for token in sentence 
#  if token.is_punct != True and 
#      token.is_quote != True and 
#      token.is_bracket != True and 
#      token.is_currency != True and 
#      token.is_digit != True])
#  return processed_sentence
# 
# def lemmatize_text(sentence):
#     sentence = nlp(sentence)
#     processed_sentence = ' '.join([word.lemma_ for word in 
#     sentence])
#     
#     return processed_sentence
