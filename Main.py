# -*- coding: utf8 -*-
import DebugTag
from TedSubtitle import TedSubtitle
from TedTalk import TedTalk
import Number as Number
import sys
import ParagraphMerge as PMerge
import ParagraphRefact as PRefact
import Log 

debugTags = DebugTag.InitDebugTags()
DebugTagType = DebugTag.InitDebugTagTypes()

TED_ID = sys.argv[1]
REFACT_TYPE = sys.argv[2]

talkURL = "http://www.ted.com/talks/sebastian_wernicke_how_to_use_data_to_make_a_hit_tv_show"

enTalk = TedTalk( url = talkURL, languageCode = 'en',    id = TED_ID)
chTalk = TedTalk( url = talkURL, languageCode = 'zh-tw', id = TED_ID)
 
baseDirPath = 'practice/'
filePath = '%s/%s.txt' % (baseDirPath, str(chTalk.id))
 
filteredEnglishSubtitles = enTalk.subtitles
filteredChineseSubtitles = chTalk.subtitles

enLenOriginal = len(filteredEnglishSubtitles)
chLenOriginal = len(filteredChineseSubtitles) 
 
PRefact.RefactStartOfParagraph(enTalk, chTalk, refactType = REFACT_TYPE) 
filteredChineseSubtitles = chTalk.GroupToParagraph2()
filteredEnglishSubtitles = enTalk.GroupToParagraph2()
Log.LogInit(TED_ID, enLenOriginal, chLenOriginal, filteredEnglishSubtitles, filteredChineseSubtitles)

def MergeSubtitles( trunkSubtitles, branchSubtitles ):
  
  idxForEnglishSubtitles = 0
  lengthForChineseSubtitles = len(trunkSubtitles)
  lengthForEnglishSubtitles = len(branchSubtitles)
  
  lastObject = branchSubtitles[lengthForEnglishSubtitles-1]
  lastObject.startTime = lastObject.endTime
  branchSubtitles.append(lastObject)

  paragraph = TedSubtitle()

  filteredEnglishSubtitles = []
  for chineseSubtitle in trunkSubtitles:
    currentDurationDifference = 0

    idxForLastEnglishSubtitles = idxForEnglishSubtitles

    if DebugTagType.MergeSubtitles in debugTags:
      print chineseSubtitle.content.encode('utf8')
  

    while idxForLastEnglishSubtitles < lengthForEnglishSubtitles:
      paragraph.duration = enTalk.subtitles[idxForLastEnglishSubtitles + 1].startTime
      preDurationDifference = currentDurationDifference
      currentDurationDifference = chineseSubtitle.duration - paragraph.duration

      if DebugTagType.MergeSubtitles in debugTags:
        print chineseSubtitle.duration , paragraph.duration
        print

      if currentDurationDifference <= 0:
        if abs(preDurationDifference) >= abs(currentDurationDifference):
          idxForLastEnglishSubtitles += 1

        break

      idxForLastEnglishSubtitles += 1


    if DebugTagType.MergeSubtitles in debugTags:
      print "idx: ", idxForEnglishSubtitles, idxForLastEnglishSubtitles

    contents = [e.content for e in branchSubtitles[idxForEnglishSubtitles:idxForLastEnglishSubtitles]]
    
    if DebugTagType.MergeSubtitles in debugTags:
      for k in contents:
        #pass
        print k

      print '-' * 20

    paragraph.content += ' '.join(contents)
    idxForEnglishSubtitles = idxForLastEnglishSubtitles

    paragraph.content = paragraph.content.replace('\n',' ')
    filteredEnglishSubtitles.append(paragraph)
    paragraph = TedSubtitle()

  return filteredEnglishSubtitles

#filteredEnglishSubtitles = MergeSubtitles( filteredChineseSubtitles, enTalk.subtitles )
[filteredChineseSubtitles, filteredEnglishSubtitles] = PMerge.MergeSubtitles(filteredEnglishSubtitles, filteredChineseSubtitles)
Log.LogMerged(filteredEnglishSubtitles, filteredChineseSubtitles)  

def ReadFileContent(filePath):
  fileRead = open(filePath, 'r')
  return fileRead.read().split('\n')


def WriteFileContent(filePath, content):
  fileWrite = open(filePath,'w')
  fileWrite.write(content) # python will convert \n to os.linesep
  fileWrite.close() 

import json
def PrintResult(filteredChineseSubtitles, filteredEnglishSubtitles):
  contents = [ str(enTalk.id), '\n', '\n' ]

  obj = []
  for i in xrange(len(filteredChineseSubtitles)):    
    a1 = filteredEnglishSubtitles[i].content.encode('utf8')
    b1 = filteredChineseSubtitles[i].content.encode('utf8')
    obj.append({"chinese" : b1, "english" : a1})

  resultObj = { "title" : "test", "url" : "http:xxx", "paragraphs" : obj}
  result = json.dumps(resultObj, ensure_ascii=False, indent= 4)
  
  print result

  WriteFileContent(filePath,result)


if DebugTagType.PrintSubtitles in debugTags:
  PrintResult(filteredChineseSubtitles, filteredEnglishSubtitles)


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