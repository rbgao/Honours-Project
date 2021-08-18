import re

def footnote_stripper(string):
    new_string = re.sub("\[[0-9][0-9]\]|\[[0-9]\]", "", string)
    return new_string

#x = new_string = re.sub("\[[0-9][0-9]\]|\[[0-9]\]", " ", "It was good.[5]")
#print(x)
