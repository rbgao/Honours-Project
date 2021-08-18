def token_checker(doc):
    with open("words1.txt", "a") as text_file:
        for token in doc:
            text_file.write(token.text+ " \n")
    #for match_id, start, end in negative_matches:
    #    text_file.write("Negative word: " + doc[start:end].text + " \n")
    #for match_id, start, end in positive_matches:
    #    text_file.write("Positive word: " + doc[start:end].text + '\n')
    text_file.close()
