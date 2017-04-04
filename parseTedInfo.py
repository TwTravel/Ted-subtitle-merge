#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import json
import sys
from collections import OrderedDict
import json



def GetTitleAndURL(id):
  for attempt in range(10):
    try:
      command = "curl -s http://www.ted.com/talks/view/id/%s" % id
      output = os.popen(command).readlines()[0]
      url = output.split('"')[1]
      title = url.split('/')[-1]
      title = title.title().replace('_', ' ')
      return {"title" : title, 'url' : url}
    except:
      print id, "exe------------"
      continue


fromIdx = int(sys.argv[1])
toIdx = int(sys.argv[2])


for i in xrange(fromIdx,toIdx):
  print i
  obj = {}
  try:
    obj = GetTitleAndURL(str(i))
  except Exception, e:
    continue
  else:
    if len(obj["url"]) < 4:
      continue
    if obj["url"][0:4] != "http":
      continue

    obj["id"] = i
    sort_order = ['id', 'title', 'url']
    obj_ordered = OrderedDict(sorted(obj.iteritems(), key=lambda (k, v): sort_order.index(k)))
    content = json.dumps(obj_ordered, ensure_ascii=False)
    content += ',\n'

    fileWrite = open('infos.json','a')
    fileWrite.write(content) 
    fileWrite.close()
    print obj_ordered




