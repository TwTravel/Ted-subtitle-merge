import json


with open('tedInfos.json') as data_file:    
    data = json.load(data_file)

interval = 20

i = 0
numOfDatas = len(data)
while i < numOfDatas:
  
  endIdx = min(i + interval, numOfDatas)
  content = json.dumps(data[i:endIdx], ensure_ascii=False) 
  fileWrite = open('infos/%d.json' % i,'w')
  fileWrite.write(content)
  fileWrite.close()
  i = endIdx


