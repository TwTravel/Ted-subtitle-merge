import os
import urllib2
import json
from TedSubtitle import TedSubtitle

def GetSubtitles(talkID, languageCode):
  subtitleUrl = "http://www.ted.com/talks/subtitles/id/%s/lang/%s" % (talkID, languageCode)
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


def GetID(url):
  command = "curl -s %s | grep source=facebook | awk -F '=' '{print $3}' | awk -F '&' '{print $1}'" % ( url )
  return os.popen(command).readlines()[0].strip()

def GetTitle(url):
  return url.split('/')[-1].replace('_',' ')