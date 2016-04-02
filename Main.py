# -*- coding: utf8 -*-
import DebugTag
from TedSubtitle import TedSubtitle
from TedTalk import TedTalk
import Number as Number

debugTags = DebugTag.InitDebugTags()
DebugTagType = DebugTag.InitDebugTagTypes()








talkURL = "http://www.ted.com/talks/sebastian_wernicke_how_to_use_data_to_make_a_hit_tv_show"

chTalk = TedTalk( url = talkURL, languageCode = 'zh-tw' )
enTalk = TedTalk( url = talkURL, languageCode = 'en' )




baseDirPath = 'practice/'
filePath = '%s/%s.txt' % (baseDirPath, str(chTalk.id))




filteredChineseSubtitles = TedTalk.GroupToParagraph(chTalk.subtitles)

if DebugTagType.GroupToParagraph in debugTags:
  print chTalk
  #print enTalk



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

filteredEnglishSubtitles = MergeSubtitles( filteredChineseSubtitles, enTalk.subtitles )



def ReadFileContent(filePath):
  fileRead = open(filePath, 'r')
  return fileRead.read().split('\n')


def WriteFileContent(filePath, content):
  fileWrite = open(filePath,'w')
  fileWrite.write(content) # python will convert \n to os.linesep
  fileWrite.close() 

def PrintResult(filteredChineseSubtitles, filteredEnglishSubtitles):
  contents = [ str(enTalk.id), '\n', '\n' ]

  for i in xrange(len(filteredChineseSubtitles)):    
    contents += [ str(i+1), filteredEnglishSubtitles[i].content.encode('utf8'),  filteredChineseSubtitles[i].content.encode('utf8'), '\n', '\n' ]

  WriteFileContent(filePath,'\n'.join(contents))


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
