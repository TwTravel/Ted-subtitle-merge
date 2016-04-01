# -*- coding: utf8 -*-
class TedSubtitle(object):
  """docstring for TedSubtitle"""
  def __init__(self, startOfParagraph = True, startTime = 0, duration = 0, content = ''):
    super(TedSubtitle, self).__init__()
    self.startOfParagraph = startOfParagraph
    self.startTime = startTime / 1000
    self.duration = duration / 1000
    self.content = content
    self.endTime = self.startTime + self.duration



  def Description(self):
    return '\n'.join(["startTime : " + str(self.startTime),
                      "duration  : " + str(self.duration),
                      "content   : " + self.content.encode('utf8'),
                      ''])    


  def TrimNewLine(self):
    self.content = self.content.replace('\n','')

