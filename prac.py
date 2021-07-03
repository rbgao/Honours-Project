
import spacy
nlp = spacy.load('en_core_web_sm')

text = " You don't help. You do not care. no"

doc = nlp(text)


stopwords = nlp.Defaults.stop_words
stopwords -= {"n't", "not", "no"}
print(len(stopwords))

def remove_stopwords(minutes):
 bag = nlp(minutes)
 processed_minutes = ' '.join([token.text for token in bag if token.text.lower() not in stopwords ])
 return processed_minutes

text = remove_stopwords(text)
print(text)