
import sys
def LogInit(TED_ID, enLenOrigin, chLenOrigin, enSubtitles, chSubtitles):
  flag = "0"
  if (enLenOrigin<chLenOrigin):
    flag = "1"
  else:
    if  (enLenOrigin>chLenOrigin):
      flag = "2" 
  enDuration = 0
  for subtitle in enSubtitles:
    enDuration +=  subtitle.duration
  chDuration = 0
  for subtitle in chSubtitles:
    chDuration +=  subtitle.duration

  print str(TED_ID),
  print >>sys.stderr, str(TED_ID),
  print str(enLenOrigin), 
  print >>sys.stderr, str(enLenOrigin), 
  print str(enDuration),
  print >>sys.stderr, str(enDuration), 
  print str(chLenOrigin), 
  print >>sys.stderr, str(chLenOrigin), 
  print str(chDuration),
  print >>sys.stderr, str(chDuration), 
  print str(flag),
  print >>sys.stderr, str(flag), 

def getAvgWords(subtitles):
  sum = 0
  for subtitle in subtitles:
    sum = sum + len(subtitle.content)
  return sum / len(subtitles)

def LogMerged(enSubtitles, chSubtitles):

  enwords = getAvgWords(enSubtitles)
  chwords = getAvgWords(chSubtitles) 

  print str(len(enSubtitles)),
  print >>sys.stderr, str(len(enSubtitles)),
  print str(len(chSubtitles)), 
  print >>sys.stderr, str(len(chSubtitles)),
  print str(enwords),
  print >>sys.stderr, str(enwords), 
  print str(chwords), 
  print >>sys.stderr, str(chwords)