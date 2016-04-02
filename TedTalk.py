import TedTalkFetcher as tedTalkFetcher
from TedSubtitle import TedSubtitle
import ParagraphDetector as paragraphDetector

class TedTalk(object):
  """docstring for TedTalk"""
  def __init__(self, url, languageCode = "en"):
    super(TedTalk, self).__init__()
    self.url = url
    self.languageCode = languageCode
    self.id = tedTalkFetcher.GetID(url)
    self.title = tedTalkFetcher.GetTitle(url)
    self.subtitles = ResetStartTime(tedTalkFetcher.GetSubtitles(self.id, languageCode))
  
  def __str__(self):
    description = "Title:%s\n" % self.title
    for i in self.subtitles:
      description += i.__str__() + '\n'

    return description

  @staticmethod
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





# remove Intro/Ad time
def ResetStartTime(arr):
  for i in range(len(arr)):
    arr[i].startTime -= arr[0].startTime

  return arr


