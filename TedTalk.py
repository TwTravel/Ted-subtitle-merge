import TedTalkFetcher as tedTalkFetcher

class TedTalk(object):
  """docstring for TedTalk"""
  def __init__(self, url, languageCode):
    super(TedTalk, self).__init__()
    self.url = url
    self.languageCode = languageCode
    self.id = tedTalkFetcher.GetID(url)
    self.title = tedTalkFetcher.GetTitle(url)
    self.subtitles = ResetStartTime(tedTalkFetcher.GetSubtitles( self.id, languageCode))
    



def ResetStartTime(arr):
  for i in range(len(arr)):
    arr[i].startTime -= arr[0].startTime

  return arr