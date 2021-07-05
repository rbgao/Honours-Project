
import spacy
from spacy.tokens import Token

Token.set_extension("is_negation", default=False)
assert Token.has_extension("is_negation")

nlp = spacy.load('en_core_web_sm')

text = " You don't help. You do not care. no care in the world game no lol"

doc = nlp(text)


stopwords = nlp.Defaults.stop_words
stopwords -= {"n't", "not", "no"}

def negation_words(input):
    doc = nlp(input)
    for token in doc:
        if token.text == "n't" or token.text == "not" or token.text == "no":
            token._.is_negation = True
            doc[token.i+1]._.is_negation = True 
    processed_minutes = " ".join([token.text for token in doc if token._.is_negation == False])
    return processed_minutes
        

def remove_stopwords(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag if token.text.lower() not in stopwords ])
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

text = remove_stopwords(text)
text = negation_words(text)
text = remove_punctuation_special_chars(text)
doc = nlp(text)
Number_tokens = 0
for token in doc:    
    if token.text != " ":
        Number_tokens += 1
    print(token.text)
print(Number_tokens)
print(print(len(doc)))