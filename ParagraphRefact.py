import Enum

RF = Enum.enum(ORIGINAL=0, PIECE=1, EN_LINE1=2, EN_LINE2=3) 

def refactWithLine(talk, countOfLine):
	count = 0
	talk.ResetStartOfParagraph(False)
	subtitle = talk.subtitles
	subtitle[0].startOfParagraph = True 
	for i in xrange(1,len(subtitle)):
	  if(subtitle[i].content[-1] == "." or subtitle[i].content[-1] == "?"):
	    count = count + 1
	    if(i < len(subtitle)-1 and count == countOfLine):
	      subtitle[i+1].startOfParagraph = True
	      count = 0 

def methodOriginal(enTalk, chTalk):
	return

def methodPIECE(enTalk, chTalk):
	chTalk.ResetStartOfParagraph(True)
	enTalk.ResetStartOfParagraph(True)	    

def methodEN_LINE1(enTalk, chTalk):
	chTalk.ResetStartOfParagraph(True)
	refactWithLine(enTalk, 1)     

def methodEN_LINE2(enTalk, chTalk):
	chTalk.ResetStartOfParagraph(True)
	refactWithLine(enTalk, 2)         

def RefactStartOfParagraph(enTalk, chTalk, refactType = RF.ORIGINAL):
	doMethod = {
		   RF.ORIGINAL : methodOriginal,
           RF.PIECE    : methodPIECE,
           RF.EN_LINE1 : methodEN_LINE1,
           RF.EN_LINE2 : methodEN_LINE2, 
	}
	doMethod[int(refactType)](enTalk, chTalk)