#!/usr/bin/python
# -*- coding: utf8 -*-
import DebugTag
from TedSubtitle import TedSubtitle
from TedTalk import TedTalk
import Number as Number
import sys
import ParagraphMerge as PMerge
import ParagraphRefact as PRefact
import Log 
import json
import os
import requests
def GetIntroDuration(id, languageCode):
  for attempt in range(20):
    try:
      r = requests.get("http://www.ted.com/talks/view/id/%s?lang=%s" % (id, languageCode))
      arr = r.text.split('\n')
      url = ''
      introDuration = 0

      for i in arr:
        introLine = i.split('introDuration":')
        if len(introLine) > 1:
          introText = introLine[1].split(',"')[0]
          introDuration = float(introText)
          return introDuration
        
    except Exception, e:
      print e
    continue
 


def get_time(millseconds):
    hours = millseconds/ 3600000
    millseconds -= hours* 3600000
    minutes = millseconds/ 60000
    millseconds -= minutes* 60000
    seconds = millseconds/ 1000
    millseconds -= seconds* 1000
    return '%02d:%02d:%02d,%03d' % (hours, minutes, seconds, millseconds)

debugTags    = DebugTag.InitDebugTags()
DebugTagType = DebugTag.InitDebugTagTypes()

TED_ID        = sys.argv[1]
REFACT_TYPE   = 2#sys.argv[2]
enIntroDuration = GetIntroDuration(TED_ID, "en")
chIntroDuration = GetIntroDuration(TED_ID, "zh-tw")
enTalk = TedTalk(languageCode = 'en',    id = TED_ID, introDuration = enIntroDuration)
chTalk = TedTalk(languageCode = 'zh-tw', id = TED_ID, introDuration = chIntroDuration)

filteredEnglishSubtitles = enTalk.subtitles
filteredChineseSubtitles = chTalk.subtitles

enLenOriginal = len(filteredEnglishSubtitles)
chLenOriginal = len(filteredChineseSubtitles) 


PRefact.RefactStartOfParagraph(enTalk, chTalk, refactType = REFACT_TYPE) 
filteredChineseSubtitles = chTalk.GroupToParagraph()
filteredEnglishSubtitles = enTalk.GroupToParagraph()
Log.LogInit(TED_ID, enLenOriginal, chLenOriginal, filteredEnglishSubtitles, filteredChineseSubtitles)

[filteredEnglishSubtitles, filteredChineseSubtitles] = PMerge.MergeSubtitles(filteredEnglishSubtitles, filteredChineseSubtitles)
Log.LogMerged(filteredEnglishSubtitles, filteredChineseSubtitles)   

def ReadFileContent(filePath):
  fileRead = open(filePath, 'r')
  return fileRead.read().split('\n')

import io

def WriteFileContent(filePath, content):
  with io.open(filePath, 'w') as f:
    f.write(content) # python will convert \n to os.linesep


def GetTitleAndURL(id):
  for attempt in range(20):
    try:
      r = requests.get("http://www.ted.com/talks/view/id/%s" % id)
      arr = r.text.split('\n')
      
      for i in arr:
        if "og:url" in i:
          texts = i.split('"')
          url = texts[3]
          break

      title = url.split('/')[-1]
      title = title.title().replace('_', ' ')
      return {u"title" : title, u'url' : url}
    except Exception, e:
      print e
      continue

def PrintResult(filteredEnglishSubtitles, filteredChineseSubtitles): 
  obj = []
  srtTexts = ''
  for i in xrange(len(filteredChineseSubtitles)):    
    a1 = unicode(filteredEnglishSubtitles[i].content)
    b1 = unicode(filteredChineseSubtitles[i].content)
    obj.append({u"zh-tw" : b1, u"en" : a1})

    startTime = filteredEnglishSubtitles[i].startTime
    duration = filteredEnglishSubtitles[i].duration
    srtTexts += '%d\n%s --> %s\n%s\n%s\n\n' % (i+1, get_time(startTime),\
            get_time(startTime+ duration), a1, b1)


  resultObj = GetTitleAndURL(TED_ID)
  resultObj[u"paragraphs"] = obj
  result = json.dumps(resultObj, ensure_ascii=False, sort_keys=True) 

  baseDirPath = 'output/'
  filePath = '%s/%s.json' % (baseDirPath, TED_ID)
  WriteFileContent(filePath,result)
  filePath = '%s/%s.srt' % (baseDirPath, TED_ID)
  WriteFileContent(filePath,srtTexts)


if DebugTagType.PrintSubtitles in debugTags:
  PrintResult(filteredEnglishSubtitles, filteredChineseSubtitles)

if DebugTagType.File in debugTags:
  contentsInFile = ReadFileContent(filePath)
  lengthForChineseSubtitles = len(filteredChineseSubtitles)
  idxForChineseSubtitles = 0
  i = 0
  while i < len(contentsInFile):
    if Number.IsInt(contentsInFile[i]):
      i += 2
      hasTranslated = len(contentsInFile[i]) > 0 or True
      if hasTranslated:
        contentsInFile[i] = filteredChineseSubtitles[idxForChineseSubtitles].content.encode('utf8')
      idxForChineseSubtitles += 1
    i += 1
  
  WriteFileContent(filePath,'\n'.join(contentsInFile))

