import json
f = open('Practice/data1.json')
file = json.load(f)

file= file.replace('\n' , '').replace ('\t' , '').replace ('\r' , '').replace ('<\p>' , '')   # do your cleanup here
data = json.loads(file)