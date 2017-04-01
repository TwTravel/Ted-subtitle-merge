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
      tedSubtitles.append(tedSubtitle)

    return tedSubtitles

  except urllib2.HTTPError:
    print "Not found for url : %s" % subtitleUrl
    exit(0)
  except ValueError:
    print "The response data isn't JSON format. (%s)" % subtitleUrl
    exit(0)
 

def GetID(url):
  command = "curl -s %s | grep al:ios:ur  | awk -F '/' '{print $4}'  | awk -F '?' '{print $1}'" % ( url )
  talkID = os.popen(command).readlines()[0].strip()
  try:
    talkID = int(talkID)
  except:
    print "talk id %s is't int" % talkID
    exit(0)

  return talkID
  



def GetTitle(url):
  return url.split('/')[-1].replace('_',' ')