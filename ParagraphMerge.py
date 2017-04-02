import Enum 

TRS = Enum.enum(EN=0, CH=1, LEN=2)

def printParagraph(paragraphs):
  description = "" #"Title:%s\n" % self.title
  for i in paragraphs:
    description += i.__str__() + '\n'
  print description 

def diffTime(paragraphSRC, paragraphDST): 
  return paragraphDST.endTime - paragraphSRC.endTime

def overTime(paragraphSRC, paragraphDST): 
  return paragraphDST.endTime > paragraphSRC.endTime 
 
def mergeParagraph(paragaph, src, dst): 
  for i in xrange(src+1, dst):
    paragaph[src].extendContent(paragaph[i]);
  return paragaph[src]
 
def MergeSubtitles(enParagraph, chParagraph):
  newParagraph = [[],[]]
  indexLen = [len(enParagraph), len(chParagraph)]
  indexSRC = [0, 0]
  indexDST = [0, 0]
  pParagraph = [enParagraph, chParagraph]
  end = False
  while(end==False):
    diff = diffTime(pParagraph[TRS.EN][indexSRC[TRS.EN]], pParagraph[TRS.CH][indexSRC[TRS.CH]])
    if(abs(diff) < 500):
      for i in xrange(0, TRS.LEN):
        indexDST[i] = indexDST[i] + 1
    else:
      error1 = 0
      error2 = 0
      if(diff < 0): # en > ch
        idx1 = TRS.CH
        idx2 = TRS.EN
      else:         # ch > en
        idx1 = TRS.EN
        idx2 = TRS.CH
      while(indexDST[idx1] < indexLen[idx1]):
        if(overTime(pParagraph[idx2][indexSRC[idx2]], pParagraph[idx1][indexDST[idx1]])): 
          error2 = diffTime(pParagraph[idx2][indexSRC[idx2]], pParagraph[idx1][indexDST[idx1]])   
          if(abs(error2) <= abs(error1)):
            indexDST[idx1] = indexDST[idx1]+1

          indexDST[idx2] = indexDST[idx2]+1 
          break
        else:
          error1 = diffTime(pParagraph[idx2][indexSRC[idx2]], pParagraph[idx1][indexDST[idx1]])  
          indexDST[idx1] = indexDST[idx1]+1 

    if(indexDST[TRS.EN] >= indexLen[TRS.EN] or indexDST[TRS.CH] >= indexLen[TRS.CH]):
      for i in xrange(0, TRS.LEN):
        indexDST[i] = indexLen[i]
      end = True

    for i in xrange(0, TRS.LEN):
      newParagraph[i].append(mergeParagraph(pParagraph[i], indexSRC[i], indexDST[i])) 
      indexSRC[i] = indexDST[i]
  return newParagraph         
  