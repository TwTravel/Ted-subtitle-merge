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

debugTags    = DebugTag.InitDebugTags()
DebugTagType = DebugTag.InitDebugTagTypes()

TED_ID      = sys.argv[1]
REFACT_TYPE = sys.argv[2]
 
enTalk = TedTalk(languageCode = 'en',    id = TED_ID)
chTalk = TedTalk(languageCode = 'zh-tw', id = TED_ID)
 
baseDirPath = 'practice/'
filePath = '%s/%s.json' % (baseDirPath, str(chTalk.id))
 
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

def WriteFileContent(filePath, content):
  fileWrite = open(filePath,'w')
  fileWrite.write(content) # python will convert \n to os.linesep
  fileWrite.close() 

def GetTitleAndURL(id):
  command = "curl -s http://www.ted.com/talks/view/id/%s" % id
  output = os.popen(command).readlines()[0]
  url = output.split('"')[1]
  title = url.split('/')[-1]
  title = title.title().replace('_', ' ')
  return {"title" : title, 'url' : url}

def PrintResult(filteredEnglishSubtitles, filteredChineseSubtitles): 
  obj = []
  for i in xrange(len(filteredChineseSubtitles)):    
    a1 = filteredEnglishSubtitles[i].content.encode('utf8')
    b1 = filteredChineseSubtitles[i].content.encode('utf8')
    obj.append({"zh-tw" : b1, "en" : a1})

  resultObj = GetTitleAndURL(TED_ID)
  resultObj["paragraphs"] = obj
  result = json.dumps(resultObj, ensure_ascii=False) 

  WriteFileContent(filePath,result)


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

