# -*- coding: utf8 -*-
class TedSubtitle(object):
  """docstring for TedSubtitle"""
  def __init__(self, startOfParagraph = True, startTime = 0, duration = 0, content = ''):
    super(TedSubtitle, self).__init__()
    self.startOfParagraph = startOfParagraph
    self.startTime = startTime #/ 1000
    self.duration = duration   #/ 1000
    self.content = self.FilterContent(content)
    self.endTime = self.startTime + self.duration
    self.content = self.content  

  def __str__(self): 
    return str(int(self.startOfParagraph))+ " " +str(self.startTime)+" "+str(self.duration)+" "+str(self.endTime)+" "+self.content.encode('utf8')
     
  def TrimNewLine(self, content):
    return content.replace('\n',' ')

  def FilterContent(self, content):
    redundantWords = ["(Audience whistles)", "(Applause)", "(Laughter)", "(Cheer)", u"(掌聲)", u"(笑聲)", u"（笑聲）", u"（掌聲）", u"(笑)", u"(歡呼)", u"－－"]
    for word in redundantWords:
      content = self.TrimNewLine(content.replace(word, ''))
    return content.strip()

  def extendDuration(self, startTime, duration):
    self.endTime = startTime + duration
    self.duration = self.endTime - self.startTime

  def extendContent(self, other):
    self.content += other.content.replace('\n','')
    self.extendDuration(other.startTime, other.duration)