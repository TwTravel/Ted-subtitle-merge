# -*- coding: utf8 -*-
class TedSubtitle(object):
  """docstring for TedSubtitle"""
  def __init__(self, startOfParagraph = True, startTime = 0, duration = 0, content = ''):
    super(TedSubtitle, self).__init__()
    self.startOfParagraph = startOfParagraph
    self.startTime = startTime #/ 1000
    self.duration = duration #/ 1000
    self.content = self.FilterContent(content)
    self.endTime = self.startTime + self.duration
    self.content = self.content 
    #self.startOfParagraph = True
    #if( len(self.content) > 0 and (self.content[-1] == u"。" or self.content[-1] == ".")):c
    #  print self.startOfParagraph 
    #  self.startOfParagraph = True
    #  print self.content
      #raw_input("Press enter to continue")

  def __str__(self):
    sp = "0"
    if(self.startOfParagraph==True):
      sp = "1"
    return sp+ " " +str(self.startTime)+" "+str(self.duration)+" "+str(self.endTime)+" "+self.content.encode('utf8')
    #return '\n'.join(["startTime : " + str(self.startTime),
    #                  "duration  : " + str(self.duration),
    #                  "content   : " + self.content.encode('utf8'),
    #                  ''])    

  def TrimNewLine(self):
    self.content = self.content.replace('\n','')

  def FilterContent(self, content):
    redundantWords = ["(Audience whistles)", "(Applause)", "(Laughter)", "(Cheer)", u"(掌聲)", u"(笑聲)", u"（笑聲）", u"（掌聲）", u"(笑)", u"(歡呼)", u"－－", "\n"]
    for word in redundantWords:
      content = content.replace(word, '')
    return content.strip()

  def extendDuration(self, startTime, duration):
    self.endTime = startTime + duration
    self.duration = self.endTime - self.startTime

  def extendContent(self, other):
    self.content += other.content.replace('\n','')
    self.extendDuration(other.startTime, other.duration)