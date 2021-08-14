
import json

Dates = []

with open('smp_data_pre2006_us.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

list = []
for p in data:
    json_1 = {}
    json_2 = {}
    json_1['Date'] = p['Date'][0]
    json_2['Subtext'] = p['Text']
    json_1['Text'] = json_2
    list.append(json_1)

with open('smp_data_pre2006_s.json','w', encoding = 'utf-8') as f:
   json.dump(list,f)