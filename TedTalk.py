import TedTalkFetcher as TedTalkFetcher
from TedSubtitle import TedSubtitle

class TedTalk(object):
  """docstring for TedTalk"""
  def __init__(self, languageCode = "en", id="0"):
    super(TedTalk, self).__init__() 
    self.languageCode = languageCode
    self.id = id 
    self.subtitles = ResetStartTime(TedTalkFetcher.GetSubtitles(self.id, languageCode))
  
  def __str__(self):
    description = "" #"Title:%s\n" % self.title
    for i in self.subtitles:
      description += i.__str__() + '\n'

    return description

  #@staticmethod
  def GroupToParagraph(self):
    paragraphs = []
    subtitles = self.subtitles 

    for i in xrange(0,len(subtitles)):
      subtitle = subtitles[i]
      if(subtitle.startOfParagraph):
        paragraph = TedSubtitle(content = "")
        paragraph.startTime = subtitle.startTime  
      paragraph.content += " "+subtitle.content

      if(i == (len(subtitles)-1) or subtitles[i+1].startOfParagraph == True):
        paragraph.endTime = subtitle.endTime
        paragraph.duration = subtitle.endTime - paragraph.startTime
        paragraphs.append(paragraph) 
    return paragraphs

  def ResetStartOfParagraph(self, flag):
    for subtitle in self.subtitles:
      subtitle.startOfParagraph = flag
# remove Intro/Ad time
def ResetStartTime(arr):
  for i in range(len(arr)):
    arr[i].startTime -= arr[0].startTime

  return arr


