from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#test = "I like cats a lot"
def senti_score(text):
    senti = SentimentIntensityAnalyzer()
    sentiment_dict = senti.polarity_scores(text)
    return (sentiment_dict['neg'] - sentiment_dict['pos'])

#print(senti_score(test))

