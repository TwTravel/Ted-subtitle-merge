def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def InitDebugTagTypes():
  return enum( 'GroupToParagraph', 'MergeSubtitles', 'PrintSubtitles', 'File' )

def InitDebugTags():
  DebugTagType = InitDebugTagTypes()
  debugTags = []

  debugTags.append(DebugTagType.GroupToParagraph)
  #debugTags.append(DebugTagType.MergeSubtitles)

  debugTags.append(DebugTagType.PrintSubtitles)
  #debugTags.append(DebugTagType.File)

  return debugTags

