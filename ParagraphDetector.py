# -*- coding: utf8 -*-
def HasContainsEndMark(content):
  if len( content) < 2:
    return False

  endMarks = [ '.', '?', '!', '。', '？', '！' ]
  for i in endMarks:
    if content[-1].encode('utf8') == i:
      return True

  return False


def HasEvenQuotes( content ):
  return content.count('"') % 2 == 0 

def HasPairChar( content ):
  leftChars =  [ u'「', u'(', u'（', u'{', u'【', u'｛', u'[']
  rightChars = [ u'」', u')', u'）', u'}', u'】', u'｝', u']']
  
  for i in range(len(leftChars)):
    if ( content.count(leftChars[i].encode('utf8')) == content.count(rightChars[i].encode('utf8')) ):
      return True

  return False

def IsNewParagraph(isStartOfParagraph, sentence):
  maxCharInSentence = 150
  
  newParagraph = isStartOfParagraph
  newParagraph = newParagraph and HasEvenQuotes(sentence)
  newParagraph = newParagraph and HasContainsEndMark(sentence)
  newParagraph = newParagraph and HasPairChar(sentence.encode('utf8'))
  newParagraph = newParagraph and len(sentence) != 0
  newParagraph = newParagraph or len(sentence) > maxCharInSentence
  return newParagraph
  