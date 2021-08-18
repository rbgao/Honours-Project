def unicode_stripper(string):
    newstring = string.encode("ascii", "ignore")
    newstring = newstring.decode("utf-8")
    return newstring
#x = unicode_stripper("around 6\u201312 months earlier than previously expected. The unemployment rate is likely to have already peaked and is now expected to decline steadily to around 5\u00bc per cent by mid 2023.")
#print(x)