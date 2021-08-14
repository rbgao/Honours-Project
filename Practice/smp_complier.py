import json

with open('smp_data_pre2006_s.json', encoding='utf-8') as json_file1:
    data1 = json.load(json_file1)

with open('smp_data_post2007_s.json', encoding='utf-8') as json_file2:
    data2 = json.load(json_file2)

list = data1 + data2

with open('smp_data_s.json','w', encoding = 'utf-8') as f:
   json.dump(list,f)