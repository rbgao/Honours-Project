
import json
from footnote_stripper import footnote_stripper
from unicode_stripper import unicode_stripper

Dates = []

with open('smp_data_post2007_us.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

for p in data:
    if len(p['Date']) != 0:
        Dates.append(p['Date'][0])
    else:
        p['Date'] = ['']

def removedup(x):
  return list(dict.fromkeys(x))
Dates = removedup(Dates)
print(Dates)
print(len(Dates))

list = []

for date in Dates:
   json_1 = {}
   json_2 = {}
   for p in data:
       if p['Date'][0] == date:
           #print(p['Section'])
           sectiontitle =""
           for word in p['Section']:
              sectiontitle += word
           if sectiontitle.replace(" ", "").lower() != "listoftables":
               json_2[sectiontitle] = p['Text']
               #json_2[sectiontitle + "_url"] = p['URL']
       json_1['Date'] = date
       json_1['Text'] = json_2
   list.append(json_1)
with open('smp_data_post2007_s.json','w', encoding = 'utf-8') as f:
   json.dump(list,f)