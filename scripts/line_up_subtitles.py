
from datetime import datetime, timedelta

durationData = {
    "DmT_OP_GanonWakeUp_PreRender": 6421.0,
    "DmT_SY_BloodyMoonDarkZelda_PreRender": 520.0,
    "DmT_SY_BloodyMoonFirst_PreRender": 1100.0,
    "DmT_ZE_Birth_PreRender": 7562.0,
    "DmT_ZE_LieServant_PreRender": 5515.0,
    "DmT_ZE_Meet_PreRender": 3245.0,
    "DmT_ZE_Molduga_PreRender": 4663.0,
    "DmT_ZE_QueenDead_PreRender": 3506.0,
    "Dm_BC_0012_PreRender": 1867.0,
    "Dm_BZ_0005_PreRender": 1365.0,
    "Dm_ED_0007_PreRender": 10749.0,
    "Dm_GE_0025_PreRender": 5109.0,
    "Dm_GO_0021_PreRender": 4912.0,
    "Dm_OT_0015_PreRender": 3313.0,
    "Dm_RT_0022_PreRender": 4536.0,
    "Dm_SK_0003_PreRender": 1940.0,
    "Dm_ZE_0004_PreRender": 4892.0,
    "Dm_ZE_0005_PreRender": 5876.0,
    "Dm_ZE_0006_PreRender": 6333.0,
    "Dm_ZE_0007_PreRender": 5315.0,
    "Dm_ZE_0008_PreRender": 5955.0,
    "Dm_ZE_0010_PreRender": 5975.0,
    "Dm_ZE_0011_PreRender": 7850.0,
    "Dm_ZN_0033_PreRender": 9507.0,
    "Dm_ZN_0039_PreRender": 5284.0,
    "Dm_ZO_0032_PreRender": 4615.0,
}

FPS = 30
timeFormat = r'%H:%M:%S,%f'
zeroTimeFormat = '00:00:00,000'

'''
0015
wake up
meet
0004
0006
molduga
lieservant
ze0005
queendead
birth
bz0005
ze0007
ze0008
0033
0010
0039
0011
0003
Ed0007

'''

targets = ['Dm_OT_0015_PreRender',
           'DmT_OP_GanonWakeUp_PreRender',
           'DmT_ZE_Meet_PreRender',
           'Dm_ZE_0004_PreRender',
           'Dm_ZE_0006_PreRender',
           'DmT_ZE_Molduga_PreRender',
           'DmT_ZE_LieServant_PreRender',
           'Dm_ZE_0005_PreRender',
           'DmT_ZE_QueenDead_PreRender',
           'DmT_ZE_Birth_PreRender',
           'Dm_BZ_0005_PreRender',
           'Dm_ZE_0007_PreRender',
           'Dm_ZE_0008_PreRender',
           'Dm_ZN_0033_PreRender',
           'Dm_ZE_0010_PreRender',
           'Dm_ZN_0039_PreRender',
           'Dm_ZE_0011_PreRender',
           'Dm_SK_0003_PreRender',
           'Dm_ED_0007_PreRender']


def getSrtData(fileName):
  with open(fileName + '.srt', 'r', encoding='utf8') as srtFile:
    srtLines = srtFile.readlines()
    index = 0
    innerBlockIndex = 0
    innerBlockData = []
    srtData = []
    line = srtLines[index]
    length = len(srtLines)
    while index < length:
      line = srtLines[index]
      while line != '\n':
        if (innerBlockIndex == 1):
          times = line.replace('\n', '').split(' --> ')
          startTime = datetime.strptime(times[0], timeFormat)
          endTime = datetime.strptime(times[1], timeFormat)
        elif (innerBlockIndex > 1):
          innerBlockData.append(line)
        innerBlockIndex += 1
        index += 1
        line = srtLines[index]

      if (len(innerBlockData) > 0):
        srtData.append([startTime, endTime] + innerBlockData)
      index += 1
      innerBlockIndex = 0
      innerBlockData.clear()
    return srtData


timeBase = datetime.strptime(zeroTimeFormat, timeFormat)
srtLines = []
counter = 0
for fileName in targets:
  srtData = getSrtData(fileName)
  for data in srtData:
    startTime = timeBase + timedelta(hours=data[0].hour, minutes=data[0].minute, seconds=data[0].second, microseconds=data[0].microsecond)
    endTime = timeBase + timedelta(hours=data[1].hour, minutes=data[1].minute, seconds=data[1].second, microseconds=data[1].microsecond)
    startTimeStr = datetime.strftime(startTime, timeFormat)
    endTimeStr = datetime.strftime(endTime, timeFormat)

    srtLines.append("{}\n".format(counter))
    subTitleLine = '{} --> {}'.format(startTimeStr[:-3], endTimeStr[:-3])
    srtLines.append("{}\n".format(subTitleLine))
    texts = data[2:]
    for text in texts:
      srtLines.append(text)

    timeBase += timedelta(seconds=durationData[fileName]/FPS)
    srtLines.append('\n')
    counter += 1

with open('./sum.srt', 'w+', encoding='utf8') as subtitleFile:
  subtitleFile.writelines(srtLines)
  pass
print('DONE')
