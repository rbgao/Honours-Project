import re

def footnote_stripper(string):
    new_string = re.sub("\[\d\]", "", string)
    return new_string

#x = new_string = re.sub("\[\d\]", " ", "It was good.[2]")
#print(x)
#