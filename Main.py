# -*- coding: utf8 -*-
import DebugTag
import ParagraphDetector as paragraphDetector
import TedTalkFetcher as tedTalkFetcher
from TedSubtitle import TedSubtitle
from TedTalk import TedTalk

debugTags = DebugTag.InitDebugTags()
DebugTagType = DebugTag.InitDebugTagTypes()


def IsInt(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False





talkURL = "http://www.ted.com/talks/sebastian_wernicke_how_to_use_data_to_make_a_hit_tv_show"

chTalk = TedTalk( url = talkURL, languageCode = 'zh-tw' )
enTalk = TedTalk( url = talkURL, languageCode = 'en' )




baseDirPath = 'practice/'
filePath = '%s/%s.txt' % (baseDirPath, str(chTalk.id))




def GroupToParagraph(subtitles):
  lastAddedIndex = 0
  lastAddedChar = ' '
  paragraphs = []
  paragraph = TedSubtitle()

  subtitles.insert(0, subtitles[0])

  for i in xrange(1,len(subtitles)):
    subtitle = subtitles[i]

    if paragraph.startOfParagraph:
      paragraph.startTime = subtitles[i-1].startTime
      paragraph.startOfParagraph = False    
    
    if paragraphDetector.IsNewParagraph(subtitle.startOfParagraph, paragraph.content):
      paragraph.TrimNewLine()
      if paragraph.duration == 0:
        paragraph.duration = subtitles[i-1].endTime

      paragraphs.append(paragraph)
      paragraph = TedSubtitle(content = subtitle.content)
      lastAddedIndex = i
    else:
      paragraph.content += subtitle.content
      paragraph.duration = subtitle.endTime
      

  if lastAddedIndex < len(subtitles):
    paragraphs.append(paragraph)

  return paragraphs




filteredChineseSubtitles = GroupToParagraph(chTalk.subtitles)

if DebugTagType.GroupToParagraph in debugTags:
  print chTalk
  print enTalk



def MergeSubtitles( trunkSubtitles, branchSubtitles ):
  
  idxForEnglishSubtitles = 0
  lengthForChineseSubtitles = len(trunkSubtitles)
  lengthForEnglishSubtitles = len(branchSubtitles)
  
  lastObject = enTalk.subtitles[lengthForEnglishSubtitles-1]
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
  contents = [ enTalk.id, '\n', '\n' ]

  for i in xrange(len(filteredChineseSubtitles)):    
    contents += [ str(i+1), filteredEnglishSubtitles[i].content, '\n', '\n', '\n' ]

  WriteFileContent(filePath,'\n'.join(contents))


if DebugTagType.PrintSubtitles in debugTags:
  PrintResult(filteredChineseSubtitles, filteredEnglishSubtitles)


if DebugTagType.File in debugTags:
  
  contentsInFile = ReadFileContent(filePath)

  lengthForChineseSubtitles = len(filteredChineseSubtitles)

  idxForChineseSubtitles = 0
  i = 0
  while i < len(contentsInFile):
    if IsInt(contentsInFile[i]):
      i += 2
      hasTranslated = len(contentsInFile[i]) > 0

      if hasTranslated:
        contentsInFile[i] = filteredChineseSubtitles[idxForChineseSubtitles].content.encode('utf8')

      idxForChineseSubtitles += 1

    i += 1
  
    
  WriteFileContent(filePath,'\n'.join(contentsInFile))
