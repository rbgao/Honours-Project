from text_cleaning import remove_punctuation_special_chars, remove_stopwords, lowercase, lemmatize_text, negation_words
import spacy
from html_stripper import strip_tags

nlp = spacy.load('en_core_web_sm')


## Test text

text = "The rebound in energy prices had been supported by cold weather in the northern hemisphere and the strong recovery in industrial production; base metals prices had also benefited from the rebound in global industrial activity. Other input costs, such as those for shipping, had also risen sharply in preceding months."

#-------------------------------------Test code for test text--------------------------------------------------#

text = strip_tags(text)
text = remove_punctuation_special_chars(text)
text = remove_stopwords(text)
text = lowercase(text)
text = lemmatize_text(text)
text = negation_words(text)
 
print(text)
doc = nlp(text)
number = -1
for token in doc:
    number += 1
print(number)
with open("words.txt", "w") as text_file:
    for token in doc:
        text_file.write(token.text+ " \n")
text_file.close()