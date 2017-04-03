import os
import urllib2
import json
from TedSubtitle import TedSubtitle


def GetSubtitles(talkID, languageCode):
  subtitleUrl = "http://www.ted.com/talks/subtitles/id/%s/lang/%s" % (talkID, languageCode)

  try:  
    response = urllib2.urlopen(subtitleUrl)
    html = response.read() 
    subtitles = json.loads(html)["captions"]

    tedSubtitles = []
    for subtitle in subtitles:
      tedSubtitle = TedSubtitle(subtitle["startOfParagraph"], 
                                subtitle["startTime"], 
                                subtitle["duration"], 
                                subtitle["content"])
      if(len(tedSubtitle.content) > 0):
        tedSubtitles.append(tedSubtitle)
      else:
        if(len(tedSubtitles) > 0):
          tedSubtitles[-1].extendDuration(subtitle["startTime"], subtitle["duration"])
    return tedSubtitles

  except urllib2.HTTPError:
    #print "Not found for url : %s" % subtitleUrl
    exit(0)
  except ValueError:
    print "The response data isn't JSON format. (%s)" % subtitleUrl
    exit(0)
 
 