
import spacy
from spacy.tokens import Token
from dictionary import positive_list, negative_list, negative_list_with_unemploy

nlp = spacy.load('en_core_web_sm')

## is_negation new attribute for SpaCy tokens

Token.set_extension("is_negation", default=False)
assert Token.has_extension("is_negation")
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
