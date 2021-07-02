import spacy
nlp = spacy.load('en_core_web_sm')

text = "SHARPLY"

doc = nlp(text)

for token in doc:
    print(token.pos_)